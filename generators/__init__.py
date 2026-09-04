"""Turn a LinkML schema into the shapes the artifact templates need.

LinkML says whether a class has an identifier and whether a slot is inlined.
Neither is a graph concept, but together they decide everything the four
targets disagree about: what becomes a node, what becomes a property, and what
has to be promoted because the target cannot nest a record.

Three kinds of slot come out of a class:

    Field   a scalar, an enum, or a list of scalars -- a property everywhere
    Embed   an inlined value object with no identity of its own
    Edge    a reference to a class that has an identifier -- a relationship

Embeds are where the targets part company. A single embed flattens into
prefixed properties (``nutrition_calories``) everywhere. A *multivalued* embed
cannot: Neo4j properties are scalars or lists of scalars, and TypeDB attributes
are values, so a list of records has to be promoted to a node. Ladybug alone
can hold it, as ``STRUCT(...)[]``. ``Embed.promote`` marks that case so the
templates that must promote can, and the one that need not, doesn't.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition

# LinkML type -> target type. Kept here rather than in the templates so the
# four stay honest with each other: adding a LinkML type breaks all of them at
# once instead of silently emitting STRING in three places and nothing in one.
TYPES: dict[str, dict[str, str]] = {
    #                neo4j          ladybug         typeql      obsidian
    "string":     {"neo4j": "STRING",  "ladybug": "STRING",   "typeql": "string",   "obsidian": "text"},
    "uri":        {"neo4j": "STRING",  "ladybug": "STRING",   "typeql": "string",   "obsidian": "text"},
    "uriorcurie": {"neo4j": "STRING",  "ladybug": "STRING",   "typeql": "string",   "obsidian": "text"},
    "integer":    {"neo4j": "INTEGER", "ladybug": "INT64",    "typeql": "integer",  "obsidian": "number"},
    "float":      {"neo4j": "FLOAT",   "ladybug": "DOUBLE",   "typeql": "double",   "obsidian": "number"},
    "double":     {"neo4j": "FLOAT",   "ladybug": "DOUBLE",   "typeql": "double",   "obsidian": "number"},
    "decimal":    {"neo4j": "FLOAT",   "ladybug": "DECIMAL(18, 4)", "typeql": "decimal", "obsidian": "number"},
    "boolean":    {"neo4j": "BOOLEAN", "ladybug": "BOOLEAN",  "typeql": "boolean",  "obsidian": "checkbox"},
    "date":       {"neo4j": "DATE",    "ladybug": "DATE",     "typeql": "date",     "obsidian": "date"},
    "datetime":   {"neo4j": "ZONED DATETIME", "ladybug": "TIMESTAMP", "typeql": "datetime", "obsidian": "datetime"},
}
FALLBACK = {"neo4j": "STRING", "ladybug": "STRING", "typeql": "string", "obsidian": "text"}


def snake(name: str) -> str:
    """CamelCase -> snake_case. RecipeImage -> recipe_image."""
    out: list[str] = []
    for i, ch in enumerate(name):
        if ch.isupper() and i and not name[i - 1].isupper():
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def kebab(name: str) -> str:
    return snake(name).replace("_", "-")


@dataclass
class Field:
    name: str
    range: str                      # LinkML type name, or enum name
    description: str = ""
    required: bool = False
    multivalued: bool = False
    enum: Optional[str] = None      # enum name when the range is an enum
    concept: Optional[str] = None   # pkmv: CURIE from see_also
    identifier: bool = False
    prefix: str = ""                # set when flattened out of an embed
    surrogate: bool = False         # minted by promotion, not in the schema

    @property
    def key(self) -> str:
        """Flattened property name, without the stutter.

        RecipeSource.source_kind embedded at `source` is source_kind, not
        source_source_kind -- the slot already carries its owner's name.
        """
        if not self.prefix:
            return self.name
        if self.name.startswith(f"{self.prefix}_"):
            return self.name
        return f"{self.prefix}_{self.name}"

    def type(self, target: str) -> str:
        base = TYPES.get(self.range, FALLBACK)[target]
        if not self.multivalued:
            return base
        return {"neo4j": f"LIST<{base}>", "ladybug": f"{base}[]"}.get(target, base)


@dataclass
class Embed:
    name: str
    shape: "Shape"
    multivalued: bool
    description: str = ""

    @property
    def promote(self) -> bool:
        """True when the target has to make this a node instead of a property."""
        return self.multivalued

    def struct(self, target: str = "ladybug") -> str:
        """Nested record type. Ladybug is the only target that can store one."""
        cols = ", ".join(f"{f.name} {f.type(target)}"
                         for f in self.shape.fields if not f.surrogate)
        return f"STRUCT({cols})" + ("[]" if self.multivalued else "")


@dataclass
class Edge:
    name: str
    target: "Shape"
    source: "Shape"
    multivalued: bool
    description: str = ""
    renamed: str = ""          # set by Model when the default name collides

    @property
    def rel(self) -> str:
        """Neo4j relationship type. HAS_INGREDIENT.

        De-stuttered like `table` and `relation`: Recipe -> RecipeImage is
        HAS_IMAGE, since the label on the other end already says Recipe.
        """
        return f"HAS_{snake(self._target).upper()}"

    @property
    def _target(self) -> str:
        """Target name with the source's name stripped off the front.

        Recipe -> RecipeImage reads as RecipeHasImage, not RecipeHasRecipeImage.
        """
        if self.target.name.startswith(self.source.name) and self.target.name != self.source.name:
            return self.target.name[len(self.source.name):]
        return self.target.name

    @property
    def table(self) -> str:
        """Ladybug rel table. Globally unique, so it carries both ends."""
        return f"{self.source.name}Has{self._target}"

    @property
    def relation(self) -> str:
        """TypeQL relation type. recipe-ingredient.

        `renamed` is set when the default would clash with an entity type --
        TypeDB keeps entity, relation, and attribute type names in one
        namespace, so `entity recipe-image` and `relation recipe-image` cannot
        coexist. See Model._disambiguate.
        """
        return self.renamed or f"{kebab(self.source.name)}-{kebab(self._target)}"

    @property
    def role_source(self) -> str:
        return kebab(self.source.name)

    @property
    def role_target(self) -> str:
        """Target role, de-stuttered like the relation name.

        `relation recipe-image, relates recipe, relates image` -- not
        `relates recipe-image`, which reads as if the role were the relation.
        """
        return kebab(self._target)


@dataclass
class Shape:
    name: str
    description: str = ""
    comments: list[str] = field(default_factory=list)
    class_uri: str = ""
    concept: Optional[str] = None
    fields: list[Field] = field(default_factory=list)
    embeds: list[Embed] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    identifier: Optional[Field] = None
    promoted_from: Optional[str] = None   # set on shapes promoted out of an embed

    @property
    def is_node(self) -> bool:
        return self.identifier is not None

    def flat(self) -> list[Field]:
        """Scalars, plus the scalars of every embed that is not promoted.

        Prefixed, because Obsidian's property editor does not handle nested
        objects and Neo4j has no nested properties at all.
        """
        out = list(self.fields)
        for e in self.embeds:
            if e.promote:
                continue
            for f in e.shape.fields:
                out.append(Field(**{**f.__dict__, "prefix": e.name}))
        return out


class Model:
    """Every shape in a schema, plus the derived node set."""

    def __init__(self, path: str):
        self.sv = SchemaView(path)
        self.schema = self.sv.schema
        self.shapes: dict[str, Shape] = {}
        self.enums = self.sv.all_enums()
        for name in self.sv.all_classes():
            self._shape(name)
        for name in self.sv.all_classes():
            self._link(name)
        self._promote()
        self._edges = [e for s in self.shapes.values() for e in s.edges] + [
            Edge(e.name, e.shape, s, True, e.description)
            for s in self.shapes.values() for e in s.embeds if e.promote
        ]
        self._disambiguate()

    # -- build -----------------------------------------------------------
    def _shape(self, name: str) -> Shape:
        if name in self.shapes:
            return self.shapes[name]
        c: ClassDefinition = self.sv.get_class(name)
        s = Shape(
            name=name,
            description=(c.description or "").strip(),
            comments=list(c.comments or []),
            class_uri=c.class_uri or "",
            concept=next((x for x in (c.see_also or []) if x.startswith("pkmv:")), None),
        )
        self.shapes[name] = s
        return s

    def _link(self, name: str) -> None:
        s = self.shapes[name]
        for slot in self.sv.class_induced_slots(name):
            rng = slot.range
            if rng in self.sv.all_classes():
                target = self.shapes[rng]
                if self._has_id(rng):
                    s.edges.append(Edge(slot.name, target, s, bool(slot.multivalued),
                                        (slot.description or "").strip()))
                else:
                    s.embeds.append(Embed(slot.name, target, bool(slot.multivalued),
                                          (slot.description or "").strip()))
            else:
                f = self._field(slot)
                s.fields.append(f)
                if f.identifier:
                    s.identifier = f

    def _field(self, slot: SlotDefinition) -> Field:
        rng = slot.range or "string"
        is_enum = rng in self.enums
        return Field(
            name=slot.name,
            range=rng,
            description=(slot.description or "").strip(),
            required=bool(slot.required) or bool(slot.identifier),
            multivalued=bool(slot.multivalued),
            enum=rng if is_enum else None,
            concept=next((x for x in (slot.see_also or []) if x.startswith("pkmv:")), None),
            identifier=bool(slot.identifier),
        )

    def _has_id(self, cname: str) -> bool:
        return any(s.identifier for s in self.sv.class_induced_slots(cname))

    def _promote(self) -> None:
        """Give every promoted embed a synthetic identifier.

        A RecipeImage has no natural key -- it is a value object. But Neo4j
        needs something to MERGE on and Ladybug requires a PRIMARY KEY, so the
        promoted node gets a surrogate `id` and the loader is responsible for
        minting it. Recorded on the shape so the templates can say so.
        """
        for s in list(self.shapes.values()):
            for e in s.embeds:
                if e.promote and not e.shape.is_node:
                    surrogate = Field("id", "uriorcurie", "Surrogate key -- the value object "
                                      "has no natural identifier.", required=True,
                                      identifier=True, surrogate=True)
                    e.shape.fields.insert(0, surrogate)
                    e.shape.identifier = surrogate
                    e.shape.promoted_from = s.name

    def _disambiguate(self) -> None:
        """Rename any relation that collides with an entity type name.

        Promotion makes this systematic rather than rare: promoting
        Recipe.images mints an entity named after both ends (`recipe-image`),
        which is exactly what the relation between them is called. TypeDB has
        one namespace for type names, so one of the two has to move. The
        relation does, because the entity name is also what Neo4j and Ladybug
        already call the promoted node.
        """
        taken = {kebab(s.name) for s in self.nodes}
        for e in self._edges:
            if e.relation in taken:
                e.renamed = f"{kebab(e.source.name)}-has-{kebab(e._target)}"

    # -- views -----------------------------------------------------------
    @property
    def nodes(self) -> list[Shape]:
        return [s for s in self.shapes.values() if s.is_node]

    @property
    def declared_nodes(self) -> list[Shape]:
        """Nodes the schema actually declared, before promotion."""
        return [s for s in self.nodes if not s.promoted_from]

    @property
    def edges(self) -> list[Edge]:
        return self._edges

    @property
    def declared_edges(self) -> list["Edge"]:
        """Only references the schema actually declared.

        Ladybug stores nested records, so it does not promote value objects and
        does not want the synthetic edges that promotion creates.
        """
        return [e for s in self.shapes.values() for e in s.edges]

    @property
    def typeql_attributes(self) -> dict[str, Field]:
        """Every attribute TypeDB needs, deduplicated by name.

        Attribute types are global in TypeDB -- `name` is one type that many
        entities own, not one per entity. So this collapses the flattened
        fields of every shape into a single set, and raises if two shapes want
        the same attribute name with different value types, because TypeDB
        allows an attribute exactly one value type.
        """
        attrs: dict[str, Field] = {}
        for s in self.nodes:
            for f in s.flat():
                key = kebab(f.key)
                prior = attrs.get(key)
                if prior is None:
                    attrs[key] = f
                elif prior.type("typeql") != f.type("typeql"):
                    raise ValueError(
                        f"TypeQL attribute '{key}' wants two value types: "
                        f"{prior.type('typeql')} (from {prior.range}) and "
                        f"{f.type('typeql')} (from {f.range}). Rename one slot."
                    )
        return dict(sorted(attrs.items()))

    def values(self, enum: str) -> str:
        """Permitted values of an enum, comma-joined, for a generated comment."""
        return ", ".join(self.used_enums[enum].permissible_values.keys())

    def quoted(self, enum: str) -> str:
        """Permitted values as a TypeQL @values argument list."""
        return ", ".join(f'"{v}"' for v in self.used_enums[enum].permissible_values)

    @property
    def used_enums(self) -> dict:
        return {n: e for n, e in self.enums.items()}
