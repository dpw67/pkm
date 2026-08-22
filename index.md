---
layout: default
title: PKM — Persistent URI Namespace
---

# PKM

A persistent URI namespace at **`https://w3id.org/pkm`** with Linked Data resources on
Personal Knowledge Management (PKM) for the Knowledge System Architecture (KSA) project.

All identifiers in this namespace are `w3id.org/pkm/...` URIs. They are stable and
independent of where the site happens to be hosted — please cite them, not the
underlying host.

## Resources

| Resource | URI | Description |
| --- | --- | --- |
| [Ontology](ontology/) | `w3id.org/pkm/ontology#` | RDF/OWL classes, properties, and relationships |
| [Vocabulary](vocab/) | `w3id.org/pkm/vocab/` | SKOS terms and definitions (glossary) |
| [Taxonomy](taxonomy/) | `w3id.org/pkm/taxonomy` | SKOS concept hierarchy |
| [Shapes](shapes/) | `w3id.org/pkm/shapes/` | SHACL and JSON Schema validation artifacts |
| [Examples](examples/) | `w3id.org/pkm/examples/` | Worked instance data |
| [Graph](graph/) | `w3id.org/pkm/graph/` | Neo4j nodes, relationships, and Cypher |
| [Tools](tools/) | `w3id.org/pkm/tools/` | Python and Swift apps, services, intents, Siri |
| [Resources](resources/) | `w3id.org/pkm/resources/` | Related documentation and reading |

Machine-readable descriptions of the namespace itself:
[`context.jsonld`](context.jsonld) (JSON-LD context) and
[`void.ttl`](void.ttl) (VoID dataset description).

## Status

Version 0.1.0 — early draft. Terms are not yet stable and may change without notice
until a 1.0.0 release is tagged.

## License

Content is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code examples and build scripts are dedicated to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

## Contact

Administered by Doug Warren ([@dpw67](https://github.com/dpw67)).
Issues and suggestions: [github.com/dpw67/pkm/issues](https://github.com/dpw67/pkm/issues).
