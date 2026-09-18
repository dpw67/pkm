# Roadmap

What is done, what is next, and which version level each item lands in.

Status is the first thing in this file on purpose: the question it has to answer
is "what changed since I last read it", and that is a `git log ROADMAP.md` away.
Section letters are stable, so a diff shows state changes rather than a reflow.

Version levels come from [Versioning](CHANGELOG.md#versioning) and describe
impact on consumers, not volume of work. At `0.x` patch and minor both advance
the third position; only major advances the second. **They are impact levels,
not SemVer position names** — by position `0.2.0` is a minor bump — so read a
"major" below in terms of what it does to a consumer, not which digit moves.

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
| 14 | 0.1.9 — released: Cluster says what the graph says, collections say what decides membership | done — §H, §E1 |
| 15 | The meals shape layer's open decisions | recorded — §I |
| 16 | Where this vocabulary sits against OWL-Time and the platform types | recorded — §J |
| 17 | What the eighteen collections actually are | measured — §E1 |
| 18 | 0.1.10 — released: four pages, a collapsible tree, search, a generated hub | done — §L |
| 19 | Upstream validation as a second opinion | done — §M |
| 20 | SKOS Editor fixed #77/#78/#81 — 74 literals repaired at source | confirmed — §N |
| 21 | Turtle round-trips losslessly; who owns the vocabulary is open | recorded — §O |
| 22 | A second PKM tool read the vocabulary; four primitives missing, four parents wrong | measured — §P |
| 23 | The hierarchy before 0.2.0 restructures it — 33% of links undifferentiated | measured — §Q |
| 24 | 0.1.11 — the hierarchy drawn, one chunk per top concept | done — §R |

### Where 0.1.9 left the graph

`make check` on the export: **4387 triples**, 223 concepts, 18 collections, 236
hierarchy links, 318 ISO 25964 links, 8 top concepts. **0 error, 1 warn.**

**The repaired export has landed**, so this paragraph is no longer a
prediction. Two of the three warnings were upstream residue:
`doubled-attribution` (39) and `lang-tag-in-text` (35), SKOS Editor artifacts
that `transform.py` repaired on the way out so the published graph was clean
either way. Both are now fixed at the source — see §N — and the count has duly
fallen from three to **1 warn**. That one is `scaffolding-local-name` on
`pkmv:TemplateCopy`, which the transform cannot repair because the fix is a
rename. See §D, and do not silence it.

The triple count rose 4377 → 4387 with that same export. Recorded because this
section exists to answer "what changed since I last read it", and a count that
silently moves is the drift it is meant to catch.

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

  Worth keeping the total honest while here: `transform.py` repaired **95**
  literals on every build, not the 94 once claimed, and only 21 of them
  silently. The other 74 were exactly the two WARN groups `make check` printed —
  35 `lang-tag-in-text` and 39 `doubled-attribution` — so "silently repaired"
  overstated the invisible part more than fourfold.

  **As of §N the 74 are fixed upstream, so the number is 21 and all of them are
  the invisible kind** — which is the measurement finally agreeing with the
  story this section tells.

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
  together. Additive, so minor on its own. **A reader using a different tool
  independently found the same gap and four more** — see §P.
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

**`DecadeCollection` has a prior question that has to be answered first: which
ten years?** A *calendar* decade is 2020–2029 — the "2020s". A *life* decade is
ten years from a birthday: for someone born 15 March 1945, the ninth decade
runs 15 March 2025 to 14 March 2035. They are different spans, they partition
time differently, and nothing in the vocabulary says which `pkmv:Decade` means.
Raised while rewriting the collection descriptions in 0.1.9 and recorded here
rather than in the note, because a published description should state a
membership rule rather than ask a question — and because this is where the
answer changes something, since it decides what `DecadeCollection` could ever
hold.

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
- **`Tag`, `Object`, `Property`, `Relationship`** — none exists, and all four
  are primitives of a PKM tool that is not Obsidian. `Tag` is the sharpest: it
  is fundamental to Obsidian *and* to Capacities, this project models tags
  nowhere, and the only trace of one is `pkmv:tag` — lowercase, abandoned in
  `z/pkmv_tag.ttl` and never published. See §P for where the four came from.
  Mint `Collection` with them or the set is half-done; §E says why `Collection`
  waits for `Cluster`.
- **The interface kinds PKM Services exposes.** None of `API`, `REST`,
  `GraphQL`, `Apollo`, `MCP`, `Server`, `Protocol`, `Endpoint` or `Command`
  exists, while `FastAPI`, `Hummingbird`, `Cypher` and `Script` all do — **the
  implementations are named and the kinds they implement are not**, which is
  the same shape of gap §P found from Capacities and §Q4 found in the general
  tier. `MCP` survives nowhere except inside the Obsidian plugin label `Local
  REST API with MCP`, so the service layer's MCP tools have no term and neither
  do its REST endpoints. Raised 2026-09-17, when Doug added GraphQL to PKM
  Services beside its REST APIs, MCP tools, Python scripts and commands; see
  §Q6 for where PKM Services sits in the implementation tier.

  **Three literals already name FastAPI as though it were the category**, and
  GraphQL narrows or falsifies all three: `pkmv:PKMPythonAPI`'s definition
  ("Python FastAPI routes providing an API for PKM services.") and its scope
  note ("Includes FastAPI routes for Python services, classes, and
  functions."), plus `pkmv:PKMPythonServices`'s scope note ("Includes FastAPI
  routes, services, classes, functions, scripts, commands, and agents."). Prose
  only, so **patch** — separable from the mints and shippable before them. This
  is the drift `make review` is built to surface, and the sheet is stale.

  `FastAPI → pkmv:PKMPythonAPI` is also one of §Q1's bare 77, and it is an
  `instantial` case by ISO 25964's own definition — a named individual under
  the class it implements. That is the qualifier asserted **zero** times
  anywhere, so this tier and §Q1's missing third are one piece of work.

  **All of it is minor.** Minting the kinds is additive; adding them to the
  `TechStack` collection is additive too — §E's "every membership change is
  major" is about *dropping* a member, not adding one. So the interface tier can
  land in a minor release without waiting for §D to force 0.2.0, the same
  conclusion §Q1 reached for the bare links. (§E also notes `TechStack` is a
  hand-copy of the `Tool` subtree missing six, which this would add to rather
  than fix.)
- **Any OWL-Time alignment** — see §J, and §J3 before writing a triple.

## L. 0.1.10 — the vocabulary you can actually read

**Shipped.** Presentation only: no triple moved, which the build proves rather
than asserts — `vocab/pkm-vocab.ttl` and all 241 per-term files are
byte-identical across the change. The version literal came from the editor,
which cost a round-trip worth recording — see §L6.

### L1. The measured problem

`vocab/index.md` was **721 lines, 51 KB, one page**: Hierarchy 249 lines,
Collections 41, All terms 406. The A–Z section headings existed and **no A–Z
index linked to them**. There were **zero** `<details>` blocks. Everything was
emitted flat by `render_vocabulary()` in `scripts/pkm_vocab/render.py`.

The consequence was an ordering problem as much as a length one: the collections
sat *after* 249 lines of hierarchy, and "All terms" — the section a first-time
reader most likely wants — was last. The front page at `index.md` does the
opposite and does it well, opening on a table of what exists with a link per
row. The vocabulary page is now shaped like its own parent.

### L2. The constraint that decided the design

**Three render targets, not one**: the Pages site (Jekyll/kramdown), the
**GitHub repo view** of the same Markdown, and **Obsidian**.

`<details>`/`<summary>` renders in all three. JavaScript renders in exactly
one. So the collapsible outline is the primary navigation because it degrades
everywhere, and search is a Pages-only enhancement layered on top — not the
other way round.

GitHub Pages also runs Jekyll in safe mode against a fixed plugin allowlist, so
a search *plugin* was not an option. A generated `search.json` plus vanilla JS
in `_layouts/default.html` needs no plugin and is.

### L3. What shipped

- **Four pages, not one.** `vocab/index.md` is **39 lines**: a summary table
  with a row per view, then Download. The three views are sub-pages under
  `vocab/browse/` — `hierarchy.md`, `collections.md`, `all.md` — each with
  hand-written prose around a spliced block, the same arrangement the landing
  page already used.
- **`browse/` rather than `/vocab/hierarchy/`.** Term URIs are
  `/vocab/{Term}`, so a flat sub-page would permanently reserve a plausible
  term local name *and* sit in the slot an RDF client expects a term in. One
  reserved name instead of three, and it reads as navigation.
  `pages.RESERVED` grew by one entry, which is what keeps the build refusing a
  term that would overwrite a published page.
- **Collapsible hierarchy.** One `<details markdown="1">` per top concept,
  closed, the eight summaries as the open top level — expanding all eight puts
  the 249 lines back. Each summary carries its descendant count, and those
  eight counts sum to 236, which is the `skos:broader` link count `make check`
  reports.
- **A–Z index row** above All terms, emitting only the initials that exist, so
  no link is a dead end. The anchors were already there.
- **Collections on their own page**, no longer 249 lines down.
- **Search.** `vocab/search.json`, 241 entries, 38 KB, written by
  `render_search_index()`; vanilla JS in `_layouts/default.html` behind a
  `search: true` front-matter flag, so a page outside the vocabulary does not
  offer a box that searches only the vocabulary. Fetched on first use rather
  than on load, because most visits to a term page never search. The box is
  rendered `hidden` and unhidden by the script, so a reader without JavaScript
  is never shown an input that cannot do anything. Ranking is exact label,
  then label prefix, then label substring, then altLabel, then definition.
- **The Obsidian hub is generated.** `pkm/vocab.md` in the vault was
  hand-written and two releases stale in two places — frontmatter
  `version: 0.1.3`, body "version 0.1.4". `make hub` now fills three named
  blocks in it: `summary` (counts, version, modified date, licence read from
  `dcterms:license`), `tops`, and `collections`. Its prose is left alone, which
  is the seam: the facts are generated, the explanation is not.
  **The 18 hand-copied member counts turned out to be correct** — §E1
  invalidated the descriptions, not the arithmetic — so the staleness this
  fixed was the version, and what it prevents is the next membership edit.

### L4. Three things worth knowing about the implementation

- **`splice()` grew named blocks.** `<!-- pkm:begin generated: summary -->`.
  The hub needs two regions with hand-written prose between them, which one
  unnamed block per file cannot express. The unnamed form is unchanged, so
  `vocab/index.md`, `resources/index.md` and `agents/index.md` were untouched
  by the change. It also split into a pure `spliced()` plus the file I/O, so
  the hub composes three blocks and writes once.
- **`make hub` refuses rather than appends.** A generated block appended to the
  end of a hand-written page is in the wrong place and silently so, so a
  missing marker pair is an error that prints the markers to paste. The markers
  were positioned once, by hand; after that the target only ever fills them.
- **`make site` was counting `_site/vocab/*/` and expecting exactly one
  directory per term page.** `browse/` made that 242 against 241, so the check
  failed on a correct build until its grep excluded `browse/` alongside
  `terms/`. Worth recording because the check is the only thing that verifies
  the term permalinks still resolve, and a check that fails for the wrong
  reason gets disabled.

### L5. Why it is a release of its own

It moves no triple, so by the versioning table nothing a consumer queries
changes meaning — patch, and at `0.x` the third position is an integer, so
0.1.9 → 0.1.10. Keeping it separate also keeps the boundary that has held for
four releases: an editor pass and a tooling pass do not ride together, because
when they do it is no longer possible to say which one broke the build.

### L6. The version literal, and the export that reverted a release

`owl:versionInfo` lives **only** in the SKOS Editor export — `transform.py`
merely reads it to derive `owl:versionIRI` — so a release that moves no triple
still needs a round-trip through the editor for that one literal. Worth planning
into a presentation release rather than discovering at tagging time.

**The first re-export reverted 0.1.9 outright.** The editor held two projects:
the stale one, and the copy import restores *beside* an existing project rather
than overwriting it — the conflict path §O describes. Exporting from the wrong
one produced 4387 → 4359 triples with **33 prose literals reverted**: the 7
Cluster definitions, 11 scope notes and 15 collection descriptions §H and §E1
had just written, plus 13 net change notes including 0.1.9's own dated history.
`pkmv:WeekCluster` was back to "The *set* of structured notes … aggregating and
analyzing its constituent Day Clusters" — the pre-0.1.9 sentence, with the
clause the graph does not assert.

**Nothing in the build noticed.** The export parsed, `make check` reported 0
error, `make validate` passed 247/247, and the pages rendered. It was caught by
running `scripts/compare_exports.py` against the committed export by hand, which
is the only reason this section is not a post-mortem. §L7 wires that in.

The export from the correct project is clean: 4387 → 4387 triples, **one subject
touched** — the scheme — and `modified` plus `versionInfo` the only properties,
with zero `definition`/`scopeNote`/`note` differences anywhere in the graph.

**The divergence was between two editor projects, not between the editor and
the repo.** The stale project's contents match `z/pkm-vocab.export-0.1.8.ttl`
plus the 74 change-note repairs exactly — identical triple count, zero
definition, scope note or note differences — which is what the §N round-trip
test produced when it imported the 0.1.8 export as a new project to prove import
fidelity. That test project was still there, and it is the one that got picked.
Import leaving existing projects untouched is the feature §O praises; a test
import left lying around beside the real work is the bill for it.

So 0.1.9's prose was never missing from the editor. `733dd9e` landed it from
there — *"the export is the SKOS Editor's own output, and all 41 worklist
literals are byte-identical to the spec the hand-edited branch had become"* —
and `z/pkm-vocab.export-0.1.9.ttl` matching the committed export byte for byte
is explained by that commit archiving it at release time rather than at the
start of 0.1.10, deliberately, as the same message says.

What this does settle is the acceptance test for a future editor session: **no
`definition`, `scopeNote` or `note` line in `compare_exports.py` output unless
the release is about prose** — and, before exporting, check which project is
open. A stale project is indistinguishable from a current one until its prose is
compared.

**Correction.** The commit that landed this release, `a799d3b`, says 0.1.9 "was
applied by editing the export directly" and offers the archive's byte-identity
as proof. Both are wrong, for the reasons above: the byte-identity has an
innocent explanation and `733dd9e` is the record of the editor pass. The error
is left in the commit message, which cannot be corrected without rewriting the
branch, and is corrected here instead.

### L7. The check that would have caught it

`compare_exports.py` existed and was wired into nothing — §O1 lists it as
machinery that arrived incidentally. `make build` now runs it against the export
committed at `HEAD` before writing anything, and prints the prose delta and
triple count: loud when definitions, scope notes or notes move, silent when they
do not. It degrades rather than fails when git or the blob is unavailable, so a
build from a tarball still works.

This is the same move as §D4 and §H2 — the defect is cheap to fix once and
expensive to find twice.

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

## N. The editor fixed the two artifact classes at the source

Found by testing whether the editor could reload this project's own export —
not by looking for it, which is the only reason it was found at all.

Importing `z/pkm-vocab.export-0.1.8.ttl` into the editor at `dce18c0` and
re-exporting rewrote **74 change notes across 57 subjects**: 35 carrying a
language tag inside a quoted label, 39 naming the proposer twice. Exactly the
two classes `transform.py` has repaired on every build since 0.1.6, and exactly
the two `make check` reported as WARN. Nothing else moved — 4359 triples in and
out, 241 URIs with none minted or lost, 236 broader pairs identical, 318 ISO
25964 triples, no collection membership changed.

| upstream | defect | state |
|---|---|---|
| [#77](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/77) | language tag inside a quoted label — `“AppIntent@en”` | **fixed** |
| [#78](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/78) | doubled attribution — `(proposed by X) (by X)` | **fixed** |
| [#81](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/81) | the migration walked only stored history, not imported notes | **fixed** |

**#81 is the one that matters here**, because it is why this file recorded the
other two as permanent. The editor's own source comment explains it: the
earlier migration "only walked history, so notes present at a user's last
import kept their `@en` and doubled names — hence the apparent 'date cutoff'."
This vocabulary is entirely imported notes, so it saw none of the fix.

**The fix arrives without an import.** `repairNoteText()` and
`migrateHistoryNotes()` are called from `boot()` and followed by `save()`, so
any project repairs itself when it is opened. That is stronger than the
migration this project asked for in the #77 draft.

### N1. What it changes here

- **`make check` falls from 3 warn to 1** once 0.1.9's export lands, leaving
  only `scaffolding-local-name` — see §D.
- **`transform.py` step 7 becomes a no-op.** `DOUBLED_ATTRIBUTION` and
  `LANG_IN_TEXT` will match nothing. **Leave the code**: it costs one pass over
  the literals and defends against an export from an older editor or another
  machine. But it is belt-and-braces now, not load-bearing, and §C1's count
  drops from 95 repaired literals to 21.
- **74 repaired literals ride in 0.1.9** whether or not anything else changes,
  because the migration runs on load. They are upstream's work, not this
  project's, and the changelog says so.
- The two checks stay. A rule that finds nothing because the defect was fixed
  is a rule doing its job, and neither costs anything to keep.

**Confirmed on the real export.** 0.1.9's export from the editor carries the 74
repairs exactly as the round-trip predicted, and `make check` fell from three
warnings to one — the survivor being `scaffolding-local-name`, which waits for
§D. The prediction was made from a test import and held against a session that
also changed 41 literals, which is the stronger result.

### N2. The editor does not log collection edits

Measured on the same export, and the counterpart to the good news above.
0.1.9 rewrote prose on **26 terms — 11 concepts and 15 collections**. The
editor wrote a dated change note for **every one of the eleven concepts and
none of the fifteen collections**.

The sharper version of that, measured across the same export: collections
carrying `dcterms:modified` went from 3 of 18 to **18 of 18**, while
collections carrying `skos:changeNote` stayed at **0 of 18**. The editor knows
the collection was edited — it stamps the date — and records nothing about
what changed. So the changelog is the only account of why fifteen descriptions
moved.

This is the same second-class treatment as upstream
[#58](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/58),
which was about collections exporting with `rdfs:label` and `skos:note` where
concepts get `skos:prefLabel` and `skos:definition`. That one is closed; the
edit history was not part of it.

**Filed as [#84](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/84)
and fixed the same day** — nineteen minutes, closed `COMPLETED`. Editing a
collection now seeds a history entry for every kind of edit (name
add/change/remove, note add/update/remove, toggling ordered, adding or
removing a member), exports each as `skos:changeNote` at parity with concept
history, and round-trips imported collection change notes through a new
`changeNote` array so re-opening an exported file keeps the trail. Jessica
drew the same line to #58 unprompted: "same second-class treatment, one layer
over." **Collections now match concepts on all three axes** — labels and
definitions (#58), Dublin Core dates, and edit history.

**Expect new output in the next export, and do not read it as a defect.**
Collections will begin carrying `skos:changeNote`. The lesson from the 74
repaired notes in §N is that unexplained new content in an export looks like
damage until it is traced; this one is written down in advance.

**0.1.9's fifteen collection rewrites cannot be recovered, and should not be
re-entered.** They happened before the fix, so no history was seeded, and
re-editing them now would date notes today for edits made on the 14th — a
worse record than none. The changelog stays the account of why those
descriptions moved.

## O. Turtle as interchange, and who owns the vocabulary

The round-trip test in §N was run to answer a small question — can the editor
reload this project's own export — and answered a larger one. Worth recording
now because **PKM Studio** and the SKOS backend taking shape in
`pkm-neo4j-service` (`app/services/ontology/pkm/concepts/`, `mcp/`) would each
become another writer on the same vocabulary.

**What it proved.** A Turtle export goes into the SKOS Editor and comes back
with 241 URIs intact, 236 broader pairs identical, 318 ISO 25964 relations
preserved and no membership moved — and 74 literals repaired on the way. So
Turtle is a viable interchange format between tools, which is the precondition
the whole plan rests on. Import is a first-class feature of the editor, not a
side effect, and its "new project" path leaves existing projects untouched.

**What it did not prove, and 0.1.9 is the case study.** Interchange is not the
same as multiple sources of truth. This release went wrong precisely because
two copies existed — the editor's in browser localStorage and the repo's in
`vocab/src/` — and the wrong one was edited. Nothing detected it. The export
parsed, `make check` passed, the generated pages rendered, and the divergence
was only found by reading `CONTRIBUTING.md` and asking. A third and fourth
writer multiply that failure rather than change its shape.

### O1. What a multi-writer setup needs

| need | state today |
|---|---|
| a staleness signal per resource | `dcterms:modified` on every concept and, since 0.1.9, **18 of 18** collections |
| a diff that ignores serialization order | `scripts/compare_exports.py` |
| an independent validator | `make validate-skos` — §M |
| **a declared owner per artifact** | **missing. This is the open question.** |

The first three arrived incidentally while fixing something else, which is
worth noticing: most of the machinery a second writer needs already exists. The
fourth is not machinery at all, it is a decision.

### O2. The sentence that has to change

`CONTRIBUTING.md` states that the vocabulary is authored in the Intentional
Arrangement SKOS Editor, exported to `vocab/src/pkm-vocab.export.ttl`, and
built from there. **That sentence becomes false the day PKM Studio writes a
term**, and it is exactly the rule this release spent four commits re-learning
after ignoring it.

So it cannot be allowed to lapse quietly. Either it is restated — one tool
authors, the others read — or it is replaced with something that says how two
writers reconcile. The editor's own answer is worth knowing and is not a model
to copy: its workspace restore keeps a per-project `updated` timestamp and
resolves conflicts by refusing to overwrite, restoring the incoming copy
*beside* the existing one as "(restored)". Safe, and it leaves a human to
merge.

The honest default until there is something better: **one tool owns authoring
and the rest read.** A vocabulary with 241 URIs and no merge story is not the
place to discover that two editors disagree.

## P. How much of this is Obsidian's vocabulary, not PKM's

**Measured 2026-09-17.** Chris, an LYT community manager, highlighted this
project in the community newsletter and asked the readership "Do you have a PKM
vocabulary?" — while using **Capacities** rather than Obsidian. Recorded here
for the same reason §E records the fifty-three suggested alternatives to
"Cluster": a reader outside this vault tried to read the vocabulary, and what
they could not find is data.

Capacities models objects, templates, collections, tags, properties and
relationships. Checked against the published graph:

| their primitive | here |
|---|---|
| Template | present — but the generic one is `pkmv:TemplateCopy`, the mislabeled URI §D has to rename |
| Object | **no concept** |
| Collection | **no concept**, while 18 `skos:Collection` instances exist — §E already had this one |
| Tag | **no concept**; only `pkmv:tag`, lowercase, abandoned in `z/` and never published |
| Property | **no concept** |
| Relationship | **no concept** |

Banked in §K, because all four are additive.

### P1. "Collection" already means two things

Worth stating outright, since the newsletter framed this as the power of names.
Here a collection is a `skos:Collection`: a grouping that carries **no**
hierarchical meaning, which is the first thing every collection page says. In
Capacities a collection does organisational work. Same word, opposite claim
about whether membership implies structure — and §E1 has already measured that
six of the eighteen here are redundant mirrors of a subtree anyway.

This is not a rename. It is a reason the `Collection` definition §E is waiting
on has to say what a collection is *not*.

### P2. Four parents say a note type is a kind of folder

Found while measuring the above. Every concept whose parent is a folder or the
vault, by relation:

| relation | count | reading |
|---|---|---|
| `broaderPartitive` | 20 | "is part of" — fine, and the whole/part reading §E calls pervasive |
| plain `skos:broader` | 8 | unqualified |
| **`broaderGeneric`** | **4** | **"is a kind of" — wrong** |

The four are `pkmv:Action`, `pkmv:Area`, `pkmv:Interest` and `pkmv:Project`, all
`broaderGeneric pkmv:EffortsFolder`. That asserts a project is a *kind of*
folder. The twenty partitive ones next to them assert the defensible thing —
that a note of this type *lives in* that folder — so the fix is the qualifier,
not the parent, and the four are the odd ones out rather than the pattern.

`pkmv:Note broader pkmv:ObsidianNotes` is the other direction of the same
confusion: the general term sits under the tool-specific one, so the vocabulary
says a note is a kind of Obsidian note. It is one of the eight unqualified
links above.

Not patch. Both leave `skos:broader` intact, so a query on `skos:broader`
returns the same rows — but a query on `isothes:broaderGeneric` returns fewer,
and the versioning table calls that major. Do them with §D.

### P3. The vocabulary is more portable than its shape suggests

`pkmv:ObsidianNotes` is the largest of the eight top-concept subtrees: **109
concepts including itself**. That number invites the conclusion that half the
vocabulary is tool-specific, and it is wrong. The eight subtrees sum to 284
against 223 concepts, so they overlap heavily through the polyhierarchy:

- **50 concepts (22%)** are reachable *only* from `pkmv:ObsidianNotes`
- **59 of the 109** are also under another top concept
- **0** concepts sit under no top concept at all

And the exclusive 50 are not all Obsidian either. Genuinely tool-specific:
`Dataview`, `Templater`, `Excalidraw`, `QuickAdd`, `Bases`, `Canvas`, `Publish`,
`Sync`, `Workspaces`, `Vault`, `ObsidianPlugin`, `ObsidianSettings`, the six ACE
folders. Tool-neutral but merely *filed* there: `Day`, `Week`, `Month`,
`Quarter`, `Year`, `Decade`, `Time`, `Life`, `Note`, `Idea`, `Draft`, `Area`,
`Project`, `Interest`, `Focus`, `Health`, `Finance`, `Map`, `Calendar`.

So the honest answer to "do you have a PKM vocabulary?" is yes, with about a
fifth of it describing one tool — and the awkwardness a second tool's user hits
is §P2, not the size of the Obsidian subtree.

## Q. The hierarchy as it stands, before 0.2.0 restructures it

**Measured 2026-09-17, at 0.1.10.** Doug is reworking the hierarchy for 0.2.0 —
top concepts, some labels, many relationships — through iterated Excalidraw
drawings, and named the defects before any of this was counted: generic,
whole-part and instance relations blended without differentiation; PKM and Notes
intertwined with Obsidian; and no split between the generic PKM vocabulary and
his own implementation.

**This section is the before-picture and nothing else.** It proposes no
hierarchy. The drawing is still moving, and a roadmap that picked a shape now
would fix a direction that is not settled. What it does is put numbers on the
current state, so that when the restructuring lands the improvement is
measurable rather than asserted.

### Q1. A third of the hierarchy does not say what kind of link it is

| | count | share |
|---|---:|---:|
| `skos:broader` pairs | 236 | |
| carrying an ISO 25964 qualifier | 159 | 67% |
| **bare — no qualifier at all** | **77** | **33%** |

By kind: **partitive 103, generic 56, instantial 0.** No pair carries two
qualifiers, so the 33% is absence rather than contradiction — nothing has to be
un-decided first.

**`isothes:broaderInstantial` is used zero times**, and ISO 25964 reserves it
for exactly what several of the bare groups look like: a named individual under
the class it instantiates, rather than a narrower class. The bare 77 by parent,
largest first:

| parent | bare children | |
|---|---:|---|
| `ObsidianPlugin` | 13 | Advanced URI, Bases, Book Search, Canvas, Dataview, Excalidraw, Local REST API with MCP, Periodic Notes, Publish, QuickAdd, Sync, Templater, Workspaces |
| `PKMPython` | 7 | including `Python` itself and `PythonTemplate` |
| `ObsidianNotes` | 6 | `Base`, `Map`, `Note`, `ObsidianPlugin`, `ObsidianTemplate`, `View` |
| `EffortCluster` | 5 | Index, Journal, Log, Plan, Review |
| `TopicCluster` | 5 | Index, Journal, Log, Plan, Review |
| `Source` | 5 | Book, Clipping, Movie, Person, Quote |
| `ClaudeAI` | 3 | Claude Chat, Claude Cowork, Claude Desktop |
| `HealthData` | 3 | Apple Health, Dexcom Data, Glooko Data |
| `GraphDatabase` | 3 | Cypher, Neo4j, Neo4j Desktop |
| `Area` | 3 | Finance, Health, Life |
| `Ideaverse` | 3 | ACE Organization, ARC Ideation, Idea Emergence |
| `KnowledgeSystem` | 3 | Knowledge, Knowledge Graph, Term |
| 15 more parents | 18 | 1–2 children each |

**Ten of the 77 are already banked.** §K records that `pkmv:EffortCluster` and
`pkmv:TopicCluster` are alone among the clusters in carrying no ISO relations,
and that their five parts each are the same shape as the period clusters' — so
those two rows are a decision already taken and not yet applied.

`Calendar → Day` is also in this list, and §E already flags `Day`'s parents as
reparenting work. Which qualifier each of the remaining links should take is the
restructuring's call, not this section's.

**Most of this does not need 0.2.0.** Qualifying a bare link is *additive*:
every ISO 25964 link asserts both `skos:broader` and the sub-property, so a
bare link that gains one keeps the `skos:broader` it already had and no query
comes back shorter. By [Versioning](CHANGELOG.md#versioning) that is **minor**,
and at `0.x` minor advances the third position — so **all 77 could ship as
0.1.11**, before §D forces 0.2.0 at all.

The exceptions are the four in §P2, which *change* a qualifier rather than add
one and are therefore major, and any link where qualifying turns out to expose
the wrong parent — that is a reparent, and major. A versioning fact about the
links as measured, not a proposal about which qualifier any of them takes.

### Q2. 68 concepts sit under more than one top concept

| top concept | subtree | exclusive | shared |
|---|---:|---:|---:|
| Knowledge System Architecture | 92 | 35 | 57 |
| Obsidian Notes | 109 | 50 | 59 |
| PKM Swift | 49 | 46 | 3 |
| Tool | 16 | 5 | 11 |
| PKM Python | 11 | 7 | 4 |
| Graph Database | 7 | 4 | 3 |
| Claude AI | 4 | 4 | 0 |
| Health Data | 4 | 4 | 0 |

**68 of 223 concepts (30%)** are reachable from more than one of the eight.
Polyhierarchy is legitimate in SKOS and §L3 already handles it in the rendered
tree, so the number is not a defect by itself — it is the measure of how much
the eight top concepts overlap, which is what a re-rooting has to resolve.

### Q3. The implementation blend, in one figure

**56 concepts sit under both `pkmv:KnowledgeSystemArchitecture` and
`pkmv:ObsidianNotes`** — simultaneously part of the architecture and a kind of
Obsidian note. That is 61% of the KSA subtree and 51% of the Obsidian one.

The overlap is the Day Cluster family end to end: `DayActions`, `DayAnalysis`,
`DayBase`, `DayBoard`, `DayCanvas`, `DayCluster` and its four parts,
`DayDiabetes`, `DayDiagram`, `DayDrawing`, `DayHealth`, `DayIndex`,
`DayJournal`, `DayLinks`, `DayLog`, `DayMealPlan`, `DayMeeting`, `DayMindmap`,
`DayPlan`, `DayReview` and the rest.

This is the single number for "the implementation is not split from the generic
vocabulary", and it is the one to watch across 0.2.0.

### Q4. The generic tier does not exist yet

None of these is a concept: **`Knowledge Management`, `PKM System`,
`Technology`, `PKM Apps`, `PKM Services`, `PKM Diabetes`** — nor `Folder`,
`File` or `Object`. `Knowledge System` does exist, under
`KnowledgeSystemArchitecture`.

So the tier is nine new mints, not a rename of anything. Minting is **additive,
therefore minor**, which means the generic tier can land without waiting for §D
to force 0.2.0 — the reparenting underneath it cannot. §E says the same of
`Collection`, and §K banks `Tag`, `Object`, `Property` and `Relationship` from
§P's cross-check; `Object` appears in both lists and is one concept.

### Q5. What a folderless tool cannot take

Eleven concepts are file-system artifacts: `Vault`, the six `*Folder`s, plus
`Note`, `Base`, `Canvas` and `View`. §P2 counted a further 28 concepts whose
parent is a folder or the vault, 20 of them partitive — "lives in".

Capacities has **no folders and no files, only objects**, which is what makes
this the implementation boundary rather than a portability nuance: in a
folderless model those 11 have no counterpart and the 28 lose their parent. See
§P for where that cross-check came from.

### Q6. The shape Doug is aiming at

**Stated by Doug, 2026-09-17**, after iterating Excalidraw drawings and reading
the generated map. Recorded because it was said and is written down nowhere
else — the same treatment §E gives the fifty-three reader-suggested
alternatives to "Cluster". **Not a commitment, and not my design.** Q1–Q5 are
the before-picture this will be diffed against.

His reading of the current top concepts: *"they're mostly NOT top Concepts, but
focused on Technology"* — which measures out. Five of the eight are technology
of one sort or another:

| current top concept | what it actually is |
|---|---|
| Claude AI | technology — one vendor's products |
| Graph Database | technology |
| PKM Python | technology — his own code |
| PKM Swift | technology — his own code |
| Tool | technology — the category itself |
| Obsidian Notes | one specific tool |
| Knowledge System Architecture | his own architecture |
| Health Data | data |

And **`Technology` is not a concept at all**, so the thing five of the eight are
instances or parts of is the one term missing. `Capacities` does not exist
either, checked here for the first time — §Q4 tested the other nine names.

The tier he describes separates three kinds of thing that the graph currently
mixes:

| kind | terms |
|---|---|
| **General** | Knowledge Management, PKM System, Technology |
| **His implementation** | Knowledge System Architecture, PKM Apps, PKM Services, PKM Diabetes |
| **Tool instances** | Obsidian Notes, Capacities |

*"There's so much intermingling under Obsidian Notes that should be separated"*
— §Q3 is that intermingling measured: 56 concepts sit under both
`KnowledgeSystemArchitecture` and `ObsidianNotes`, which is 61% of the one and
51% of the other. *"And then there's all the stuff about my PKM Apps, PKM
Services, and PKM Diabetes that's not generic"* — the general/specific split
§Q4 priced at nine new mints.

Two things this shape implies that are worth noticing early. **Capacities as a
second tool instance is what makes the tier testable**: a tier that only ever
holds Obsidian cannot be shown to separate the tool from the practice, which is
why §P's cross-check found what it found. And **`instantial` is the relation
this tier needs** — Obsidian and Capacities are named individuals under a class,
not narrower classes of it — which is the qualifier §Q1 found asserted exactly
zero times.

## R. 0.1.11 — the hierarchy drawn

**Released 2026-09-17.** Presentation only: no triple moved, and the bulk Turtle
plus all 241 per-term files were byte-identical to 0.1.10 until the version
literal landed, which changed the three scheme triples and nothing else.

`z/pkm-vocab.export-0.1.10.ttl` was archived correctly on the way in —
byte-identical to both the pre-bump export and the `v0.1.10` tag, which is the
release-time snapshot §N asks for and did not get for 0.1.8. The release sequence that
produced it is now written down in [CONTRIBUTING](CONTRIBUTING.md#releasing),
because it had existed only as scattered lessons here.

The vocabulary had no diagram anywhere — not an SVG, not a PNG, not a line of
Mermaid. 0.1.10 made it readable as text; nothing made it visible as a shape,
which is the gap the 0.2.0 design work kept running into. There is now one
diagram per top concept at `/vocab/browse/map/`.

### R1. Generated, because drawings of this graph drift

Every hand-maintained second representation here has drifted from the graph it
describes: §E1's five of six subtree-mirroring collections, the Obsidian hub's
version and counts before `make hub`, and `reports/vocab-review.md` whenever it
is not re-run.

The distinction that matters, and the reason the Excalidraw work is unaffected:
**a drawing of a target cannot drift, because it proposes a graph rather than
describing one.** A published drawing of what exists can. So the design drawings
stay hand-made and the map is derived on every build.

### R2. The dotted arrows are the point

A grey labelled arrow carries its ISO 25964 word — `generic`, `partitive`,
`instantial`. **An amber arrow marked `?` has no qualifier at all.** §Q1
measured that as 77 of 236 links, and the map is where that third stops being a
number: the `Claude AI` chunk, for instance, is entirely unqualified, and so is
`PKM Python` at 10 of 10, while all twelve of `Tool`'s are qualified.

**Correction.** This section and the published v0.1.11 release notes first said
"`Tool` is 12 of 13 qualified", which implies one unqualified link. `Tool`'s
chunk has twelve hierarchy arrows and all twelve are grey; the thirteenth link
statement is a `+N more` depth stub, which is a statement about what the diagram
omits and not a relationship at all. Counting stub connectors as relations is
exactly the mistake the stubs are styled differently to prevent.

**Four cues for that one distinction, and the first attempt shipped with one.**
Dotted versus solid at 1px was unreadable on a 13" laptop — Doug found it
immediately. Colour carries the distinction now, stroke weight and a `?` label
back it up so it survives a colourblind reader or greyscale, and the dotted
style stays because it reads as weaker and costs nothing. The `+N more`
connectors keep the plain default style, so "not drawn" cannot be mistaken for
"unqualified". A generated legend heads the page, built from the same constants
as the diagrams so it cannot drift from them.

`instantial` appears on no arrow anywhere, because it is asserted nowhere — §Q1
again, and the thirteen named plugins under `ObsidianPlugin` are the clearest
place it is missing.

### R3. Three targets, one format

Mermaid renders natively in the GitHub view of the same Markdown and in
Obsidian. Only the Pages build needs help, and rouge has no mermaid lexer, so a
fence arrives as `<pre><code class="language-mermaid">` with the source intact
and no inserted spans — a few lines of vanilla JS read `textContent` and hand it
over. The same three-target test that chose `<details>` over a script in §L2.

Two things worth recording for whoever touches it next. The class sits on the
`<code>`, **not** on a wrapper, so a `.language-mermaid code` selector matches
nothing — that was a real bug, caught by diffing the built HTML against the
generated source rather than by reading it. And the bundle is **3.3 MB**, so it
loads only where `mermaid: true` is set; if it fails to load the fence is left
alone and the source stays readable.

Depth and fan-out were tuned by measuring: depth 2 draws 100 concepts with the
largest chunk at 35 nodes, depth 3 draws 132 with the largest at 57, depth 4
reaches 96 in one diagram and defeats the purpose. Depth 3, fan-out 12.

## S. What the map says about the top concepts

**Measured 2026-09-18.** Doug read the generated map, searched the vocabulary
for its own subject, and asked which terms to add first and what prose to
adjust. Measurement and consequence only — **this proposes no final shape.** How
many top concepts there are and how they relate is his to settle; §Q6 records
his direction as explicitly not a commitment.

### S1. The vocabulary never names its own subject

**"Personal Knowledge Management" appears in 0 of 223 concepts** — not as a
label, not as an altLabel, not in a single definition or scope note. Neither
does "Knowledge Management". The namespace is `w3id.org/pkm`, the README opens
on Personal Knowledge Management, the repository About says it, and the
vocabulary is silent.

Worth separating from a search complaint: `pkm` *does* match, 29 hits, verified
by running the published widget's own ranking against the published index. It is
the phrase that is absent, and the absence is in the graph rather than in the
search.

### S2. The spine already exists, and the folders took it

| concept | narrower | its folder twin | narrower |
|---|---:|---|---:|
| `Knowledge` | **4** — Cluster, Concept, Source, Topic | `AtlasFolder` | **0** |
| `Time` | **0** | `Calendar` | **7** — the six periods **and `Time` itself** |
| `Action` | **0** | `EffortsFolder` | **4** — `Action` itself, Area, Interest, Project |

Inverted per branch: under Knowledge the concept won and its folder is empty;
under Time and Action the folder won and the concept is childless. So
Knowledge / Time / Action is not a new idea to be introduced — it is a spine
already present and out-ranked by three Obsidian folders.

**The vocabulary already says so twice, in its own prose.** `AtlasFolder`'s
scope note: *"Distinguishes notes for Knowledge (Atlas) from those about Time
(Calendar) or Action (Efforts) in the Ideaverse ACE organization framework"* —
the Knowledge/Time/Action reading of ACE, written down. And `Time`'s scope note:
*"Treated as the anchor/parent for the Calendar hierarchy (Life > Decade > Year
> Quarter > Month > Week > Day)."*

**`Time` declares itself the parent of the period hierarchy, and the graph
asserts the opposite** — `Calendar`, a folder, holds all six periods, and `Time`
hangs beneath it with nothing. That is not a shape to be invented; it is a
declared intent never implemented, and the single link most of this untangling
turns on.

### S3. Two Calendars, and a folder defined as a thing

- **`Calendar` and `CalendarFolder` are two concepts for one folder, stacked.**
  `CalendarFolder` ("The Calendar (Time) folder is the PKM knowledge space for
  time-based notes") parents `Calendar` plus the six clusters; `Calendar` ("A
  major space for time-based notes") parents the six periods plus `Time`. §E's
  four-way `Day` question is this same knot from the other side.
- **`EffortsFolder` is defined "A unit of directed work toward an outcome, such
  as a project or initiative"** — the definition of an *Effort*, not of a
  folder. Checked across every folder and space concept: it is the only one
  whose definition describes a thing rather than a place. `AtlasFolder`'s
  definition is the shape it should copy.

### S4. A phantom the check cannot see

`Action`'s scope note opens *"Narrower than an Effort, and alongside Area,
Interest, or Project."* **`pkmv:Effort` does not exist** — §K records that
already, with seven `Effort*` terms that do. So the note promises a concept the
vocabulary has never had.

`prose.py`'s phantom-citation rule exists to catch exactly this and cannot:
`CAMEL_TOKEN` is `\b(?:[A-Z][a-z0-9]+){2,}\b`, **two or more** CamelCase
segments, so `EffortCluster` matches and a one-word `Effort` never does. The
rule catches phantoms only when they are spelled as compounds. Widening it is
cheap; the risk is that every capitalised English word becomes a candidate, so
it wants the lexicon check `prose.py` already carries.

### S5. What can move now, and what cannot

Using the rules already written down, not new ones:

| | level | when |
|---|---|---|
| Mint absent terms; add `skos:hasTopConcept` for them | **minor** | now |
| Fix definitions and scope notes | **patch** | now |
| Reparent the six periods from `Calendar` to `Time` | **major** | 0.2.0 |
| Move Action/Area/Interest/Project off `EffortsFolder` | **major** | 0.2.0 |
| Demote the technology top concepts | **major** | 0.2.0 |
| Resolve `Calendar` vs `CalendarFolder` | **major** | 0.2.0 |

The first two rows are a release on their own, and they do not presume the final
hierarchy — which is what makes the transformation incremental rather than one
irreversible pass. `z/drafts/0.1.12-prep-worklist.md` is that worklist.

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
