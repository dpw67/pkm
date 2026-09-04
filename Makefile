# Build glue for the PKM namespace.
#
# Not published (excluded in _config.yml). No Python package lives in this repo —
# invoke LinkML from whatever environment has it installed, e.g. the pkm-neo4j-services
# virtualenv, or `pipx install linkml`.
#
#   make check      validate the SKOS Editor export -> reports/vocab-check.md
#   make build      generate every published artifact from the export
#   make shapes     regenerate SHACL + JSON Schema from schema/pkm.yaml
#   make models     regenerate dev artifacts from the LinkML domain modules
#   make artifacts  render the Obsidian/Neo4j/Ladybug/TypeQL templates
#   make validate   parse-check every published Turtle file
#   make notes      regenerate the Obsidian term stubs in the WarrenWeb vault
#   make serve      preview the site locally
#   make clean      remove build output

# schema/pkm.yaml still declares the retired Note/Tag/Source placeholders, so
# `shapes` builds a model that no longer exists. Left in place rather than
# quietly repointed, because shapes/ is published and pkm-meals is not ready to
# publish. Retire or rewrite it before trusting `make shapes`.
SCHEMA  := schema/pkm.yaml
SHAPES  := shapes

# LinkML domain modules and the unpublished artifacts they generate. One module
# per domain; meals is the first. `generated/` is excluded in _config.yml.
MODULES := schema/pkm-meals.yaml
GEN     := generated

# Classes worth a JSON Schema of their own. LinkML's default output has an empty
# root with everything under $defs, which quicktype cannot follow -- it emits a
# bare `typealias = [String: JSONAny]`. --top-class gives each one a real root,
# and then the whole struct graph below it generates.
TOPS    := Recipe Meal
EXPORT  := vocab/src/pkm-vocab.export.ttl
PYTHON  := .venv/bin/python
BIN     := .venv/bin
VOCAB   := PYTHONPATH=scripts $(PYTHON) -m pkm_vocab

# Obsidian vault directory the term stubs are mirrored into. Override on the
# command line for a different vault: make notes NOTES_OUT=/path/to/pkm/vocab
NOTES_OUT := $(HOME)/Obsidian/WarrenWeb/pkm/vocab

# Hand-authored Turtle plus the generated bulk dump. The 241 per-term files under
# vocab/terms/ are checked by `validate` through the wildcard, not listed here.
TTL     := void.ttl ontology/pkm.ttl taxonomy/pkm-taxonomy.ttl \
           vocab/pkm-vocab.ttl agents/index.ttl resources/index.ttl

.PHONY: all check build shapes models artifacts validate notes serve clean

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

# Dev artifacts for prototyping: Pydantic, JSON Schema, SHACL, OWL, Swift.
# Nothing here is published or citable -- regenerate freely. Needs linkml in
# .venv (`.venv/bin/python -m pip install linkml`) and quicktype on PATH.
models:
	@mkdir -p $(GEN)/jsonschema $(GEN)/pydantic $(GEN)/shacl $(GEN)/owl $(GEN)/swift
	@for m in $(MODULES); do \
	  base=$$(basename $$m .yaml); \
	  echo "  $$m"; \
	  $(BIN)/gen-json-schema $$m > $(GEN)/jsonschema/$$base.schema.json; \
	  $(BIN)/gen-pydantic    $$m > $(GEN)/pydantic/$$(echo $$base | tr - _).py; \
	  $(BIN)/gen-shacl       $$m > $(GEN)/shacl/$$base.shacl.ttl; \
	  $(BIN)/gen-owl         $$m > $(GEN)/owl/$$base.owl.ttl; \
	  for c in $(TOPS); do \
	    $(BIN)/gen-json-schema --top-class $$c $$m > $(GEN)/jsonschema/$$c.schema.json; \
	    quicktype --src-lang schema --lang swift -o $(GEN)/swift/$$c.swift \
	      $(GEN)/jsonschema/$$c.schema.json >/dev/null 2>&1; \
	    echo "    $$c -> swift"; \
	  done; \
	done

# The four targets LinkML has no generator for. Everything upstream of this --
# JSON Schema, Pydantic, SHACL, OWL -- comes from `models`; these come from
# generators/templates, driven by the shape model in generators/__init__.py.
# Separate from `models` because they are a different toolchain, not because
# they are optional: run both to regenerate everything under $(GEN).
artifacts:
	@for m in $(MODULES); do \
	  echo "  $$m"; \
	  $(BIN)/python -m generators $$m --out $(GEN); \
	done

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
