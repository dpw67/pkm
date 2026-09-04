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
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from . import Model, Shape


def surrogate(parent_id: str, slot: str, index: int) -> str:
    """Deterministic key for a promoted value object. `<parent>#images/0`.

    Derived rather than random so the loaders are idempotent: MERGE on this id
    updates the existing node instead of adding another one.
    """
    return f"{parent_id}#{slot}/{index}"


@dataclass
class Seed:
    model: Model
    raw: dict[str, list[dict[str, Any]]]
    nodes: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    nested: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    pairs: dict[str, list[tuple[str, str]]] = field(default_factory=dict)

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
                self.pairs[edge.table].extend((parent, t) for t in targets)
            for embed in shape.embeds:
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
                    self.pairs[edge.table].append((parent, key))


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
