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
| 12 | 0.1.7 — notes rendered, two definitions settled | done — §E |
| 13 | 0.1.8 — phantom citations fixed, four prose checks | done — §H1, §H2 |
| 14 | 0.1.9 — the Cluster family says what the graph says | done — §H |
| 15 | The meals shape layer's open decisions | recorded — §I |
| 16 | Where this vocabulary sits against OWL-Time and the platform types | recorded — §J |
| 17 | What the eighteen collections actually are | measured — §E1 |
| 18 | 0.1.10 — the vocabulary you can actually read | chartered — §L |
| 19 | Upstream validation as a second opinion | done — §M |

### Where 0.1.9 left the graph

`make check` on the export: 4377 triples, 223 concepts, 18 collections, 236
hierarchy links, 318 ISO 25964 links, 8 top concepts. **0 error, 3 warn.**

Two of the three are upstream residue, not defects here: `doubled-attribution`
(39) and `lang-tag-in-text` (35) are SKOS Editor artifacts that `transform.py`
repairs on the way out, so the **published** graph is clean either way. Upstream
#81 covers them. The third is `scaffolding-local-name` on `pkmv:TemplateCopy`,
which the transform cannot repair because the fix is a rename — see §D, and do
not silence it.

So `make build` prints **`1 warn remain after transform`**, and that one warning
is the whole of what is left. The line first appeared in 0.1.8, when the rule
that produces it was written; this file claimed until 0.1.9 that no such line
was printed, which had been false for a release. 0.1.9 took it from nine to one
by quoting the eight recorded names — see §H2. Nine to zero is §D's to finish.

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
- **Literals with edge whitespace.** `transform.py` strips them on publish, so
  the published graph is already clean and no reader can perceive the
  difference. Invisible edits in a browser textarea buy nothing. Measured again
  for 0.1.9: **21** literals, 20 with a trailing run and 14 padded at an edge,
  and **zero** with the mid-prose double space `padded-literal` reports — so the
  whole class is the unreported kind. `pkmv:TimeCluster`'s was fixed at the
  source in 0.1.9 because its scope note was being rewritten anyway.

  Worth keeping the total honest while here: `transform.py` repairs **95**
  literals on every build, not the 94 once claimed, and only 21 of them
  silently. The other 74 are exactly the two WARN groups `make check` prints —
  35 `lang-tag-in-text` and 39 `doubled-attribution` — so "silently repaired"
  overstates the invisible part more than fourfold.

## D. 0.2.0 — two malformed URIs

**The renames are what force a major version.** A change is major when an
existing query can return different results, and a query for `pkmv:Month-Health`
returns nothing once it is renamed. The `index.md` instability licence permits
the change without notice; it does not make it editorial.

| current URI | prefLabel | problem | becomes |
|---|---|---|---|
| `pkmv:Month-Health` | Month Health | the only hyphenated local name of 241; siblings are `DayHealth`, `WeekHealth`, `QuarterHealth`, `YearHealth` | `pkmv:MonthHealth` |
| `pkmv:TemplateCopy` | Template | editor scaffolding in the URI; scope note copy-pasted verbatim from `ObsidianTemplate` | `pkmv:Template` |

Both first appeared in 0.1.3 and both return 200 today. As of 0.1.8
`scaffolding-local-name` flags `pkmv:TemplateCopy` as a WARN — deliberately
not an ERROR, because the fix is this section and an ERROR would block
`make build` until it lands. **That warning is expected until §D ships; do
not silence it.**
`pkmv:Month-Health` is still flagged by nothing: `numeric-suffix` wants a digit,
`opaque-uri` matches neither, and a hyphen is legal in a local name.

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

The three Claude interfaces are the same shape, found while fixing
`pkmv:ClaudeCowork`'s stale definition in 0.1.8. `pkmv:ClaudeDesktop`,
`pkmv:ClaudeCowork` and `pkmv:ClaudeChat` are all `skos:broader
pkmv:ClaudeAI`, i.e. siblings — but Cowork and Chat are surfaces *inside*
Claude Desktop, which `pkmv:ClaudeDesktop`'s own scope note says. Moving
them under it is reparenting, so it waits with the rest of this section.
Missing alongside them: a term for **Claude Code**, the third interface
beside Chat and Cowork. Adding a term is additive and minor, so it need not
wait for 0.2.0 — but it is the reason `pkmv:ClaudeDesktop`'s scope note
lists two interfaces rather than three, and both notes should change in one
editor session.

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
  descendants. See §E1 for what the other seventeen turned out to be, and §E2
  for why "make it both" is not available.

  **Every membership change is major**, which is what forces all of this into
  one release rather than letting it arrive a collection at a time. Dropping a
  member means `SELECT ?m { pkmv:DayCollection skos:member ?m }` returns fewer
  rows, and the table calls that major; deprecating a collection outright is
  listed as major too. 0.1.9 took the part that *is* patch — the descriptions —
  and left every member in place.
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

