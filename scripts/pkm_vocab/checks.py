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

#: Documentation properties carrying prose, whether or not a reader ever sees
#: it. Same list as `transform.DOCUMENTED`, plus the scheme's own description.
DOCUMENTED = (SKOS.definition, SKOS.scopeNote, SKOS.note, SKOS.editorialNote,
              SKOS.historyNote, SKOS.changeNote, SKOS.example)
PROSE = DOCUMENTED + (DCTERMS.description,)

#: The two of those the renderers drop on the floor. Both are unused today, so
#: nothing is hidden; the point is that `skos:editorialNote` was in this state
#: for as long as term pages have existed -- 0.1.4 through 0.1.6 -- and the
#: only thing that would have said so was a check like this one.
UNRENDERED = (SKOS.historyNote, SKOS.example)

#: `..` that is not part of an ellipsis. Scope notes legitimately contain
#: `...` inside code spans like `<% ... %>`, so those must not match.
DOUBLE_PERIOD = re.compile(r"(?<!\.)\.\.(?!\.)")
#: Two or more spaces between non-space characters. Renders as one space in
#: HTML, so it is invisible on the page and only shows in the RDF.
PADDED_LITERAL = re.compile(r"\S {2,}\S")
#: What a finished definition ends with. `)` is here because a definition may
#: close on a parenthetical — "\u2026 Recipe Maker (WPRM)".
TERMINAL_PUNCTUATION = ".?!)"
#: Verbs that make prose a claim about what the subject gathers up, with any
#: article that follows them. Only a match whose next words are the subject's
#: own name is a defect, so this half of the test can afford to be generous.
AGGREGATING_VERB = re.compile(
    r"\b(?:aggregates?|comprises?|collects?|consists\s+of|rolls\s+up|"
    r"contains?|includes?)\s+(?:the|its|all|any)?\s*"
)
#: A language tag written *inside* the text, as in `“Day Meal Plan@en”`. The
#: SKOS Editor emits this when it quotes a label into a change note.
LANG_IN_TEXT = re.compile(r"@[a-z]{2}(?=[”\"'])")
#: The editor names the proposer and then names them again as the actor.
DOUBLED_ATTRIBUTION = re.compile(r"\(proposed by ([^)]+)\) \(by \1\)")
#: Every editor-generated change note ends in `(by Someone)`. A note that is
#: dated but unattributed was therefore typed by hand, which is how a
#: duplicate of the editor's own record gets in.
ATTRIBUTED = re.compile(r"\(by [^)]+\)\s*$")
DATED = re.compile(r"\d{4}-\d{2}-\d{2}")

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

    # Text hygiene. None of this breaks a query, but definitions and scope
    # notes are rendered verbatim onto every term page, so a reader sees them.
    # The first two mirror a normalisation step in `transform.py`, so the build
    # repairs them on the way out. The two after do not: only an author knows
    # what the text was meant to say, so the check reports and stops there.
    for prop in PROSE:
        for subj, obj in g.subject_objects(prop):
            if not isinstance(obj, Literal) or obj.datatype is not None:
                continue
            text = str(obj)
            if DOUBLE_PERIOD.search(text):
                report.add(
                    WARN, "double-period",
                    f"{vocab.curie(prop)} ends a sentence with two periods",
                    ln(subj) or "scheme",
                )
            if PADDED_LITERAL.search(text):
                report.add(
                    WARN, "padded-literal",
                    f"{vocab.curie(prop)} has two or more consecutive spaces; "
                    "HTML collapses them, so the page hides what the RDF says",
                    ln(subj) or "scheme",
                )

    # A definition that stops without punctuation reads as truncated. One
    # missing full stop across 223 definitions is a typo; the check exists so
    # that the next one shows up as a line in the report rather than on a page.
    for subj, obj in g.subject_objects(SKOS.definition):
        if not isinstance(obj, Literal) or obj.datatype is not None:
            continue
        text = str(obj).strip()
        if text and text[-1] not in TERMINAL_PUNCTUATION:
            report.add(
                WARN, "definition-no-terminal-punctuation",
                f"skos:definition ends with {text[-1]!r} rather than a full "
                f"stop: \u201c\u2026{text[-32:]}\u201d",
                ln(subj) or "scheme",
            )

    # Prose naming its own subject as the thing it gathers up. A roll-up chain
    # (Day to Week to Month to Quarter to Year) reads as a loop when one rung
    # points at itself, and the wording at every rung is identical but for the
    # period name, so the copy-paste that causes it is invisible one term at a
    # time. Deliberately narrow: an aggregating verb, then the subject's own
    # name, and nothing else counts.
    for prop in (SKOS.definition, SKOS.scopeNote):
        for subj, obj in g.subject_objects(prop):
            if not isinstance(obj, Literal) or obj.datatype is not None:
                continue
            text = str(obj)
            names = {ln(subj)}
            names.update(str(x) for x in g.objects(subj, SKOS.prefLabel))
            names = sorted((n for n in names if n), key=len, reverse=True)
            for match in AGGREGATING_VERB.finditer(text):
                rest = text[match.end():]
                hit = next((n for n in names if rest.startswith(n)), None)
                # A name that is merely the prefix of a longer term is not a
                # self-reference: `pkmv:TopicCluster` may legitimately contain
                # Topic Cluster Core notes. Only a lowercase or punctuated
                # continuation means the subject itself was named.
                if hit is None or rest[len(hit):][:1].isupper():
                    continue
                report.add(
                    WARN, "self-referential-prose",
                    f"{vocab.curie(prop)} says it {match.group().strip()} "
                    f"{hit} \u2014 itself",
                    ln(subj) or "scheme",
                )
                break

    # High-volume editor artifacts: counted, with an example, because naming
    # 151 subjects individually would bury everything else in the report.
    for pattern, code, note in (
        (LANG_IN_TEXT, "lang-tag-in-text",
         "carry a language tag inside the text, as in \u201cDay Meal Plan@en\u201d"),
        (DOUBLED_ATTRIBUTION, "doubled-attribution",
         "name the same person twice, as in \u201c(proposed by X) (by X)\u201d"),
    ):
        hits = [
            (s, o) for prop in PROSE for s, o in g.subject_objects(prop)
            if isinstance(o, Literal) and o.datatype is None and pattern.search(str(o))
        ]
        if hits:
            report.add(
                WARN, code,
                f"{len(hits)} documentation literal(s) {note}, e.g. "
                f"{ln(hits[0][0])}; the build step can fix these",
            )

    # A dated change note with no `(by ...)` is a hand edit, and the one in the
    # data duplicates an editor-generated note for the same change.
    for subj, obj in g.subject_objects(SKOS.changeNote):
        text = str(obj)
        if DATED.match(text) and not ATTRIBUTED.search(text):
            report.add(
                WARN, "unattributed-changenote",
                f'change note "{text}" is dated but not attributed, so it was '
                "typed by hand; check it does not duplicate an editor-generated one",
                ln(subj),
            )

    # The versionIRI names a snapshot, not a term, so it must not sit in the
    # term namespace -- there it serialises as `pkmv:0.1.4` and a consumer
    # enumerating the namespace by prefix picks up a concept that is not one.
    # Mirrors step 9 of `transform.py`, which now mints it beside the scheme.
    for version_iri in g.objects(vocab.scheme, OWL.versionIRI):
        if vocab.is_local(version_iri):
            report.add(
                WARN, "versioniri-in-term-namespace",
                f"owl:versionIRI <{version_iri}> is inside the term namespace, "
                "so it reads as a concept; it belongs beside the scheme",
                ln(vocab.scheme) or "scheme",
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

    # Collections are terms too: they have URIs in the same namespace, get their
    # own file, and dereference like a concept. A collection whose only content
    # is a label and a member list tells a reader nothing about why those members
    # were grouped. The build can supply prefLabel and inScheme; only an editor
    # can say what the grouping means.
    # skos:note counts. The SKOS Editor writes a collection's description there
    # rather than to skos:definition, so demanding definition alone would report
    # 18 undescribed collections when only 3 really are.
    describing = (SKOS.definition, SKOS.scopeNote, SKOS.note)
    for collection in collections:
        if not any(o for prop in describing for o in g.objects(collection, prop)):
            report.add(
                INFO, "collection-without-definition",
                "has no skos:definition, skos:scopeNote, or skos:note to say "
                "what the grouping means",
                ln(collection),
            )

    # Written on the term, present in the Turtle, absent from both the term
    # page and the Obsidian stub. Prose nobody reads is prose nobody corrects.
    for prop in UNRENDERED:
        for subject in sorted(set(g.subjects(prop, None))):
            report.add(
                INFO, "unrendered-prose",
                f"has {vocab.curie(prop)}, which reaches the RDF but not the "
                "term page or the Obsidian stub; move it to skos:note or "
                "teach pages.py and notes.py to render it",
                ln(subject),
            )

    untagged = sum(
        1 for prop in DOCUMENTED for o in g.objects(None, prop)
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
