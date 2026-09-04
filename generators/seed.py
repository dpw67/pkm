"""Turn a schema-shaped fixture into per-target rows.

The fixture is written once, in the shape of the LinkML schema: value objects
nested, references by id. Every difference between the targets is applied here
rather than in the fixture, so example data never has to be restated per store.

The interesting case is promotion. A multivalued inlined value object cannot be
a property in Neo4j or TypeDB, so the model promotes it to a node -- which means
the fixture's two images under one recipe have to become two rows and two edges,
with identifiers that do not exist in the source data. Those are minted here,
deterministically from the parent id and the list position, so re-running the
generator produces the same graph rather than a second copy of it.

The other case is the association class, which goes the opposite way: the fixture
nests it like any other value object, but it collapses onto the relationship, so
its scalars end up on the link rather than on a row at either end.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from . import Embed, Field, Model, Shape


def surrogate(parent_id: str, slot: str, index: int) -> str:
    """Deterministic key for a promoted value object. `<parent>#images/0`.

    Derived rather than random so the loaders are idempotent: MERGE on this id
    updates the existing node instead of adding another one.
    """
    return f"{parent_id}#{slot}/{index}"


@dataclass
class Link:
    """One edge, with whatever properties the relationship itself carries.

    A plain reference leaves `props` empty; a collapsed association class fills
    it with the scalars that described the use rather than the thing.
    """

    source: str
    target: str
    props: dict[str, Any] = field(default_factory=dict)


@dataclass
class Seed:
    model: Model
    raw: dict[str, list[dict[str, Any]]]
    nodes: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    nested: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    pairs: dict[str, list[Link]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for shape in self.model.declared_nodes:
            self._rows(shape)
        for edge in self.model.edges:
            self.pairs.setdefault(edge.table, [])
        for shape in self.model.declared_nodes:
            self._links(shape)

    def _rows(self, shape: Shape) -> None:
        """Flat rows for the stores that cannot nest, nested rows for the one that can."""
        flat_rows, nested_rows = [], []
        for item in self.raw.get(shape.name, []):
            flat: dict[str, Any] = {f.name: item.get(f.name) for f in shape.fields}
            nest: dict[str, Any] = dict(flat)
            for embed in shape.embeds:
                value = item.get(embed.name)
                if embed.reifies is not None:
                    continue  # belongs to the relationship, not to either end
                if embed.promote:
                    nest[embed.name] = value or []
                    continue
                nest[embed.name] = value
                for sub in embed.shape.fields:
                    if sub.surrogate:
                        continue
                    prefixed = next(f for f in shape.flat()
                                    if f.prefix == embed.name and f.name == sub.name)
                    flat[prefixed.key] = (value or {}).get(sub.name)
            flat_rows.append(flat)
            nested_rows.append(nest)
        self.nodes[shape.name] = flat_rows
        self.nested[shape.name] = nested_rows

    def _links(self, shape: Shape) -> None:
        """Edge pairs, plus the promoted rows and edges that promotion implies."""
        for item in self.raw.get(shape.name, []):
            parent = item[shape.identifier.name]
            for edge in shape.edges:
                targets = item.get(edge.name) or []
                if not edge.multivalued:
                    targets = [targets] if targets else []
                self.pairs[edge.table].extend(Link(parent, t) for t in targets)
            for embed in shape.embeds:
                if embed.reifies is not None:
                    self._associations(shape, parent, item, embed)
                    continue
                if not embed.promote:
                    continue
                edge = next(e for e in self.model.edges
                            if e.source.name == shape.name and e.target.name == embed.shape.name)
                rows = self.nodes.setdefault(embed.shape.name, [])
                for i, value in enumerate(item.get(embed.name) or []):
                    key = surrogate(parent, embed.name, i)
                    row = {"id": key}
                    row.update({f.name: value.get(f.name)
                                for f in embed.shape.fields if not f.surrogate})
                    rows.append(row)
                    self.pairs[edge.table].append(Link(parent, key))

    def _associations(self, shape: Shape, parent: str, item: dict[str, Any],
                      embed: Embed) -> None:
        """Links carrying properties, from an association class in the fixture.

        The fixture nests these -- `ingredients: [{ingredient: ..., quantity: ...}]`
        -- so the target id is read from the association's own reference slot and
        everything else becomes a property of the link.
        """
        inner = embed.reifies
        edge = next(e for e in self.model.edges
                    if e.via == embed.shape.name and e.source.name == shape.name)
        values = item.get(embed.name) or []
        if not embed.multivalued:
            values = [values]
        for value in values:
            target = value.get(inner.name)
            if target is None:
                continue
            props = {f.key: value.get(f.name) for f in edge.fields}
            for sub in edge.embeds:
                held = value.get(sub.name) or {}
                for f in edge.flat():
                    if f.prefix == sub.name:
                        props[f.key] = held.get(f.name)
            self.pairs[edge.table].append(Link(parent, target, props))


def load(model: Model, path: Path) -> Seed:
    return Seed(model, yaml.safe_load(path.read_text()) or {})


def cypher(value: Any) -> str:
    """Render a Python value as a Cypher literal.

    Strings are single-quoted with backslash and quote escaped. Datetimes are
    wrapped in datetime() rather than left as strings, since a Neo4j property
    typed ZONED DATETIME will not accept the string form.
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(cypher(v) for v in value) + "]"
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace("'", "\\'")
    if len(text) == 20 and text.endswith("Z") and text[10] == "T":
        return f"datetime('{escaped}')"
    return f"'{escaped}'"