### E1. Three kinds of collection, and only one earns its keep

Measured for 0.1.9 against the subtree each one shadows. The intuition that
these are loose bags of "everything that mentions a day" turns out to be
backwards, and the truth points somewhere more actionable.

| kind | collections | what is wrong |
|---|---|---|
| **Mirrors a subtree** | Day (26), Week (11), Year (7), Quarter (6), Month (5), Recipe (7) | redundant — the hierarchy already derives them — and five of the six have drifted |
| **Genuine facet** | NoteTypes (20), MealDomain (16), SemanticWebStandards (11), TechStack (10), Concept (10), Effort (5), Knowledge (4) | nothing; these cut across the tree and cannot be derived |
| **Degenerate** | Decade (1), Life (1), Time (2), Ideaverse (2), Spark (2) | one or two members — a decision half-made |

**The five period collections have five different shapes**, which is the
clearest evidence that no rule was ever applied: Day holds the period, the
cluster and 24 of 25 descendants; Week holds the period and all ten parts but
not the cluster; Month holds the period and four of five parts and not the
cluster; Quarter holds the period, the cluster, three of five parts **and
`MonthJournal`**; Year holds the period, the cluster and all five parts.

`QuarterCollection`'s stray `MonthJournal` is not random — `QuarterCluster`'s
own change note reads `Duplicated from "MonthCluster"`, so the collection was
copied along with the concept and only partly corrected. That is the same
`stale-duplicate-definition` mechanism §H2 already checks for, one level up at
the collection.

So the 0.2.0 worklist is decidable rather than open-ended: **retire the six
mirrors** (the hierarchy already says it), **finish or drop the five
degenerates**, **keep the seven facets**. A `collection-mirrors-subtree` check
is cheap and is already proposed above.

### E2. `Concept` and `Collection` are disjoint, so "make it both" is not available

SKOS Reference **S37**: `skos:Collection` is disjoint with `skos:Concept` and
`skos:ConceptScheme`. `skos:member` has domain `skos:Collection` (S31) while
`skos:broader`, `skos:narrower` and `skos:related` inherit domain and range
`skos:Concept` from `skos:semanticRelation` (S19, S20) — so asserting
`skos:broader` at a collection makes the graph inconsistent, which the
Reference gives as Example 46.

The sanctioned workaround is Example 48: relate the concepts with
`skos:narrower`, and *separately* gather them with `skos:member`. So a twin
collection beside a concept is legal SKOS — `DayCollection` beside
`DayCluster` is exactly that shape.

**It is still not worth minting more of them.** Giving `DayClusterCore`,
`DayClusterHealth`, `DayClusterSupport` and `DayClusterVisual` a collection
each was considered for 0.1.9 and rejected: all four already carry
`isothes:narrowerPartitive` to their own notes, which **is** the grouping, so a
collection would restate by hand what the hierarchy derives — the rule stated
two bullets above. The evidence against is the existing twin: `DayCollection`
is that pattern applied once, and it has already drifted by a member. Four more
would be four more things to drift.

### E3. Two classes that cannot be fixed by prose

Both found while measuring 0.1.9, both recorded here because the resolution is
structural and therefore major.

- **13 concepts where a change note and the hierarchy flatly disagree.** Eleven
  say a parent was removed and it is still there — ten of them `Tool`
  (`Cypher`, `Neo4j`, `Python`, `Swift`, `Script`, `FastAPI`, `Hummingbird`,
  `AppIntent`, `ObsidianTemplate`, `PythonTemplate`) plus `TimeCluster` against
  `Cluster`. Two say a parent was added that is not there: `OWL` and `RDF`
  against `Standard`, both now under `W3CStandard`, so those two read as a note
  recording an intermediate state rather than an error. The obvious explanation
  for the `Tool` ten — that the editor removed `skos:broader` and left
  `isothes:broaderGeneric` behind — was checked and is **wrong**: `Tool` is
  present as both. The removal simply never took. Deciding whether `Tool` stays
  is reparenting, so major. **A `changenote-contradicts-hierarchy` check is
  mechanically decidable and finds all 13** — same shape as §H2's four.
