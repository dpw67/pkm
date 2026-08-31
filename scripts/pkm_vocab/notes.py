"""Generate Obsidian term stubs from the published vocabulary.

The stubs mirror the vocabulary into an Obsidian vault so that terms take part
in the vault's link graph -- backlinks, graph view, and above all *unlinked
mentions*, which is the mechanism that connects migrated notes to the
vocabulary. A static site cannot offer any of that.

They are a cache, not a source. Definitions stay canonical at
w3id.org/pkm/vocab; every stub links back to its term page and Turtle file, and
the whole output directory is safe to delete and regenerate. Hand edits are
lost on the next run, which is why prose that matters lives one level up in the
vault (the hub, open questions, changelog) rather than in here.

Input is the PUBLISHED Turtle rather than the SKOS Editor export, so the URIs
and dates in the notes match what actually resolves.
"""

from __future__ import annotations

import re
from pathlib import Path

from rdflib import URIRef

from . import (
    DCTERMS,
    ISO_BROADER,
    ISOTHES,
    OWL,
    RDFS,
    SKOS,
    Vocabulary,
)

#: Filename qualifier per kind. Twenty preferred labels collide with notes that
#: already exist in the vault (App, Map, Project, Taxonomy, Health, Swift, ...),
#: and an ambiguous [[App]] is the exact drift the vocabulary exists to prevent.
#: The suffix follows the vault's own "(Source)" / "(Prompts)" convention.
CONCEPT_SUFFIX = "Term"
COLLECTION_SUFFIX = "Collection"

#: Characters that cannot appear in a filename on macOS/Windows.
_UNSAFE = re.compile(r'[\\/:*?"<>|]')

#: Scalars needing quotes in YAML: anything with structural punctuation, or
#: leading/trailing whitespace.
_NEEDS_QUOTE = re.compile(r'''[:#\[\]{},&*?|<>=!%@`"']|^\s|\s$''')

ISO_QUALIFIER = {
    ISOTHES.broaderGeneric: "generic",
    ISOTHES.broaderPartitive: "partitive",
    ISOTHES.broaderInstantial: "instantial",
}


def _yaml(value: str) -> str:
    if value == "" or _NEEDS_QUOTE.search(value):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def _first(vocab: Vocabulary, subject: URIRef, prop) -> str | None:
    value = vocab.graph.value(subject, prop)
    return None if value is None else str(value)


def _all(vocab: Vocabulary, subject: URIRef, prop) -> list[str]:
    return sorted(str(o) for o in vocab.graph.objects(subject, prop))


def stems(vocab: Vocabulary) -> dict[URIRef, str]:
    """Map every concept and collection URI to its note filename stem."""
    out: dict[URIRef, str] = {}
    for uri in vocab.concepts():
        out[uri] = _UNSAFE.sub("-", f"{vocab.label(uri)} ({CONCEPT_SUFFIX})")
    for uri in vocab.collections():
        out[uri] = _UNSAFE.sub("-", f"{vocab.label(uri)} ({COLLECTION_SUFFIX})")
    return out


def _link(vocab: Vocabulary, stem: dict[URIRef, str], uri: URIRef) -> str:
    """A piped wikilink, so bodies read as labels rather than as filenames."""
    if uri not in stem:
        return f"<{uri}>"                      # outside the scheme
    return f"[[{stem[uri]}|{vocab.label(uri)}]]"


