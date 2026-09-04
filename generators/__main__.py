"""Render a LinkML schema to the development artifacts.

    python -m generators schema/pkm-meals.yaml --out generated
    python -m generators schema/pkm-meals.yaml --out generated --target neo4j
    python -m generators schema/pkm-meals.yaml --dry-run

Each target returns a {relative path: text} map, so a target is free to emit one
file or one per class without the driver caring which.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from . import Model, kebab, snake
from .seed import cypher, load

TEMPLATES = Path(__file__).parent / "templates"


UNITS = {"g", "mg", "kg", "ml", "l", "oz", "lb"}


def label(key: str) -> str:
    """Property key as a column header. `nutrition_sodium_mg` -> `Nutrition sodium (mg)`.

    A trailing unit suffix is the one part of a slot name that reads badly when
    it is just another word, so it goes in parentheses where a header expects it.
    """
    parts = key.split("_")
    if len(parts) > 1 and parts[-1] in UNITS:
        return f"{' '.join(parts[:-1]).capitalize()} ({parts[-1]})"
    return key.replace("_", " ").capitalize()


def env() -> Environment:
    e = Environment(
        loader=FileSystemLoader(TEMPLATES),
        undefined=StrictUndefined,      # a typo in a template is an error, not a blank
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    e.globals.update(kebab=kebab, snake=snake)
    e.filters["label"] = label
    e.filters["cypher"] = cypher
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
    for s in m.declared_nodes:
        common = dict(ctx, shape=s, enums=m.used_enums,
                      edges_out=[x for x in m.edges if x.source.name == s.name])
        out[f"obsidian/templates/{s.name}.md"] = e.get_template("obsidian.note.md.jinja").render(**common)
        out[f"obsidian/bases/{s.name}.base"] = e.get_template("obsidian.base.jinja").render(**common)
    return out


TARGETS = {"obsidian": obsidian, "neo4j": neo4j, "ladybug": ladybug, "typeql": typeql}


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
