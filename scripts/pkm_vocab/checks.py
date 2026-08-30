"""Validation checks for the PKM SKOS vocabulary.

Three tiers, deliberately distinguished:

  ERROR  violates a SKOS integrity condition, or references something that
         does not exist. Would publish broken data.
  WARN   structurally wrong or unpublishable as-is, but not a spec violation.
         Some of these the build step can fix for you; those say so.
  INFO   editorial completeness. Nothing is broken; work remains.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field

from rdflib import Literal, URIRef

from . import (
    DCTERMS,
    FOAF,
    ISO_BROADER,
    ISO_NARROWER,
    ISOTHES,
    OWL,
    PROV,
    RDF,
    RDFS,
    SKOS,
    SKOSXL,
    VANN,
    XSD,
    Vocabulary,
)

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"

#: Local names the SKOS Editor mints automatically. Lowercase-only on purpose:
#: `pkmv:Concept` is a real term, `pkmv:concept3` is editor scaffolding.
OPAQUE = re.compile(r"^(collection|agent|doc|document|concept|scheme|person)\d*$")
#: Local names ending in a digit, which is how duplicate proposals show up.
NUMERIC_SUFFIX = re.compile(r"^(?P<stem>.*?[A-Za-z])(?P<n>\d+)$")

#: XSD lexical spaces we can cheaply police. rdflib is permissive here — it
#: silently truncates a dateTime handed to xsd:date — but Jena and SHACL are not.
LEXICAL = {
    XSD.date: re.compile(r"^-?\d{4}-\d{2}-\d{2}(Z|[+-]\d{2}:\d{2})?$"),
    XSD.dateTime: re.compile(r"^-?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$"),
    XSD.gYear: re.compile(r"^-?\d{4}(Z|[+-]\d{2}:\d{2})?$"),
}

#: Properties that should name an agent by URI once the agent has one.
AGENT_PROPS = (DCTERMS.creator, DCTERMS.contributor, DCTERMS.publisher)

#: Dates that describe a single event and so should hold a single value.
SINGLE_DATE = (DCTERMS.created, DCTERMS.modified, DCTERMS.issued)

#: Classes whose instances are metadata resources, not vocabulary terms.
NON_TERM_TYPES = (
    PROV.Person, PROV.Agent, PROV.Organization, PROV.SoftwareAgent,
    FOAF.Person, FOAF.Organization, FOAF.Document,
)

MAPPING_PROPS = (
    SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
    SKOS.narrowMatch, SKOS.relatedMatch,
)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str
    subject: str = ""

    def sort_key(self) -> tuple:
        order = {ERROR: 0, WARN: 1, INFO: 2}
        return (order[self.level], self.code, self.subject, self.message)


@dataclass
class Report:
    vocab: Vocabulary
    findings: list[Finding] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)

    def add(self, level: str, code: str, message: str, subject: str = "") -> None:
        self.findings.append(Finding(level, code, message, subject))

    def count(self, level: str) -> int:
        return sum(1 for f in self.findings if f.level == level)


def _ancestors(pairs: set[tuple[URIRef, URIRef]]) -> dict[URIRef, set[URIRef]]:
    """Transitive closure of the child -> parents relation (skos:broaderTransitive)."""
    direct: dict[URIRef, set[URIRef]] = defaultdict(set)
    for child, parent in pairs:
        direct[child].add(parent)

    closure: dict[URIRef, set[URIRef]] = {}

    def walk(node: URIRef, seen: frozenset[URIRef]) -> set[URIRef]:
        if node in closure:
            return closure[node]
        result: set[URIRef] = set()
        for parent in direct.get(node, ()):
            result.add(parent)
            if parent not in seen:
                result |= walk(parent, seen | {parent})
        closure[node] = result
        return result

    for node in list(direct):
        walk(node, frozenset({node}))
    return closure


def check(vocab: Vocabulary) -> Report:
    report = Report(vocab=vocab)
    g = vocab.graph
    ln = vocab.local_name
    concepts = vocab.concepts()
    concept_set = set(concepts)
    collections = vocab.collections()
    pairs = vocab.broader_pairs()
    ancestors = _ancestors(pairs)

    _stats(report, vocab, concepts, collections, pairs)

    # --- ERROR: SKOS integrity conditions ------------------------------------

    # S13/S14 — a preferred label must identify exactly one concept per language.
    by_label: dict[tuple[str, str], list[URIRef]] = defaultdict(list)
    for concept in concepts:
        per_lang: dict[str, list[Literal]] = defaultdict(list)
        for label in g.objects(concept, SKOS.prefLabel):
            if isinstance(label, Literal):
                per_lang[label.language or ""].append(label)
                by_label[(label.language or "", str(label).strip().casefold())].append(concept)
        for lang, labels in per_lang.items():
            if len(labels) > 1:
                shown = ", ".join(f'"{x}"' for x in sorted(map(str, labels)))
                report.add(
                    ERROR, "S14-multiple-preflabel",
                    f"has {len(labels)} preferred labels in @{lang or 'none'}: {shown}",
                    ln(concept),
                )

    for (lang, _), owners in sorted(by_label.items()):
        if len(owners) > 1:
            names = ", ".join(sorted(ln(c) for c in owners))
            report.add(
                ERROR, "S13-ambiguous-preflabel",
                f'preferred label "{g.value(owners[0], SKOS.prefLabel)}" '
                f"(@{lang or 'none'}) is shared by {len(owners)} concepts: {names}",
            )

    # S27 — skos:related is disjoint with skos:broaderTransitive.
    seen_related: set[frozenset[URIRef]] = set()
    for a, b in g.subject_objects(SKOS.related):
        if not (isinstance(a, URIRef) and isinstance(b, URIRef)):
            continue
        key = frozenset({a, b})
        if key in seen_related:
            continue
        seen_related.add(key)
        if b in ancestors.get(a, ()) or a in ancestors.get(b, ()):
            report.add(
                ERROR, "S27-related-disjoint",
                f"{ln(a)} and {ln(b)} are both skos:related and in the same "
                "broader/narrower chain; pick one relation",
                ln(a),
            )
        if a == b:
            report.add(ERROR, "S27-related-disjoint", "is skos:related to itself", ln(a))

    # Cycles in the hierarchy.
    for concept in concepts:
        if concept in ancestors.get(concept, ()):
            report.add(ERROR, "hierarchy-cycle", "is its own ancestor", ln(concept))

    # References into the vocabulary namespace that resolve to nothing.
    referring = (
        SKOS.broader, SKOS.narrower, SKOS.related, SKOS.member,
        SKOS.hasTopConcept, *ISO_BROADER, *ISO_NARROWER,
    )
    dangling: dict[str, set[str]] = defaultdict(set)
    for prop in referring:
        for subj, obj in g.subject_objects(prop):
            if vocab.is_local(obj) and obj not in concept_set and obj not in set(collections):
                dangling[ln(obj)].add(f"{ln(subj)} {vocab.curie(prop)}")
    for target, sources in sorted(dangling.items()):
        report.add(
            ERROR, "dangling-reference",
            f"referenced by {', '.join(sorted(sources))} but never declared "
            "a skos:Concept or skos:Collection",
            target,
        )

    # --- WARN: structural problems -------------------------------------------

    parents_of = defaultdict(set)
    for child, parent in pairs:
        parents_of[child].add(parent)

    top_declared = set(g.objects(vocab.scheme, SKOS.hasTopConcept)) if vocab.scheme else set()
    top_declared |= set(g.subjects(SKOS.topConceptOf, vocab.scheme)) if vocab.scheme else set()

    for concept in sorted(top_declared & concept_set, key=ln):
        if parents_of.get(concept):
            names = ", ".join(sorted(ln(p) for p in parents_of[concept]))
            report.add(
                WARN, "topconcept-with-parent",
                f"is a top concept but also has parent(s): {names}. "
                "A top concept is a root; drop one or the other",
                ln(concept),
            )

    # ISO relations entail skos:broader but do not assert it. Plain-SKOS
    # consumers see no hierarchy at all until the build materialises it.
    iso_only = 0
    for prop in ISO_BROADER:
        for child, parent in g.subject_objects(prop):
            if (child, SKOS.broader, parent) not in g:
                iso_only += 1
    if iso_only:
        report.add(
            WARN, "iso-not-materialised",
            f"{iso_only} ISO 25964 hierarchy statement(s) have no matching "
            "skos:broader. Entailed, but invisible to plain-SKOS consumers. "
            "The build step will materialise these",
        )

    asymmetric = sum(
        1 for child, parent in pairs
        if (child, SKOS.broader, parent) in g and (parent, SKOS.narrower, child) not in g
    )
    if asymmetric:
        report.add(
            INFO, "inverse-not-materialised",
            f"{asymmetric} skos:broader statement(s) have no matching "
            "skos:narrower. Valid — the two are declared inverses — but the "
            "build step will materialise them for consumers without reasoning",
        )

    for collection in collections:
        members = list(g.objects(collection, SKOS.member))
        if not members:
            report.add(
                WARN, "empty-collection",
                f'"{vocab.label(collection)}" has no skos:member; '
                "it will be filtered out of the published vocabulary",
                ln(collection),
            )

    for node in concepts + collections + _agents_and_docs(vocab):
        name = ln(node)
        if OPAQUE.match(name):
            report.add(
                WARN, "opaque-uri",
                f'URI local name is "{name}" but the label is '
                f'"{vocab.label(node)}"; the build step can rename it from the label',
                name,
            )
            continue
        match = NUMERIC_SUFFIX.match(name)
        if match:
            stem = match.group("stem")
            twin = URIRef(vocab.base + stem)
            hint = (
                f"; {stem} already exists — merge them"
                if twin in concept_set
                else " (leftover from the Proposals tab?)"
            )
            report.add(WARN, "numeric-suffix", f"local name ends in a digit{hint}", name)

    for concept in concepts:
        if vocab.scheme is not None and (concept, SKOS.inScheme, vocab.scheme) not in g:
            report.add(WARN, "missing-inscheme", "has no skos:inScheme", ln(concept))
        for label in g.objects(concept, SKOS.prefLabel):
            if isinstance(label, Literal):
                if not label.language:
                    report.add(WARN, "untagged-label", f'prefLabel "{label}" has no language tag', ln(concept))
                if str(label) != str(label).strip():
                    report.add(WARN, "padded-label", f'prefLabel "{label}" has leading/trailing whitespace', ln(concept))

    if any(g.triples((None, RDF.type, SKOSXL.Label))):
        n = len(set(g.subjects(RDF.type, SKOSXL.Label)))
        report.add(WARN, "skosxl-present", f"{n} skosxl:Label node(s) present; plain SKOS labels expected")

    # A literal whose lexical form is outside its datatype's lexical space.
    # rdflib accepts these silently; Jena and SHACL sh:datatype do not.
    ill: dict[tuple[str, str], list[str]] = defaultdict(list)
    for subj, prop, obj in g:
        if not isinstance(obj, Literal) or obj.datatype not in LEXICAL:
            continue
        if not LEXICAL[obj.datatype].match(str(obj)):
            key = (vocab.curie(prop), str(obj.datatype).rsplit("#", 1)[-1])
            ill[key].append(f"{ln(subj)} = \"{obj}\"")
    for (prop, dtype), cases in sorted(ill.items()):
        report.add(
            ERROR, "ill-typed-literal",
            f"{len(cases)} {prop} value(s) typed ^^xsd:{dtype} but outside that "
            f"lexical space, e.g. {cases[0]}",
        )

    # Two creation dates means the resource was created twice.
    for prop in SINGLE_DATE:
        offenders = [s for s in set(g.subjects(prop, None)) if len(list(g.objects(s, prop))) > 1]
        if offenders:
            report.add(
                WARN, "duplicate-date",
                f"{len(offenders)} resource(s) carry more than one {vocab.curie(prop)} "
                f"value, e.g. {ln(offenders[0])}; keep one",
            )

    # A minted agent URI that the data then ignores in favour of a bare string.
    named_agents = {
        str(name): subj
        for subj in g.subjects(RDF.type, None)
        for name in g.objects(subj, FOAF.name)
    }
    for prop in AGENT_PROPS:
        literals = [o for o in g.objects(None, prop) if isinstance(o, Literal)]
        resolvable = [x for x in literals if str(x) in named_agents]
        if resolvable:
            target = named_agents[str(resolvable[0])]
            report.add(
                WARN, "literal-agent",
                f"{len(resolvable)} {vocab.curie(prop)} value(s) are the string "
                f'"{resolvable[0]}" where <{target}> exists; use the URI',
            )

    # Agents and documents are metadata, not vocabulary terms. Minting them
    # inside the concept namespace makes them dereference as terms and puts
    # them in the per-term split.
    intruders = sorted(
        {s for cls in NON_TERM_TYPES for s in g.subjects(RDF.type, cls) if vocab.is_local(s)},
        key=ln,
    )
    for node in intruders:
        kinds = ", ".join(sorted(vocab.curie(t) for t in g.objects(node, RDF.type)))
        report.add(
            WARN, "non-term-in-concept-namespace",
            f"is a {kinds}, not a concept, but lives at {vocab.base}{ln(node)}; "
            "mint it outside the concept namespace",
            ln(node),
        )

    # SKOS mapping properties have domain and range skos:Concept. Pointing one
    # at an RDF property infers that the property is a concept, which is false.
    # Heuristic: lowerCamelCase local name means property, UpperCamelCase means class.
    for prop in MAPPING_PROPS:
        for subj, obj in g.subject_objects(prop):
            if not isinstance(obj, URIRef) or vocab.is_local(obj):
                continue
            tail = re.split(r"[#/]", str(obj).rstrip("/"))[-1]
            if tail[:1].islower():
                report.add(
                    WARN, "mapping-to-property",
                    f"{vocab.curie(prop)} <{obj}> targets what looks like an RDF "
                    "property, not a concept; rdfs:seeAlso says this without "
                    "implying the target is a skos:Concept",
                    ln(subj),
                )

    # --- INFO: editorial completeness and publication metadata ---------------

    for concept in concepts:
        if not any(g.objects(concept, SKOS.definition)):
            report.add(INFO, "missing-definition", "has no skos:definition", ln(concept))
        if not any(g.objects(concept, SKOS.scopeNote)):
            report.add(INFO, "missing-scopenote", "has no skos:scopeNote", ln(concept))
        if not parents_of.get(concept) and concept not in top_declared:
            report.add(
                INFO, "orphan", "has no parent and is not a top concept", ln(concept)
            )

    documented = (SKOS.definition, SKOS.scopeNote, SKOS.note, SKOS.editorialNote,
                  SKOS.historyNote, SKOS.changeNote, SKOS.example)
    untagged = sum(
        1 for prop in documented for o in g.objects(None, prop)
        if isinstance(o, Literal) and o.datatype is None and not o.language
    )
    if untagged:
        report.add(
            INFO, "untagged-note",
            f"{untagged} documentation literal(s) have no language tag while the "
            "rest of the vocabulary is @en; the build step can tag them",
        )

    if vocab.scheme is not None:
        for prop, code, note in (
            (VANN.preferredNamespacePrefix, "missing-vann", 'vann:preferredNamespacePrefix "pkmv"'),
            (VANN.preferredNamespaceUri, "missing-vann", "vann:preferredNamespaceUri"),
            (DCTERMS.license, "missing-license", "dcterms:license as a URI (not a dcterms:rights string)"),
            (OWL.versionInfo, "missing-version", "owl:versionInfo"),
        ):
            if not any(g.objects(vocab.scheme, prop)):
                report.add(
                    INFO, code,
                    f"concept scheme has no {note}; the build step adds this",
                    ln(vocab.scheme) or "scheme",
                )

    report.findings.sort(key=Finding.sort_key)
    return report


def _agents_and_docs(vocab: Vocabulary) -> list[URIRef]:
    from . import FOAF, PROV

    g = vocab.graph
    found: set[URIRef] = set()
    for cls in (PROV.Person, PROV.Agent, PROV.Organization, FOAF.Person, FOAF.Document):
        found |= {s for s in g.subjects(RDF.type, cls) if isinstance(s, URIRef)}
    return sorted(found, key=vocab.local_name)


def _stats(report: Report, vocab: Vocabulary, concepts, collections, pairs) -> None:
    g = vocab.graph
    s = report.stats
    s["triples"] = len(g)
    s["concepts"] = len(concepts)
    s["collections"] = len(collections)
    s["hierarchy links"] = len(pairs)
    s["skos:broader"] = sum(1 for _ in g.subject_objects(SKOS.broader))
    s["skos:narrower"] = sum(1 for _ in g.subject_objects(SKOS.narrower))
    s["ISO 25964 links"] = sum(
        1 for p in (*ISO_BROADER, *ISO_NARROWER) for _ in g.subject_objects(p)
    )
    s["skos:related pairs"] = len(
        {frozenset((a, b)) for a, b in g.subject_objects(SKOS.related)}
    )
    s["top concepts"] = len(set(g.objects(vocab.scheme, SKOS.hasTopConcept))) if vocab.scheme else 0
    s["with definition"] = sum(1 for c in concepts if any(g.objects(c, SKOS.definition)))
    s["with scope note"] = sum(1 for c in concepts if any(g.objects(c, SKOS.scopeNote)))
    s["with altLabel"] = sum(1 for c in concepts if any(g.objects(c, SKOS.altLabel)))
    s["mappings"] = sum(
        1 for p in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                    SKOS.narrowMatch, SKOS.relatedMatch)
        for _ in g.subject_objects(p)
    )
