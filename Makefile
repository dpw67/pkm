# Build glue for the PKM namespace.
#
# Not published (excluded in _config.yml). No Python package lives in this repo —
# invoke LinkML from whatever environment has it installed, e.g. the pkm-neo4j-services
# virtualenv, or `pipx install linkml`.
#
#   make check      validate the SKOS Editor export -> reports/vocab-check.md
#   make build      generate every published artifact from the export
#   make shapes     regenerate SHACL + JSON Schema from schema/pkm.yaml
#   make validate   parse-check every published Turtle file
#   make notes      regenerate the Obsidian term stubs in the WarrenWeb vault
#   make serve      preview the site locally
#   make clean      remove build output

SCHEMA  := schema/pkm.yaml
SHAPES  := shapes
EXPORT  := vocab/src/pkm-vocab.export.ttl
PYTHON  := .venv/bin/python
VOCAB   := PYTHONPATH=scripts $(PYTHON) -m pkm_vocab

# Obsidian vault directory the term stubs are mirrored into. Override on the
# command line for a different vault: make notes NOTES_OUT=/path/to/pkm/vocab
NOTES_OUT := $(HOME)/Obsidian/WarrenWeb/pkm/vocab

# Hand-authored Turtle plus the generated bulk dump. The 241 per-term files under
# vocab/terms/ are checked by `validate` through the wildcard, not listed here.
TTL     := void.ttl ontology/pkm.ttl taxonomy/pkm-taxonomy.ttl \
           vocab/pkm-vocab.ttl agents/index.ttl resources/index.ttl

.PHONY: all check build shapes validate notes serve clean

all: build validate

# Exits non-zero when there are errors, so it doubles as a pre-commit gate.
check:
	@mkdir -p reports
	-$(VOCAB) check $(EXPORT) --format markdown -o reports/vocab-check.md
	$(VOCAB) check $(EXPORT)

# Depends on check, so a broken export can never reach the published tree.
# The build re-checks its own output and refuses to write if the transform
# introduced anything the checker would flag.
build: check
	$(VOCAB) build $(EXPORT)

shapes:
	gen-shacl $(SCHEMA)      > $(SHAPES)/pkm.shacl.ttl
	gen-json-schema $(SCHEMA) > $(SHAPES)/pkm.schema.json

# rdflib rather than Jena's riot, so this runs without `brew install jena`.
# The script adds vocab/terms/*.ttl and shapes/*.ttl to whatever is listed in TTL.
validate:
	@$(PYTHON) scripts/validate_ttl.py $(TTL)

# Mirrors the PUBLISHED vocabulary rather than the export, so the stubs carry
# URIs and dates that actually resolve. Deliberately not a dependency of `all`:
# it writes outside this repo, into a vault that syncs to a public site, so it
# stays an explicit action. Stale stubs are pruned; run with --dry-run first if
# the vocabulary has had terms renamed.
notes:
	$(VOCAB) notes vocab/pkm-vocab.ttl --out $(NOTES_OUT)

serve:
	bundle exec jekyll serve --livereload

clean:
	rm -rf _site .jekyll-cache