- **36 concepts (16%) whose last prose edit predates a later structural
  change.** A risk list, not a defect list: spot-checking sixteen found most
  survived their reparenting intact, because a definition of what Python *is*
  does not depend on where Python sits. Two are real. `pkmv:Event`'s scope note
  opens "Top concept for the Event hierarchy" while the concept was unmarked as
  a top concept and now sits under `pkmv:PKMMeals` — which is itself worth a
  look. `pkmv:Time`'s says it is "the anchor/parent for the Calendar hierarchy
  (Life > Decade > Year > Quarter > Month > Week > Day)" while `Time` is a
  *child* of `Calendar`, so the note is inverted. That same note ends "Worth
  deciding OWL Time alignment before finalizing" — §J reached the identical
  question from outside, weeks after the note asked it and nothing read it.
  **This is the argument for §L**: a note nobody can find is a note nobody acts
  on.

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

## H. The rest of the Cluster family — shipped in 0.1.9

**Done.** 0.1.7 rewrote `pkmv:Cluster` and `pkmv:DayCluster`; 0.1.8 shipped §H1
and §H2; 0.1.9 rewrote the seven definitions in the table below, nine scope
notes in the same family, and the eight change notes of §H2's convention. The
itemised worklist is in the [0.1.9 changelog entry](CHANGELOG.md); what is worth
keeping here is what the exercise settled and what it did not.

**Two of the seven could not take the same sentence, and the graph is why.**
`pkmv:TimeCluster` is `narrowerGeneric` to all five period clusters where they
are `narrowerPartitive` to their own notes — it is a kind-of parent, not a
whole — so it got a kind-of definition. `pkmv:EffortCluster` and
`pkmv:TopicCluster` carry **no ISO 25964 relations at all**, plain
`skos:broader`/`skos:narrower` only, alone among the clusters. Writing "unlike
parts" into their definitions would have asserted in prose exactly what §H
exists to stop asserting, so they kept the subject clause without the partition
claim and their scope notes say plainly that no partitive structure is asserted
yet. **Adding those relations is additive, so minor** — see §K.

**What stayed open.** The label. Four tests, fifty-three alternatives and the
whole of §E still sit on `Cluster` the word, and nothing in 0.1.9 touched it —
by design, since §E says to decide it with the `Collection` definition and not
before.

| concept | definition until 0.1.9 | relation to `pkmv:Cluster` |
| --- | --- | --- |
| `pkmv:TimeCluster` | A group of related notes for a time period (or time horizon). | direct child, `broaderGeneric` |
| `pkmv:EffortCluster` | A group of related notes about an effort. | direct child |
| `pkmv:TopicCluster` | A group of related notes about a topic. | direct child |
| `pkmv:MonthCluster` | A group of related notes about a month. | via `TimeCluster` |
| `pkmv:QuarterCluster` | A group of related notes about a quarter. | via `TimeCluster` |
| `pkmv:YearCluster` | A group of related notes about a year. | via `TimeCluster` |
| `pkmv:WeekCluster` | The **set** of structured notes and artifacts generated for a single week, aggregating and analyzing its constituent Day Clusters. | via `TimeCluster`; `DayCluster`'s sibling |

`pkmv:WeekCluster` was the sharpest of the seven: it held the sentence
`pkmv:DayCluster` carried until 0.1.7, word *set* included, on its own sibling.

**The expectation recorded here — that its replacement should hold for both,
since a week aggregates days the way a day aggregates its four parts — turned
out to be wrong, and the graph is what corrected it.** No containment between
`pkmv:WeekCluster` and `pkmv:DayCluster` is asserted anywhere: they are
siblings under `pkmv:TimeCluster`, and the ten `narrowerPartitive` children
`WeekCluster` does have are the week's own notes. So the old definition's
closing clause, "aggregating and analyzing its constituent Day Clusters", was
itself prose the graph contradicts — a second defect in the sentence that was
already the worst of the seven, and invisible until the relations were read
rather than the words. It was dropped rather than rephrased. Whether the
roll-up *should* be asserted is a reparenting question, so §E.

`pkmv:DayCluster`'s four parts are **not** on this list. "The core set of daily
notes within a Day Cluster", and the three like it, describe one part holding
notes of one kind — which is what a part is, so the bag reading is correct
there.

### H1. Two scope notes cite terms that do not exist — fixed in 0.1.8 and 0.1.9

**Half in each release, which is worth recording as a pattern rather than a
footnote.** 0.1.8 removed the two phantom citations, because that is what
`phantom-citation` could see. The *omission* in the same sentence — three real
children the note failed to name — no rule could see, and it survived another
release until 0.1.9 read the note against the hierarchy by hand. A check finds
what it was written to find; the defect beside it waits for a reader.

`pkmv:Cluster`'s scope note named seven examples; two of them were not in the
vocabulary.

- **`ConceptCluster`** was real once. In `z/pkm-vocab.export-0.1.2.ttl` it is
  `pkm:collection10`, labelled "Concept Cluster", with the ten members
  `pkmv:ConceptCollection` carries today — it was reclassified from a Cluster
  to a Collection and the scope note was never updated. That reclassification
  is the same Cluster/Collection distinction §E defers, so the fix is evidence
  for that decision rather than a prejudgement of it.
