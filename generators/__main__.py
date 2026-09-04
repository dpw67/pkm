"""Render a LinkML schema to the development artifacts.

    python -m generators schema/pkm-meals.yaml --out generated
    python -m generators schema/pkm-meals.yaml --out generated --target neo4j
    python -m generators schema/pkm-meals.yaml --dry-run

Each target returns a {relative path: text} map, so a target is free to emit one
file or one per class without the driver caring which.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import textwrap
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from . import Model, kebab, snake
from .seed import cypher, frontmatter, load, notes, record

TEMPLATES = Path(__file__).parent / "templates"


UNITS = {"g", "mg", "kg", "ml", "l", "oz", "lb"}

# Segments that read badly title-cased. `pkm-meals` is the PKMMeals module, not
# the PkmMeals one.
ACRONYMS = {"pkm", "rdf", "skos", "uri", "url", "api", "json", "html"}


def label(key: str) -> str:
    """Property key as a column header. `nutrition_sodium_mg` -> `Nutrition sodium (mg)`.

    A trailing unit suffix is the one part of a slot name that reads badly when
    it is just another word, so it goes in parentheses where a header expects it.
    """
    parts = key.split("_")
    if len(parts) > 1 and parts[-1] in UNITS:
        return f"{' '.join(parts[:-1]).capitalize()} ({parts[-1]})"
    return key.replace("_", " ").capitalize()


def headers(fields: list) -> dict[str, str]:
    """Column header per flattened property key.

    A slot's `title` wins where it has one, and wins unprefixed: in a Recipe
    table the nutrition columns are obviously nutrition, so `Cal` and `Carbs`
    read better than `Nutrition calories` and the prefix only costs width. The
    prefix exists to disambiguate the property *key*, which is a different job.

    Only a title wins unprefixed, though. An untitled embedded slot keeps its
    prefix, because dropping it silently is how `source.url` becomes a column
    headed `Url` in a table that has no other url and still does not say whose.
    A title is a decision someone made; a humanised key is just a fallback.

    And a title loses again if it collides. `name` and `source_name` are the
    same slot embedded twice, so titling it would label two columns identically
    -- the defect this whole function exists to avoid. Any header that is not
    unique gets its prefix back, which leaves the shape's own field bare and
    qualifies the embedded ones.
    """
    out = {f.key: (f.title or label(f.key)) for f in fields}
    seen: dict[str, int] = {}
    for h in out.values():
        seen[h] = seen.get(h, 0) + 1
    return {k: (label(f.key) if seen[v] > 1 and f.prefix else v)
            for (k, v), f in zip(out.items(), fields)}


# Swift keywords a slot name could plausibly collide with. Escaped rather than
# renamed, so the property still matches the schema slot.
KEYWORDS = {
    "associatedtype", "class", "deinit", "enum", "extension", "fileprivate",
    "func", "import", "init", "inout", "internal", "let", "open", "operator",
    "private", "protocol", "public", "rethrows", "static", "struct", "subscript",
    "typealias", "var", "break", "case", "continue", "default", "defer", "do",
    "else", "fallthrough", "for", "guard", "if", "in", "repeat", "return",
    "switch", "where", "while", "as", "any", "catch", "false", "is", "nil",
    "super", "self", "throw", "throws", "true", "try",
}


def camel(name: str) -> str:
    """Slot or class name as a Swift property name. `carbohydrates_g` -> `carbohydratesG`.

    The `_g`/`_mg` suffixes come through as `G` and `Mg`, which reads badly on
    purpose: a unit welded into a property name is the cohesion problem a
    Measurement or an Amount value object exists to solve. See Values.swift.
    """
    parts = [p for p in snake(name).split("_") if p]
    if not parts:
        return name
    out = parts[0] + "".join(p.capitalize() for p in parts[1:])
    return f"`{out}`" if out in KEYWORDS else out


def pascal(name: str) -> str:
    """Schema or slot name as a Swift type name. `pkm-meals` -> `PKMMeals`."""
    parts = [p for p in snake(name).replace("-", "_").split("_") if p]
    return "".join(p.upper() if p in ACRONYMS else p.capitalize() for p in parts)


def swift(member, layer: str = "payload") -> str:
    """Swift type of a Field, an Embed, or an Edge.

    `payload` is the transport shape: a reference is the id string it travels
    as, and an association carries the `DTO` suffix like the records at either
    end. `model` is the stored shape: the same reference is the object
    SwiftData resolves it to.

    Multivalued comes out non-optional with an empty default rather than
    `[T]?`: a recipe with no images has no images, and a caller should not have
    to tell that apart from one whose images were never decoded.
    """
    if hasattr(member, "shape"):                       # Embed -- inlined
        base = member.shape.name
        if layer == "payload" and member.shape.association:
            base += "DTO"
        required = False
    elif hasattr(member, "target"):                    # Edge -- reference
        base = (member.target.name if layer == "model"
                else member.target.identifier.scalar("swift"))
        required = member.required
    else:                                              # Field -- scalar or enum
        base = member.enum or member.scalar("swift")
        required = member.required
    if member.multivalued:
        return f"[{base}]"
    return base if required else f"{base}?"


def bare(kind: str) -> str:
    """The type without its optional marker, for a `T.self` in a decode call."""
    return kind[:-1] if kind.endswith("?") else kind


def plural(name: str) -> str:
    """Class name as a collection property. Naive, and only used for those.

    Recipe -> recipes, Meal -> meals. Wrong on an irregular noun, which is why
    it is nowhere near a type name.
    """
    lower = camel(name)
    if lower.endswith("y") and lower[-2:-1] not in "aeiou":
        return lower[:-1] + "ies"
    if lower.endswith(("s", "x", "z", "ch", "sh")):
        return lower + "es"
    return lower + "s"


def iso(value: object) -> str:
    """JSON form of anything json.dumps cannot take.

    Only dates arrive here. A LinkML `datetime` may be quoted in the fixture or
    parsed by the YAML loader, and Swift's `.iso8601` strategy wants the `Z`
    form either way -- `isoformat()` alone writes `+00:00`, which it rejects.
    """
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat().replace("+00:00", "Z")
    raise TypeError(f"cannot serialise {type(value).__name__} for JSON")


def dflt(kind: str) -> str:
    """The ` = ...` an initialiser parameter of this type gets, if any."""
    if kind.startswith("["):
        return " = []"
    return " = nil" if kind.endswith("?") else ""


# A slot name the JSON coders can put back exactly as they found it. Lowercase
# parts separated by single underscores, each starting with a letter, is the
# shape for which Foundation's two key strategies are true inverses.
RECOVERABLE = re.compile(r"^[a-z][a-z0-9]*(_[a-z][a-z0-9]*)*$")


def wire_names(m: Model) -> None:
    """Refuse a schema whose slot names would not survive the key strategies.

    The Swift target has no per-type CodingKeys to fall back on -- SwiftData
    reads a stored value object's properties by reflection and then encodes it
    through Codable, so renaming keys makes the two disagree and the insert
    traps at runtime. That leaves `convertFromSnakeCase` carrying the whole
    mapping, and it only round-trips for names of the shape above: `source_url`
    is fine, `source_URL` comes back `source_url` and `fat_2g` comes back
    `fat2g`, because a part beginning with a digit gets no underscore.

    Raised rather than worked around because the alternative is Swift code that
    compiles, loads the fixture, and writes a subtly different key than the
    schema declares.
    """
    bad = sorted({member.name
                  for shape in m.shapes.values()
                  for member in shape.members
                  if not RECOVERABLE.match(member.name)})
    if bad:
        raise ValueError(
            "slot names not recoverable through JSON key conversion, so the "
            f"Swift target cannot name them: {', '.join(bad)}. Rename to "
            "lowercase words joined by underscores.")


def doc(text: str, indent: int = 4) -> str:
    """Description as a Swift doc-comment body, wrapped.

    The first line is placed by the template; continuations carry their own
    indent and `///`, so a long description does not run off the page.
    """
    if not text:
        return ""
    pad = " " * indent + "/// "
    return ("\n" + pad).join(textwrap.wrap(" ".join(text.split()), width=92 - indent))


def tidy(text: str) -> str:
    """Collapse runs of blank lines, and drop the one before a closing brace.

    Generated Swift is assembled from independent fragments, several of them
    conditional. Deciding at every seam whether a blank line is wanted makes
    the templates unreadable for no gain, so they emit freely and the spacing
    is normalised once, here.
    """
    text = re.sub(r"\n{3,}", "\n\n", text)
    return re.sub(r"\n\n([ \t]*\})", r"\n\1", text)


def env() -> Environment:
    e = Environment(
        loader=FileSystemLoader(TEMPLATES),
        undefined=StrictUndefined,      # a typo in a template is an error, not a blank
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    e.globals.update(kebab=kebab, snake=snake, camel=camel, pascal=pascal,
                     swift=swift, dflt=dflt, bare=bare, plural=plural)
    e.filters["label"] = label
    e.filters["camel"] = camel
    e.filters["pascal"] = pascal
    e.filters["swift"] = swift
    e.filters["dflt"] = dflt
    e.filters["bare"] = bare
    e.filters["plural"] = plural
    e.filters["doc"] = doc
    # A member the model initialiser has to be given. Everything else either
    # defaults to nil or to an empty list, and Embed has no `required` at all
    # for selectattr to reach.
    e.tests["mandatory"] = lambda m: not dflt(swift(m, "model"))

    # A member the store holds as a @Relationship rather than an attribute --
    # a reference, or an association class. Only these lose list order, so the
    # harness needs to know which they are and Models.swift needs to annotate
    # them; the rule is here so the two cannot drift apart.
    e.tests["relationship"] = lambda m: bool(getattr(m, "target", None)) or bool(
        getattr(getattr(m, "shape", None), "association", False))
    e.filters["cypher"] = cypher
    e.filters["frontmatter"] = frontmatter
    e.filters["record"] = record
    e.filters["cypher_pair"] = lambda kv: f"{kv[0]}: {cypher(kv[1])}"
    return e


def _one(e: Environment, template: str, out: str, **ctx) -> dict[str, str]:
    return {out: e.get_template(template).render(**ctx)}


def neo4j(m: Model, e: Environment, ctx: dict) -> dict[str, str]:
    """Schema, parameterised load patterns, and -- if a fixture exists -- seed data.

    The load file is the one to use in an application: it takes $rows and does
    not care where they came from. The seed file inlines the fixture so there is
    something runnable to point cypher-shell at.
    """
    out = {
        "neo4j/pkm-meals.cypher": e.get_template("neo4j.cypher.jinja").render(**ctx),
        "neo4j/pkm-meals.load.cypher": e.get_template("neo4j.load.cypher.jinja").render(**ctx),
    }
    if ctx.get("seed"):
        out["neo4j/pkm-meals.seed.cypher"] = e.get_template("neo4j.seed.cypher.jinja").render(**ctx)
    return out


def ladybug(m: Model, e: Environment, ctx: dict) -> dict[str, str]:
    return {
        "ladybug/pkm-meals.cypher": e.get_template("ladybug.cypher.jinja").render(**ctx),
        "ladybug/pkm-meals.load.cypher": e.get_template("ladybug.load.cypher.jinja").render(**ctx),
    }


def typeql(m: Model, e: Environment, ctx: dict) -> dict[str, str]:
    return {"typeql/pkm-meals.tql": e.get_template("typeql.tql.jinja").render(**ctx)}


def obsidian(m: Model, e: Environment, ctx: dict) -> dict[str, str]:
    """A template note and a Bases view per node.

    Only the nodes the schema declared. A promoted value object is a node in
    Neo4j and TypeQL because those stores cannot nest one, but in a vault it is
    just properties on the note that owns it -- there is no reason to make the
    user maintain a separate file for a photo caption.
    """
    out: dict[str, str] = {}
    for s in [x for x in m.declared_nodes if x.note]:
        # A multivalued scalar is prose, not a column. Obsidian's property editor
        # shows `instructions` as three chips of a sentence each and a Base cannot
        # usefully filter or group on it, so it moves to the body as an ordered
        # list -- which is also the only place its order is visible.
        #
        # Nutrition deliberately does NOT move. Six numbers are exactly what a
        # frontmatter property is for, they are the columns of the Base, and
        # Obsidian already renders them as a table at the top of the note. A body
        # section would state the same figures a second time in the same file.
        lists = [f for f in s.flat() if f.multivalued and not f.identifier]
        props = [f for f in s.flat() if not f.multivalued or f.identifier]
        common = dict(ctx, shape=s, enums=m.used_enums, headers=headers(s.flat()),
                      props=props, lists=lists,
                      # Three kinds of outgoing edge, and the difference is only
                      # ever "does the target exist as a note".
                      #
                      # A note target gets `[[…]]`, which is what makes backlinks
                      # and graph view work. A target the schema marked
                      # obsidian_note: false gets its id instead: the reference is
                      # real and has to survive a round trip, but a wikilink to a
                      # file nobody will create is a broken link, and `[[salt]]` in
                      # a large vault is a name collision waiting to resolve
                      # somewhere else. A promoted value object gets neither -- it
                      # is not a class at all, just a record in the body.
                      links_out=[x for x in m.edges if x.source.name == s.name
                                 and not x.target.promoted_from and x.target.note],
                      refs_out=[x for x in m.edges if x.source.name == s.name
                                and not x.target.promoted_from and not x.target.note],
                      nests=[x for x in s.embeds if x.promote])
        out[f"obsidian/templates/{s.name}.md"] = e.get_template("obsidian.note.md.jinja").render(**common)
        out[f"obsidian/bases/{s.name}.base"] = e.get_template("obsidian.base.jinja").render(**common)
        for note in notes(m, ctx["seed"], s) if ctx.get("seed") else []:
            out[f"obsidian/notes/{note.slug}.md"] = e.get_template(
                "obsidian.seed.md.jinja").render(**common, note=note)
    return out


def swiftdata(m: Model, e: Environment, ctx: dict) -> dict[str, str]:
    """Five files: values, payloads, models, mapping, store access.

    Split rather than emitted as one file because the layers have different
    audiences. A view wants Values and Payloads and nothing else; a preview
    wants the store too. One file would make every one of them import all of it.

    Everything goes through tidy(), because the templates emit blank lines
    freely rather than deciding at each conditional seam whether one is wanted.
    """
    wire_names(m)
    files = {"Values": "swift.values.jinja", "Payloads": "swift.payloads.jinja",
             "Models": "swift.models.jinja", "Mapping": "swift.mapping.jinja",
             "Repositories": "swift.repositories.jinja"}
    module = ctx["module"]
    out = {f"swift/{module}/{name}.swift": tidy(e.get_template(t).render(**ctx))
           for name, t in files.items()}
    if ctx.get("seed"):
        # The fixture in the shape the generated Fixture type decodes. YAML is
        # the editable form; an app bundles JSON, and the harness needs a file
        # rather than a literal.
        out[f"swift/{module}/fixture.json"] = json.dumps(
            ctx["seed"].raw, indent=2, sort_keys=True, default=iso) + "\n"
        out[f"swift/{module}Harness/Smoke.swift"] = tidy(
            e.get_template("swift.smoke.jinja").render(**ctx))
    return out


TARGETS = {"obsidian": obsidian, "neo4j": neo4j, "ladybug": ladybug, "typeql": typeql,
           "swift": swiftdata}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="generators", description=__doc__)
    ap.add_argument("schema", type=Path)
    ap.add_argument("--out", type=Path, default=Path("generated"))
    ap.add_argument("--target", action="append", choices=sorted(TARGETS),
                    help="repeatable; default is all of them")
    ap.add_argument("--dry-run", action="store_true", help="list what would be written")
    ap.add_argument("--seed", type=Path,
                    help="example-data fixture; defaults to "
                         "schema/examples/<schema>-seed.yaml when that exists")
    a = ap.parse_args(argv)

    model = Model(str(a.schema))
    fixture = a.seed or a.schema.parent / "examples" / f"{a.schema.stem}-seed.yaml"
    ctx = {
        "model": model,
        "title": model.schema.title or model.schema.name,
        "source": a.schema.as_posix(),
        "fixture": fixture.as_posix() if fixture.exists() else None,
        "seed": load(model, fixture) if fixture.exists() else None,
        # For the generated invocation comments. The database name drops the
        # separators because Neo4j database names allow letters, digits, dots,
        # and dashes but must start with a letter -- `pkmmeals` is safe anywhere.
        "db": a.schema.stem.replace("-", "").replace("_", ""),
        "stem": a.schema.stem,
        # Swift module and type-name prefix. pkm-meals -> PKMMeals.
        "module": pascal(a.schema.stem),
        "out": (a.out / "neo4j" / a.schema.stem).as_posix(),
    }
    e = env()

    written = 0
    for name in a.target or sorted(TARGETS):
        for rel, text in TARGETS[name](model, e, ctx).items():
            path = a.out / rel
            if a.dry_run:
                print(f"  would write  {path}  ({len(text):,} B)")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
                print(f"  {path}  ({len(text):,} B)")
            written += 1
    print(f"{written} file{'s' if written != 1 else ''}"
          f"{' (dry run)' if a.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
