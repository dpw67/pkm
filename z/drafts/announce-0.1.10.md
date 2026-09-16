# Draft — GitHub Discussions announcement for v0.1.10

**Status:** POSTED as
[Discussion #7](https://github.com/dpw67/pkm/discussions/7), 2026-09-16, in
Announcements, under the first of the two titles below.

**Announcements are not cross-linked, and this draft is the template, so that
decision lives here.** Discussions already lists them in sequence, which is how
a reader moves between releases, so a chain of "previous release" links would be
maintenance for no navigation benefit. The 0.1.9 draft asked for such a chain
and offered "#6 links #5" as the precedent; #6 links no discussion at all, so
the instruction had been written down twice and carried out never. Copy the
status line above, not a chain.

**The body below is deliberately unwrapped — do not re-wrap it.** Discussions
render a single newline as `<br>`, and because this one is posted by hand there
is no `gh` step in which anything of mine would unwrap it. A wrapped draft
hands the unwrapping to whoever pastes it, which is what was handed over for #2
and again for #6 — both were unwrapped while being pasted, so both read
correctly, but the work fell on the poster.

**This one needed none of that, which is the point.** #7's posted body is
byte-identical to the body below: 15 non-blank lines each, longest line 679
characters, no folds. That is the first time the draft arrived already
unwrapped, and it is the reason to keep writing them this way rather than
treating the unwrapping as a paste-time step.

**Prerequisites — both were satisfied before posting.**

1. The `v0.1.10` release is **published**, not a draft. ✅ Verified 2026-09-16:
   `isDraft: false`, published 20:03 UTC, and the tag URL returns 200 with the
   notes body present. It matters because a draft's tag URL is not a 404 — it
   returns 200 with a bare page — so the "Release notes" link below would land
   a reader on what looks like an *empty* release rather than a missing one.
2. `w3id.org/pkm` serves 0.1.10. ✅ Verified 2026-09-16: the namespace returns
   `owl:versionInfo "0.1.10"` and `owl:versionIRI .../0.1.10/vocab`, the Pages
   build completed on `19b8f43`, all three `browse/` pages return 200,
   `search.json` returns 241 entries, and content negotiation on
   `vocab/Recipe` still returns `text/html` to a browser and `text/turtle` to
   an RDF client.

**Title — the first was used:**

- `PKM Vocabulary v0.1.10 — the vocabulary you can actually read` ✅ posted
- `PKM Vocabulary v0.1.10 — same graph, a page you can find things on`

---

## Body
Every release so far has been about what the terms *say*. This one is about whether you can find them.

The vocabulary index had grown to 721 lines and 51 KB on a single page, and the order was as much the problem as the length. The collections sat 249 lines below the hierarchy. "All terms" — the section a first-time reader most likely wants — came last. The A–Z headings had existed since the first release and nothing linked to them, so a 400-line alphabetical list had no way to jump. Meanwhile the namespace front page does the opposite and does it well: it opens on a table of what exists, with a link per row.

So the vocabulary page is now shaped like its own parent. It is 39 lines with a row per view, and the three views are pages of their own: [the hierarchy](https://w3id.org/pkm/vocab/browse/hierarchy/), [the collections](https://w3id.org/pkm/vocab/browse/collections/), and [every term A–Z](https://w3id.org/pkm/vocab/browse/all/). The hierarchy collapses to its eight top concepts, so it opens as eight lines rather than 250. There is an A–Z index row that actually links to the anchors. And there is a search box, on those pages and on all 241 term pages.

**Nothing a consumer queries changed meaning.** No triple moved, and the build proves that rather than asserting it: the whole-vocabulary Turtle and all 241 per-term files came out byte-identical to 0.1.9. Every URI, definition, relationship and collection membership is exactly what it was. Only the version advanced.

A few decisions worth explaining, since they are visible in the URIs.

The new pages live under `/vocab/browse/` rather than at `/vocab/hierarchy/`. Term URIs in this namespace are `/vocab/{Term}`, so a flat sub-page would permanently reserve a plausible term name — and would sit in exactly the slot an RDF client expects a term in. Nesting them costs one reserved word instead of three, and reads as navigation rather than as a concept.

The collapsible hierarchy uses `<details>` rather than JavaScript. This Markdown renders in three places: the website, the GitHub view of the same file, and an Obsidian vault. `<details>` works in all three; a script works in one. Search is the opposite case and is layered on top accordingly — GitHub Pages runs Jekyll in safe mode against a fixed plugin allowlist, so a search *plugin* was never available, but a generated `search.json` plus a few dozen lines of vanilla JavaScript needs no plugin. The index is fetched on first use rather than on page load, and the box is revealed by the script, so a reader without JavaScript is never shown an input that cannot do anything.

One thing went wrong that is worth telling you about, because it is the kind of failure a version number is supposed to protect you from.

The version literal lives only in the SKOS Editor source, so even a release that moves no triple needs a round-trip through the editor. My editor had two projects open — one of them a leftover from an import-fidelity test months of work ago — and the first export came from the stale one. That export would have silently reverted the whole of 0.1.9: 33 pieces of prose, including the seven Cluster definitions and fifteen collection descriptions that release had just rewritten.

It passed everything. It parsed. The SKOS integrity checks reported no errors. All 247 Turtle files validated. The pages rendered correctly. It was caught only by a triple-level comparison against the previous commit that I happened to run by hand.

So that comparison now runs on every build and says out loud when prose has moved since the last commit — loudly when it has, and not at all when it has not. The defect was never that prose changes; that is what a prose release is. The defect was that it could change silently.

- [Release notes](https://github.com/dpw67/pkm/releases/tag/v0.1.10)
- [Changelog](https://github.com/dpw67/pkm/blob/main/CHANGELOG.md)
- [The vocabulary](https://w3id.org/pkm/vocab)

As always: if a definition looks wrong to you, that is the most useful thing you can tell me. This release did not change a single one — but it did make them a good deal easier to read next to each other, which is how the last three releases' worth of defects were found in the first place.
