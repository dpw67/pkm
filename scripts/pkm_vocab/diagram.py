"""Render a subtree of the vocabulary as a Mermaid diagram.

Turtle and the SKOS editor bury the shape of the graph. Reading 223 concepts a
page at a time does not show you where a family sits, which is the same
observation `review.py` makes about prose -- so this is its structural
counterpart: one small diagram per chunk rather than one unreadable graph of
everything.

**Generated, not drawn.** Every hand-maintained second representation in this
project has drifted from the graph it describes: five of six subtree-mirroring
collections (ROADMAP E1), the Obsidian hub's version and counts before
`make hub`, and `reports/vocab-review.md` whenever it is not re-run. A diagram
of the *target* cannot drift, because it proposes a graph rather than describing
one. A diagram of what *exists* can, so it is derived here instead.

Mermaid rather than an image format because it renders natively in the GitHub
view of the same Markdown and in Obsidian, and needs only a few lines of
client-side JavaScript on the Pages site -- the same three-target test that
chose `<details>` over a script in 0.1.10. An SVG would need a toolchain this
repo does not have, and would itself be a second representation.

The edge style is the point. A labelled solid edge is an ISO 25964 qualified
relation; a **dotted** edge is a bare `skos:broader` with no qualifier at all.
A third of this hierarchy is undifferentiated (ROADMAP Q1), and a reader can
see which third at a glance rather than by running a query.
"""

from __future__ import annotations

import re
from collections import defaultdict

from rdflib import Graph, URIRef
from rdflib.namespace import SKOS

from . import ISO_BROADER, ISO_QUALIFIER, Vocabulary

__all__ = ["mermaid_subtree", "render_map"]

#: Mermaid node ids must be word characters. Only `Month-Health` needs this
#: today, and the hyphen is itself the malformed local name D has to rename --
#: so the sanitiser is one line rather than a reason to wait for that fix.
_ID_UNSAFE = re.compile(r"[^A-Za-z0-9_]")

#: How deep each chunk goes, and how many children one node may show. Past
#: either limit the diagram says how much it is not showing instead of drawing
#: it.
#:
#: Tuned by measuring, not guessed. Across the eight top concepts: depth 2 shows
#: 100 of 223 concepts with the largest diagram at 35 nodes; depth 3 shows 143
#: with the largest at 57; depth 4 shows 204 with the largest at 96, which is a
#: hairball and defeats the point. Depth 3 is the trade -- two thirds of the
#: vocabulary visible, and only the Obsidian Notes chunk is genuinely dense.
DEPTH = 3
CAP = 12


def _node_id(vocab: Vocabulary, uri: URIRef) -> str:
    return _ID_UNSAFE.sub("_", vocab.local_name(uri))


def _qualifiers(graph: Graph) -> dict[tuple[URIRef, URIRef], str]:
    """(child, parent) -> the ISO 25964 word for it, where there is one."""
    out: dict[tuple[URIRef, URIRef], str] = {}
    for prop in ISO_BROADER:
        for child, parent in graph.subject_objects(prop):
            out[(child, parent)] = ISO_QUALIFIER[prop]
    return out


def mermaid_subtree(vocab: Vocabulary, published: Graph, root: URIRef, *,
                    depth: int = DEPTH, cap: int = CAP) -> str:
    """One `graph TD` block for `root` and its descendants, depth-limited."""
    g = published
    qual = _qualifiers(g)
    children: dict[URIRef, list[URIRef]] = defaultdict(list)
    for child, parent in g.subject_objects(SKOS.broader):
        children[parent].append(child)

    lines = ["graph TD"]
    seen: set[URIRef] = set()
    edges: set[tuple[str, str]] = set()

    def emit_node(uri: URIRef) -> str:
        nid = _node_id(vocab, uri)
        if uri not in seen:
            seen.add(uri)
            lines.append(f'  {nid}["{vocab.label(uri)}"]')
        return nid

    def walk(uri: URIRef, level: int) -> None:
        parent_id = emit_node(uri)
        kids = sorted(children.get(uri, ()), key=vocab.label)
        if not kids:
            return
        if level >= depth:
            # Say what is not drawn rather than drawing it. A stub per parent,
            # so the id cannot collide with another parent's stub.
            stub = f"{parent_id}__more"
            total = len(kids)
            lines.append(f'  {stub}(["+{total} more"])')
            lines.append(f"  {parent_id} -.- {stub}")
            return
        shown, hidden = kids[:cap], kids[cap:]
        for kid in shown:
            kid_id = emit_node(kid)
            if (kid_id, parent_id) in edges:
                continue
            edges.add((kid_id, parent_id))
            word = qual.get((kid, uri))
            # Dotted means "no qualifier": the reader is looking at part of
            # Q1's undifferentiated third.
            if word:
                lines.append(f"  {parent_id} -->|{word}| {kid_id}")
            else:
                lines.append(f"  {parent_id} -.-> {kid_id}")
            walk(kid, level + 1)
        if hidden:
            stub = f"{parent_id}__rest"
            lines.append(f'  {stub}(["+{len(hidden)} more"])')
            lines.append(f"  {parent_id} -.- {stub}")

    walk(root, 0)
    return "\n".join(lines)


def render_map(vocab: Vocabulary, published: Graph, *,
               depth: int = DEPTH, cap: int = CAP) -> str:
    """A section per top concept, each holding one Mermaid chunk."""
    g = published
    tops = sorted(g.objects(vocab.scheme, SKOS.hasTopConcept), key=vocab.label)

    out: list[str] = [
        "Solid arrows are qualified by ISO 25964 and carry the word — "
        "`generic` for a kind-of, `partitive` for a part-of, `instantial` for a "
        "named individual. **A dotted arrow has no qualifier at all**, and a "
        "third of this hierarchy is in that state; see the roadmap for the "
        "count and which links they are.",
        "",
        f"Each chunk is drawn {depth} levels deep, at most {cap} children per "
        f"node. `+N more` marks what is not shown; the term's own page lists it "
        f"in full.",
        "",
    ]
    for top in tops:
        total = len(_descendants(g, top))
        noun = "descendant" if total == 1 else "descendants"
        out += [
            f"## {vocab.label(top)}",
            "",
            f"[{vocab.label(top)}](../../{vocab.local_name(top)}/) — "
            f"{total} {noun}.",
            "",
            "```mermaid",
            mermaid_subtree(vocab, published, top, depth=depth, cap=cap),
            "```",
            "",
        ]
    return "\n".join(out).rstrip("\n")


def _descendants(graph: Graph, root: URIRef) -> set[URIRef]:
    out: set[URIRef] = set()
    stack = [root]
    while stack:
        for kid in graph.subjects(SKOS.broader, stack.pop()):
            if kid not in out:
                out.add(kid)
                stack.append(kid)
    return out