- **`OutputCluster`** has never existed, in any release.

The same scope note omitted `pkmv:TimeCluster` — `Cluster`'s only unnamed
direct child — along with `pkmv:QuarterCluster` and `pkmv:YearCluster`. **Fixed
in 0.1.9**, which also fixed the two scope notes whose claims the hierarchy
contradicts outright: `pkmv:DayCluster` said it mirrored the week and month
clusters when it is the only one partitioned in two levels, and
`pkmv:WeekCluster` placed itself "above DayCluster and below Month" when all
three are siblings under `pkmv:TimeCluster`.

`pkmv:TimeCluster`'s scope note repeats the defect in both directions: it lists
`DecadeCluster` and `LifeCluster` as time clusters (both exist only as
`pkmv:DecadeCollection` and `pkmv:LifeCollection`) and excludes
`ConceptCluster` and `OutputCluster` by name as the non-time clusters.

Two further mentions — `pkmv:Project` "distinguish from … the Effort Cluster /
Output Cluster structures" and `pkmv:WeekIndex` "analogous to the Index hub
notes in the Effort/Output Cluster design" — are spaced rather than CamelCase
and read as design language, not term citations. Judgement call whether they
move with the rest.

### H2. A check that would have caught this — done in 0.1.8

`scripts/pkm_vocab/prose.py` ships it as `phantom-citation`, and it found all
ten of the citations in §H1 plus one more on `pkmv:Month-Health`, whose
editorial note written the same week reads as a citation of a term that does not
exist yet. Quoting the name exempts it, which is both the fix and the
convention — **a name you are recording rather than citing goes in quotes or
backticks.**

**The `z/` snapshots skipped a release, which is why the 0.1.7 file is out of
step.** `z/pkm-vocab.export-<version>.ttl` archives the previous release's
export at the *start* of the next cycle, so the file named for release N can
carry early edits from N+1 — the 0.1.7 snapshot is 8 lines into 0.1.8. No 0.1.8
snapshot was taken at all. 0.1.9 adds `z/pkm-vocab.export-0.1.8.ttl`, which is
byte-identical to the v0.1.8 tag and doubles as the import source for the
editor round-trip test. **Archive 0.1.9's export when 0.1.10 opens**, rather
than skipping again.

**Correction, made in 0.1.9.** This section said the surviving `Month-Health`
hit was that editorial note. It was not: the note had already been quoted, and
the finding was coming from an older, unquoted change note beside it — `Added
definition and scope notes to MonthHealth.` The check aggregates by token across
every literal on a concept, so the report names the concept and not the literal,
and the wrong one was assumed. **When a rule reports per subject, confirm which
literal fires before writing down which one it is.**

Two things the sketch here did not anticipate. The rule is ERROR only on
reader-facing prose and WARN in the audit trail, because a change note naming a
concept that has since gone is a record rather than a mistake — seven of those
exist. Six are correct cleanup of `Proposals`-generated duplicates; the seventh
is `pkmv:Action`'s own record of this same class of fix, "Removed ActionGroup
reference in scope note since not defined in vocabulary yet." Which is the
convention above arriving one note early: a name being recorded rather than
cited belongs in quotes. It stays a WARN either way, so it was worth
quoting the next time that note was touched rather than opening the editor for
it — which is what **0.1.9** did, to all eight at once, taking
`phantom-citation` to zero findings and `make build`'s surviving warnings from
nine to one. And the same tokenising pass gives `misspelled-word` for free,
since deciding whether `DayLog` is a term and whether `mispelling` is a word are
the same lookup.

Two more rules landed with those, covering the rest of what the editor can
get wrong without the graph noticing: `stale-duplicate-definition` (a
definition still byte-identical to the concept it was duplicated from) and
`scaffolding-local-name` (a local name ending in `Copy`, `NewConcept` or
`Untitled`) — see §D for the one it already caught.

Level: patch throughout. Prose only — no URI, label, parent or membership
moves — so by the versioning table nothing a consumer queries changes meaning.

## I. The meals shape layer's open decisions

`schema/pkm-meals.yaml` records a dozen open decisions in its `comments:`
fields, and until this section existed every one of them named **0.1.4** as its
target. 0.1.4 shipped on 2026-09-09 and none of them landed; the vocabulary is
now at 0.1.8, so the file spent four releases pointing at a date in the past.
The decisions are all still open — only the dates were wrong.

**Why they went stale where the changelog's counts did not.** Nothing in the
release pipeline reads this file. `schema/` is excluded in `_config.yml`, so it
has no page and no reader; `make artifacts` does read it, but writes to
`generated/`, which is `.gitignore`d with zero tracked files; and `schema/` was
byte-identical across 0.1.8, which is why that release skipped `make artifacts`
altogether. A file no build reads and no browser renders can be wrong for four
releases without anything noticing.

