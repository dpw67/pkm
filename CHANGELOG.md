# Changelog

All notable changes to the PKM vocabulary and the resources published at
[w3id.org/pkm](https://w3id.org/pkm) are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version levels are explained under [Versioning](#versioning).

## [Unreleased]

Nothing yet. Work starts on a branch named for the version it targets.

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
| **Minor** | Additive; every existing URI keeps its meaning | New concepts or collections, new relations, new cross-vocabulary mappings |
| **Major** | An existing query can return different results | A concept split or merged, a term reparented, a term deprecated, a namespace change |

A concept split is always major, and its changelog entry has to say which URI
kept which meaning.

While the vocabulary is at `0.x`, patch and minor changes both advance the third
position — `0.1.3` → `0.1.4` — and a major change advances the second, `0.1.x` →
`0.2.0`. After `1.0.0` the three levels map onto the three positions directly.

`main` is the published branch: **merging to `main` publishes to w3id.org/pkm
immediately, with no staging step.** Work happens on a branch named for the
version it targets, so the level is decided before the work starts rather than
at release time. Each published version is tagged.

[Unreleased]: https://github.com/dpw67/pkm/compare/v0.1.6...HEAD
[0.1.6]: https://github.com/dpw67/pkm/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/dpw67/pkm/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/dpw67/pkm/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/dpw67/pkm/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/dpw67/pkm/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/dpw67/pkm/releases/tag/v0.1.1
