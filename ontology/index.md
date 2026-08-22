---
layout: default
title: PKM Ontology
---

# PKM Ontology

**Namespace:** `https://w3id.org/pkm/ontology#` (preferred prefix `pkm:`)
**Version:** 0.1.0

RDF/OWL classes, properties, and relationships for Personal Knowledge Management.

Terms use hash URIs, so every term resolves through this one document —
`https://w3id.org/pkm/ontology#Note` is defined in
[`pkm.ttl`](pkm.ttl).

## Download

- [`pkm.ttl`](pkm.ttl) — Turtle (canonical, hand-authored)

## Classes

| Term | Label | Definition |
| --- | --- | --- |
| `pkm:Note` | Note | An atomic unit of captured knowledge, authored as a Markdown document with YAML frontmatter. |
| `pkm:Tag` | Tag | A user-assigned label used to group notes across the folder hierarchy. |
| `pkm:Source` | Source | An external work from which a note derives — an article, book, dataset, or web page. |

## Object properties

| Term | Label | Domain | Range |
| --- | --- | --- | --- |
| `pkm:linksTo` | links to | `pkm:Note` | `pkm:Note` |
| `pkm:hasTag` | has tag | `pkm:Note` | `pkm:Tag` |
| `pkm:derivedFrom` | derived from | `pkm:Note` | `pkm:Source` |

## Relationship to the vocabulary

Each class carries a `skos:exactMatch` to its glossary entry in the
[vocabulary](../vocab/). The ontology is the formal model; the vocabulary is the
human-facing glossary. Definitions are authored once and mirrored via
`skos:definition`.