So the comments now name a **level** and point here, and this section carries
the ordering. A level is a property of the change and cannot expire; a release
number is a schedule. At `0.x` both patch and minor advance the third position,
so an additive mint below lands at 0.1.9 if it precedes §D and at 0.2.1 if it
follows — naming either number is exactly what went stale.

### I1. Concepts the shapes need and the vocabulary does not have

Sixteen, every one still absent from published 0.1.8 — checked against the
export rather than taken from the comments:

| shape site | absent concepts |
| --- | --- |
| `Recipe`'s definition names "instructions" | `Instructions` |
| `RecipeIngredient` — the use, not the food (`pkmv:Ingredient` exists) | `RecipeIngredient`, `Amount`, `UnitOfMeasure` |
| `RecipeNutrition`'s six slots — `pkmv:Nutrition` has **no** narrowerPartitive children at all | `Calories`, `Carbohydrates`, `Fat`, `Fiber`, `Protein`, `Sodium` |
| `RecipeTime`'s three slots | `PrepTime`, `CookTime`, `TotalTime` |
| `SourceKind`'s three values | `Website`, `Cookbook`, `Magazine` |

Additive throughout, so minor. Two are decisions before they are work:

- **`SourceKind` can be dropped rather than minted.** LinkML's `meaning:` slot
  wants a `pkmv:` URI per permissible value, so an un-minted enum is precisely
  the thing with nowhere to point. Free text is the alternative, and it costs
  the three concepts.
- **`UnitOfMeasure` needs a dimension tag before it is worth minting.** lb and
  oz are mass, cup is volume, can is packaging, and they do not inter-convert —
  which is why any `convert(to:)` over it has to be failable, unlike the
  single-dimension diabetes units it would otherwise resemble.

### I2. Prose the graph contradicts

- **`pkmv:Meal`'s scope note names six children and parents none of them.** It
  reads "Parent concept for the meal-planning domain (Breakfast, Lunch, Dinner,
  Snack, Recipe, DayMeal, etc.)". Its actual children are `pkmv:Food`,
  `pkmv:MealPlan` and `pkmv:Restaurant`. The four meal kinds sit under
  `pkmv:DayMeal`, `DayMeal` sits under `MealPlan`, and `Recipe` is `Meal`'s
  **sibling** under `pkmv:PKMMeals` — so none of the six it names, and it names
  none of the three it has. `phantom-citation` cannot see this, because all six
  names exist and the rule fires on names that do not. **Fixed in 0.1.9**, along
  with `pkmv:Knowledge`, which turned out to have the same defect — see §I4.
- **`pkmv:RecipeServings` is defined as a count** — "the number of servings or
  portions a recipe yields" — where the shape carries two slots, because what a
  source claims ("makes 24 cookies", "one 9-inch loaf") does not always reduce
  to a number. Either broaden that definition and add `RecipeYield` as a
  narrowerPartitive child, or keep it scalar and mint a grouping concept above
  it. Minor either way; both branches mint.
- **No `skos:related` links `Meal` and `Recipe`**, though `Recipe`'s scope note
  says it is "referenced by meals".

The first and last are one reading twice over: `Meal`'s prose claims a
relationship to `Recipe` that the graph does not assert, and says nothing about
the three concepts it does hold.

### I3. A naming policy, not a rename

The yaml asks whether `pkmv:RecipeImages` should be renamed singular to match
the `RecipeImage` class beside it. **It does not belong in §D.** §D's two URIs
are malformed — editor scaffolding in one, a stray hyphen in the other — and a
plural label is neither. Twenty-six concepts carry one, among them `Bases`,
`Day Actions`, `Day Links`, `Note Types`, `Obsidian Notes`, `Periodic Notes`,
`Recipe Servings`, `Semantic Web Standards`, `Week Analysis` and `Workspaces`.
So the real question is whether this vocabulary has a singular/plural
convention at all, and it gets answered once for twenty-six concepts or not at
all.

### I4. A fifth check — the deferral condition is met, and the answer is not the rule that was sketched

A rule reading a scope note's parenthetical list against the concept's actual
narrower set would have caught `pkmv:Meal`. Deferring it was deliberate:
designing a rule from a single example produces a rule that fits a single
example. Fix `Meal`, see whether the shape recurs, then decide.

**Measured for 0.1.9, over `like` / `such as` / `including` lists as well as
parentheticals.** Thirteen scope notes name a term that is not a direct child.
They split in two, and the split is the finding:

