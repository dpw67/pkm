---
layout: default
title: PKM Ontology
---

# PKM Ontology

**Namespace:** `https://w3id.org/pkm/ontology#` (preferred prefix `pkm:`)
**Version:** 0.1.0 — declaration only, no classes yet

RDF/OWL classes, properties, and relationships for Personal Knowledge Management.

The model is in development. [`pkm.ttl`](pkm.ttl) currently carries the ontology
declaration and nothing else: the seed `Note`/`Tag`/`Source` classes minted when the
namespace was registered have been removed, because they pointed at vocabulary terms
that no longer exist.

Work is happening in the [vocabulary](../vocab/) first. Once the 223 SKOS concepts
settle, the ones that describe *things* rather than *topics* become OWL classes here,
and the ontology gains the axioms — domains, ranges, disjointness, cardinality — that
SKOS cannot express.

Terms will use hash URIs, so every term resolves through this one document:
`https://w3id.org/pkm/ontology#Note` will be defined in `pkm.ttl`.

## Download

- [`pkm.ttl`](pkm.ttl) — Turtle (canonical, hand-authored)

## Relationship to the vocabulary

The ontology is the formal model; the [vocabulary](../vocab/) is the human-facing
glossary. They stay separate documents with separate URIs. A class will point at the
concept it formalises with `foaf:focus`, not `skos:exactMatch` — the SKOS mapping
properties are defined between concepts, so aiming one at an `owl:Class` is a type
error.
