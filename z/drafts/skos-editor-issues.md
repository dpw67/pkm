# SKOS Editor — draft issues

Drafts against [`jesstalisman-ia/intentional-arrangement-skos`](https://github.com/jesstalisman-ia/intentional-arrangement-skos).

**Status.** The six drafts that used to head this file are all filed and closed —
#58 through #63. They are kept below as an archive, because their shape is the one
Jessica accepted and it is worth matching. Do not re-file them.

Two new drafts are ready, A and B. Both are visible in the source at `main`
(through `48b1ae35`), so they do not need a fresh export to demonstrate. Evidence
is from `../../vocab/src/pkm-vocab.export.ttl` (223 concepts, 18 collections).

**Cite the commit SHA, not a version string.** The `v0.17.3` at `app/index.html:933`
belongs to the Crosswalk panel, not the app.

---

## A. `[Bug]: The label comparison key is written into change-note prose, so notes read “Day Meal Plan@en”`

**Label:** `bug` · **Area:** Concept editor / change history

### What happened?

Editing a preferred label writes a change note that quotes the label with its
language tag glued on:

```
2026-09-07 — Preferred label changed from “Day.Meal Plan@en” to “Day Meal Plan@en” (by Doug Warren)
```

The `@en` is not part of the label. It comes from the key used to diff the two
label sets — `app/index.html:1926`:

```js
function labelsSet(arr){ return (arr||[]).filter(l=>l.val).map(l=> l.val+(l.lang?"@"+l.lang:"")); }
```

That key is correct *as a key*: it keeps `"Recipe"@en` and `"Recept"@nl` distinct
across a set difference, which is exactly what you want. The problem is that the
same string is then interpolated straight into human prose, at `:1934` and `:1935`:

```js
if(f==="pref"&&add.length===1&&rem.length===1){ ch.push(`Preferred label changed from “${rem[0]}” to “${add[0]}”`); return; }
add.forEach(x=>ch.push(`${name} “${x}” added`)); rem.forEach(x=>ch.push(`${name} “${x}” removed`));
```

So it affects preferred-label changes and alternative/hidden label add and remove.
`noteDiff` also calls `labelsSet`, but it never interpolates the result — it emits
only "Definition updated" / "Scope note updated" — which is why definition and
scope-note edits produce clean notes.

**Reproduction:** `pkmv:DayMealPlan` — 7 change notes, 3 of them defective.

**Scale:** 151 literals across a full export of 223 concepts carry a language tag
inside their text.

### Why it matters

`skos:changeNote` is prose meant for a human reader. These notes are published:
they render on each term's HTML page and ship in the Turtle. A reader who does not
know the editor's internals sees a label that appears to be named `Day Meal Plan@en`.

### Suggested fix

Two parts, and the second matters as much as the first.

1. **Separate the display form from the comparison key.** Keep `labelsSet` as-is for
   diffing, and carry the plain `l.val` (optionally " (nl)" where the language is
   worth stating) into the message. Something like a parallel `labelsDisplay(arr)`,
   or having `labelsSet` return objects and letting the caller choose.

2. **Migrate stored history.** This is the part a display-only fix would miss.
   `app/core.js:277` shows only the `(by X)` suffix is generated at export time —
   the note body comes from `h.changes`, which was written into the workspace when
   the edit happened:

   ```js
   const who = h.author ? " (by " + h.author + ")" : "";
   add(s, iri(NS.skos+"changeNote"), lit((when? when+" — ":"") + changes + who, defLang));
   ```

   So every existing workspace keeps its defective notes forever unless they are
   rewritten in place. A one-time pass over `history[].changes` stripping the
   `@lang` from inside the quotes would clear them.

### Related

Adjacent to **#71** (language dropdown on concept change notes), not a duplicate.
#71 was about the language tag *of* the note literal; this is a language tag
*inside* the note text. Different layer, different fix.

---

## B. `[Bug]: Approving your own proposal names you twice — “(proposed by X) (by X)”`

**Label:** `bug` · **Area:** Proposals / change history

### What happened?

Creating a concept through the proposal workflow and then approving it yields:

```
2026-08-25 — Created from approved proposal (proposed by Doug Warren) (by Doug Warren)
```

The same person is named through two independent channels that meet at export.
Three lines, in order:

```js
$('#pSubmitter').value=getEditor();                                                                 // index.html:3868
seedHistory(c, "Created from approved proposal"+(p.submitter?` (proposed by ${p.submitter})`:""));  // index.html:3942
const who = h.author ? " (by " + h.author + ")" : "";                                               // core.js:277
```

1. The submitter field pre-fills with the current editor identity.
2. Approval bakes `(proposed by …)` into the change *text*.
3. The serializer appends `(by …)` from the entry's `author` field.

When submitter and editor are the same person — the common case for a solo
vocabulary, since the field defaults to exactly that — the name appears twice.

**Scale:** 39 change notes in one export.

### Why it matters

Same as A: these are published prose. It also makes the attribution ambiguous —
a reader cannot tell whether two people were involved or one person was recorded
twice.

### Suggested fix

Carry the submitter as structured data rather than in prose: store it on the
history entry (`{ ts, author, submitter, changes }`) and let the serializer decide
how to render one name versus two. That also lets the export say something
genuinely useful when they differ — "(proposed by A, approved by B)".

As with A, existing workspaces need a migration pass; the doubled text is already
stored in `h.changes`.

---

# Filed and closed

Archived below. Kept for the format, which was accepted; do not re-file.

---

## 1. `[Bug]: Collections export as second-class citizens — rdfs:label and skos:note where concepts get skos:prefLabel and skos:definition`

**Filed as [#58 — Collections export](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/58). Closed.**

**Label:** `bug` · **Area:** Import / Export

### What happened?

A collection and a concept describe the same kind of thing — a named resource in the
scheme with a label and a description — but they come out of the exporter using
different predicates, and the collection is missing two properties entirely.

Side by side, from one export:

```turtle
pkmv:Recipe a skos:Concept ;
    skos:inScheme <https://w3id.org/pkm/vocab> ;
    skos:prefLabel "Recipe"@en ;
    skos:definition "A set of ingredients, instructions, nutrition, and information…"@en ;
    skos:scopeNote "Reusable building block referenced by meals; imported into…"@en ;
    dcterms:created "2026-08-16"^^xsd:date ;
    dcterms:modified "2026-08-29"^^xsd:date ;
    …

pkmv:ConceptCollection a skos:Collection ;
    rdfs:label "Concept Collection"@en ;
    skos:note "All notes related to a Concept."@en ;
    skos:member pkmv:Concept, pkmv:Term, pkmv:Taxonomy, … .
```

Across all 18 collections in my vocabulary:

| Property | Concepts | Collections |
| --- | ---: | ---: |
| `skos:prefLabel` | 223/223 | **0/18** |
| `skos:inScheme` | 223/223 | **0/18** |
| `rdfs:label` | 0/223 | 18/18 |
| `skos:definition` | 223/223 | **0/18** |
| `skos:note` | 0/223 | 15/18 |
| `dcterms:created` / `modified` | 223/223 | **0/18** |

### Why it matters

Collections are published resources. Each one has a URI in the same namespace, gets its
own Turtle file, and dereferences exactly like a concept does. Three consequences:

1. **No `skos:prefLabel`** — any consumer that reads labels the SKOS way (which is what
   `prefLabel` is *for*) finds 18 unlabelled resources. Falling back to `rdfs:label`
   works, but only if you know to look.
2. **No `skos:inScheme`** — nothing in the data ties a collection to the scheme it
   belongs to. A `DESCRIBE`-style crawl of the scheme finds 223 of 241 resources.
3. **`skos:note` instead of `skos:definition`** — `skos:note` is the generic
   superproperty of the whole documentation family, so a tool asking "what is the
   definition of this thing?" gets nothing back. I lost 15 collection descriptions this
   way: they were in the export the whole time, my renderer looked for `skos:definition`
   like it does for concepts, and the published page showed bare member lists.

Neither `skos:prefLabel` nor `skos:inScheme` has an `rdfs:domain` in SKOS, so both are
perfectly legal on a `skos:Collection` — this is not a spec constraint pushing the
current shape.

### Suggested fix

For collections, emit what concepts get:

- `skos:prefLabel` (keeping `rdfs:label` too is harmless if it helps other consumers)
- `skos:inScheme` pointing at the concept scheme
- `skos:definition` for the description field, with `skos:scopeNote` and
  `skos:editorialNote` available the way they are for concepts — the Collection editor
  currently offers one generic note field, and it lands in `skos:note`
- `dcterms:created` / `dcterms:modified`, since collections are edited like anything else

If changing the note predicate would break round-trips for existing users, writing
`skos:definition` *in addition to* `skos:note` would solve the consumer side without
touching the import path.

### Browser & device

Safari / Chrome on macOS 26. SKOS Editor `<VERSION>`.

---

## 2. `[Bug]: dcterms:creator is exported as a literal string even when the agent has a URI in the same file`

**Filed as [#59 — Dublin Core literals in dcterms:creator](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/59). Closed.**

**Label:** `bug` · **Area:** Import / Export

### What happened?

I defined myself as an agent on the Source tab, so the export contains:

```turtle
pkmv:Doug-Warren a prov:Person ;
    foaf:name "Doug Warren" ;
    foaf:homepage <https://blog.warrenweb.net> .
```

The concept scheme attributes itself to that resource correctly:

```turtle
<https://w3id.org/pkm/vocab> dcterms:creator pkmv:Doug-Warren ;
```

But every one of the 223 concepts attributes itself to a **string**:

```turtle
pkmv:Recipe a skos:Concept ;
    dcterms:creator "Doug Warren" ;
```

Counted across the file: **223 literal-valued `dcterms:creator`, 1 URI-valued.**

### Why it matters

The whole point of minting an agent resource is that attribution becomes machine-readable
— you can follow the URI to a homepage, an ORCID, an affiliation. A bare string is not
resolvable, does not deduplicate across vocabularies, and cannot be distinguished from
another Doug Warren. The editor already knows the URI; it uses it one line earlier.

It also means a multi-contributor vocabulary can't be queried by contributor, which
undercuts [#50](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/50).

### Suggested fix

When a `dcterms:creator` / `dcterms:contributor` value matches a defined agent's
`foaf:name`, emit the agent's URI rather than the string. Same treatment the scheme
already gets. If some users want the human-readable string too, `foaf:name` on the agent
already provides it — no need to duplicate it at every concept.

### Browser & device

Safari / Chrome on macOS 26. SKOS Editor `<VERSION>`.

---

## 3. `[Bug]: A few ISO 25964 relations export without the skos:broader they entail`

**Filed as [#60 — ISO 25964 links without skos:broader](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/60). Closed.**

**Label:** `bug` · **Area:** Import / Export

### What happened?

`isothes:broaderPartitive` is an `rdfs:subPropertyOf skos:broader`, so the editor
sensibly writes both. It does this **315 times out of 318**. Three statements get the
ISO property with no `skos:broader` alongside:

```turtle
pkmv:KnowledgeGraph  isothes:broaderPartitive  pkmv:GraphDatabase .   # no skos:broader
pkmv:PythonTemplate  isothes:broaderPartitive  pkmv:ObsidianNotes .   # no skos:broader
pkmv:Day             isothes:broaderPartitive  pkmv:Week .            # no skos:broader
```

(and the three matching `isothes:narrowerPartitive` statements, likewise without
`skos:narrower`).

All three share a shape: the concept already has at least one *other* parent that did get
its `skos:broader`, and the ISO-qualified parent is an additional one.

```turtle
pkmv:KnowledgeGraph  skos:broader pkmv:KnowledgeSystem ;
                     isothes:broaderPartitive pkmv:GraphDatabase .
pkmv:Day             skos:broader pkmv:Calendar ;
                     isothes:broaderPartitive pkmv:Week .
pkmv:PythonTemplate  skos:broader pkmv:PKMPython, pkmv:Tool ;
                     isothes:broaderGeneric pkmv:Tool ;
                     isothes:broaderPartitive pkmv:ObsidianNotes .
```

So my guess is a second/subsequent parent added with an ISO relation type doesn't get its
plain-SKOS statement written — but 100 other `broaderPartitive` links are fine, so
whatever the trigger is, it's narrower than that.

### Why it matters

The relationship is *entailed* — a reasoner would derive `skos:broader` from the
sub-property axiom. But almost nothing in the SKOS ecosystem reasons. Skosmos, most
SPARQL queries, and every hierarchy renderer I've tried read `skos:broader` literally, so
those three parent links are simply invisible: `pkmv:Day` looks like a child of Calendar
and nothing else, and the Day-in-Week partitive structure disappears.

Easy to work around downstream (I materialise them in my build), but it's a silent gap —
nothing in the editor flags it.

### Steps to reproduce

Not isolated to a minimal case yet. Happy to send the full Turtle export, or to try
reproducing on a small scheme if that's more useful.

### Browser & device

Safari / Chrome on macOS 26. SKOS Editor `<VERSION>`.

---

## 4. `[Feature]: Export the validation report`

**Filed as [#61 — Downloadable validation report](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/61). Closed.**

**Label:** `enhancement` · **Area:** Validation (qSKOS)

### What are you trying to do?

Work through validation findings away from the editor. The Validation tab shows problems
clearly, but they live on screen — to fix 40 findings I'm scrolling the panel, fixing one,
losing my place, and scrolling again. I can't diff two runs to see whether an editing
session improved things, can't paste findings into a task list, and can't keep a record of
what a release looked like when it shipped.

### What would you like the tool to do?

A download button on the Validation tab producing the current findings as a file.
Markdown would suit me best — I keep vocabulary notes in Obsidian, and a checklist is
directly actionable:

```markdown
## Warnings (15)
### mapping-to-property (5)
- [ ] **Source** — skos:relatedMatch <http://purl.org/dc/terms/source> targets an RDF property
```

CSV or JSON would serve people scripting against it. Any one of the three is a large
improvement over none.

Useful either way: a severity for each finding (spec violation vs. structural problem vs.
editorial nit), a stable machine-readable code per rule so runs can be diffed, and counts
per rule in a header.

### Anything else?

I ended up writing a Python checker over the export to get this — about 450 lines,
mirroring what the Validation tab already computes. Happy to share the rule list if it's
useful input; several rules are ones the editor could catch at edit time rather than
export time.

---

## 5. `[Feature]: Warn when a mapping property points at an RDF property rather than a concept`

**Filed as [#62 — Mapping property targets as RDF](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/62). Closed.**

**Label:** `enhancement` · **Area:** Validation (qSKOS)

### What are you trying to do?

Record that my `Source` concept lines up with the Dublin Core notion of a source. On the
Crosswalk tab I added `skos:relatedMatch` targets, and got:

```turtle
pkmv:Source a skos:Concept ;
    skos:relatedMatch dcterms:source,
                      dcterms:bibliographicCitation,
                      dcterms:conformsTo,
                      dcterms:references,
                      <https://www.dublincore.org/…/dcmi-terms/elements11/source/> .
```

Which is a type error, and my own fault — but the editor accepted all five without
comment. `skos:relatedMatch` is a sub-property of `skos:semanticRelation`, whose
`rdfs:domain` and `rdfs:range` are both `skos:Concept`. `dcterms:source` is an
`rdf:Property`. Asserting the mapping entails `dcterms:source a skos:Concept`, which is
false and will make an OWL reasoner unhappy about anyone who imports my vocabulary.

I wanted "these are related ideas," which is `rdfs:seeAlso` — it carries no typing at all.
Nothing told me the difference until I ran a reasoner over the published file.

### What would you like the tool to do?

On the Crosswalk tab, when a mapping target looks like an RDF property rather than a
concept, warn and offer `rdfs:seeAlso` instead. Something like:

> `dcterms:source` looks like an RDF property, not a concept. `skos:relatedMatch` asserts
> the target is a `skos:Concept`. Use `rdfs:seeAlso` to link without that claim?
> [Use rdfs:seeAlso] [Keep relatedMatch]

Detection needn't be clever. A lowerCamelCase final segment is a property by convention
and UpperCamelCase is a class, which catches the whole `dcterms:` and `foaf:` surface. For
a namespace the editor knows (Dublin Core, schema.org, FOAF, SKOS itself) a small
built-in list would be exact. If neither applies, stay quiet — a false warning on someone's
own namespace would be worse than silence.

A validation-tab rule would work as well as an inline warning, and would pair with #4.

### Anything else?

Same underlying theme as
[#39](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/39) — the
editor accepting a mapping target that isn't the kind of thing the property means.

---

## 6. `[Feature]: Separate the agents namespace from the documents namespace`

**Filed as [#63 — Separate the agents namespace](https://github.com/jesstalisman-ia/intentional-arrangement-skos/issues/63). Closed.**

**Label:** `enhancement` · **Area:** Import/Export
**Follow-up to:** #57 (closed, shipped in 0.16.7)

### What are you trying to do?

Publish agents and cited documents at two different, already-advertised sections of my
namespace:

- `https://w3id.org/pkm/agents#` — people and software credited in the vocabulary
- `https://w3id.org/pkm/resources#` — documents the vocabulary cites

Both are listed on the namespace home page, both are declared in `void.ttl`, and both are
named in the w3id.org registration for `https://w3id.org/pkm`. They dereference
separately, so a document minted under `agents#` is wrong on its face —
`agents#RDF-Ontology-Glossary` says a glossary is an agent.

### What would you like the tool to do?

Split the existing *Agents & documents namespace* field into two optional fields, or add a
second optional field for documents that falls back to the first when blank:

```
Agents namespace      https://w3id.org/pkm/agents#
Documents namespace   https://w3id.org/pkm/resources#     (blank = same as agents)
```

`prov:Person` / `prov:Agent` / `prov:Organization` / `prov:SoftwareAgent` mint under the
first, `foaf:Document` under the second. Both blank keeps today's behaviour; documents
blank keeps 0.16.7's behaviour exactly, so nothing existing changes.

### Anything else?

0.16.7 already does most of this — thank you. Measuring against my own export, the single
annex field resolves 4 of my 8 metadata resources:

| Resource | Type | 0.16.7 mints | I need |
|---|---|---|---|
| Doug-Warren | `prov:Person` | `agents#Doug-Warren` | ✅ same |
| Jessica-Talisman | `prov:Person` | `agents#Jessica-Talisman` | ✅ same |
| Claude-AI | `prov:SoftwareAgent` | `agents#Claude-AI` | ✅ same |
| SKOS-Editor | `prov:SoftwareAgent` | `agents#SKOS-Editor` | ✅ same |
| ACE-Organization | `foaf:Document` | `agents#ACE-Organization` | `resources#ACE-Organization` |
| PKM-URI-Namespace | `foaf:Document` | `agents#PKM-URI-Namespace` | `resources#PKM-URI-Namespace` |
| RDF-Ontology-Glossary | `foaf:Document` | `agents#RDF-Ontology-Glossary` | `resources#…` |
| RDF-Ontology-Glossary-Abbreviated | `foaf:Document` | `agents#…-Abbreviated` | `resources#…` |

There is a workaround that already works, and it may be enough — setting an explicit
identity URI of `https://w3id.org/pkm/resources#{Name}` on each document, which 0.16.7
uses verbatim as documented. I simulated it against my build: it produces a published
graph isomorphic to what my post-processing produces today, with nothing left for the
script to do. So this is a convenience request rather than a blocker — four documents is
four fields to remember, but it is not a lot of typing, and I'd rather you spend the time
on it only if others hit the same split.
