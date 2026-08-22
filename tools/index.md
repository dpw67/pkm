---
layout: default
title: PKM Tools
---

# Tools

Documentation for the applications, services, scripts, and intents that operate over
the PKM knowledge graph.

This namespace documents the tools; their source lives in separate repositories.

| Tool | Language | Repository |
| --- | --- | --- |
| Neo4j services | Python | [`pkm-neo4j-services`](https://github.com/dpw67/pkm-neo4j-services) |
| Obsidian vault | Markdown / YAML | — |
| Siri intents | Swift | — |

## Vocabulary integration

Tools consume this namespace rather than duplicating it. Pin a released tag of the
[`pkm`](https://github.com/dpw67/pkm) repository, or fetch the published artifacts at
their `w3id.org` URIs — never at the underlying hosting URL, which is subject to
change.