- **Names a descendant that is not a direct child** — `pkmv:Cluster`,
  `pkmv:Event` (twice), `pkmv:HealthEvent`, `pkmv:KnowledgeSystem`,
  `pkmv:Standard`. Naming a grandchild in a list of examples is ordinary
  writing. **A rule drawn from `Meal` alone would have errored on all six.**
- **Names something outside the subtree entirely** — seven. Two were real
  defects and 0.1.9 fixed both: `pkmv:Meal`, and `pkmv:Knowledge`, which called
  its own siblings "more specific forms" of itself. The remaining five are
  benign — `pkmv:MealPlan`'s "Day, Week" are horizons, not children;
  `pkmv:PeriodicNotes`, `pkmv:AppEvent`, `pkmv:PKMNeo4jServiceProject` and
  `pkmv:CalendarFolder` are the same shape.

So the condition for writing the rule is satisfied — there was a second example,
and a third — but **the rule cannot be "names a non-child" at ERROR**, because
`make check` gates `make build` and five benign hits would block it. It lands at
WARN, or it lands after those five are triaged. That triage is the next
measurement, not a checkbox, which is the same discipline §H2's four rules were
drawn under.

Level: I1 and the last two items of I2 are minor, since every existing URI
keeps its meaning. `pkmv:Meal`'s scope note was patch and shipped in 0.1.9. I3
and I4 are unscheduled.


## J. Where this vocabulary sits against the time vocabularies

Raised while §H was open, because the Cluster question keeps turning into a
question about periods. Nothing here is scheduled and nothing here is RDF: a
mapping triple is a new cross-vocabulary mapping, which the versioning table
calls **minor**. This section is the measurement 0.2.0 needs and cannot make
from nothing.

### J1. OWL-Time does not have a quarter

Ten individuals of `time:TemporalUnit`: `unitSecond`, `unitMinute`, `unitHour`,
`unitDay`, `unitWeek`, `unitMonth`, `unitYear`, `unitDecade`, `unitCentury` and
`unitMillenium` — spelled with one `n` in the ontology, which is worth knowing
before typing it. There is no `unitQuarter`. Membership of `TemporalUnit` is
explicitly open, so an extension may mint one; the W3C Recommendation does not.

`pkmv:Quarter` is therefore the fault line, and it is not an obscure one:
`pkm-quarter` writes quarter notes, `pkmv:QuarterCluster` carries five children,
and the concept has no counterpart in the standard this vocabulary would most
naturally align to.

### J2. There are no OWL-Time classes named Day, Week, Month or Year

The declared classes are `time:DateTimeDescription`, `time:Instant`,
`time:Interval`, `time:ProperInterval`, `time:MonthOfYear`, `time:DayOfWeek`,
`time:Duration`, `time:TRS` and the rest. Calendar granularity lives in
*properties* on `time:GeneralDateTimeDescription` (`time:day`, `time:week`,
`time:month`, `time:year`) and in the unit individuals above.

So `pkmv:Day` — a `skos:Concept` denoting the kind "calendar day" — has no class
to point at. Its nearest counterpart is `time:unitDay`, an **individual**. That
makes `skos:closeMatch` the strongest defensible predicate and rules out
`skos:exactMatch` outright.

### J3. The build already has an opinion, and it would bite silently

`transform.py` step 8 rewrites any `skos:*Match` whose object's local name
begins with a lowercase letter into `rdfs:seeAlso`, because the mapping
properties have domain and range `skos:Concept` and pointing one at a property
asserts that the property is a concept.

**Every `time:unit*` name begins lowercase.** So
`pkmv:Day skos:closeMatch time:unitDay` would be written in the editor, pass
`make check`, and arrive in the published graph as `rdfs:seeAlso` — the mapping
would not survive its own build, and nothing would say so. `time:ProperInterval`
begins uppercase and *would* survive, which is worse: it is precisely the type
error step 8 exists to prevent.

This is the same shape as the `pkmv:Book skos:relatedMatch schema:Book` problem
§E already banks, arriving from a second direction. **Decide the predicate and
the step-8 interaction before writing a triple, not after.**

### J4. What each target can express

Measured against the five places these concepts are generated or consumed.
OWL-Time and Cypher confirmed against their specifications; Swift confirmed
against `NSCalendar.h` in the local SDK, which `make swiftcheck` already
resolves.

| | Day | Week | Month | Quarter | Year | Decade |
|---|---|---|---|---|---|---|
| OWL-Time | `unitDay` | `unitWeek` | `unitMonth` | — | `unitYear` | `unitDecade` |
| Python stdlib | `date` | `isocalendar()` | `.month` | — | `.year` | — |
| Swift `Calendar.Component` | `.day` | `.weekOfYear` | `.month` | `.quarter` | `.year` | — |
| Cypher temporal | `.day` | `.week` | `.month` | `.quarter` | `.year` | — |
| Obsidian Periodic Notes | daily | weekly | monthly | quarterly | yearly | — |

