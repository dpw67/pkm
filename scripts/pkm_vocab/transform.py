"""Turn a SKOS Editor export into the published graph.

Every step here is the mirror image of a check in `checks.py`: the export is
what the editor can express, the published graph is what a consumer should
receive. Running `check` over the output of `publish` should come back clean,
which is the build's real test.

Nothing is edited in place. `publish` returns a new graph so the export in
`vocab/src/` stays the source of truth.
"""

from __future__ import annotations

import re

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

#: The editor quotes a label into a change note and carries its language tag
#: along, giving `“Day Meal Plan@en”` inside running prose.
LANG_IN_TEXT = re.compile(r"@[a-z]{2}(?=[”\"'])")
#: `(proposed by X) (by X)` names one person twice. Only collapsed when the two
#: names match -- a proposal someone else actioned is real information.
DOUBLED_ATTRIBUTION = re.compile(r"\(proposed by ([^)]+)\) \(by \1\)")


def _parent(base: str) -> str:
    """`https://w3id.org/pkm/vocab/` -> `https://w3id.org/pkm/`."""
    return base.rstrip("/").rsplit("/", 1)[0] + "/"


def agent_base(vocab: Vocabulary) -> str:
    return _parent(vocab.base) + "agents#"


def resource_base(vocab: Vocabulary) -> str:
    return _parent(vocab.base) + "resources#"


def _under(uri: URIRef, *bases: str) -> bool:
    return any(str(uri).startswith(base) for base in bases)


def relocations(vocab: Vocabulary) -> dict[URIRef, URIRef]:
    """Metadata resources that are not where they belong, and where they belong.

    Local names keep their hyphens. `Claude-AI` and `ACE-Organization` would
    collide with the existing concepts `ClaudeAI` and `ACEOrganization` if
    CamelCased, silently merging a software agent into a vocabulary term.

    SKOS Editor 0.16.7 can mint these outside the concept namespace itself, so
    on a fresh export this may have nothing to do. It has a single annex
    namespace for both kinds, though, so with the annex set to `agents#` the
    documents arrive among the agents and still need separating.

    A resource moves when it sits under one of our three bases but not the
    right one. Anything else -- an ORCID, a homepage -- is left verbatim, which
    is the whole point of giving an agent an explicit identity URI.
    """
    g = vocab.graph
    agents, resources = agent_base(vocab), resource_base(vocab)
    ours = (vocab.base, agents, resources)
    moves: dict[URIRef, URIRef] = {}
    for types, target in ((AGENT_TYPES, agents), (DOCUMENT_TYPES, resources)):
        for cls in types:
            for subj in g.subjects(RDF.type, cls):
                if not isinstance(subj, URIRef):
                    continue
                if _under(subj, *ours) and not _under(subj, target):
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

    # 6. Change notes are generated by the editor, and it leaks its own
    #    internals into them: the language tag of a label it quotes, and the
    #    proposer's name a second time when the proposer is also the actor.
    #    Both are noise in prose a reader may see. Runs after step 5 so every
    #    literal already carries its tag and only the text needs rewriting.
    for prop in DOCUMENTED:
        for s, o in list(out.subject_objects(prop)):
            if not isinstance(o, Literal) or o.datatype is not None:
                continue
            fixed = DOUBLED_ATTRIBUTION.sub(r"(by \1)", LANG_IN_TEXT.sub("", str(o)))
            if fixed != str(o):
                out.remove((s, prop, o))
                out.add((s, prop, Literal(fixed, lang=o.language)))

    # 7. Mapping properties have domain and range skos:Concept, so pointing one
    #    at an RDF property asserts that the property is a concept. rdfs:seeAlso
    #    says the same thing without the type error.
    for prop in MAPPING_PROPS:
        for s, o in list(out.subject_objects(prop)):
            if isinstance(o, URIRef) and not str(o).startswith(vocab.base):
                tail = str(o).rstrip("/").replace("#", "/").rsplit("/", 1)[-1]
                if tail[:1].islower():
                    out.remove((s, prop, o))
                    out.add((s, RDFS.seeAlso, o))

    # 8. Collections come out of the editor with rdfs:label and skos:member and
    #    nothing else -- no prefLabel, no inScheme. A SKOS consumer looking for
    #    labels the way it does everywhere else finds 18 anonymous resources, and
    #    nothing ties them to the scheme they belong to. Neither property is
    #    domain-constrained to skos:Concept, so both are legal on a Collection.
    for coll in set(out.subjects(RDF.type, SKOS.Collection)) | set(
        out.subjects(RDF.type, SKOS.OrderedCollection)
    ):
        if not any(out.objects(coll, SKOS.prefLabel)):
            for label in out.objects(coll, RDFS.label):
                out.add((coll, SKOS.prefLabel, label))
        if vocab.scheme is not None and not any(out.objects(coll, SKOS.inScheme)):
            out.add((coll, SKOS.inScheme, vocab.scheme))

    # 9. A versionIRI names this snapshot, so a consumer can cite what they read.
    #    It goes beside the scheme, not under it: everything under `vocab/` is
    #    the term namespace `vann:preferredNamespaceUri` declares, so a
    #    versionIRI there serialises as `pkmv:0.1.4` and reads like a concept
    #    that does not exist. Beside the scheme it is also clear of the term
    #    rewrite in `scripts/w3id.htaccess` outright, rather than by relying on
    #    that rule's pattern continuing to exclude digits and dots.
    if vocab.scheme is not None:
        version = out.value(vocab.scheme, OWL.versionInfo)
        if version is not None and not any(out.objects(vocab.scheme, OWL.versionIRI)):
            root, _, name = str(vocab.scheme).rstrip("/").rpartition("/")
            out.add((vocab.scheme, OWL.versionIRI, URIRef(f"{root}/{version}/{name}")))

    return out
