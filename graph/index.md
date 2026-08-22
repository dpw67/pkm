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

RDF and property graphs disagree about where information lives, so the mapping is
stated explicitly rather than assumed:

| Ontology | Neo4j |
| --- | --- |
| `pkm:Note` | `:Note` label |
| `pkm:Tag` | `:Tag` label |
| `pkm:Source` | `:Source` label |
| `pkm:linksTo` | `[:LINKS_TO]` relationship |
| `pkm:hasTag` | `[:HAS_TAG]` relationship |
| `pkm:derivedFrom` | `[:DERIVED_FROM]` relationship |

Each node carries a `uri` property holding its `w3id.org/pkm` identifier, so graph
nodes and RDF resources can be reconciled in both directions.

## Constraints

```cypher
CREATE CONSTRAINT note_uri IF NOT EXISTS
FOR (n:Note) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT tag_uri IF NOT EXISTS
FOR (t:Tag) REQUIRE t.uri IS UNIQUE;

CREATE CONSTRAINT source_uri IF NOT EXISTS
FOR (s:Source) REQUIRE s.uri IS UNIQUE;
```

## Implementation

Services that load and query this graph live in
[`pkm-neo4j-services`](https://github.com/dpw67/pkm-neo4j-services). This namespace
documents the model; that repository implements it.
