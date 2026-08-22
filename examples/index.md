---
layout: default
title: PKM Examples
---

# Examples

Worked instance data using the [PKM ontology](../ontology/). Every example is valid
against the [shapes](../shapes/).

Code in this directory is dedicated to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) — reuse it without
attribution.

## Download

- [`note.jsonld`](note.jsonld) — a single note in JSON-LD

## A note in JSON-LD

Using the namespace [`context.jsonld`](../context.jsonld), ordinary JSON becomes
Linked Data with one added line:

```json
{
  "@context": "https://w3id.org/pkm/context.jsonld",
  "id": "https://w3id.org/pkm/examples/note/atomic-notes",
  "type": "Note",
  "title": "Atomic notes",
  "created": "2026-08-22T09:00:00Z",
  "hasTag": ["https://w3id.org/pkm/examples/tag/zettelkasten"],
  "linksTo": ["https://w3id.org/pkm/examples/note/note-linking"]
}
```

## Planned

Equivalents in Turtle, Cypher, SQL, TypeDB, Python, and Swift, so the same instance
can be compared across every representation the KSA project uses.