Three readings:

- **Quarter is expressible in three of the five and in neither OWL-Time nor the
  Python standard library** — the two that matter most, since LinkML generates
  Python and OWL-Time is the alignment target.
- **Decade is the mirror image**: OWL-Time has it, no platform does.
  `pkmv:Decade` exists as a concept and `pkmv:DecadeCollection` has one member.
- **`pkmv:Life` is in none of them**, which is expected — it is this system's
  horizon, not a calendar unit — and is a reason not to force the whole period
  tier through one external vocabulary.

### J5. Why this belongs to §E rather than beside it

OWL-Time maps to `pkmv:Day` the period. It has nothing to say about
`pkmv:DayCluster` the bundle of notes, and no vocabulary of temporal units
ever will. That is §E's four-way question — `Day` the period, `Day Folder` the
path, `Day Cluster` the concept, `Day Collection` the flat bag — arriving from
outside the system rather than from reading it.

The useful consequence is a test §E did not have: **a term that an external time
vocabulary could map to is a period; a term it could not is a cluster.** That
cuts the four-way question cleanly in two and says nothing about the
`Cluster`/`Collection` half, which remains where §E left it.

## K. Banked as minor — additive, so not waiting for 0.2.0

At `0.x` a minor advances the third position like a patch, so none of these
needs §D to ship first. They are separated from §E because every existing URI
keeps its meaning.

- **`pkmv:Effort` does not exist.** `pkmv:EffortCluster`, `pkmv:EffortIndex`,
  `pkmv:EffortJournal`, `pkmv:EffortLog`, `pkmv:EffortPlan`,
  `pkmv:EffortReview`, `pkmv:EffortCollection` and `pkmv:EffortsFolder` all do.
  `pkmv:Topic` exists and anchors its family the way this one cannot. Found
  while writing §H's definitions, which is why `pkmv:EffortCluster` cannot say
  what its subject is the way the period clusters can.
- **ISO 25964 relations on `pkmv:EffortCluster` and `pkmv:TopicCluster`.** Alone
  among the clusters they carry only `skos:broader`/`skos:narrower`. Their five
  members each are the same shape as the period clusters' — index, journal, log,
  plan, review — so `narrowerPartitive` is the relation, and adding it is what
  lets their definitions say "unlike parts" as the other five now do.
- **`skos:related` between `pkmv:WeekCluster` and `pkmv:Week`.**
  `pkmv:DayCluster`, `pkmv:MonthCluster`, `pkmv:QuarterCluster` and
  `pkmv:YearCluster` all assert it to their period. Week is the only gap, and it
  looks like an omission rather than a decision.
- **Any OWL-Time alignment** — see §J, and §J3 before writing a triple.

## L. 0.1.10 — the vocabulary you can actually read

**Chartered, not started.** Presentation only: no triple moves, so this is a
different file set from every release so far and it cannot collide with §D.

### L1. The measured problem

`vocab/index.md` is **721 lines, 51 KB, one page**: Hierarchy 249 lines,
Collections 41, All terms 406. The A–Z section headings exist and **no A–Z
index links to them**. There are **zero** `<details>` blocks. Everything is
emitted flat by `render_vocabulary()` in `scripts/pkm_vocab/render.py`.

The consequence is an ordering problem as much as a length one: the collections
sit *after* 249 lines of hierarchy, and "All terms" — the section a first-time
reader most likely wants — is last. The front page at `index.md` does the
opposite and does it well, opening on a table of what exists with a link per
row. The vocabulary page should be shaped like its own parent.

### L2. The constraint that decides the design

**Three render targets, not one**: the Pages site (Jekyll/kramdown), the
**GitHub repo view** of the same Markdown, and **Obsidian**.

`<details>`/`<summary>` renders in all three. JavaScript renders in exactly
one. So the collapsible outline is the primary navigation because it degrades
everywhere, and search is a Pages-only enhancement layered on top — not the
other way round.

GitHub Pages also runs Jekyll in safe mode against a fixed plugin allowlist, so
a search *plugin* is not an option. A generated `search.json` plus vanilla JS
in `_layouts/default.html` needs no plugin and is.

### L3. The work

- **Collapsible hierarchy** — `<details>` per top concept, top level open.
- **A–Z index row** above "All terms"; the anchors already exist.
- **Collections before the hierarchy**, not 249 lines after it.
- **A vocabulary landing page shaped like `index.md`** — summary table, one row
  per view — with Hierarchy, Collections and All terms as linked sub-pages
  rather than one scroll. `render.py` already has `splice()` for writing
  generated blocks into hand-written pages; reuse it rather than inventing a
  second mechanism.
