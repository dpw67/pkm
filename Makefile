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
#   make artifacts  render the Obsidian/Neo4j/Ladybug/TypeQL/Swift templates
#   make swiftcheck compile the generated Swift against the macOS SDK
#   make swiftrun   run the generated harness against the fixture
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
# root with everything under $defs, so a consumer that needs a single rooted
# document -- an API contract, a validator -- gets one per top class here.
#
# This used to feed quicktype as well. It no longer does: quicktype sees JSON
# Schema, which has no idea which classes have identity, so a reference came out
# as a nested copy of the whole record and `Nutrition` was redeclared in every
# file. The Swift now comes from `artifacts`, off the same shape model as the
# graph targets. See generators/templates/swift.*.jinja.
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

.PHONY: all check build shapes models artifacts swiftcheck swiftrun validate notes serve clean

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

# Dev artifacts for prototyping: JSON Schema, Pydantic, SHACL, OWL. Nothing here
# is published or citable -- regenerate freely. Needs linkml in .venv
# (`.venv/bin/python -m pip install linkml`). quicktype is no longer required.
models:
	@mkdir -p $(GEN)/jsonschema $(GEN)/pydantic $(GEN)/shacl $(GEN)/owl
	@for m in $(MODULES); do \
	  base=$$(basename $$m .yaml); \
	  echo "  $$m"; \
	  $(BIN)/gen-json-schema $$m > $(GEN)/jsonschema/$$base.schema.json; \
	  $(BIN)/gen-pydantic    $$m > $(GEN)/pydantic/$$(echo $$base | tr - _).py; \
	  $(BIN)/gen-shacl       $$m > $(GEN)/shacl/$$base.shacl.ttl; \
	  $(BIN)/gen-owl         $$m > $(GEN)/owl/$$base.owl.ttl; \
	  for c in $(TOPS); do \
	    $(BIN)/gen-json-schema --top-class $$c $$m > $(GEN)/jsonschema/$$c.schema.json; \
	  done; \
	done

# The five targets LinkML has no generator for. Everything upstream of this --
# JSON Schema, Pydantic, SHACL, OWL -- comes from `models`; these come from
# generators/templates, driven by the shape model in generators/__init__.py.
# Separate from `models` because they are a different toolchain, not because
# they are optional: run both to regenerate everything under $(GEN).
artifacts:
	@for m in $(MODULES); do \
	  echo "  $$m"; \
	  $(BIN)/python -m generators $$m --out $(GEN); \
	done

# The one generated target that can be verified rather than eyeballed: emitting a
# module typechecks every file together, so a bad @Relationship inverse or a
# @Model that SwiftData's macro rejects fails here instead of in Xcode. Needs the
# Command Line Tools; nothing is installed by this repo.
# Typecheck only: it writes nothing, and it still expands the macros, which is
# where a bad @Relationship inverse keypath is caught. The harness is skipped
# because it has a @main and no module of its own -- swiftrun compiles it.
swiftcheck:
	@sdk=$$(xcrun --show-sdk-path) && for d in $(GEN)/swift/*/; do \
	  case $$d in *Harness/) continue;; esac; \
	  echo "  $$d"; \
	  swiftc -sdk $$sdk -parse-as-library -typecheck \
	    -module-name $$(basename $$d) $$d*.swift; \
	done
	@echo "  ok"

# Compiling proves the generated code parses; only running it proves SwiftData
# accepts the shapes. swiftcheck passed on a version that trapped on the first
# insert, so this is the gate that matters.
swiftrun:
	@sdk=$$(xcrun --show-sdk-path) && tmp=$$(mktemp -d) && \
	for d in $(GEN)/swift/*Harness/; do \
	  m=$$(basename $$d | sed 's/Harness$$//'); \
	  echo "  $$m"; \
	  swiftc -sdk $$sdk -o $$tmp/$$m $(GEN)/swift/$$m/*.swift $$d*.swift && \
	    $$tmp/$$m $(GEN)/swift/$$m/fixture.json; \
	done; \
	rm -rf $$tmp

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
