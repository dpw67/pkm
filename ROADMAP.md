# Roadmap

What is done, what is next, and which version level each item lands in.

Status is the first thing in this file on purpose: the question it has to answer
is "what changed since I last read it", and that is a `git log ROADMAP.md` away.
Section letters are stable, so a diff shows state changes rather than a reflow.

Version levels come from [Versioning](CHANGELOG.md#versioning) and describe
impact on consumers, not volume of work. At `0.x` patch and minor both advance
the third position; only major advances the second.

## Status

| # | Item | State |
|---|---|---|
| 1 | 0.1.5 released — tagged, published, spot-checked live | done |
| 2 | 0.1.5 announcement, [Discussions #3](https://github.com/dpw67/pkm/discussions/3) | done |
| 3 | Circle post on the "Cluster" naming question | done |
| 4 | Upstream migration-cutoff issue → [#81](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/81) | done |
| 5 | `definition-no-terminal-punctuation` + `self-referential-prose` checks | committed, unreleased |
| 6 | This roadmap, in the repo | done — §A |
| 7 | `make review` — the family-grouped review sheet | §B |
| 8 | 0.1.6 — the prose patch | needs an editor session — §C |
| 9 | 0.2.0 — two malformed URIs renamed | after 0.1.6 — §D |
| 10 | LinkedIn 0.1.4/0.1.5 follow-up; third Circle post | unscheduled — §F |

### Where 0.1.5 left the graph

`make check` on the current export: 4292 triples, 223 concepts, 18 collections,
236 hierarchy links, 318 ISO 25964 links, 8 top concepts. **0 error, 4 warn.**

Two of the four warns are real and two are upstream residue:

- `definition-no-terminal-punctuation` — `WeekReview`. Real; §C1.
- `self-referential-prose` — `QuarterLog`. Real; §C1.
- `doubled-attribution` (39) and `lang-tag-in-text` (35) — SKOS Editor
  artifacts. `transform.py` repairs both on the way out, so the **published**
  graph is clean. Upstream #81; nothing to do here.

`make build` reports `2 warn remain after transform`. That is expected: the two
new checks name defects the transform cannot repair. **Those 2 returning to 0 is
the signal that §C1 landed.**

## A. This roadmap

Excluded from the built site in `_config.yml`, next to `README.md`, for the same
reason given there — `index.md` is the site index and this is a repo document.
Published at `w3id.org/pkm/ROADMAP.html` it would read as a commitment surface,
and it names defects that are not yet fixed.

## B. `make review` — the family-grouped review sheet

**Why.** Reading 223 terms one page at a time does not surface template drift.
Printing a suffix family side by side does. Three of the five `*Review`
definitions were defective and it was invisible term-by-term; `QuarterLog`
naming itself as its own source only showed up next to `WeekLog` and `MonthLog`.

`scripts/pkm_vocab/review.py`, a fourth subcommand beside `check` / `build` /
`notes`, writing `reports/vocab-review.md`.

Reuse rather than reimplement — in particular **`Vocabulary.broader_pairs()`**,
which merges `skos:broader`, `skos:narrower` *and* the ISO 25964 sub-properties.
Reading `skos:broader` directly misses 318 links.

The sheet, in order:

1. **Periodic families.** Group by prefix (`Day`, `Week`, `Month`, `Quarter`,
   `Year`, `Decade`, `Life`), pivot on suffix, and print each suffix family as
   one table with a row per period. A gap in the grid is a missing term; a row
   that reads unlike its neighbours is drift.
2. **Everything else, grouped by parent**, so siblings stay adjacent.
3. **Collections**, each with its description and member count.

Flags are hints for a human reader, not check failures: mark a family whose
definitions differ by more than the period name, and mark a childless term whose
siblings all have children.

## C. 0.1.6 — the prose patch

**Patch throughout.** Definition, scope-note and change-note prose only. No URI,
no label, no membership, no relationship.

Ship this before and independently of §D. It is finished work, it needs no
decisions, and since 0.1.5 gave every page its own `og:description` each of
these defects is rendering in link cards.

These are **not** the four misspellings 0.1.5 fixed. Those are verified gone. A
dictionary sweep plus a family-alignment pass found 27 further misspelling
occurrences in 26 different literals, plus three defects that are not
misspellings at all.

### C1. Definitions and scope notes — 13 literals

| term | field | defect | corrected |
|---|---|---|---|
| `WeekReview` | definition | `compled`, **and no terminal period** | `A structured retrospective evaluating a completed week.` |
| `MonthReview` | definition | `retrospectivee` | `A structured retrospective evaluating a completed month.` |
| `QuarterReview` | definition | `retrospectivee` | `A structured retrospective evaluating a completed quarter.` |
| `Bases` | definition | `thatcreates` | `A core plugin that creates custom views to edit, sort, and filter files using properties.` |
| `DayBoard` | definition | `Kanboard board` | `An Obsidian Kanban board note for the day.` |
| `DayClusterCore` | definition | names five core notes; the hierarchy has six | `The core set of daily notes within a Day Cluster - typically Index, Plan, Log, Journal, Review, and Analysis.` |
| `AdvancedURI` | scopeNote | `workspacces`, `headlngs` — two in one literal | `- Open files, workspaces, headings, blocks, lines, and settings.` |
| `Base` | scopeNote | `crtieria` | `…different query criteria, which can be selected…` |
| `Finance` | scopeNote | `financies` | `…managing and maintaining your finances over time…` |
| `YearLog` | scopeNote | `Yeary` | `Yearly factual roll-up; aggregates QuarterLog entries.` |
| `QuarterLog` | scopeNote | **aggregates itself** | `Quarterly factual roll-up; aggregates MonthLog entries.` |
| `PKMNeo4jServiceProject` | scopeNote | `Grqph` | `…for Calendar, Health, Graph, Obsidian, Recipe, and Review.` |
| `DMPMealPlan` | scopeNote | `Wordpress` | `WordPress Recipe Maker (WPRM)` |

Two of these are not typos, and they are the most valuable finds:

- **`QuarterLog` says it aggregates `QuarterLog`.** The roll-up chain is Day →
  Week → Month → Quarter → Year and every other rung names the rung below it. A
  reader following the chain hits a loop. Its own changelog bullet — this is a
  wrong statement, not a misspelling.
- **`WeekReview` is the only definition of 223 with no terminal punctuation**,
  which is what makes that check worth having: the signal is not buried.

### C2. Change notes — 15 literals

| defect | count | terms |
|---|---:|---|
| `definiton` → `definition` | 9 | `EffortIndex`, `EffortJournal`, `EffortLog`, `EffortPlan`, `TopicIndex`, `TopicJournal`, `TopicLog`, `TopicPlan`, `TopicReview` |
| `definintion` → `definition` | 2 | `PKMPythonAPI`, `PKMPythonServices` |
| `deinition` → `definition` | 2 | `Finance`, `Health` |
| `Pujblish` → `Publish` | 1 | `Publish` |
| `changiing` → `changing` | 1 | `Clipping` |

`TopicReview`'s note also names the wrong term — "Added definiton and scope
notes for a Topic **Index**", copy-pasted from the line above. Fix both in one
edit.

> **Two change notes must be left exactly as they are.** They quote a
> misspelling deliberately, as the record of what 0.1.5 corrected: `Map`'s note
> quotes `collectio`, and `Idea`'s quotes `explicityl`. A find-and-replace over
> the export destroys that record. Do the change notes by hand in the editor, or
> exclude quoted strings explicitly. The quotes are curly, so a straight-quote
> grep will not find them.

Whether to rewrite history at all is a judgment call. For: they render verbatim
on 241 public pages, `definiton` appears nine times, and nothing about the
substance — date, author, described change — moves. C1 alone is still a
worthwhile release if C2 is dropped.

### C3. Optional, descending value — all patch-level

- **`View`'s scope note** uses "collection" informally for the thing
  `skos:Collection` names formally. Harmless today, confusing the moment a
  `Collection` concept exists. One word: "group".
- **Five formulaic `*Cluster` definitions** — `EffortCluster`, `MonthCluster`,
  `QuarterCluster`, `TopicCluster` and `YearCluster` all read "A group of
  related notes about a …" while `DayCluster` and `WeekCluster` carry real ones.
  Editorial, but authoring rather than correction; reasonable to fold into the
  §E restructure instead.
- **`DayMealPlan`'s sixth change note is undated and unattributed.** No check
  fires, because `unattributed-changenote` requires a date.
- **23 literals with edge whitespace.** `transform.py` strips them on publish,
  so the published graph is already clean and no reader can perceive the
  difference. Leave them — 23 invisible edits in a browser textarea.

## D. 0.2.0 — two malformed URIs

**The renames are what force a major version.** A change is major when an
existing query can return different results, and a query for `pkmv:Month-Health`
returns nothing once it is renamed. The `index.md` instability licence permits
the change without notice; it does not make it editorial.

| current URI | prefLabel | problem | becomes |
|---|---|---|---|
| `pkmv:Month-Health` | Month Health | the only hyphenated local name of 241; siblings are `DayHealth`, `WeekHealth`, `QuarterHealth`, `YearHealth` | `pkmv:MonthHealth` |
| `pkmv:TemplateCopy` | Template | editor scaffolding in the URI; scope note copy-pasted verbatim from `ObsidianTemplate` | `pkmv:Template` |

Both first appeared in 0.1.3, both return 200 today, and `make check` flags
neither — `numeric-suffix` wants a digit and `opaque-uri` matches neither.

### D1. Leave a tombstone at each old URI

The front page promises that a retired URI keeps resolving, marked
`owl:deprecated` and pointed at its replacement with `dcterms:isReplacedBy`, so
that a link made today does not rot. A bare rename breaks that promise two
paragraphs below the licence that permits it.

So rename, **and** keep `vocab/terms/Month-Health.ttl` and
`vocab/terms/TemplateCopy.ttl` as two-triple tombstones. The new URI is primary,
the correction lands now, and no link rots. This is the vocabulary's first use
of either predicate — both are at zero occurrences today.

`make build` reports per-term files whose URIs the vocabulary no longer defines
rather than deleting them, so tombstones survive a build by design. Confirm it
reports them as known orphans rather than failing.

### D2. Prose that rides with the rename

`TemplateCopy` is not only misnamed. Its definition reads like a generic parent,
its scope note is `ObsidianTemplate`'s verbatim, and its parents are identical
to `ObsidianTemplate`'s. Renaming it to `Template` without rewriting both
literals ships a duplicate.

### D3. Reparenting — a separate decision

`ObsidianTemplate` and `PythonTemplate` are currently `Template`'s siblings,
which looks like an intent that was never finished. Adding `Template` as an
additional broader is additive and minor; removing their existing parents is
reparenting and major. Both can ride in 0.2.0, but the changelog has to say
which happened.

### D4. Two checks that would have caught these

Same shape as `numeric-suffix` in `scripts/pkm_vocab/checks.py` — stem
extraction, twin lookup, two-way hint. Extend rather than invent.

- **`scaffolding-suffix`** — a local name ending `Copy`. Hint by whether the
  stem already exists. One hit today.
- **`non-camelcase-uri`** — a local name containing anything outside
  `[A-Za-z0-9]`. One hit today.

`pkmv:LocalRESTAPIWithMCP` against "Local REST API with MCP" is the only other
name/label divergence and is benign. Neither check may fire on it.

### D5. Documentation that must change

- The URI-stability section asserts that no URI has been removed, renamed or
  reused since 0.1.1. That becomes false; rewrite it to state the exception, the
  two URIs, and the licence it rests on.
- The same section cites `Day.Meal Plan` as precedent for *not* moving a URI
  when a label is wrong. Say why these two differ: the label was wrong there,
  the identifier is malformed here.
- `index.md` needs no change if D1 is taken.

## E. Also banked for 0.2.0 — structural

Measured, and worth taking only if 0.2.0 is already happening for §D.

- **`Cluster` vs `Collection`.** `DayCluster` is a `skos:Concept` carrying 63
  hierarchy links; `skos:Collection` cannot be the target of `skos:broader`, so
  converting it orphans all 63. The real duplication is that `DayCollection`
  restates the hierarchy by hand and **has already drifted** — `DayMeeting` is
  in the tree and missing from the collection, 26 members against 25
  descendants.
- **A collection rule:** enumerate only what the hierarchy cannot derive.
  `TechStack` is a hand-copy of the `Tool` subtree missing six — `App`,
  `AppIntent`, `ObsidianTemplate`, `PythonTemplate`, `TemplateCopy`, `Widget`. A
  `collection-mirrors-subtree` check is cheap. (`SemanticWebStandards` is *not*
  an example: 11 members against a 90-descendant subtree, so it mirrors
  nothing.)
- **Missing concepts:** no `Collection` and no `Vocabulary`, while 14
  `*Collection` collections exist. `Cluster` exists, defined "A group of related
  notes." Defining `Collection` is what forces `Cluster` to resolve — do them
  together. Additive, so minor on its own.
- **The four-way question** — `Day` the period, `Day Folder` the path (not
  modelled), `Day Cluster` the concept with 25 descendants, `Day Collection` the
  flat bag with 26 members. `DayFolder` alone is odd without
  `MonthFolder`/`YearFolder`: do the periodic folder tier as a set, or add a
  generic `Folder` and let the six major spaces narrow from it.
- **`Day`'s parents differ from its cluster's** — `Day` broader is
  `Calendar` + `Week`; `DayCluster` broader is `TimeCluster` + `CalendarFolder`.
  Reparenting, so major.
- **The ACE spine is half-built.** `AtlasFolder`, `ExtraFolder` and
  `ArchiveFolder` have no children at all, against `Vault` 8, `EffortsFolder` 4
  and `CalendarFolder` 7. "Group the note types by ACE space" cannot be
  expressed — not for want of a SKOS mechanism, but because half the spine is
  missing.
- **`Category` and `Group`** — neither exists. The vault experiment was real but
  small; `group:` carries values on 11 notes. Settle with `Collection`.
- **Three schema.org mappings** — `pkmv:Book skos:relatedMatch schema:Book`
  points a concept at an OWL class. A consumer can query it today, so changing
  it is major.

## F. Unscheduled

- **LinkedIn 0.1.4/0.1.5 follow-up** — drafted; its link-card claim is verified.
- **A third Circle post** on the Spectrum — drafted, 220 lines.
- **Stub filenames** — `vocab/terms/IdeaEmergence.md` with an `aliases:` entry,
  so wikilinks keep resolving while the filename matches the URI local name.
  `notes.py` work plus a 241-file rename. **Becomes load-bearing if §D ships**:
  two stubs would need renaming with their URIs.
- **Vault reorganisation commit** — the move still shows as two deletes with no
  matching adds; the destinations are untracked.

## Backlog

Folding the `pages.py` and `notes.py` extraction into one place; a CI build
check on version branches; `rel="alternate"` pointing browsers at the Turtle;
two stale `navigationHiddenItems` entries on pre-`z/` paths; a
`make changelog FROM=v0.1.1` graph-diff generator. Publish exclusion still does
not retract, so roughly 103 notes stay live until unpublished by hand.
