"""Validate the export with the SKOS Editor's own engine, not ours.

`make check` runs `scripts/pkm_vocab/checks.py`, which encodes what this
project has decided a good term looks like. This runs the validator that ships
with the editor the vocabulary is authored in -- a second opinion from the tool
upstream, on the same graph.

The overlap is deliberate and the gap is the point. `checks.py` does not test
five SKOS integrity conditions that the editor's SHACL shapes do:

    S9   skos:Concept and skos:ConceptScheme are disjoint
    S13  prefLabel / altLabel / hiddenLabel are pairwise disjoint
    S14  at most one skos:prefLabel per language tag
    S37  skos:Collection is disjoint with Concept and ConceptScheme
         plus: two concepts sharing one prefLabel in one language

S37 is the condition that settles whether a term can be both a concept and a
collection -- a question this project answered by reading the spec when a
validator could have answered it mechanically.

Run through `make validate-skos`, which supplies the interpreter and the
PYTHONPATH. The engine lives outside this repository and is not installed by
it, so an absent engine is reported and skipped rather than failed -- the same
contract `make swiftcheck` has with the Command Line Tools.
"""

from __future__ import annotations

import io
import sys

try:
    import skoslib
except ImportError:
    print("skos engine not importable -- set SKOS_ENGINE to the editor checkout "
          "and run through `make validate-skos`", file=sys.stderr)
    raise SystemExit(0)   # absent engine is a skip, not a failure


def report(path: str) -> int:
    """Validate one file. Returns the number of hard failures."""
    result = skoslib.validate_rdf(io.open(path, encoding="utf-8").read(), "turtle")
    profile = result["profile"]
    summary = result["summary"]
    conforms = result["shacl_conforms"]

    coverage = profile["documentation_coverage"]
    print(f"{path}")
    print(f"  {result['triples']} triples · {profile['concepts']} concepts · "
          f"{profile['top_concepts']} top · documented {coverage:.0%}")

    # None means pySHACL is missing, which is not the same as "did not conform".
    # Saying so explicitly stops a silent skip reading as a pass.
    if conforms is None:
        print(f"  SHACL  not run — {result['shacl_report']}")
    else:
        print(f"  SHACL  {'conforms' if conforms else 'VIOLATIONS'}")
        if not conforms:
            print(result["shacl_report"])

    findings = result["structural_findings"]
    if findings:
        for finding in findings:
            print(f"  [{finding['severity']}] {finding['check']}: "
                  f"{finding.get('message') or finding}")
    else:
        print("  structural  no cycles, no orphans")

    # A missing pySHACL must not count as a failure; a real non-conformance must.
    return summary["violations"] + (1 if conforms is False else 0)


def main(argv: list[str]) -> int:
    paths = argv or ["vocab/src/pkm-vocab.export.ttl"]
    failures = sum(report(path) for path in paths)
    if failures:
        print(f"\n{failures} upstream violation(s)", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
