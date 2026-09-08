---
layout: default
title: PKM Vocabulary
---

# PKM Vocabulary

**Concept scheme:** `https://w3id.org/pkm/vocab`
**Concept URIs:** `https://w3id.org/pkm/vocab/{term}`

A SKOS glossary of Personal Knowledge Management terms. Concepts use slash URIs so
each term dereferences independently.

## Download

- [`pkm-vocab.export-0.1.2.ttl`](pkm-vocab.export-0.1.0.ttl) — Turtle

## Terms

| Concept                               | Preferred label | Also known as       |
|---------------------------------------|-----------------|---------------------|
| [`pkmv:Recipe`](pkmv_Recipe.ttl)      | Recipe          |                     |
| [`pkmv:note`](../z/pkmv_note.ttl)     | note            | atomic note, zettel |
| [`pkmv:tag`](../z/pkmv_tag.ttl)       | tag             | —                   |
| [`pkmv:source`](../z/pkmv_source.ttl) | source          | reference           |

Hierarchical relationships between these concepts live in the
[taxonomy](../taxonomy/), keeping definitions in exactly one place.
