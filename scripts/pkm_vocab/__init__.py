"""Build tooling for the PKM SKOS vocabulary.

Reads a SKOS Editor export and produces reviewable reports and published
artifacts. Nothing here is served: `scripts/` is in the Jekyll `exclude:`
list, so it can never become a resolvable URI.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCTERMS, FOAF, OWL, RDF, RDFS, SKOS, XSD

ISOTHES = Namespace("http://purl.org/iso25964/skos-thes#")
SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")
VANN = Namespace("http://purl.org/vocab/vann/")
PROV = Namespace("http://www.w3.org/ns/prov#")

__all__ = [
    "DCTERMS", "FOAF", "ISOTHES", "OWL", "PROV", "RDF", "RDFS", "SKOS",
    "SKOSXL", "VANN", "XSD", "Vocabulary", "load", "wrap",
]

#: ISO 25964 hierarchy properties, each a sub-property of skos:broader/narrower.
ISO_BROADER = (
    ISOTHES.broaderGeneric,
    ISOTHES.broaderPartitive,
    ISOTHES.broaderInstantial,
)
ISO_NARROWER = (
    ISOTHES.narrowerGeneric,
    ISOTHES.narrowerPartitive,
    ISOTHES.narrowerInstantial,
)

#: The word each ISO 25964 broader property adds to a plain parent. Lives here
#: rather than in a renderer because more than one of them needs it.
ISO_QUALIFIER = {
    ISOTHES.broaderGeneric: "generic",
    ISOTHES.broaderPartitive: "partitive",
    ISOTHES.broaderInstantial: "instantial",
}

#: A change note that opens with an ISO date, as every editor-written one does:
#: `2026-08-29 — Renamed from "Ideaverse" (by Doug Warren)`. 231 of the 964 are
#: hand-typed without one, and cannot be placed on a date they do not carry.
_DATED = re.compile(r"^\d{4}-\d{2}-\d{2}")


@dataclass
class Vocabulary:
    """A parsed SKOS vocabulary plus the handful of things we look up often."""

    graph: Graph
    path: Path
    scheme: URIRef | None
    base: str

    def concepts(self) -> list[URIRef]:
        return sorted(
            (s for s in self.graph.subjects(RDF.type, SKOS.Concept) if isinstance(s, URIRef)),
            key=self.local_name,
        )

    def collections(self) -> list[URIRef]:
        found = set(self.graph.subjects(RDF.type, SKOS.Collection))
        found |= set(self.graph.subjects(RDF.type, SKOS.OrderedCollection))
        return sorted((s for s in found if isinstance(s, URIRef)), key=self.local_name)

    def local_name(self, uri: URIRef) -> str:
        text = str(uri)
        if self.base and text.startswith(self.base):
            return text[len(self.base):]
        for sep in ("#", "/"):
            if sep in text:
                return text.rsplit(sep, 1)[1]
        return text

    def curie(self, uri: URIRef) -> str:
        if self.base and str(uri).startswith(self.base):
            return f"pkmv:{self.local_name(uri)}"
        return self.graph.namespace_manager.normalizeUri(uri)

    def is_local(self, node: object) -> bool:
        return isinstance(node, URIRef) and bool(self.base) and str(node).startswith(self.base)

    def label(self, uri: URIRef) -> str:
        for prop in (SKOS.prefLabel, RDFS.label, DCTERMS.title):
            value = self.graph.value(uri, prop)
            if value is not None:
                return str(value)
        return self.local_name(uri)

    def broader_pairs(self) -> set[tuple[URIRef, URIRef]]:
        """(child, parent) from skos:broader, skos:narrower, and ISO sub-properties."""
        pairs: set[tuple[URIRef, URIRef]] = set()
        for prop in (SKOS.broader, *ISO_BROADER):
            for child, parent in self.graph.subject_objects(prop):
                pairs.add((child, parent))
        for prop in (SKOS.narrower, *ISO_NARROWER):
            for parent, child in self.graph.subject_objects(prop):
                pairs.add((child, parent))
        return pairs

    def change_notes(self, uri: URIRef) -> list[str]:
        """A term's skos:changeNote values, newest first.

        ISO dates sort lexically, so reversing a plain sort is chronological.
        The undated notes follow, sorted alphabetically, rather than being
        interleaved on a date they do not have. Ordering is fixed either way:
        these land in a generated file, and an unstable sort would churn the
        diff on every build.

        Lives here rather than in a renderer because both of them need it.
        """
        notes = [str(o) for o in self.graph.objects(uri, SKOS.changeNote)]
        dated = sorted((n for n in notes if _DATED.match(n)), reverse=True)
        return dated + sorted(n for n in notes if not _DATED.match(n))


def load(path: str | Path) -> Vocabulary:
    """Parse a Turtle file and work out its concept scheme and base namespace.

    The base namespace is read out of the data rather than hardcoded, so
    renaming the scheme in the SKOS Editor does not require a code change.
    """
    import rdflib

    # Off by default rdflib rewrites "2026-08-16T12:05:34Z"^^xsd:date to
    # "2026-08-16" on parse, hiding exactly the malformed literals we want to
    # report. A linter must see the file as written.
    previous = rdflib.NORMALIZE_LITERALS
    rdflib.NORMALIZE_LITERALS = False
    try:
        path = Path(path)
        graph = Graph()
        graph.parse(path, format="turtle")
    finally:
        rdflib.NORMALIZE_LITERALS = previous

    return wrap(graph, path)


def wrap(graph: Graph, path: str | Path = "<memory>") -> Vocabulary:
    """Find the concept scheme and base namespace of an already-parsed graph.

    Split out of `load` so the build can run `check` over the transformed
    graph without a round trip through the filesystem.
    """
    schemes = [s for s in graph.subjects(RDF.type, SKOS.ConceptScheme) if isinstance(s, URIRef)]
    scheme = schemes[0] if schemes else None

    base = ""
    if scheme is not None:
        base = str(scheme).rstrip("/") + "/"
    else:
        bound = dict(graph.namespaces())
        for prefix in ("pkmv", "pkm", ""):
            if prefix in bound:
                base = str(bound[prefix])
                break

    return Vocabulary(graph=graph, path=Path(path), scheme=scheme, base=base)
