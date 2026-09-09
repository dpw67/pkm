"""Write the published graph out as files.

One bulk dump plus one file per resource, so every URI in the namespace
dereferences to a document describing it. This replaces splitting the export
by hand, which had to be redone on every edit.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import SKOS

from . import Vocabulary
from .transform import agent_base, resource_base

__all__ = ["write_all", "TERMS_DIR"]

#: Per-term files live one level down so `vocab/` stays readable. The URIs are
#: unaffected -- the w3id rewrite points at this directory.
TERMS_DIR = "terms"

#: Editorial history belongs in the bulk dump, not on every term page. It is
#: the largest thing in most records and the least useful to a consumer.
STRIP_FROM_TERMS = (SKOS.changeNote,)

#: Pulled in pointing *at* the subject as well as away from it. skos:member has
#: no inverse in SKOS, so without this a term file cannot tell you which
#: collections the term belongs to -- the statement lives only on the collection.
#: Including it keeps the triple exactly as authored; the term file simply
#: describes two subjects, which is ordinary for an RDF document.
INBOUND = (SKOS.member,)


def _subgraph(source: Graph, subject: URIRef, strip=(), inbound=()) -> Graph:
    g = Graph()
    for prefix, uri in source.namespaces():
        g.bind(prefix, uri, replace=True)
    for p, o in source.predicate_objects(subject):
        if p not in strip:
            g.add((subject, p, o))
    for p in inbound:
        for s in source.subjects(p, subject):
            g.add((s, p, subject))
    return g


def _write(graph: Graph, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(graph.serialize(format="turtle", encoding="utf-8"))
    return path


def write_all(vocab: Vocabulary, published: Graph, root: Path) -> list[Path]:
    """Emit the dump, the per-term files, and the two metadata files.

    `vocab` supplies the naming helpers; `published` is the graph to write.
    """
    written: list[Path] = []
    vocab_dir = root / "vocab"

    # The whole graph, change notes and all. void:dataDump points here.
    written.append(_write(published, vocab_dir / "pkm-vocab.ttl"))

    # One file per concept and per collection. Collections carry URIs in the
    # same namespace, so they have to dereference too.
    terms = root / "vocab" / TERMS_DIR
    for uri in [*vocab.concepts(), *vocab.collections()]:
        term = _subgraph(published, uri, strip=STRIP_FROM_TERMS, inbound=INBOUND)
        written.append(_write(term, terms / f"{vocab.local_name(uri)}.ttl"))

    # Agents and documents, each collected into the hash namespace it now lives
    # in: one request returns every subject under that URI.
    for base, out in ((agent_base(vocab), root / "agents" / "index.ttl"),
                      (resource_base(vocab), root / "resources" / "index.ttl")):
        graph = Graph()
        for prefix, uri in published.namespaces():
            graph.bind(prefix, uri, replace=True)
        for s, p, o in published:
            if isinstance(s, URIRef) and str(s).startswith(base):
                graph.add((s, p, o))
        written.append(_write(graph, out))

    return written


def stale_term_files(root: Path, keep: set[str]) -> list[Path]:
    """Per-term files for URIs the vocabulary no longer defines.

    Both representations: the Turtle and the `.md` the term page is built from,
    since a renamed term leaves one of each behind.

    Reported rather than deleted: a term disappearing usually means it was
    renamed, and the old URI should be deprecated rather than made to 404.
    """
    terms = root / "vocab" / TERMS_DIR
    if not terms.is_dir():
        return []
    return sorted(p for p in terms.iterdir()
                  if p.suffix in (".ttl", ".md") and p.stem not in keep)
