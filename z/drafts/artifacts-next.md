# Development artifacts — open questions

Working notes for `make artifacts`, carried over from the session that landed
`fdedbc5` (Swift) and `ae964f2` (Obsidian). Nothing here is decided.

## Needs a decision before more can be generated

**`MealPlan` does not exist.** It was named as a wanted Obsidian note type
alongside Meal and Recipe, but `schema/pkm-meals.yaml` has no such class, so
nothing generates for it in any target. Minting it is the prerequisite. Open
with it: does a plan reference meals, or own them? A reference gives
`[[2026-09-04-dinner]]` and lets one meal appear in two plans; ownership makes
the plan a composition and the meals cascade with it.

**Seed note file names.** `slug()` takes the last segment of the id, so
`pkm:rec/weeknight-chili` becomes `weeknight-chili.md`. The alternative is the
`name` slot -- `Weeknight chili.md` -- which reads better in a Base's first
column and in a wikilink, at the cost of a name that changes when the recipe is
retitled. Obsidian is the one target where the file name *is* the identity, so
this is the only target where the choice matters.

**The Meal/Recipe Cluster.** Ingredients and Instructions are body sections
today. If either grows long enough, the argument is to split it into a linked
sub-note -- `Weeknight chili (Instructions)` -- which makes the recipe a small
cluster rather than one file. Undecided: whether the generator should ever do
this, or whether it is a manual move once a note gets unwieldy. A generated
split needs a rule for "long", and the seed fixture will never trip it.

## Cross-target, affects the schema

**List order is stored nowhere.** A SwiftData to-many is a set, a Cypher MATCH
is unordered, and a Ladybug rel-table has no implicit sequence. The seed
generator mints position into a promoted value object's surrogate key
(`pkm:rec/weeknight-chili#images/0`), but a collapsed association gets no such
key, so ingredient order survives only in the Obsidian body, which is text. An
ordinal slot on the association is the only place order could actually live --
and adding one changes all five targets.

**`Ingredient.nutrition` is amount-scoped.** Ground beef's 1088 kcal is for the
1.5 lb the chili calls for, not per serving or per 100 g, which is why the
recipe's 1488 is exactly 220 + 1088 + 180. Flagged in the class comments and
the fixture header. Fixing it properly means nutrition per unit amount plus a
scaling rule, which is a modelling change rather than a fixture edit.

**A back-reference on a collapsed association.** SwiftData synthesises nothing
on the far end, so "what do I cook with kidney beans" needs a
`#Predicate<RecipeIngredient>` fetch rather than `ingredient.recipes`. Whether
the generator should emit that inverse is open.

## Vocabulary, for 0.1.4

None of these concepts exist yet: `RecipeIngredient`, `Amount`, `Quantity`,
`UnitOfMeasure`, and the six nutrients (calories, carbohydrates, protein, fat,
fiber, sodium -- `pkmv:Nutrition` has no `narrowerPartitive` children at all).
`pkmv:RecipeServings` also needs settling: its 0.1.3 definition is a count, but
the class now holds both a count and a yield.

`UnitOfMeasure` wants a dimension tag and a failable conversion: lb and oz are
mass, cup is volume, and can is packaging, so `convert(to:)` has to be able to
refuse.

## Next, on the Obsidian target

**Column widths.** `columnSize` is a view-level mapping of qualified property to
pixel width, sitting beside `order` and `sort`:

    columnSize:
      note.name: 193
      note.served_at: 213

Undocumented in the Bases syntax page -- read off the hand-made
`+/Notes/Meal1.base`, where it was set by dragging in the app. The six nutrition
columns are all short numbers under a short header and render far wider than
their content, so they want an explicit width. Two questions before generating
one: what number, given the widths in that file came from dragging rather than
from a rule, and where the number comes from -- a per-slot annotation in the
schema, or a heuristic on the slot's type and header length. A width is
presentation, and the schema has held nothing presentational so far except
`title`.

Note that a width the generator writes will be overwritten the moment the column
is dragged in the app, and `make vault` will then put the generated one back.
That is the same overwrite `--delete` already implies for the tree, but a width
is the first thing a reader is likely to adjust by hand and lose.

## Also unresolved

`schema/pkm.yaml` is superseded by `pkm-meals.yaml` but still present -- retire
it, mark it superseded, make it an umbrella, or repurpose it as the shared base
module where `Amount` would live. The target functions in
`generators/__main__.py` still hardcode `pkm-meals` rather than reading
`ctx["stem"]`, which only matters once there is a second module. And the seed
pipeline feeds Obsidian, Neo4j and Ladybug but not TypeQL, which has no seed
template at all.
