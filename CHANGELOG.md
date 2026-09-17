# Changelog

All notable changes to the PKM vocabulary and the resources published at
[w3id.org/pkm](https://w3id.org/pkm) are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version levels are explained under [Versioning](#versioning).

## [Unreleased]

Nothing yet. Work starts on a branch named for the version it targets.

## [0.1.10] — 2026-09-16

The vocabulary you can actually read. `vocab/index.md` was 721 lines and 51 KB
on one page, with the collections 249 lines down and "All terms" — the section
a first-time reader most likely wants — last. It is now a 39-line landing page
with a row per view, and the three views are pages of their own. Presentation
only: **no triple moved**, and the build proves it rather than asserting it —
`vocab/pkm-vocab.ttl` and all 241 per-term Turtle files are byte-identical
across this release. [Versioning](#versioning) makes that a patch.

### Added

- **Three browse pages** at `w3id.org/pkm/vocab/browse/hierarchy/`,
  `/browse/collections/` and `/browse/all/`. They nest under `browse/` rather
  than sitting flat at `/vocab/hierarchy/` because term URIs are
  `/vocab/{Term}`: a flat sub-page would permanently reserve a plausible term
  local name, and would occupy the slot an RDF client expects a term in. One
  reserved name instead of three, and it reads as navigation.
- **A collapsible hierarchy.** One `<details>` per top concept, closed, so the
  page opens as eight lines rather than 250. `<details>` and not JavaScript
  because this Markdown renders in three places — the Pages site, the GitHub
  repo view of the same file, and Obsidian — and it works in all three where a
  script works in one. Each summary carries its descendant count; the eight
  counts sum to 236, which is the `skos:broader` link count `make check`
  reports.
- **An A–Z index row** above All terms. The section anchors had existed since
  the first release with nothing linking to them, which left a 400-line
  alphabetical list with no way to jump. Only the initials that exist are
  emitted, so no link is a dead end.
- **Search**, on the vocabulary pages and on all 241 term pages.
  `vocab/search.json` — 241 entries, 38 KB — plus vanilla JavaScript in the
  layout. GitHub Pages runs Jekyll in safe mode against a fixed plugin
  allowlist, so a search plugin was never an option. The index is fetched on
  first use rather than on page load, because most visits to a term page never
  search, and the box is rendered hidden and unhidden by the script, so a
  reader without JavaScript is not shown an input that cannot do anything.
  Ranking is exact label, then label prefix, then label substring, then
  `skos:altLabel`, then definition.
- **`make hub`**, which fills the generated blocks in the Obsidian vocabulary
  hub. The hub was hand-written and stale in two places — frontmatter
  `version: 0.1.3` against a body reading "version 0.1.4", for a vocabulary at
  0.1.9. Counts, version, modified date, licence, top concepts and collection
  membership now come from the graph; the surrounding prose is left alone. The
  licence is read from `dcterms:license` rather than written in, so the hub
  cannot claim a licence the graph does not. The 18 hand-copied member counts
  turned out to be correct, so what this fixes is the version and what it
  prevents is the next membership edit.

### Changed

- **`splice()` takes a block name.** The hub needs two generated regions with
  hand-written prose between them, which one unnamed block per file cannot
  express. The unnamed form is unchanged, so `vocab/index.md`,
  `resources/index.md` and `agents/index.md` were untouched by the change.
- **`render_vocabulary()` became four renderers** — one per view plus the
  landing page — sharing the polyhierarchy walk that expands a shared subtree
  once and cross-references it thereafter.
- **Term pages carry `search: true`** and a search box. A reader arriving on a
  term page from a search engine had no way to reach a sibling term, which is
  the awkwardness this release is about.

### Fixed

- **`make site` was failing on a correct build.** It counts the directories
  under `_site/vocab/` and expects exactly one per term page, so the new
  `browse/` directory made that 242 against 241. Its grep now excludes
  `browse/` alongside `terms/`. Worth naming because that check is the only
  thing verifying the term permalinks still resolve, and a check that fails for
  the wrong reason is a check that gets switched off.

## [0.1.9] — 2026-09-14

The Cluster family now says what the graph says. Seven definitions that still
described a cluster as a bag, nine scope notes in the same family, two
elsewhere whose prose the hierarchy contradicted, and fifteen collection
descriptions that were the same bag language one layer over. Prose only — no
URI, label, membership or relationship moved — so [Versioning](#versioning)
makes this a patch.

### Changed

- **Seven concepts under `pkmv:Cluster` still defined a cluster as a bag, and
  all three of its direct children were among them.** 0.1.7 rewrote
  `pkmv:Cluster` and `pkmv:DayCluster` to say that a cluster is a whole of
  unlike parts about one subject, and left the rest of the family reading "A
  group of related notes about a …" — so following the hierarchy down one level
  met the phrasing the parent had just abandoned. `pkmv:MonthCluster`,
  `pkmv:QuarterCluster` and `pkmv:YearCluster` carry **exactly the same five
  partitive children** — plan, log, review, journal and health — so they take
  one parallel sentence naming those parts, which is what `make review` reads as
  a family rather than as drift. `pkmv:WeekCluster` was the sharpest of the
  seven: it held the sentence `pkmv:DayCluster` carried until 0.1.7, word *set*
  included, on `DayCluster`'s own sibling. Its old definition also ended
  "aggregating and analyzing its constituent Day Clusters", which the graph does
  not assert — `pkmv:DayCluster` is its sibling under `pkmv:TimeCluster`, not
  its child — so that clause went with the rest. **`pkmv:TimeCluster` is a
  generic parent, not a whole:** it is `narrowerGeneric` to all five period
  clusters where they are `narrowerPartitive` to their own notes, so it gets a
  kind-of sentence instead. **`pkmv:EffortCluster` and `pkmv:TopicCluster` carry
  no ISO 25964 relations at all** — plain `skos:broader` and `skos:narrower`,
  unlike every other cluster — so writing "unlike parts" into their definitions
  would assert in prose what the graph does not. They keep the subject-focused
  clause without the partition claim, and their scope notes say so outright. The
  missing relations are recorded in ROADMAP as minor work; the word *record* is
  avoided throughout, because it is already this vocabulary's word for a `Log`.

- **Nine scope notes in the Cluster family, five of them saying nothing the
  definition did not.** `pkmv:MonthCluster`, `pkmv:QuarterCluster`,
  `pkmv:YearCluster`, `pkmv:EffortCluster` and `pkmv:TopicCluster` all read
  "Parent context for all notes associated with a ‹X›." Three more were
  contradicted by the graph they describe. `pkmv:DayCluster` claimed to mirror
  "the Week/Month clusters at other granularities" when it is the only cluster
  partitioned in two levels — its four parts each hold notes of their own, where
  the week, month, quarter and year clusters hold theirs directly.
  `pkmv:WeekCluster` said it "Sits above DayCluster and below Month in the
  Calendar hierarchy", which is wrong in both directions: its parents are
  `pkmv:TimeCluster` and `pkmv:CalendarFolder`, and `pkmv:DayCluster` and
  `pkmv:MonthCluster` are siblings. `pkmv:TimeCluster` still opened "Parent
  context for a group of related notes" — the exact phrasing 0.1.7 rejected on
  the parent — and carried a trailing space, one of the literals `transform.py`
  repairs silently on every build, now fixed at the source instead.
  `pkmv:Cluster`'s omission is the other half of a fix 0.1.8 started: that
  release removed the two phantom citations from its scope note and left it
  still failing to name `pkmv:TimeCluster`, its only unnamed direct child, along
  with two of the five period clusters.

- **Two scope notes outside the Cluster family that name the wrong concepts.**
  `pkmv:Meal`'s read "Parent concept for the meal-planning domain (Breakfast,
  Lunch, Dinner, Snack, Recipe, DayMeal, etc.)" and parents none of the six: its
  children are `pkmv:Food`, `pkmv:MealPlan` and `pkmv:Restaurant`, the four meal
  kinds sit under `pkmv:DayMeal`, and `pkmv:Recipe` is `Meal`'s sibling under
  `pkmv:PKMMeals`. `phantom-citation` cannot see this, because all six names
  exist and that rule fires on names that do not. `pkmv:Knowledge` was the same
  defect found by looking for a second example: it called `pkmv:Metadata`,
  `pkmv:Ontology`, `pkmv:Taxonomy`, `pkmv:KnowledgeGraph` and `pkmv:Term` "more
  specific forms" of itself when all five are children of
  `pkmv:KnowledgeSystem`, which is `Knowledge`'s own parent — so they are its
  siblings — and it named none of its four actual children. It also called
  itself "the broadest top concept" while having a parent and not being one of
  the eight. Both now name what they hold and place what they mention.

- **Eight change notes recorded a name without quoting it, and
  `phantom-citation` was right to flag all eight.** 0.1.8 established the
  convention — a name you are recording rather than citing goes in quotes — and
  left the notes themselves for the next time the file was open. `Removed
  redundant AppIntent2 generated by Proposals when already exists` and seven
  like it across `pkmv:Action`, `pkmv:AppIntent`, `pkmv:DayJournal`,
  `pkmv:DayLog`, `pkmv:DayReview`, `pkmv:MealPlan`, `pkmv:Month-Health` and
  `pkmv:MonthCluster` now quote the name they record. This takes
  `phantom-citation` from eight findings to none, and the warnings surviving
  `make build` from nine to one — the one being `scaffolding-local-name` on
  `pkmv:TemplateCopy`, which is expected until the 0.2.0 rename and must not be
  silenced. 18 term pages changed.

- **Fifteen collection descriptions said "All notes related to ‹X›", which is
  what made the collections read as unfocused.** Fourteen of the eighteen
  opened that way, and the four that did not — `NoteTypes`, `TechStack`,
  `SemanticWebStandards` and `IdeaverseCollection` — are exactly the ones not
  named `*Collection`. "All notes related to X" is not a membership rule, so
  nothing in the description let a reader decide whether a given term belonged;
  each now states the rule instead. **No member was added or removed**, because
  that is not available at this level: the versioning table makes Major "an
  existing query can return different results", and dropping a member is
  precisely that. So where a collection is a hand copy of a subtree, the
  description now says so **and says which side wins** — `pkmv:DayCollection`
  records that it holds 26 members against the 25 concepts under
  `pkmv:DayCluster`, that `pkmv:DayMeeting` is in the tree and not in the
  collection, and that the hierarchy is authoritative where they disagree. That
  is the honest patch: it cannot fix the drift, so it tells a consumer which
  source to trust and leaves the membership to 0.2.0. Two descriptions were not
  vague but wrong. `pkmv:EffortCollection` read "All the related notes for a
  single Effort" while holding `pkmv:Area`, `pkmv:EffortCluster`,
  `pkmv:EffortsFolder`, `pkmv:Interest` and `pkmv:Project` — **zero overlap**
  with `pkmv:EffortCluster`'s own subtree, because it is the effort vocabulary
  and not one effort's notes. `pkmv:QuarterCollection` claimed a quarter's
  notes while holding `pkmv:MonthJournal` and omitting `pkmv:QuarterHealth` and
  `pkmv:QuarterJournal`, which is the copy it was made from showing through —
  `pkmv:QuarterCluster`'s own change note records it as "Duplicated from
  MonthCluster". Two spelling errors went with them, in
  `pkmv:QuarterCollection` ("uses for medium-term planning") and
  `pkmv:YearCollection` ("a calendar Year groups Quarters and Months").
  **None of the fifteen carries a change note recording the rewrite**, because
  the SKOS Editor writes them for concepts and not for collections — all
  eleven edited concepts were logged and none of the fifteen collections was.
  So the collections' audit trail is still empty at 0 of 18, and this entry is
  the only record that their descriptions changed. 15 more term pages
  changed.

- **Seventy-four change notes repaired upstream, arriving here for free.** The
  SKOS Editor fixed the two artifact classes this vocabulary has worked around
  since 0.1.6: a language tag written inside a quoted label
  (`Preferred label changed from “AppIntent@en”`, 35 of them) and a proposer
  named twice when they approved their own proposal
  (`Created from approved proposal (proposed by Doug Warren) (by Doug Warren)`,
  39). They are upstream
  [#77](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/77)
  and [#78](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/78),
  with
  [#81](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/81)
  explaining why the fix had appeared not to reach this vocabulary — the
  earlier migration walked only stored edit history and not notes that arrived
  by import, and every note here arrived by import. The repair now runs
  whenever a project is opened, so it landed without anything being asked of
  it. **This is upstream's work, not this project's**, and it is recorded here
  only because the published prose changes: 74 literals across 57 concepts,
  measured rather than counted from the diff. Two consequences worth stating.
  `make check` drops from three warnings to one — the survivor being
  `scaffolding-local-name` on `pkmv:TemplateCopy`, which waits for the 0.2.0
  rename. And `transform.py`'s matching repair becomes a no-op: it is kept as a
  defence against an export from an older editor, but the count of literals it
  rewrites on every build falls from 95 to 21, all of them now the invisible
  whitespace kind that no reader could ever perceive.
## [0.1.8] — 2026-09-13

Two editorial notes rewritten for the audience that can now read them, the
convention behind that written down, and four new checker rules that catch
editor mistakes the graph checks cannot see. Prose and tooling only — no URI,
label, membership or relationship moved — so [Versioning](#versioning) makes
this a patch.

### Changed

- **Two of the three editorial notes were addressed to the maintainer, on pages
  that tell a reader they are looking at an open question.** 0.1.7 made
  `skos:editorialNote` render, and what it put in front of readers was a to-do
  list: `pkmv:Map` carried three imperative bullets ("Add a Home Note to the
  vocabulary as a broader (parent) concept for a Map", "Maps should have an
  upward path toward the Home Note") and `pkmv:Month-Health` read "Remove the
  hyphen from local name; it should be named MonthHealth. Deferred to 0.2.0
  since it changes the URI." Both sit under the heading the generator writes —
  *An open question about this term, not part of its definition* — which
  promises a question and delivered an assignment. Neither was mistyped: the
  SKOS Primer's own words for `skos:editorialNote` are "reminders of editorial
  work still to be done" and warnings about "future editorial changes", so
  these were exactly what the property is for. The mismatch was voice. SKOS
  frames the property as one "useful for KOS managers or editors", but defines
  no audience, privacy or access control anywhere — the Reference says only
  "there is no restriction on the nature of this information", and the one
  visibility mechanism in SKOS, `skos:hiddenLabel`, governs labels rather than
  notes. So *editorial* names the addressee, not the access, and these notes
  were public for as long as they have existed: the documentation guide
  advertises `pkm-vocab.ttl` as carrying "every concept, collection, and
  editorial note", and 0.1.7 changed only whether a browser could see them.
  `pkmv:Map`'s note now opens with the question itself — should a Home Note be
  its parent? — and keeps every fact from the bullets in one paragraph;
  `pkmv:Month-Health`'s now answers what a consumer actually needs, which is
  whether the URI is safe to cite today, and restates the guarantee that the
  old URI stays resolvable when the rename lands. `pkmv:DayClusterCore`'s note
  is untouched: it already reads outward ("It seems that... It could be argued
  that...") and is the model the other two now match. `CONTRIBUTING.md` records
  the convention under [What a term needs](CONTRIBUTING.md#what-a-term-needs),
  so the next note is written this way rather than corrected afterwards. 2 term
  pages changed; the note count is unchanged at three.

- **Four checker rules for the mistakes that survive a graph check, and the
  thirteen defects they found.** Every check in `checks.py` until now read the
  graph; none read the words, so a note could cite a concept that does not exist
  and nothing would notice. `phantom-citation` flags a CamelCase token in prose
  that is not a term in this scheme — ERROR where a reader sees it, WARN in the
  audit trail, where a name that has since gone is a record rather than a
  mistake. It found eleven reader-facing citations, of nine names that are not
  terms, across seven concepts: `pkmv:Cluster` and `pkmv:TimeCluster` between
  them named `ConceptCluster` and `OutputCluster` (the first was reclassified to
  `pkmv:ConceptCollection` back in 0.1.2 and the scope note never followed; the
  second has never existed in any release), `pkmv:TimeCluster` also listed
  `DecadeCluster` and `LifeCluster` as time clusters when both exist only as
  collections, `pkmv:Action` cited `ActionGroups`, and `pkmv:MonthPlan`,
  `pkmv:QuarterPlan` and `pkmv:YearPlan` cited CamelCase plurals of their real
  children. The eleventh was already in the `pkmv:Month-Health` editorial note
  rewritten above, and survived that rewrite unnoticed: it cites `MonthHealth` —
  not a term precisely because the note exists to propose it, and now quoted so
  the rule reads it as a string rather than a citation.
  `stale-duplicate-definition` reads the editor's own `Duplicated from "X"` note
  and flags a definition still byte-identical to its source's: 96 of the 223
  concepts were authored by duplicating a sibling, so what separates a finished
  copy from an abandoned one is whether the definition ever changed.
  `pkmv:ClaudeCowork` still read "Desktop app for Claude AI.", inherited from
  `pkmv:ClaudeDesktop` and never rewritten after the rename landed. Fixing it
  surfaced a second defect in the same concept that no rule here can see: the
  scope note still read "Available for macOS with Apple Silicon.", which
  described the January 2026 research preview. Cowork now runs on Claude Desktop
  for macOS and Windows, plus web and mobile, on paid plans, with no Apple
  Silicon requirement — and the same stale claim sat in `pkmv:ClaudeDesktop`'s
  scope note, which is where the duplicate inherited it. Both are corrected. A
  wrong fact about someone else's product is a different defect from prose
  hygiene: it goes stale on their release schedule, not on any edit made here,
  so no check in this repository can detect it and only rereading the source
  can. `scaffolding-local-name` flags a local name ending in `Copy`,
  `NewConcept` or `Untitled`, which caught the one that is already published:
  the concept labelled *Template* resolves at `w3id.org/pkm/vocab/TemplateCopy`,
  an unfinished duplicate whose original is gone from the vocabulary. It is a
  WARN rather than an ERROR, beside `numeric-suffix` for the same reason —
  renaming moves a live URI, so it waits for 0.2.0, and a gate that is
  permanently red teaches you to ignore red. `misspelled-word` checks prose
  against the system dictionary behind a suffix morphology helper and a
  committed `wordlist.txt`, because `/usr/share/dict/web2` is a 1934 Webster's
  that knows "interoperability" but not "workflow". It found exactly one:
  `mispelling`, in a note recording a spelling correction. The two prose rules
  blank quoted spans before reading them, which is what makes an ERROR severity
  safe here — the editor's change notes quote the string they record fixing
  (`Corrected typo from "definiton" to "definition"`), and fourteen of the
  fifteen misspellings in this vocabulary are that pattern, correctly spelled
  wrong on purpose. Where no system dictionary exists, `misspelled-word` reports
  no words at all and adds a single `no-dictionary` INFO saying why — with
  nothing to compare against every word is unrecognised, and unchecked is not
  the same as suspect. `/usr/share/dict` is macOS-only and
  [CONTRIBUTING.md](CONTRIBUTING.md) invites contributors; the other three rules
  need no dictionary. Two defects fixed in this release sit outside all four
  rules:
  `pkmv:YearLog` carries a change note reading `Corrected type from "Yeary" to
  "Yearly"` and `pkmv:PKMNeo4jServiceProject` one reading `Fixed type from
  "Grqph" to "Graph"`, where both mean `typo`. No check here can see them,
  because every word is spelled correctly and none is a citation. Those two were
  found by reading. 11 term pages changed.

## [0.1.7] — 2026-09-12

One rendering fix and two prose corrections. The rendering fix moved nothing in
the graph — the export, `pkm-vocab.ttl` and all 241 per-term Turtle files were
byte-identical across it — and the two definitions are rewordings, so
[Versioning](#versioning) makes this a patch.

### Fixed

- **Editorial notes and change history never reached a term page.** 0.1.6 said of
  `pkmv:Month-Health`'s editorial note that the defect was "recorded on the
  concept, where anyone dereferencing the term will see it". That was true of the
  RDF and false of the page: the generator rendered neither
  `skos:editorialNote` nor `skos:changeNote`, so three open questions written
  deliberately where a reader would find them — on `pkmv:DayClusterCore` (is
  Analysis a Core note?), `pkmv:Map` (should a Home Note be its parent?), and
  `pkmv:Month-Health` (the local name is wrong; see 0.1.6) — were invisible to
  everyone who arrived with a browser, which is nearly all of them. So were 968
  change notes across 223 concepts: the whole record the 0.1.5 and 0.1.6 audit
  convention exists to produce, readable nowhere but the RDF. Editorial notes
  now render open, because a question nobody sees is a question nobody answers;
  change history renders collapsed, because the median term carries four notes
  and `pkmv:Recipe` carries ten. Dated notes sort newest first — 735 of the 968
  open with an ISO date and the other 233 were typed by hand without one, so an
  alphabetical sort read backwards for a history. 223 term pages changed; the 18
  collections carry no notes and are untouched.

### Changed

- **`pkmv:Cluster` and `pkmv:DayCluster` described a bag, while the relations
  underneath them assert a whole of unlike parts about one subject.** `Cluster`
  read "A group of related notes" and `DayCluster` "The set of structured notes
  and artifacts generated for a single day within the PKM system, organized into
  core, support, health, and visual groupings" — the second using *set*, the
  exact word the open naming question rejects for implying no structure.
  Underneath, `pkmv:DayCluster` carries `isothes:narrowerPartitive` to four
  unlike parts (`pkmv:DayClusterCore`, `pkmv:DayClusterHealth`,
  `pkmv:DayClusterSupport`, `pkmv:DayClusterVisual`) and is itself both
  `isothes:broaderGeneric` of `pkmv:TimeCluster` and `isothes:broaderPartitive`
  of `pkmv:CalendarFolder`. 103 concepts assert `broaderPartitive`, so the
  whole/part reading is pervasive rather than incidental. The two now read
  "Notes and artifacts assembled around a single subject, where each member is a
  part of the whole rather than one more instance of a kind" and "Everything the
  system produces about a single day, partitioned into four unlike parts: core,
  support, health, and visual". `pkmv:Cluster`'s scope note carried the same
  phrasing one line below its definition, and now reads "Parent context for all
  notes associated with a single subject, like DayCluster, WeekCluster,
  MonthCluster, EffortCluster, TopicCluster, ConceptCluster, OutputCluster,
  etc." — which also matches the wording `pkmv:MonthCluster`,
  `pkmv:YearCluster`, `pkmv:QuarterCluster`, `pkmv:EffortCluster` and
  `pkmv:TopicCluster` already use. No URI, label, parent or membership changed.

  Prompted by the naming question, which drew fifty-three alternatives to the
  label "Cluster" from four readers and, more usefully, produced four tests a
  name has to pass: a plain English word a script author would guess, no
  collision with a term already inside the vocabulary, a whole of unlike parts
  rather than many of one kind, and about one subject. The label passed all
  four. The definitions did not, which is why this release changes them and not
  the label.

## [0.1.6] — 2026-09-11

A prose patch. 0.1.5 fixed the four misspellings I happened to see; a systematic
sweep afterwards found 29 more defective literals, and this fixes those. No URI,
label, membership or relationship changed, so [Versioning](#versioning) makes it
a patch.

### Fixed

- **`pkmv:QuarterLog`'s scope note claimed it aggregates `QuarterLog`.** The
  roll-up chain is Day → Week → Month → Quarter → Year and every other rung
  names the rung below it, so a reader following the chain upward hit a loop at
  the fourth step. It now names `MonthLog`. This is a false statement rather
  than a typo, which is why it is first.
- **`pkmv:DayClusterCore`'s definition was still one note short.** 0.1.5
  corrected it to name Analysis and left Index out, so it named five of the six
  concepts that are actually narrower than it. All six are named now: Index,
  Plan, Log, Journal, Review, Analysis. Nothing was reparented, then or now.
- **`pkmv:WeekReview` was the only definition of 223 with no terminal
  punctuation.** Found by a check written for this release rather than by
  reading, which is the argument for writing it.
- Misspellings in six definitions and eight scope notes: `compled`,
  `retrospectivee` (on both `pkmv:MonthReview` and `pkmv:QuarterReview`),
  `thatcreates`, `Kanboard`, `workspacces` and `headlngs` (both on
  `pkmv:AdvancedURI`), `crtieria`, `financies`, `Yeary`, `Grqph`, and
  `Wordpress` for WordPress Recipe Maker.
- Misspellings in 15 change notes: `definiton` nine times, `definintion` twice,
  `deinition` twice, plus `Pujblish` and `changiing`. `pkmv:TopicReview`'s note
  also named a Topic *Index* — a copy-paste from the line above it — and now
  names a Topic Review.

Each correction above leaves a companion change note recording what was fixed, so
the record survives the fix. Twenty-one quote the old spelling — the convention
0.1.5 started on `pkmv:Map` and `pkmv:Idea` — and six describe the edit instead,
as `pkmv:AdvancedURI`'s `Removed duplicated "c" from "workspaces"` and
`pkmv:Bases`'s `Insert missing space between "that" and "creates"` do. Either way
a raw count of `definiton` in the export is still nine while all nine are now
correct, because they are quotations.

### Changed

- `pkmv:View`'s scope note says a "group" of notes where it said a "collection".
  The informal word already collides with `skos:Collection`, which this
  vocabulary uses formally for its 18 collections, and it would collide harder
  the moment a `Collection` concept exists.

### Added

- A `skos:editorialNote` on `pkmv:Month-Health` recording that its local name is
  wrong. It is the only hyphenated local name of 241 — its siblings are
  `pkmv:DayHealth`, `pkmv:WeekHealth`, `pkmv:QuarterHealth` and
  `pkmv:YearHealth` — and it should be `pkmv:MonthHealth`. **The rename is
  deferred to 0.2.0 because it moves a URI**, and a query for
  `pkmv:Month-Health` would stop returning what it returns today. The defect is
  recorded on the concept, where anyone dereferencing the term will see it,
  rather than only in a tracker. `pkmv:Month-Health` is unchanged in this
  release, which is what keeps 0.1.6 a patch. The term also carries two change
  notes dated 2026-09-11 recording a rename to `pkmv:MonthHealth` and back: the
  rename was made while preparing this release and reverted once it was clear it
  belonged in 0.2.0. They are the evidence for the deferral, not a URI change.

## [0.1.5] — 2026-09-11

### Added

- A description for the last three collections that had none. `NoteTypes`,
  `SemanticWebStandards` and `TechStack` were the only 3 of 18 collections
  carrying no `skos:note`, so their pages opened straight onto a member list
  and their link cards fell back to the site description. They are also the
  only three that list *types* rather than everything about one subject, which
  is why the phrasing the other collections use — "All the related notes for a
  single calendar Day." — does not fit them, and why they stayed undescribed
  this long. Each now says plainly what its list holds. Membership is
  unchanged.
- Two `skos:editorialNote`s recording open questions where they belong, on the
  concept rather than in a tracker. `pkmv:DayClusterCore` carries the argument
  for and against Analysis being a Core note rather than a Support one, and
  `pkmv:Map` carries the case for adding a Home Note as its parent — a map of
  the maps — in place of the current `pkmv:ObsidianNotes`.

### Changed

- Eighteen preferred labels gained the space they were missing: `AppEvent` now
  reads "App Event", and likewise for Activity, Agent, Alert, Device,
  Diabetes, Glucose, Health, Insulin, Meal, Meditation, Note, Script, Service,
  Sleep, Tool, User and Weight. "EKG Event" and "Blood Pressure Event" were
  already spaced, which is what made the rest look inconsistent. A preferred
  label does not need to match the technology artifact it names — the URI
  already does that, and the URI is what the Swift app and the Python services
  key on. `pkmv:AppEvent` and every other URI are unchanged, so this is a
  patch: [Versioning](#versioning) counts a corrected preferred label as
  editorial. `FastAPI` and `QuickAdd` keep their spelling; those are product
  names, not CamelCased phrases.
- Three definitions reworded for precision. A `Map` is now "A note used to
  think, plan, organize, and/or navigate a group of related notes" —
  navigation was the use it was actually put to and the word was missing. A
  `Day Meeting` is "An event with attendees, agenda, topics, decisions, and
  actions", where it read "with other people with agenda". An `Idea` is a
  distillation from "a Spark, Concept, or Interest" rather than from all three
  at once.

### Fixed

- `pkmv:DayClusterCore`'s definition disagreed with the hierarchy. It named
  "Plan, Log, Journal, and Review" as the core set while `pkmv:DayAnalysis` has
  been one of its six narrower concepts all along. The definition now names
  Analysis too, so a reader and a query agree about what the core set contains.
  Nothing was reparented.
- Four spelling errors in published prose: "opporuntities" and "explicityl" on
  `pkmv:Idea`, "collectio" on `pkmv:Map`, and "Web Clipped" for the Obsidian
  Web Clipper on `pkmv:Clipping`.
- Four definitions ended in a doubled period — `pkmv:Base`,
  `pkmv:EffortCluster`, `pkmv:TopicCluster` and `pkmv:ClaudeDesktop`.
- The 11 invisible double spaces are now fixed in the export itself, not only
  on the way out. The build has collapsed them since they were found (below),
  but the export is the citable artifact, so the RDF said `with  JavaScript`
  while every page read correctly. `pkmv:TimeCluster` had two problems in one
  scope note — a double space, and a missing one after the comma in
  `DecadeCluster,LifeCluster`; both are gone.
- A duplicate change note on `pkmv:DayMealPlan`, hand-typed to describe a label
  change the editor had already recorded on the same date. Seven change notes,
  six distinct changes.
- Canonical URLs on every published page. `url` carried the `/pkm` path and
  GitHub Pages adds `baseurl: /pkm` on top of it, so each page advertised
  itself as `w3id.org/pkm/pkm/...` — a 404 — in its `canonical` tag, its
  `og:url`, and the "PKM" link in the site header. Term-to-term navigation was
  never affected; those links are relative. Predates 0.1.4.
- Change notes no longer carry the editor's internals into their prose. Some
  quoted a label with its language tag still attached — `“Day Meal Plan@en”` —
  and some named the same person twice, as `(proposed by X) (by X)`. Both are
  artifacts of the SKOS Editor's generated notes. It has since fixed the
  generator and repaired most of the stored history, and the build normalises
  whatever is left, so the published graph is clean either way.
- `owl:versionIRI` moved out of the term namespace. It was minted under
  `https://w3id.org/pkm/vocab/`, the namespace `vann:preferredNamespaceUri`
  declares to hold terms, so it serialised as `pkmv:0.1.4` and read like a
  concept that does not exist. It now sits beside the scheme, at
  `https://w3id.org/pkm/{version}/vocab`.
- Every term page described itself with the same sentence. None carried its own
  `description`, so jekyll-seo-tag fell back to the site's, and a link card for
  any of the 241 terms read "Persistent URI namespace at ..." rather than what
  the term means. Each page now takes its `og:description` from the term's own
  `skos:definition`. The three collections that had no definition fell back
  too, which is the gap the notes above close.
- The page footer no longer invites a web edit. The Primer theme offers
  "Improve this page", but term pages are rewritten in place on every build and
  are maintained in the SKOS Editor export, so the change would have been
  discarded — and the link pointed at a `gh-pages` branch the site does not
  build from. The footer now points at Issues and Discussions.
- Invisible whitespace no longer reaches the published graph. 31 definitions,
  scope notes and change notes carried whitespace no reader could see: 11 held
  a run of two or more spaces mid-sentence, the rest only padding at the end of
  a line or at the edges of the literal. HTML collapses all of it, so every
  page read correctly while the RDF underneath said `with  JavaScript`. The
  build now collapses horizontal whitespace in prose and trims the edges,
  leaving newlines alone so a bulleted scope note stays a list.

## [0.1.4] — 2026-09-09

### Fixed

- `pkmv:DayMealPlan` — preferred label corrected from `Day.Meal Plan` to
  `Day Meal Plan`. The period was a typo, not a namespacing convention. The URI
  is unchanged.

### Added

- An HTML page for every term, at the term's own URI. Until now a browser opening
  `https://w3id.org/pkm/vocab/{Term}` got a 404, because every rewrite rule was
  gated on an RDF `Accept` header and nothing served HTML. The same URI now
  returns a readable page to a browser and Turtle to an RDF client. The
  vocabulary index links to those pages rather than straight into Turtle.
- Community health files: `CODE_OF_CONDUCT.md`, `SECURITY.md`, a pull request
  template, and issue forms for bug reports, feature requests, term proposals,
  and term changes.
- `docs/` — a guide to accessing and using the vocabulary, pointing at the
  companion Obsidian notes and Ghost blog for the longer-form material.
- This changelog.

## [0.1.3] — 2026-08-31

### Added

- `rdfs:label` on every concept and collection, mirroring `skos:prefLabel`, so
  tools that read RDFS but not SKOS have a label to display. Touched all 241
  per-term files.

### Changed

- Rendered vocabulary pages moved classification and dates into a footer.

## [0.1.2] — 2026-08-31

### Added

- Obsidian term stubs, generated by `make notes` from the published vocabulary.

### Changed

- Republished from SKOS Editor v0.17.0.
- Collection descriptions now appear in the rendered vocabulary.

## [0.1.1] — 2026-08-30

First published release of the PKM vocabulary, retiring the placeholder
Note/Tag/Source model that preceded it.

### Added

- 241 URIs in the `https://w3id.org/pkm/vocab/` namespace — 223 concepts and 18
  collections — each dereferencing to its own Turtle document.
- Linked Data structure for the namespace: the bulk dump, the per-term files,
  and the `agents` and `resources` hash namespaces.
- Tolerance for the SKOS Editor 0.16.7 annex namespace on import.

## URI stability

**No concept or collection URI has been removed, renamed, or reused since
0.1.1.** All 241 URIs published in that release still identify the same thing.

They dereference through content negotiation at w3id.org: a request carrying an
RDF `Accept` header (`text/turtle`, `application/rdf+xml`, `application/n-triples`,
`text/n3`) is redirected to the term's Turtle document. Everything else — a
browser, or any client sending the default `*/*` — gets the term's HTML page. So
a term URI is a link you can hand someone as well as an identifier and an RDF
lookup.

A URI is minted once, when the term is created, and does not follow later label
changes — correcting `Day.Meal Plan` to `Day Meal Plan` in 0.1.4 left
`pkmv:DayMealPlan` untouched.

When a term is eventually retired it will be marked `owl:deprecated true` and,
where a successor exists, linked with `dcterms:isReplacedBy`. It will not be
deleted. `make build` reports per-term files whose URIs the vocabulary no longer
defines rather than removing them, so this is enforced by the build rather than
by memory.

## Versioning

Version levels describe impact on consumers, not volume of work.

| Level | Means | Examples |
|---|---|---|
| **Patch** | Editorial only; nothing a consumer queries changes meaning | Typo fix, added or reworded scope note, change note, corrected preferred label |
| **Minor** | Additive; every existing URI keeps its meaning | New concepts or collections, new relations, an ISO 25964 qualifier added to a link that had only `skos:broader`, a new top concept, new cross-vocabulary mappings |
| **Major** | An existing query can return different results | A concept split or merged, a term reparented, a relation qualifier changed or removed, a top concept demoted, a term deprecated, a namespace change |

A concept split is always major, and its changelog entry has to say which URI
kept which meaning.

**The test is that nothing previously true becomes false.** Read literally, the
Major column would swallow Minor: adding anything changes what a query returns,
if only by returning one more row. It does not mean that. Major is for a
statement the vocabulary *used* to make and no longer makes — or makes
differently. Minor adds statements and retracts none.

That is what separates the two relation cases, which are otherwise easy to
confuse. **Adding** a qualifier is additive: every ISO 25964 link asserts *both*
`skos:broader` and the sub-property — `transform.py` materializes the plain link
because the ISO relations entail it without asserting it — so a bare link that
gains `isothes:broaderPartitive` keeps the `skos:broader` it already had, and a
consumer querying either property still gets every row it got before.
**Changing** one is not: `broaderGeneric` → `broaderPartitive` retracts a
triple, and a query for the generic relation comes back short. One caveat — the
additive ruling holds only while the parent stays. If qualifying a link reveals
the parent itself is wrong, that is a reparent, and major.

While the vocabulary is at `0.x`, patch and minor changes both advance the third
position — `0.1.3` → `0.1.4` — and a major change advances the second, `0.1.x` →
`0.2.0`. After `1.0.0` the three levels map onto the three positions directly.

`main` is the published branch: **merging to `main` publishes to w3id.org/pkm
immediately, with no staging step.** Work happens on a branch named for the
version it targets, so the level is decided before the work starts rather than
at release time. Each published version is tagged.

[Unreleased]: https://github.com/dpw67/pkm/compare/v0.1.10...HEAD
[0.1.10]: https://github.com/dpw67/pkm/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/dpw67/pkm/compare/v0.1.8...v0.1.9
[0.1.8]: https://github.com/dpw67/pkm/compare/v0.1.7...v0.1.8
[0.1.7]: https://github.com/dpw67/pkm/compare/v0.1.6...v0.1.7
[0.1.6]: https://github.com/dpw67/pkm/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/dpw67/pkm/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/dpw67/pkm/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/dpw67/pkm/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/dpw67/pkm/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/dpw67/pkm/releases/tag/v0.1.1
