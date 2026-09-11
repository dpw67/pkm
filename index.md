---
layout: default
title: PKM — Personal Knowledge Management
---

A persistent URI namespace at **`https://w3id.org/pkm`** with Linked Data resources on
Personal Knowledge Management (PKM) for the Knowledge System Architecture (KSA) project.

All identifiers in this namespace are `w3id.org/pkm/...` URIs. They are stable and
independent of where the site happens to be hosted — please cite them, not the
underlying host.

## Resources

| Resource | URI | Description | Status |
| --- | --- | --- | --- |
| [Vocabulary](vocab/) | `w3id.org/pkm/vocab/` | SKOS glossary — 223 concepts, 18 collections | **published** |
| [Agents](agents/) | `w3id.org/pkm/agents#` | People and software credited in the vocabulary | published |
| [Resources](resources/) | `w3id.org/pkm/resources#` | Documents the vocabulary cites, plus related reading | published |
| [Ontology](ontology/) | `w3id.org/pkm/ontology#` | RDF/OWL classes, properties, and relationships | declared, empty |
| [Taxonomy](taxonomy/) | `w3id.org/pkm/taxonomy` | SKOS concept hierarchy, once it moves out of the vocabulary | declared, empty |
| [Shapes](shapes/) | `w3id.org/pkm/shapes/` | SHACL and JSON Schema validation artifacts | planned |
| [Examples](examples/) | `w3id.org/pkm/examples/` | Worked instance data | planned |
| [Graph](graph/) | `w3id.org/pkm/graph/` | Neo4j nodes, relationships, and Cypher | planned |
| [Tools](tools/) | `w3id.org/pkm/tools/` | Python and Swift apps, services, intents, Siri | planned |

"Declared, empty" means the URI resolves and carries its metadata, but no terms have
been minted yet. "Planned" means the page describes intent only.

Machine-readable descriptions of the namespace itself:
[`context.jsonld`](context.jsonld) (JSON-LD context) and
[`void.ttl`](void.ttl) (VoID dataset description).

## Status

Vocabulary **0.1.6** — early draft, published for feedback. Terms are not yet stable
and may change without notice until 1.0.0 is tagged.

Nothing is deleted outright: a retired URI keeps resolving, marked `owl:deprecated`
and pointed at its replacement with `dcterms:isReplacedBy`, so a link made today does
not rot. Comments and corrections are welcome — that is what this release is for.

See the [changelog](https://github.com/dpw67/pkm/blob/main/CHANGELOG.md) for what
changed in each version and what counts as a breaking change.

## License

Content is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code examples and build scripts are dedicated to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

## Contact

Administered by Doug Warren ([@dpw67](https://github.com/dpw67)).
Issues and suggestions: [github.com/dpw67/pkm/issues](https://github.com/dpw67/pkm/issues).