- **Search** — generated `search.json`, vanilla JS, Pages only.
- **Generate the Obsidian hub.** `pkm/vocab.md` in the vault is hand-written —
  `notes.py` writes the 241 stubs beside it and not the hub — and is stale:
  frontmatter `version: 0.1.3`, body "version 0.1.4", against a vocabulary at
  0.1.9, with 18 hand-copied collection counts that §E1 has just invalidated.
  It already has the shape the web page wants, leading with top concepts and
  then collections, so the fix is to generate it from the same source and
  splice the hand-written prose around it.

### L4. Why it is a release of its own

It moves no triple, so by the versioning table nothing a consumer queries
changes meaning — patch, and at `0.x` the third position is an integer, so
0.1.9 → 0.1.10. Keeping it separate also keeps the boundary that has held for
four releases: an editor pass and a tooling pass do not ride together, because
when they do it is no longer possible to say which one broke the build.

## M. A second opinion from the editor's own validator

`make validate-skos`. The vocabulary is authored in the Intentional Arrangement
SKOS Editor, and that editor ships a validator — SHACL integrity shapes plus
qSKOS-style structural checks. Running it is a second opinion on the same graph
from the tool upstream, and the overlap with `checks.py` is deliberate: what
matters is the gap.

**Five integrity conditions `checks.py` does not test:**

| | condition |
|---|---|
| **S9** | `skos:Concept` and `skos:ConceptScheme` are disjoint |
| **S13** | `prefLabel` / `altLabel` / `hiddenLabel` are pairwise disjoint |
| **S14** | at most one `skos:prefLabel` per language tag |
| **S37** | `skos:Collection` is disjoint with `Concept` and `ConceptScheme` |
| — | two concepts sharing one `prefLabel` in one language (Z39.19 6.2.1 homographs) |

All five are clean today, so this is assurance rather than a defect finder.
It is still worth having: **S37 is the condition that settles whether a term can
be both a concept and a collection** — the question §E2 answers by quoting the
SKOS Reference, when a validator answers it mechanically.

**What it is not.** The editor's REST API and MCP server are stateless —
`validate_skos`, `convert_skos`, `skos_profile`, and `/validate`, `/convert`,
over a library exposing only parse, convert and validate. There are no create,
update, delete or persist functions anywhere in them and no project store, so
**they are not an authoring surface**: validating a hand-edited export confirms
the RDF is sound without making it authoritative. `convert_skos` is also not a
round-trip test — it is rdflib parse-and-reserialize and never exercises the
editor's own `triplesToModel`, which is where import fidelity lives. The
authoring path stays what CONTRIBUTING says it is.

**Operationally.** Not wired into `all`, because it depends on a checkout this
repo does not own — the same contract `swiftcheck` has with the Command Line
Tools. `SKOS_ENGINE` is overridable and the target tests for the interpreter
before invoking it, so a machine without the editor prints a skip rather than
failing. The engine's venv is uv-managed and has no `pip`; add the SHACL
dependency with
`uv pip install --python $SKOS_ENGINE/.venv/bin/python pyshacl==0.40.1`.
Without pyshacl the structural half still runs and the report says the SHACL
half did not, rather than letting a silent skip read as a pass.

## Backlog

Folding the `pages.py` and `notes.py` extraction into one place — both define
`_first`, `_all` and `_link` with divergent signatures; `rel="alternate"`
pointing browsers at the Turtle, which needs a front-matter key out of
`pages.py` as well as a line in `_layouts/default.html`; a
`make changelog FROM=v0.1.1` graph-diff generator.

**A CI build check on version branches is the one with downside behind it, and
it is a build from scratch: there is no `.github/workflows/` directory at all.**
Merging to `main` publishes to w3id.org with no staging step, so nothing today
runs `make check` between a branch and the live namespace except a human
remembering to.

Two vault items, both measured for 0.1.9 and both larger than recorded:

- Not two stale `navigationHiddenItems` entries but **twelve of seventeen**,
  and six of seventeen in `navigationOrdering`. Six are pre-`z/` (five
  `Calendar/Notes/…` files plus the `Calendar` entry), four moved under `+/`,
  one to `Efforts/Works`, one deleted. Every one is now **redundant** rather
  than merely stale: `z`, `+`, `Atlas`, `Calendar` and `Efforts` are all in the
  publish `excluded` list, so hiding them from navigation does nothing. This is
  server-side site configuration, not a file in this repo.
- Publish exclusion still does not retract, so **98** notes stay live until
  unpublished by hand — Atlas 37, `+` 31, Efforts 30, against 344 live files of
  which 246 belong there. Not "roughly 103"; the count is exact and comes from
  the published cache.