def render_note(vocab: Vocabulary, stem: dict[URIRef, str], uri: URIRef,
                in_collection: dict[URIRef, list[URIRef]], base: str) -> str:
    """One stub, frontmatter and body."""
    graph = vocab.graph
    is_collection = uri in set(vocab.collections())
    kind = "collection" if is_collection else "term"
    local = vocab.local_name(uri)

    label = vocab.label(uri)
    alts = _all(vocab, uri, SKOS.altLabel)
    definition = _first(vocab, uri, SKOS.definition)
    scope = _first(vocab, uri, SKOS.scopeNote)
    note = _first(vocab, uri, SKOS.note)
    created = _first(vocab, uri, DCTERMS.created)
    modified = _first(vocab, uri, DCTERMS.modified)
    broader = sorted(o for o in graph.objects(uri, SKOS.broader) if vocab.is_local(o))
    narrower = sorted(o for o in graph.objects(uri, SKOS.narrower) if vocab.is_local(o))
    related = sorted(o for o in graph.objects(uri, SKOS.related) if vocab.is_local(o))
    members = sorted(o for o in graph.objects(uri, SKOS.member) if vocab.is_local(o))
    see_also = _all(vocab, uri, RDFS.seeAlso)
    matches = _all(vocab, uri, SKOS.relatedMatch)
    is_top = bool(list(graph.objects(uri, SKOS.topConceptOf)))
    deprecated = bool(list(graph.objects(uri, OWL.deprecated)))

    # ISO 25964 specialisations are sub-properties of skos:broader, so a
    # qualified parent is ALSO a broader parent. Annotate in place rather than
    # listing the same parent under two headings.
    qualifier: dict[URIRef, str] = {}
    for prop in ISO_BROADER:
        for parent in graph.objects(uri, prop):
            if vocab.is_local(parent):
                qualifier[parent] = ISO_QUALIFIER[prop]
    parents = list(broader) + [p for p in sorted(qualifier) if p not in broader]

    fm: list[str] = ["---"]
    if alts:
        fm.append("aliases:")
        fm += [f"  - {_yaml(a)}" for a in alts]
    if len(parents) == 1:
        fm.append(f'up: "[[{stem[parents[0]]}]]"')
    elif parents:
        fm.append("up:")
        fm += [f'  - "[[{stem[p]}]]"' for p in parents]
    else:
        fm.append("up:")
    if related:
        fm.append("related:")
        fm += [f'  - "[[{stem[r]}]]"' for r in related]
    else:
        fm.append("related:")
    if created:
        fm.append(f"created: {created}")
    if modified:
        # `modified` rather than `updated`: the vault's chosen name, and it
        # echoes dcterms:modified, which is where this value comes from.
        fm.append(f"modified: {modified}")
    fm.append("tags:")
    fm.append(f"  - vocab/{kind}")
    if is_top:
        fm.append("  - vocab/top-concept")
    if deprecated:
        fm.append("  - vocab/deprecated")
    fm.append("publish: true")
    fm.append(f"uri: {base}{local}")
    fm.append("---")

    body: list[str] = [f"#vocab/{kind} ", "", f"# {label}", ""]
    if deprecated:
        replaced = _all(vocab, uri, DCTERMS.isReplacedBy)
        body += ["> [!warning] Deprecated",
                 "> This term is retired but stays resolvable."]
        body += [f"> Replaced by <{r}>" for r in replaced]
        body += [""]
    if definition:
        body += [definition, ""]
    elif note:
        body += [note, ""]

    body += ["> [!info]- Canonical definition",
             "> This term is maintained in the [[vocab|PKM Vocabulary]] SKOS source, not here.",
             f"> `{vocab.curie(uri)}` · [term page]({base}{local})"
             f" · [Turtle]({base}terms/{local}.ttl)",
             ""]

    if scope:
        body += ["## Scope", "", scope, ""]
    if note and definition:
        body += ["## Note", "", note, ""]
    if parents:
        body += ["## Broader", ""]
        for p in parents:
            tag = f" — {qualifier[p]} (ISO 25964)" if p in qualifier else ""
            body.append(f"- {_link(vocab, stem, p)}{tag}")
        body.append("")
    if narrower:
        body += ["## Narrower", ""] + [f"- {_link(vocab, stem, n)}" for n in narrower] + [""]
    if related:
        body += ["## Related", ""] + [f"- {_link(vocab, stem, r)}" for r in related] + [""]
    if members:
        body += [f"## Members ({len(members)})", ""]
        body += [f"- {_link(vocab, stem, m)}" for m in members] + [""]
    if uri in in_collection:
        body += ["## Collections", ""]
        body += [f"- {_link(vocab, stem, c)}" for c in in_collection[uri]] + [""]
    if see_also or matches:
        body += ["## External", ""]
        body += [f"- see also <{u}>" for u in see_also]
        body += [f"- related match <{u}>" for u in matches]
        body += [""]

    return "\n".join(fm) + "\n" + "\n".join(body)


def render_notes(vocab: Vocabulary) -> dict[str, str]:
    """Every stub, keyed by filename."""
    stem = stems(vocab)
    base = vocab.base or "https://w3id.org/pkm/vocab/"
    if not base.endswith("/"):
        base += "/"

    # Reverse index: concept -> the collections listing it as a member.
    in_collection: dict[URIRef, list[URIRef]] = {}
    for collection in vocab.collections():
        for member in vocab.graph.objects(collection, SKOS.member):
            if vocab.is_local(member):
                in_collection.setdefault(member, []).append(collection)
    for key in in_collection:
        in_collection[key].sort(key=vocab.label)

    return {
        f"{stem[uri]}.md": render_note(vocab, stem, uri, in_collection, base)
        for uri in list(vocab.concepts()) + list(vocab.collections())
    }


def write_notes(vocab: Vocabulary, out: Path, prune: bool = True,
                dry_run: bool = False) -> tuple[int, int, list[str]]:
    """Write every stub to `out`.

    Returns (written, unchanged, pruned). Files are only rewritten when their
    content changes, so an unchanged run leaves mtimes alone and Obsidian does
    not re-index 241 notes for nothing.
    """
    notes = render_notes(vocab)
    written = unchanged = 0
    if not dry_run:
        out.mkdir(parents=True, exist_ok=True)

    for name, text in sorted(notes.items()):
        path = out / name
        if path.exists() and path.read_text(encoding="utf-8") == text:
            unchanged += 1
            continue
        written += 1
        if not dry_run:
            path.write_text(text, encoding="utf-8")

    # A renamed or retired term leaves its old stub behind, which would go on
    # resolving as a stale wikilink target. The directory is entirely generated,
    # so anything unaccounted for is stale by definition.
    pruned: list[str] = []
    if prune and out.is_dir():
        for path in sorted(out.glob("*.md")):
            if path.name not in notes:
                pruned.append(path.name)
                if not dry_run:
                    path.unlink()

    return written, unchanged, pruned
