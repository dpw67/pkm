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
| 3 | Circle post on the "Cluster" naming question | replied; definitions settled in 0.1.7, label still open — §E |
| 4 | Upstream migration-cutoff issue → [#81](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/81) | done |
| 5 | `definition-no-terminal-punctuation` + `self-referential-prose` checks | released in 0.1.6 |
| 6 | This roadmap, in the repo | done — §A |
| 7 | `make review` — the family-grouped review sheet | done — §B |
| 8 | 0.1.6 — the prose patch, 29 literals | done — §C |
| 9 | 0.2.0 — two malformed URIs renamed | after 0.1.8 — §D |
| 10 | LinkedIn 0.1.4/0.1.5 follow-up; third Circle post | unscheduled — §G |
| 11 | Where the vocabulary and the periodic notes disagree | recorded — §F |
| 12 | 0.1.7 — notes rendered, two definitions settled | built; merge pending — §E |
| 13 | 0.1.8 — the rest of the Cluster family | next — §H |

### Where 0.1.6 left the graph

`make check` on the export: 4337 triples, 223 concepts, 18 collections, 236
hierarchy links, 318 ISO 25964 links, 8 top concepts. **0 error, 2 warn.**

Both warns are upstream residue, not defects here: `doubled-attribution` (39)
and `lang-tag-in-text` (35) are SKOS Editor artifacts that `transform.py`
repairs on the way out, so the **published** graph is clean either way. Upstream
#81 covers them. `make build` prints no "warn remain after transform" line,
which is the signal that everything the transform cannot repair has been fixed
at the source.

Three `skos:editorialNote`s now record open questions on the concepts that carry
them rather than in a tracker: `DayClusterCore` (is Analysis a Core note?),
`Map` (should a Home Note be its parent?), and as of 0.1.6 `Month-Health` (the
local name is wrong; see §D).

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

**Shipped.** Patch throughout: definition, scope-note and change-note prose
only. No URI, no label, no membership, no relationship. 29 defective literals,
none of them the four 0.1.5 fixed — those stayed fixed. The itemised worklist is
in the [0.1.6 changelog entry](CHANGELOG.md); what is worth keeping here is what
the exercise taught.

**Four editor passes, because verification kept finding the pass itself.** Two
corrections landed on the wrong side of a quotation — `Clipping`'s audit note
came back reading `from "changing" to "changing"`, which documents nothing — and
two newly-authored change notes shipped with double spaces inside them. Neither
class of defect is visible in the editor.

**The audit-note convention works, and it breaks naive verification.** Every
correction leaves a companion note quoting the old spelling. So `definiton` still
occurs nine times in the export and all nine are correct. Counting occurrences
answers the wrong question; the check has to classify *quoted* versus
*narrative*:

```python
quoted = re.findall(r'["“]\s*(?:%s)\s*["”]' % pattern, text)
```

Three grep traps, all hit:

- `grep -c` counts **lines**, and every change note on a term serialises on one
  line, so it undercounts badly. `grep -o | wc -l`.
- `collectio` is a substring of `collection`, so the 0.1.5 audit-quote check
  false-positives on any literal containing "a collection of notes".
- The editor writes curly quotes, so a straight-quote grep finds nothing and
  looks like the record was destroyed. Diff properties against `HEAD` instead.

**Two checks earned their keep**: `definition-no-terminal-punctuation` found the
only definition of 223 missing its period, and `self-referential-prose` found
`QuarterLog` claiming to aggregate itself. Neither was findable by reading.

### C1. Deliberately not done

- **Five formulaic `*Cluster` definitions** — `EffortCluster`, `MonthCluster`,
  `QuarterCluster`, `TopicCluster` and `YearCluster` all read "A group of
  related notes about a …" while `DayCluster` and `WeekCluster` carry real ones.
  Editorial, but authoring rather than correction; folded into §E, where the
  Cluster/Collection question is open anyway.
- **`DayMealPlan`'s sixth change note is undated and unattributed.** No check
  fires, because `unattributed-changenote` requires a date.
- **15 literals with edge whitespace.** `transform.py` strips them on publish,
  so the published graph is already clean and no reader can perceive the
  difference. 15 invisible edits in a browser textarea buys nothing.

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

`Month-Health` was briefly renamed during the 0.1.6 editor passes, which turned
a patch into a major release and left `vocab/terms/Month-Health.{md,ttl}` as
ghosts — complete, live-looking pages for a term the vocabulary no longer
defined, with no deprecation marker, which is worse than either a tombstone or a
404. The hyphen was restored and the rename deferred here. **As of 0.1.6 the
concept carries a `skos:editorialNote` stating the defect and the deferral**, so
anyone dereferencing the term sees it. That note comes out when §D lands.

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
- **What readers suggested instead of "Cluster"** (Circle, 2026-09-11, on the
  naming post). Worth recording because the post asked the question and these
  are the answers: **Bentō**, **Dossier**, **Kit**, **Package** and "Doug Day"
  from Malaika; **Compilation** from Zainab. Two are live candidates.
  *Compilation* carries the deliberate assembly that "Cluster" lacks — you
  compile something on purpose — and unlike *Collection* it has no SKOS meaning
  to collide with, so it can stay a `skos:Concept` and keep its 63 hierarchy
  links. *Dossier* says "assembled record of one subject" precisely and is the
  only suggestion that implies the thing is *about* something. Against both:
  every name in the vocabulary is a plain English word a script author would
  guess, and neither is.

  **Record** (Sabine, same thread) answers that objection — it is a plain word,
  it carries the assembled-record-of-one-subject sense that *Dossier* has, and
  the naming post already reached for it unprompted, calling a Day Cluster "the
  record of that one day". What rules it out is internal: *record* is already
  this vocabulary's word for a `Log`. `pkmv:DayLog` is defined as "A
  chronological record of what actually happened during a day", and
  `pkmv:WeekLog`, `pkmv:MonthLog` and `pkmv:YearLog` all read "A record of what
  happened over a …". Naming the container `Day Record` when one of its six
  members already *is* the record of the day collides at the definition level,
  not just the label. *Daily Record* also reintroduces the adjective the post
  rejected in "Daily". Worth saying back to her, since the reasoning is the
  interesting part and it is the same test that killed *Collection*: the nicer
  word turns out to be the wrong shape.

  **Oran's 46 words** (same thread, 2026-09-12) are the most useful reply yet,
  because a list that long stops being brainstorming and becomes a stress test.
  They sort into four families, none of which fits: many of one kind (20 —
  array, batch, set, stack, segment, volume, bundle …); a place where things are
  kept (14 — bank, cache, repository, store, depot, trove …); accumulation
  without intent (6 — clump, dump, gathering, heap, mass, pile); and derived
  from the thing rather than the thing (6 — aggregate, digest, roundup,
  summary …). Closest survivors *bundle* and *gathering* both stop short of
  "about one subject". `Vault` is the only word on the list that is already a
  label here, and it holds exactly the place-tier job family 2 wants.

  **Four tests, which is what the thread actually produced.** A name must be (1)
  a plain English word a script author would guess, (2) free of collision with a
  term already inside the vocabulary, (3) a whole of unlike parts rather than
  many of one kind, and (4) about one subject. Fifty-three alternatives from
  four people, and "Cluster" still passes all four — which is itself the
  finding.

  **The relations already assert (3); both definitions contradict it.**
  `DayCluster` carries `isothes:narrowerPartitive` to `DayClusterCore`,
  `DayClusterHealth`, `DayClusterSupport` and `DayClusterVisual` — four unlike
  *parts* — and is itself both `broaderGeneric pkmv:TimeCluster` and
  `broaderPartitive pkmv:CalendarFolder`. 103 concepts assert
  `broaderPartitive`, so the whole/part reading is pervasive, not incidental.
  Yet `Cluster` is defined "A group of related notes" and `DayCluster` "The
  **set** of structured notes and artifacts generated for a single day" — using
  *set*, the word the naming post rejected for implying no structure. Both
  describe a bag. **This was the likelier bug than the label**, and being prose
  only — no URI change, no reparenting — it rode in 0.1.7 rather than waiting
  for 0.2.0. Both definitions now name a whole of unlike parts about one
  subject; the label is untouched and still under question.

  Decide the label with the `Collection` definition above, not before it.
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

## F. Where the vocabulary and the periodic notes disagree

Found by comparing the five period subtrees against what the generators in
`pkm-neo4j-service` actually write. Both directions are wrong, and the gap is in
the generator rather than in any hand-copy: `pkm-week create` writes five notes
— Plan, Log, Review, Health, Diabetes — against the ten concepts narrower than
`pkmv:WeekCluster`, and its Week Health note links `[[2026 Year Health]]`, a
term that is defined and a note that is never generated.

Three questions, not three decisions. Each could be answered by minting a term
or by dropping a note, and which way round is the point.

- **`MonthDiabetes`** — the note exists in practice; `DayDiabetes` and
  `WeekDiabetes` are defined terms and Month has none. Is monthly diabetes
  tracking a real rung of the roll-up, or was that note a copy that should not
  have been made?
- **`MonthIndex`, `QuarterIndex`, `YearIndex`** — `DayIndex` and `WeekIndex`
  exist, and the generated Day Index note links to all three of the missing
  ones. Either the upper horizons get hub notes and the terms follow, or the
  links are wrong. Only `Day`, `Week`, `Effort` and `Topic` have `Index` terms
  at all, so this is a question about the whole tier.
- **The Health/Journal asymmetry** — `QuarterHealth`, `YearHealth`,
  `MonthJournal`, `QuarterJournal` and `YearJournal` are all defined, and none
  of them is generated. Defined-but-absent is the larger half of the mismatch:
  17 terms across the five periods have no note *in the current cluster*, seven
  of them at Day.

That 17 is the gap left by the **period generators**, not by the system. Four
other scripts write some of those notes on their own schedule, so measured
against the whole `Calendar/Notes` tree only **13** period terms have never
been written at all: `DayMealPlan`, `DayMeeting`, `DayDiagram`, `DayMindmap`,
`WeekAnalysis`, `WeekDiabetesAnalysis`, `WeekJournal`, `WeekMealPlan`,
`MonthJournal`, `QuarterHealth`, `QuarterJournal`, `YearHealth` and
`YearJournal` — and one of those thirteen does exist, under another name. What
fills the difference:

- `pkm-health analysis` writes `Day Analysis` (140 notes), `Day Diabetes` (219)
  and `Day Diabetes Analysis` (131). None of the three is in today's cluster
  because they follow a Dexcom/Glooko export rather than the calendar, which is
  why a single-day comparison reads them as missing.
- `pkm-recipe meal-plan --save` writes the week meal plan, six so far — but
  named `Meal Plan`, and until this round into `Calendar/Notes/2026/2026-W##/`
  rather than the cluster's own `W##/`. Six orphan folders are left in
  Ideaverse (`2026-W21`, `-W22`, `-W23`, `-W25`, `-W27`, `-W29`), each holding
  nothing but a meal plan, sitting beside the real week cluster. The path is
  fixed; moving the six existing files is a vault edit, not a code one.
- `WeekIndex` has exactly one note, `2026-W09 Week Index.md`. That is the same
  shape of evidence as `MonthDiabetes` above — one note is a decision
  half-made, not a practice.

No RDF changes here, and none implied. The `--vault` flag in
`pkm-neo4j-service` makes it possible to generate a cluster into a second
vault; whether one *should* — and against which of the two readings above — is
this question, not that one.

Two generator defects noticed in passing, in that repo rather than this one:
`week_cluster_generator.py:141` builds the previous-week link as
`{year - 1}-W{week}` instead of the week before, and the next-week link as
`W{week + 1}` with no year rollover at W52.

### F1. Two naming questions

Both are file renames, so both are 0.2.0 at the earliest, and both are the same
question the three above are: does the vocabulary follow the note, or the note
the vocabulary?

- **`Meal Plan` or `Week Meal Plan`?** `pkm-recipe` writes `2026-W25 Meal
  Plan.md` beside `2026-W25 Week Plan.md`, `Week Log.md`, `Week Health.md` —
  every sibling carries the horizon in the name and this one does not. The
  vocabulary says `pkmv:WeekMealPlan`, which argues for the rename; one of the
  six is a third name again, `2026-W23 DMP Meal Plan.md`.
- **`Diabetes Review` or `Day Diabetes`?** Three health services write
  `{date} Diabetes Review.md` — 312 of them, 261 in 2025 and 17 in 2026, the
  last on 2026-01-25. The generators and `pkm-health analysis` write `Day
  Diabetes` / `Week Diabetes`, and the vocabulary defines `pkmv:DayDiabetes`
  and `pkmv:DayDiabetesAnalysis`. So the name has already changed in practice
  and the older one stopped being written in January; what is unsettled is
  whether the 312 existing notes get renamed to match or stay as a dated layer.

### F2. The service layer still hardcodes the vault

The CLIs in `pkm-neo4j-service` now resolve the vault through `app/vault.py`
(`OBSIDIAN_VAULT_PATH`, then `--vault`), but the CLIs that talk to the FastAPI
service only send HTTP — the service picks the path. So `pkm-health` and
`pkm-review` deliberately have no `--vault` flag: it would change the
`obsidian://` URI and not the file. A worklist, so the next round is not
another grep:

| File | Lines |
|---|---|
| `app/services/review/morning_review_service.py` | 33 |
| `app/services/health/dexcom_export_service.py` | 425, 488, 587 |
| `app/services/health/glooko_export_service.py` | 332, 395, 494 |
| `app/services/health/health_service.py` | 368 |
| `app/services/health/diabetes_review_generator.py` | 24 — already parameterised, never passed |
| `app/services/health/diabetes_charts.py` | 902 |
| `app/services/health/glucose_timeline_chart.py` | 297 |
| `app/services/recipe/recipe_service.py` | 182 |
| `app/services/recipe/dmp_service.py` | 432 |

`scripts/pkm-day-pre-neo4j` and `scripts/ontology/generators/pkm-concept.py`
hardcode it too, but they are a separate question: both may simply be dead.

## G. Unscheduled

- **LinkedIn 0.1.4/0.1.5 follow-up** — drafted; its link-card claim is verified.
- **A third Circle post** on the Spectrum — drafted, 220 lines.
- **Stub filenames** — `vocab/terms/IdeaEmergence.md` with an `aliases:` entry,
  so wikilinks keep resolving while the filename matches the URI local name.
  `notes.py` work plus a 241-file rename. **Becomes load-bearing if §D ships**:
  two stubs would need renaming with their URIs.
- **Vault reorganisation commit** — done (`f207dd6` in the vault repo). One of
  the two moves records as a rename; *Three Places for One Vocabulary* does not,
  even at `-M30%`, because it was rewritten as well as renamed.

## H. 0.1.8 — the rest of the Cluster family

0.1.7 rewrote `pkmv:Cluster` and `pkmv:DayCluster` to say that a cluster is a
whole of unlike parts about one subject. Seven concepts underneath them still
say it is a bag. All three of `pkmv:Cluster`'s direct children are among them,
so a reader who follows the hierarchy down one level meets the phrasing the
parent just abandoned.

| concept | definition | relation to `pkmv:Cluster` |
| --- | --- | --- |
| `pkmv:TimeCluster` | A group of related notes for a time period (or time horizon). | direct child, `broaderGeneric` |
| `pkmv:EffortCluster` | A group of related notes about an effort. | direct child |
| `pkmv:TopicCluster` | A group of related notes about a topic. | direct child |
| `pkmv:MonthCluster` | A group of related notes about a month. | via `TimeCluster` |
| `pkmv:QuarterCluster` | A group of related notes about a quarter. | via `TimeCluster` |
| `pkmv:YearCluster` | A group of related notes about a year. | via `TimeCluster` |
| `pkmv:WeekCluster` | The **set** of structured notes and artifacts generated for a single week, aggregating and analyzing its constituent Day Clusters. | via `TimeCluster`; `DayCluster`'s sibling |

`pkmv:WeekCluster` is the sharpest of the seven: it is the sentence
`pkmv:DayCluster` carried until 0.1.7, word *set* included, on its own sibling.
Whatever replaces it should hold for both, since a week aggregates days the way
a day aggregates its four parts.

`pkmv:DayCluster`'s four parts are **not** on this list. "The core set of daily
notes within a Day Cluster", and the three like it, describe one part holding
notes of one kind — which is what a part is, so the bag reading is correct
there.

### H1. Two scope notes cite terms that do not exist

`pkmv:Cluster`'s scope note names seven examples; two of them are not in the
vocabulary.

- **`ConceptCluster`** was real once. In `z/pkm-vocab.export-0.1.2.ttl` it is
  `pkm:collection10`, labelled "Concept Cluster", with the ten members
  `pkmv:ConceptCollection` carries today — it was reclassified from a Cluster
  to a Collection and the scope note was never updated. That reclassification
  is the same Cluster/Collection distinction §E defers, so the fix is evidence
  for that decision rather than a prejudgement of it.
- **`OutputCluster`** has never existed, in any release.

The same scope note omits `pkmv:TimeCluster` — `Cluster`'s only unnamed direct
child — along with `pkmv:QuarterCluster` and `pkmv:YearCluster`.

`pkmv:TimeCluster`'s scope note repeats the defect in both directions: it lists
`DecadeCluster` and `LifeCluster` as time clusters (both exist only as
`pkmv:DecadeCollection` and `pkmv:LifeCollection`) and excludes
`ConceptCluster` and `OutputCluster` by name as the non-time clusters.

Two further mentions — `pkmv:Project` "distinguish from … the Effort Cluster /
Output Cluster structures" and `pkmv:WeekIndex` "analogous to the Index hub
notes in the Effort/Output Cluster design" — are spaced rather than CamelCase
and read as design language, not term citations. Judgement call whether they
move with the rest.

### H2. A check that would have caught this

`checks.py` has no rule for prose that cites a CamelCase name absent from the
scheme, which is why four scope notes have carried phantom terms since 0.1.2
without a single finding. A check scanning `skos:definition` and
`skos:scopeNote` for `\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b` and reporting any token
that is neither a local name nor a known exception would have flagged all of
them. Same shape as §D4's two proposals, and cheap.

Level: patch throughout. Prose only — no URI, label, parent or membership
moves — so by the versioning table nothing a consumer queries changes meaning.


## Backlog

Folding the `pages.py` and `notes.py` extraction into one place; a CI build
check on version branches; `rel="alternate"` pointing browsers at the Turtle;
two stale `navigationHiddenItems` entries on pre-`z/` paths; a
`make changelog FROM=v0.1.1` graph-diff generator. Publish exclusion still does
not retract, so roughly 103 notes stay live until unpublished by hand.
