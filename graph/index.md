---
layout: default
title: PKM Knowledge Graph
---

# Knowledge Graph

How the [ontology](../ontology/) maps onto a Neo4j property graph: labels,
relationship types, properties, and constraints.

Cypher in this directory is dedicated to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

## Mapping

Not yet defined. The table that used to sit here mapped the placeholder
`Note`/`Tag`/`Source` classes, which have been removed along with the rest of the seed
ontology; a mapping to classes that do not exist would be worse than none.

RDF and property graphs disagree about where information lives, so when the mapping
arrives it will be stated explicitly rather than assumed: one row per OWL class to
Neo4j label, one per object property to relationship type. The invariant already
settled is that every node carries a `uri` property holding its `w3id.org/pkm`
identifier, so graph nodes and RDF resources can be reconciled in both directions.

## Constraints

One uniqueness constraint per label on that `uri` property, in the shape:

```cypher
CREATE CONSTRAINT <label>_uri IF NOT EXISTS
FOR (n:<Label>) REQUIRE n.uri IS UNIQUE;
```

## Implementation

Services that load and query this graph live in
[`pkm-neo4j-services`](https://github.com/dpw67/pkm-neo4j-services). This namespace
documents the model; that repository implements it.
