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
relation; a **dotted, amber, thicker, `?`-labelled** edge is a bare
`skos:broader` with no qualifier at all. A third of this hierarchy is
undifferentiated (ROADMAP Q1), and a reader can see which third at a glance
rather than by running a query.

Four cues for that one distinction, deliberately. The first cut used dotted
versus solid alone and was unreadable on a 13" laptop -- 1px of stroke style is
not a distinction. Colour carries it now, weight and a text label back it up so
it survives a colourblind reader or a greyscale print, and the dotted style is
kept because it reads as "weaker" and costs nothing.
"""

from __future__ import annotations

import re
from collections import defaultdict

from rdflib import Graph, URIRef
from rdflib.namespace import SKOS

from . import ISO_BROADER, ISO_QUALIFIER, Vocabulary

__all__ = ["legend", "mermaid_subtree", "render_map"]

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


#: Stroke for a qualified relation, and for one missing its qualifier. Both are
#: dark enough to read on white; the amber is not relied on alone -- see the
#: module docstring.
STROKE_QUALIFIED = "stroke:#57606a,stroke-width:1.5px"
STROKE_BARE = "stroke:#bf8700,stroke-width:3px"

#: Edge label for a link with no ISO 25964 qualifier. One character, because it
#: appears on a third of the arrows and a word would widen every diagram.
#: Quoted on emission: a parse error blanks the whole graph, and mermaid's own
#: parser needs a DOM, so this cannot be syntax-checked in the build.
BARE_LABEL = "?"


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

    # `linkStyle` numbers every link statement in declaration order, and an
    # out-of-range index fails the entire diagram rather than one arrow. So the
    # count is incremented on every link emitted -- including the `+N more`
    # connectors, which are links too -- and never inferred afterwards.
    links = 0
    bare: list[int] = []

    def emit_node(uri: URIRef) -> str:
        nid = _node_id(vocab, uri)
        if uri not in seen:
            seen.add(uri)
            lines.append(f'  {nid}["{vocab.label(uri)}"]')
        return nid

    def emit_link(line: str, *, unqualified: bool = False) -> None:
        nonlocal links
        if unqualified:
            bare.append(links)
        links += 1
        lines.append(line)

    def walk(uri: URIRef, level: int) -> None:
        parent_id = emit_node(uri)
        kids = sorted(children.get(uri, ()), key=vocab.label)
        if not kids:
            return
        if level >= depth:
            # Say what is not drawn rather than drawing it. A stub per parent,
            # so the id cannot collide with another parent's stub. Left at the
            # default style, so "not drawn" stays distinct from "unqualified".
            stub = f"{parent_id}__more"
            lines.append(f'  {stub}(["+{len(kids)} more"])')
            emit_link(f"  {parent_id} -.- {stub}")
            return
        shown, hidden = kids[:cap], kids[cap:]
        for kid in shown:
            kid_id = emit_node(kid)
            if (kid_id, parent_id) in edges:
                continue
            edges.add((kid_id, parent_id))
            word = qual.get((kid, uri))
            if word:
                emit_link(f"  {parent_id} -->|{word}| {kid_id}")
            else:
                emit_link(f'  {parent_id} -.->|"{BARE_LABEL}"| {kid_id}',
                          unqualified=True)
            walk(kid, level + 1)
        if hidden:
            stub = f"{parent_id}__rest"
            lines.append(f'  {stub}(["+{len(hidden)} more"])')
            emit_link(f"  {parent_id} -.- {stub}")

    walk(root, 0)
    if links:
        lines.append(f"  linkStyle default {STROKE_QUALIFIED}")
    # Only when there is something to index: an empty list is a syntax error.
    if bare:
        lines.append(f"  linkStyle {','.join(str(i) for i in bare)} {STROKE_BARE}")
    return "\n".join(lines)


def legend() -> str:
    """A four-edge key, so the arrow styles are shown rather than described.

    Generated with the same constants the diagrams use, so it cannot fall out
    of step with them -- which a hand-written key certainly would.
    """
    return "\n".join([
        "graph LR",
        '  A["a concept"] -->|generic| B["a kind of it"]',
        '  C["a concept"] -->|partitive| D["a part of it"]',
        '  E["a concept"] -->|instantial| F["a named example of it"]',
        f'  G["a concept"] -.->|"{BARE_LABEL}"| H["related how? not stated"]',
        f"  linkStyle default {STROKE_QUALIFIED}",
        f"  linkStyle 3 {STROKE_BARE}",
    ])


def render_map(vocab: Vocabulary, published: Graph, *,
               depth: int = DEPTH, cap: int = CAP) -> str:
    """A section per top concept, each holding one Mermaid chunk."""
    g = published
    tops = sorted(g.objects(vocab.scheme, SKOS.hasTopConcept), key=vocab.label)

    out: list[str] = [
        "```mermaid",
        legend(),
        "```",
        "",
        "A **grey labelled arrow** carries its ISO 25964 kind. An **amber "
        "arrow marked `?`** has no kind at all — the vocabulary asserts "
        "`skos:broader` and stops there. A third of this hierarchy is in that "
        "state, so the amber arrows are the work outstanding rather than "
        "decoration.",
        "",
        f"Each chunk is drawn {depth} levels deep, at most {cap} children per "
        f"node. A thin `+N more` connector marks what is not drawn — that is "
        f"about depth, not about a missing qualifier; the term's own page lists "
        f"the rest in full.",
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
