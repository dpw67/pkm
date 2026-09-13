# Draft — GitHub Discussions announcement for v0.1.7 + v0.1.8

**Status:** draft. Post to
[Announcements](https://github.com/dpw67/pkm/discussions/categories/announcements)
by hand; Discussions has no draft state, so posting is immediately public.

**Prerequisites, both of which must be true before posting:**

1. The `v0.1.7` release is **published**, not a draft. Verified 2026-09-12:
   `releases/tag/v0.1.7` does not 404 for an anonymous visitor — it returns 200
   with a bare tag page, titled "Release v0.1.7" and carrying none of the
   release notes. So the "Release notes" link below currently lands a reader on
   a page that looks like an empty release rather than a missing one.
2. The `v0.1.8` release is published, and `main` carries the `Publish 0.1.8`
   merge. `releases/tag/v0.1.8` 404s until the tag exists.

**Title — pick one:**

- `PKM Vocabulary v0.1.7 and v0.1.8 — what a reader could not see`
- `PKM Vocabulary v0.1.7 and v0.1.8 — the questions reach the page, and the build learns to read`
- `PKM Vocabulary v0.1.7 and v0.1.8 — fixing what reading missed, twice`

**Lines below are deliberately unwrapped, one per paragraph.** GitHub renders a
single newline as `<br>` in Discussions, so paste the body exactly as it is
rather than reflowing it.

---------------------------------- paste below ---------------------------------

The PKM Vocabulary is a SKOS glossary of the terms I use to run my own personal knowledge management system — 223 concepts and 18 collections, each with a permanent `w3id.org/pkm/vocab/` URI that resolves to a page for a reader and to Turtle for a machine. [v0.1.6](https://github.com/dpw67/pkm/discussions/4) fixed what the descriptions said. These two releases are about something narrower and more irritating: things that were wrong in places nobody could see, including me.

**Browse it:** [w3id.org/pkm/vocab](https://w3id.org/pkm/vocab)

The 0.1.6 announcement ended by retracting a claim. I had written that an open question belongs on the concept itself, "where anyone dereferencing the term will see it" — true of the Turtle, and false of the page that nearly everyone actually opens, because the generator rendered neither `skos:editorialNote` nor `skos:changeNote`. v0.1.7 made it true. Then, having put three editorial notes in front of readers for the first time, I read them the way a stranger would and found that two of the three were addressed to me. That is v0.1.8, along with four checks that read the words rather than the graph — which promptly found eleven places where this vocabulary cites terms that do not exist, one of them in a note I had rewritten the day before without noticing the citation inside it.

## What v0.1.7 changed

**Three open questions and 968 change notes existed only in the RDF.** The open questions were written deliberately where a reader would find them — on [`pkmv:DayClusterCore`](https://w3id.org/pkm/vocab/DayClusterCore) (is Analysis a Core note?), [`pkmv:Map`](https://w3id.org/pkm/vocab/Map) (should a Home Note be its parent?) and [`pkmv:Month-Health`](https://w3id.org/pkm/vocab/Month-Health) (the local name is wrong) — and were invisible to everyone arriving with a browser. So were 968 change notes across 223 concepts: the entire record that the 0.1.5 and 0.1.6 audit convention exists to produce, readable nowhere but the Turtle. Editorial notes now render open, because a question nobody sees is a question nobody answers; change history renders collapsed, because the median term carries four notes and [`pkmv:Recipe`](https://w3id.org/pkm/vocab/Recipe) carries ten. Dated notes sort newest first — 735 of the 968 open with an ISO date and the rest were typed by hand without one, so an alphabetical sort read a history backwards.

**[`pkmv:Cluster`](https://w3id.org/pkm/vocab/Cluster) and [`pkmv:DayCluster`](https://w3id.org/pkm/vocab/DayCluster) described a bag, while the relations underneath them assert a whole of unlike parts.** `Cluster` read "A group of related notes" and `DayCluster` "The set of structured notes and artifacts generated for a single day…" — the second using *set*, the exact word the open naming question rejects for implying no structure. Underneath, 103 concepts assert `isothes:broaderPartitive`, so the whole/part reading is pervasive rather than incidental. They now read "Notes and artifacts assembled around a single subject, where each member is a part of the whole rather than one more instance of a kind" and "Everything the system produces about a single day, partitioned into four unlike parts: core, support, health, and visual". No URI, label, parent or membership changed.

Release notes: [v0.1.7](https://github.com/dpw67/pkm/releases/tag/v0.1.7)

## What v0.1.8 changed

**Two of the three editorial notes were addressed to the maintainer, on pages that promise a reader an open question.** [`pkmv:Month-Health`](https://w3id.org/pkm/vocab/Month-Health) read "Remove the hyphen from local name; it should be named MonthHealth. Deferred to 0.2.0 since it changes the URI." [`pkmv:Map`](https://w3id.org/pkm/vocab/Map) carried three imperative bullets beginning "Add a Home Note to the vocabulary…". Both sit under the heading the generator writes — *An open question about this term, not part of its definition* — which promises a question and delivered an assignment. Neither was a misuse of the property: the SKOS Primer's own words for `skos:editorialNote` are "reminders of editorial work still to be done". The mismatch was voice, and it is worth being precise about why, because I had half-assumed otherwise: *editorial* names the addressee, not the access. SKOS defines no audience, privacy or access control for the property anywhere, and these notes have been public for as long as they have existed — v0.1.7 changed only whether a browser could see them. `Month-Health`'s note now answers what a consumer actually needs, which is whether the URI is safe to cite today; `Map`'s opens with the question itself. [`pkmv:DayClusterCore`](https://w3id.org/pkm/vocab/DayClusterCore)'s is untouched — it already read outward, and is the model the other two now match. The convention is written down in [CONTRIBUTING.md](https://github.com/dpw67/pkm/blob/main/CONTRIBUTING.md) so the next note is written that way rather than corrected afterwards.

**Four new checks read the prose instead of the graph, and found thirteen defects; reading found the other four.** Every check until now read the structure, so a note could cite a concept that does not exist and nothing would notice. `phantom-citation` flags a CamelCase token in prose that is not a term in this scheme, and found eleven citations, of nine names that are not terms: [`pkmv:Cluster`](https://w3id.org/pkm/vocab/Cluster) and [`pkmv:TimeCluster`](https://w3id.org/pkm/vocab/TimeCluster) between them named `ConceptCluster` (reclassified to [`pkmv:ConceptCollection`](https://w3id.org/pkm/vocab/ConceptCollection) back in 0.1.2, with the scope note never following) and `OutputCluster` (which has never existed in any release); `TimeCluster` also listed `DecadeCluster` and `LifeCluster` as time clusters when both exist only as collections; [`pkmv:Action`](https://w3id.org/pkm/vocab/Action) cited `ActionGroups`; and [`pkmv:MonthPlan`](https://w3id.org/pkm/vocab/MonthPlan), [`pkmv:QuarterPlan`](https://w3id.org/pkm/vocab/QuarterPlan) and [`pkmv:YearPlan`](https://w3id.org/pkm/vocab/YearPlan) cited CamelCase plurals of their real children. The eleventh is in the [`pkmv:Month-Health`](https://w3id.org/pkm/vocab/Month-Health) editorial note I had rewritten the day before, which cites `MonthHealth` — not a term precisely because the note exists to propose it. `stale-duplicate-definition` reads the editor's own "Duplicated from X" note and flags a definition still byte-identical to its source's — 96 of the 223 concepts were authored by duplicating a sibling, so whether the definition ever changed is what separates a finished copy from an abandoned one; [`pkmv:ClaudeCowork`](https://w3id.org/pkm/vocab/ClaudeCowork) still read "Desktop app for Claude AI.", inherited and never rewritten. `scaffolding-local-name` flags a local name ending in `Copy`, `NewConcept` or `Untitled`. `misspelled-word` checks prose against the system dictionary behind a suffix-morphology helper and a committed word list, because `/usr/share/dict/web2` is a 1934 Webster's that knows "interoperability" but not "workflow"; it found exactly one, `mispelling`, in a note recording a spelling correction.

All four checks blank quoted spans before reading them, which is what makes an error-level severity safe here. The editor's change notes quote the string they record fixing — `Corrected typo from "definiton" to "definition"` — and seventeen of the twenty misspellings in this vocabulary are that pattern, spelled wrong on purpose and correctly so.

Release notes: [v0.1.8](https://github.com/dpw67/pkm/releases/tag/v0.1.8)

## The same mistake, four releases running

0.1.5 fixed the four misspellings I noticed while reading; a script run afterwards found 27 more. 0.1.6 fixed those, and a check written for that release found one more definition ending without punctuation. 0.1.7 rewrote `pkmv:Cluster`'s definition *and its scope note* to remove the bag language — and left the scope note citing `ConceptCluster` and `OutputCluster`, neither of which is a term in this vocabulary. 0.1.8's new check caught that, and also caught the editorial note I had rewritten the day before, in which the citation of `MonthHealth` survived the rewrite untouched — a term that does not exist, precisely because the note exists to say it should.

So the honest summary of four releases is that reading my own work does not reliably find the defects in it, and each time the fix that stuck was a machine check rather than more care.

But the split in this release is thirteen and four, and the four are the interesting ones. Thirteen of the seventeen defects came from the new checks. Four came from reading, and they fail a check for two different reasons. Two are change notes that mean `typo` and say `type`: [`pkmv:YearLog`](https://w3id.org/pkm/vocab/YearLog) read `Corrected type from "Yeary" to "Yearly"`, and [`pkmv:PKMNeo4jServiceProject`](https://w3id.org/pkm/vocab/PKMNeo4jServiceProject) read `Fixed type from "Grqph" to "Graph"` — the second getting the word wrong in a note that records fixing a misspelling. No check here can see those: every word is spelled correctly, `type` is a real word sitting in a plausible place, and nothing is cited that does not exist. The other two are worse, because no check I could write would ever see them. [`pkmv:ClaudeCowork`](https://w3id.org/pkm/vocab/ClaudeCowork)'s scope note read "Available for macOS with Apple Silicon." and [`pkmv:ClaudeDesktop`](https://w3id.org/pkm/vocab/ClaudeDesktop)'s read "Cowork requires Apple Silicon." Both described the January 2026 research preview; Cowork now runs on Claude Desktop for macOS and Windows, plus web and mobile, on paid plans, with no Apple Silicon requirement. That claim did not go stale on anything I did — it went stale on somebody else's release schedule, and nothing in this repository can detect that. So the conclusion is not that reading is useless. It is that reading and checking fail at different things, and I had been relying only on the one that fails at the common case.

Two are still open, both waiting for 0.2.0 because both move a live URI. The concept labelled *Template* is published at [`w3id.org/pkm/vocab/TemplateCopy`](https://w3id.org/pkm/vocab/TemplateCopy) — an unfinished duplicate whose original is no longer in the vocabulary. And [`pkmv:Month-Health`](https://w3id.org/pkm/vocab/Month-Health) is still the only hyphenated local name of 241. When either moves, the old URI stays resolvable, marked `owl:deprecated` and pointed at its replacement.

## The naming question is still open

The label "Cluster" drew fifty-three alternatives from four readers. What the thread produced that was more useful than a name was four tests a name has to pass: a plain English word a script author would guess, no collision with a term already inside the vocabulary, a whole of unlike parts rather than many of one kind, and about one subject. "Cluster" passed all four. Its own definition failed all four, which is why v0.1.7 changed the definitions and left the label alone.

Still taking alternatives, and still more interested in whether the four tests are the right tests.

Comments and corrections are most of what these two releases are made of. Reply here, or use the issue forms for [term proposals and term changes](https://github.com/dpw67/pkm/issues/new/choose).

**Full changelog:** [`CHANGELOG.md`](https://github.com/dpw67/pkm/blob/main/CHANGELOG.md)
