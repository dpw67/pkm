# Draft — GitHub Discussions announcement for v0.1.11

**Status:** NOT POSTED. Post by hand in Announcements, then record the
discussion number and date here. #7 is 0.1.10's, so this will be #8.

**Announcements are not cross-linked** — Discussions lists them in sequence,
which is how a reader moves between releases. Copy the status line above, not a
chain. The reasoning is in the 0.1.10 draft.

**The body below is deliberately unwrapped — do not re-wrap it.** Discussions
render a single newline as `<br>`, and because this is posted by hand there is
no `gh` step in which anything of mine would unwrap it. #7 was the first draft
handed over already unwrapped and posted byte-identical; this one is written the
same way so the unwrapping never falls on the poster.

**Prerequisites — both verified 2026-09-18, before this was handed over.**

1. `v0.1.11` is **published**, not a draft. ✅ `isDraft=false`, published
   2026-09-17T22:29:55Z, holding the **Latest** badge. Verified by content
   rather than status code, because a draft's tag URL also returns 200 with a
   bare page: the anonymous page contains "No triple moved", "Claude AI is
   entirely unqualified" and "3.3 MB", checked against the tag-stripped text
   since `<code>` and `<strong>` break strings that span them.
2. **w3id.org serves 0.1.11.** ✅ `owl:versionInfo "0.1.11"`,
   `owl:versionIRI https://w3id.org/pkm/0.1.11/vocab`, and
   `/vocab/browse/map/` and `/vocab/browse/hierarchy/` both 200.

**Every figure in the body was re-checked against the graph**: 236 broader
pairs with 77 bare, `instantial` asserted zero times, 132 concepts drawn,
largest chunk 57 nodes, Claude AI 3 of 3 amber, PKM Python 10 of 10 amber, Tool
12 grey and 0 amber.

**Title — pick one:**

- `PKM Vocabulary v0.1.11 — the hierarchy, drawn`
- `PKM Vocabulary v0.1.11 — a third of my arrows don't say what they mean`

---

## Body
For eleven releases this vocabulary had no picture. Not an SVG, not a PNG, not a line of Mermaid. Version 0.1.10 made it readable as text — a landing page, a collapsible tree, an A–Z index, a search box. None of that makes a hierarchy *visible*, and the difference turns out to matter.

There is now [a map](https://w3id.org/pkm/vocab/browse/map/): one diagram per top concept, generated from the published graph on every build.

One per top concept rather than one of everything, because 223 concepts in a single graph is a hairball, not an explanation. The useful unit is a chunk small enough to take in at once. I tuned the depth by measuring rather than by taste: two levels draws 100 concepts with the largest chunk at 35 nodes, three levels draws 132 with the largest at 57, four levels puts 96 nodes in one diagram and defeats the whole point. It draws three levels.

**Then the diagrams told me something I had been able to avoid noticing.**

Arrows in the map carry the kind of relationship they assert. A grey arrow is labelled `generic` (a kind of), `partitive` (a part of) or `instantial` (a named individual of). An amber arrow marked `?` asserts nothing at all — just `skos:broader`, one thing is narrower than another, with no statement about *how*.

**77 of my 236 hierarchy links are amber.** A third of this vocabulary's structure does not say what kind of relationship it is. Reading term pages one at a time, I had never seen that as a shape; in the diagrams it is the first thing you notice. `Claude AI` is entirely amber — all three of its arrows. `PKM Python` is 10 for 10. Meanwhile all twelve of `Tool`'s arrows are grey, which shows the difference is not inherent to the vocabulary, only unfinished in most of it. And no arrow anywhere reads `instantial`, because I have never once asserted it — even where it is plainly the right relation, like the thirteen named Obsidian plugins sitting under `Obsidian Plugin`. Dataview is not a *kind of* plugin. It *is* one.

So the amber arrows are not decoration. They are the work outstanding, and they are the single most useful thing a drawing of this particular graph could have done for me.

The diagrams are generated rather than drawn, which is deliberate. Every hand-maintained second copy of this graph has drifted from it: five of six collections that mirror a subtree had drifted from the subtree, the Obsidian mirror's hub carried a two-release-old version number and hand-copied counts until I generated it, and the review sheet is wrong the moment it is not re-run. A drawing of where you are *going* cannot drift, because it proposes a graph rather than describing one — so I still sketch the target by hand, in Excalidraw, and that work is what prompted this release. A published drawing of what *exists* is a different thing, and it has to be derived.

Mermaid rather than an image, because the same Markdown renders natively in the GitHub view and in Obsidian, so only the website needs a few lines of JavaScript. Three places, one source.

**Nothing a consumer queries changed.** No triple moved: the whole-vocabulary Turtle and all 241 per-term files came out byte-identical, and the only thing that changed at the end was the version number itself. Every URI, definition, relationship and collection membership means exactly what it meant in 0.1.10.

This is a presentation release and I will not pretend otherwise. But looking at my own hierarchy as a picture has already changed how I read it — the top concepts are mostly technology rather than concepts, and `Technology` is not one of them — and that is worth more than the page it took to find out.

- [Release notes](https://github.com/dpw67/pkm/releases/tag/v0.1.11)
- [The map](https://w3id.org/pkm/vocab/browse/map/)
- [Changelog](https://github.com/dpw67/pkm/blob/main/CHANGELOG.md)
- [The vocabulary](https://w3id.org/pkm/vocab)

If a definition looks wrong to you, that is still the most useful thing you can tell me. But this release adds a better target: **the amber arrows.** Each one is a relationship I have not yet said anything precise about, and if one of them looks obviously generic, or partitive, or an instance, you can see it in the picture faster than I can find it in the Turtle.