def slug(identifier: str) -> str:
    """File name for a note, from the schema's identifier.

    `pkm:ing/ground-beef` -> `ground-beef`. Obsidian is the one target where
    identity is the file name rather than a property: a wikilink resolves by
    name, so the id has to become the name or nothing can point at the note.
    The last segment is enough here and reads better in a Base's first column;
    the full id stays in frontmatter, which is what the other targets key on.
    """
    return identifier.rsplit("/", 1)[-1].rsplit(":", 1)[-1]


@dataclass
class Note:
    """One vault note, with the three shapes of the fixture gathered together.

    Obsidian is the only target that needs all three at once. Flat scalars go to
    frontmatter, where a Base can column them. Edges become wikilinks, and the
    properties a collapsed association put on the link have to go in the body,
    since a frontmatter property holds a list of links and not a list of links
    with attributes. Promoted value objects go in the body for the same reason.

    Which means the body is also the one place list order survives: it is text,
    so `ingredients` comes back in fixture order here even though a SwiftData
    to-many and a Cypher MATCH both return it arbitrarily.
    """

    slug: str
    front: dict[str, Any]
    lists: dict[str, list[Any]] = field(default_factory=dict)
    links: dict[str, list[tuple[str, dict[str, Any]]]] = field(default_factory=dict)
    refs: dict[str, list[tuple[str, dict[str, Any]]]] = field(default_factory=dict)
    nested: dict[str, list[dict[str, Any]]] = field(default_factory=dict)


def notes(model: Model, seed: Seed, shape: Shape) -> list[Note]:
    """Seed notes for one shape, ready to render.

    Without these a generated Base has nothing to display: the templates are
    empty by design, so the only way to see whether a view works is to fill a
    note in by hand from one of the other targets' output.
    """
    key = shape.identifier.name
    names = {row[s.identifier.name]: slug(row[s.identifier.name])
             for s in model.declared_nodes for row in seed.nodes.get(s.name, [])}
    # A note target is addressed by file name; a reference target has no file, so
    # the body says what it is called and frontmatter keeps the id. `name` is the
    # only slot a label could come from, and the slug is a readable fallback.
    labels = {row[s.identifier.name]: row.get("name") or slug(row[s.identifier.name])
              for s in model.declared_nodes for row in seed.nodes.get(s.name, [])}
    out = []
    for flat, nest in zip(seed.nodes.get(shape.name, []), seed.nested.get(shape.name, [])):
        # Empty keys are left out rather than written as nulls: a Base shows a
        # missing property and an empty one the same way, and salt genuinely has
        # no nutrition. Order follows the schema, so the frontmatter reads in the
        # same order as the Base's columns.
        front = {"type": shape.name}
        front.update({k: v for k, v in flat.items()
                      if v not in (None, [], "") and not isinstance(v, list)})
        note = Note(slug=names[flat[key]], front=front,
                    # Multivalued scalars go to the body, for the reasons the
                    # note template states: ordered prose is not a column.
                    lists={k: v for k, v in flat.items() if isinstance(v, list) and v})
        for edge in model.edges:
            # Promoted targets are not notes -- same rule the note template uses
            # to decide which edges get a wikilink section.
            if edge.source.name != shape.name or edge.target.promoted_from:
                continue
            hits = [link for link in seed.pairs[edge.table] if link.source == flat[key]]
            if not hits:
                continue
            if edge.target.note:
                note.links[edge.name] = [(names[x.target], x.props) for x in hits]
                note.front[edge.name] = [f"[[{names[x.target]}]]" for x in hits]
            else:
                # No note to link to, so the property carries the id -- the same
                # reference the other three targets store, and the join key back
                # to the row in SwiftData or the node in Neo4j. A `[[…]]` here
                # would be a link to a file the generator never writes.
                note.refs[edge.name] = [(labels[x.target], x.props) for x in hits]
                note.front[edge.name] = [x.target for x in hits]
        for embed in shape.embeds:
            if embed.promote and nest.get(embed.name):
                note.nested[embed.name] = nest[embed.name]
        note.front["tags"] = [f"pkm/{shape.name.lower()}"]
        out.append(note)
    return out


def record(item: dict[str, Any], fields: list[Field] | None = None) -> str:
    """One value object as a single line of a body list.

    A `uri`-ranged field paired with exactly one other is a link, and rendering
    it as one is the difference between a note and a dump of the row. That is
    read off the schema range rather than guessed from the value: `caption` is
    the label because `url` is the uri, not because it sorts second.

    Anything else keeps its field names. Without a range to go on the generator
    has no way to know which of two strings labels the other, and a bare pair
    reads as a pair only when it happens to be two.
    """
    live = {k: v for k, v in item.items() if v is not None}
    ranges = {f.name: f.range for f in fields or []}
    uris = [k for k in live if ranges.get(k) == "uri"]
    if len(uris) == 1 and len(live) == 2:
        label = next(k for k in live if k != uris[0])
        return f"[{live[label]}]({live[uris[0]]})"
    return ", ".join(f"{k}: {v}" for k, v in live.items())


def frontmatter(front: dict[str, Any]) -> str:
    """Render a note's frontmatter as YAML.

    Dumped rather than templated, because the values are real data: a caption
    with a colon in it, or an ingredient named `Ground beef, 85% lean`, breaks
    a hand-written `{{ key }}: {{ value }}` and quotes correctly here.
    """
    return yaml.dump(front, Dumper=_Indented, sort_keys=False, allow_unicode=True,
                     default_flow_style=False, width=10000).rstrip()


class _Indented(yaml.SafeDumper):
    """SafeDumper that indents sequences under their key.

    Only so a generated note matches what Obsidian's own property editor writes.
    Both forms parse, but the flush-left one gets rewritten the first time a
    property is touched in the UI, which makes an untouched note look edited.
    """

    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, False)
