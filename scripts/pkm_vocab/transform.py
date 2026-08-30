"""Turn a SKOS Editor export into the published graph.

Every step here is the mirror image of a check in `checks.py`: the export is
what the editor can express, the published graph is what a consumer should
receive. Running `check` over the output of `publish` should come back clean,
which is the build's real test.

Nothing is edited in place. `publish` returns a new graph so the export in
`vocab/src/` stays the source of truth.
"""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DCTERMS, FOAF, OWL, RDF, RDFS, SKOS

from . import ISO_BROADER, ISO_NARROWER, PROV, Vocabulary

__all__ = ["publish", "agent_base", "resource_base"]

#: Instances of these move to the agents namespace.
AGENT_TYPES = (PROV.Person, PROV.Agent, PROV.Organization, PROV.SoftwareAgent,
               FOAF.Person, FOAF.Organization)
#: Instances of these move to the resources namespace.
DOCUMENT_TYPES = (FOAF.Document,)

#: Properties whose literal value should name an agent by URI once one exists.
AGENT_PROPS = (DCTERMS.creator, DCTERMS.contributor, DCTERMS.publisher)

#: Documentation properties whose plain literals get a language tag.
DOCUMENTED = (SKOS.definition, SKOS.scopeNote, SKOS.note, SKOS.editorialNote,
              SKOS.historyNote, SKOS.changeNote, SKOS.example)

MAPPING_PROPS = (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                 SKOS.narrowMatch, SKOS.relatedMatch)

LANG = "en"


def _parent(base: str) -> str:
    """`https://w3id.org/pkm/vocab/` -> `https://w3id.org/pkm/`."""
    return base.rstrip("/").rsplit("/", 1)[0] + "/"


def agent_base(vocab: Vocabulary) -> str:
    return _parent(vocab.base) + "agents#"


def resource_base(vocab: Vocabulary) -> str:
    return _parent(vocab.base) + "resources#"


def relocations(vocab: Vocabulary) -> dict[URIRef, URIRef]:
    """Metadata resources minted inside the concept namespace, and where they belong.

    Local names keep their hyphens. `Claude-AI` and `ACE-Organization` would
    collide with the existing concepts `ClaudeAI` and `ACEOrganization` if
    CamelCased, silently merging a software agent into a vocabulary term.
    """
    g = vocab.graph
    moves: dict[URIRef, URIRef] = {}
    for types, target in ((AGENT_TYPES, agent_base(vocab)),
                          (DOCUMENT_TYPES, resource_base(vocab))):
        for cls in types:
            for subj in g.subjects(RDF.type, cls):
                if vocab.is_local(subj):
                    moves[subj] = URIRef(target + vocab.local_name(subj))
    return moves


def publish(vocab: Vocabulary) -> Graph:
    """The export as it should be served."""
    src = vocab.graph
    out = Graph()
    for prefix, uri in src.namespaces():
        out.bind(prefix, uri, replace=True)
    out.bind("pkma", agent_base(vocab), replace=True)
    out.bind("pkmr", resource_base(vocab), replace=True)

    # 1. Agents and documents leave the concept namespace, in both subject and
    #    object position -- concepts cite documents via dcterms:source.
    moves = relocations(vocab)
    for s, p, o in src:
        out.add((moves.get(s, s), p, moves.get(o, o) if isinstance(o, URIRef) else o))

    # 2. A minted agent URI the data then ignores in favour of a bare string.
    #    Built after the move so it resolves to the new URI.
    by_name = {str(n): s for s in out.subjects(RDF.type, None) for n in out.objects(s, FOAF.name)}
    for prop in AGENT_PROPS:
        for s, o in list(out.subject_objects(prop)):
            if isinstance(o, Literal) and str(o) in by_name:
                out.remove((s, prop, o))
                out.add((s, prop, by_name[str(o)]))

    # 3. ISO 25964 relations entail skos:broader but do not assert it, so a
    #    plain-SKOS consumer sees no hierarchy at all.
    for prop in ISO_BROADER:
        for child, parent in list(out.subject_objects(prop)):
            out.add((child, SKOS.broader, parent))
    for prop in ISO_NARROWER:
        for parent, child in list(out.subject_objects(prop)):
            out.add((child, SKOS.broader, parent))

    # 4. Both directions, so neither is invisible without a reasoner. Must
    #    follow step 3 or the newly materialised parents have no inverse.
    for child, parent in list(out.subject_objects(SKOS.broader)):
        out.add((parent, SKOS.narrower, child))
    for parent, child in list(out.subject_objects(SKOS.narrower)):
        out.add((child, SKOS.broader, parent))

    # 5. The vocabulary is @en throughout; untagged notes claim to be languageless.
    for prop in DOCUMENTED:
        for s, o in list(out.subject_objects(prop)):
            if isinstance(o, Literal) and o.datatype is None and not o.language:
                out.remove((s, prop, o))
                out.add((s, prop, Literal(str(o), lang=LANG)))

    # 6. Mapping properties have domain and range skos:Concept, so pointing one
    #    at an RDF property asserts that the property is a concept. rdfs:seeAlso
    #    says the same thing without the type error.
    for prop in MAPPING_PROPS:
        for s, o in list(out.subject_objects(prop)):
            if isinstance(o, URIRef) and not str(o).startswith(vocab.base):
                tail = str(o).rstrip("/").replace("#", "/").rsplit("/", 1)[-1]
                if tail[:1].islower():
                    out.remove((s, prop, o))
                    out.add((s, RDFS.seeAlso, o))

    # 7. A versionIRI names this snapshot, so a consumer can cite what they read.
    #    Dots keep it clear of the term-URI rewrite rule in the w3id .htaccess.
    if vocab.scheme is not None:
        version = out.value(vocab.scheme, OWL.versionInfo)
        if version is not None and not any(out.objects(vocab.scheme, OWL.versionIRI)):
            out.add((vocab.scheme, OWL.versionIRI, URIRef(f"{vocab.base}{version}")))

    return out
