# Build glue for the PKM namespace.
#
# Not published (excluded in _config.yml). No Python package lives in this repo —
# invoke LinkML from whatever environment has it installed, e.g. the pkm-neo4j-services
# virtualenv, or `pipx install linkml`.
#
#   make check      validate the SKOS Editor export -> reports/vocab-check.md
#   make build      generate every published artifact from the export
#   make review     family-grouped reading sheet -> reports/vocab-review.md
#   make shapes     regenerate SHACL + JSON Schema from schema/pkm.yaml
#   make models     regenerate dev artifacts from the LinkML domain modules
#   make artifacts  render the Obsidian/Neo4j/Ladybug/TypeQL/Swift templates
#   make swiftcheck compile the generated Swift against the macOS SDK
#   make swiftrun   run the generated harness against the fixture
#   make validate   parse-check every published Turtle file
#   make validate-skos  validate with the SKOS Editor's own engine (second opinion)
#   make notes      regenerate the Obsidian term stubs in the WarrenWeb vault
#   make hub        fill the generated blocks in that vault's vocabulary hub
#   make vault      mirror the generated Obsidian artifacts into that vault
#   make gems       install the gems GitHub Pages builds this site with
#   make site       build the site and check the term URIs resolve
#   make serve      preview the site locally (PORT=4001 if 4000 is taken)
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

# Ruby for the local site build. Pages builds this site with 3.3.4; macOS ships
# 2.6, which cannot resolve the gem set, so this is Homebrew's keg-only ruby@3.3
# reached by path -- nothing has to be on PATH and the system ruby is untouched.
# Recursive `=`, not `:=`, so `brew --prefix` runs only for the targets that
# need it rather than on every `make check`.
RUBY_BIN = $(shell brew --prefix ruby@3.3)/bin
BUNDLE   = $(RUBY_BIN)/bundle

# Vendored into the repo rather than the global gem dir, so the site's gems
# cannot drift with whatever else gets installed. Gitignored, and excluded in
# _config.yml -- Jekyll 3 drops its own default excludes once that list exists.
export BUNDLE_PATH = vendor/bundle

# Overridable because 4000 is Jekyll's default and therefore the port everything
# else also picks: `make serve PORT=4001`. Without this the target fails with a
# bind error on any machine already running something there.
PORT ?= 4000

# Jekyll's `--livereload` binds this as well as PORT, and it is invisible until
# it collides: a second `make serve` fails even on a different PORT while an
# earlier one is up. Overridable for the same reason PORT is.
LIVERELOAD_PORT ?= 35729

# The SKOS Editor checkout, for `validate-skos`. The vocabulary is authored in
# that editor (see CONTRIBUTING.md), and it ships its own validator -- so this
# is a second opinion on the same graph from the tool upstream, covering five
# SKOS integrity conditions checks.py does not test. Not installed by this
# repo, and its venv is uv-managed with no pip: add pyshacl with
# `uv pip install --python $(SKOS_ENGINE)/.venv/bin/python pyshacl==0.40.1`.
SKOS_ENGINE ?= $(HOME)/Projects/Python/skos

# Obsidian vault directory the term stubs are mirrored into. Override on the
# command line for a different vault: make notes NOTES_OUT=/path/to/pkm/vocab
NOTES_OUT := $(HOME)/Obsidian/WarrenWeb/pkm/vocab

# The hand-written hub note that sits above those stubs. A file, not a
# directory, and not inside NOTES_OUT -- `notes` prunes anything there that it
# did not generate, and this page must survive that.
HUB_OUT := $(HOME)/Obsidian/WarrenWeb/pkm/vocab.md

# Where `vault` mirrors the generated Obsidian tree. A directory this repo owns
# outright, not a folder shared with hand-written notes: the target prunes, so
# anything here that the generator no longer emits is deleted. That is the point
# -- the vault had a stale Ingredient.base and six ingredient notes from before
# Ingredient stopped being a note type, and a copy without pruning leaves a Base
# listing files the schema no longer describes.
#
# Override for a different vault: make vault VAULT_OUT=/path/to/vault/_PKM
VAULT_OUT := $(HOME)/Obsidian/WarrenWeb/+/_PKM

# Hand-authored Turtle plus the generated bulk dump. The 241 per-term files under
# vocab/terms/ are checked by `validate` through the wildcard, not listed here.
TTL     := void.ttl ontology/pkm.ttl taxonomy/pkm-taxonomy.ttl \
           vocab/pkm-vocab.ttl agents/index.ttl resources/index.ttl

.PHONY: all check build review shapes models artifacts swiftcheck swiftrun validate validate-skos notes hub vault gems site serve clean

all: build validate

# Exits non-zero when there are errors, so it doubles as a pre-commit gate.
check:
	@mkdir -p reports
	-$(VOCAB) check $(EXPORT) --format markdown -o reports/vocab-check.md
	$(VOCAB) check $(EXPORT)

# A reading aid, not a gate: it prints suffix families side by side so drift
# between terms that are meant to be parallel is visible across a row. Nothing
# here can fail, which is why it is not wired into `all`.
review:
	@mkdir -p reports
	$(VOCAB) review $(EXPORT) -o reports/vocab-review.md

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

# Deliberately not in `all`: it depends on a checkout this repo does not own,
# the same contract `swiftcheck` has with the Command Line Tools. The engine is
# tested for before it is invoked -- without the guard the shell fails with
# `No such file or directory` and exit 127 before Python runs, so the script's
# own skip path is never reached and a missing engine reads as a broken build.
validate-skos:
	@if [ -x "$(SKOS_ENGINE)/.venv/bin/python" ]; then \
	  PYTHONPATH=$(SKOS_ENGINE)/api $(SKOS_ENGINE)/.venv/bin/python \
	    scripts/validate_upstream.py $(EXPORT) vocab/pkm-vocab.ttl; \
	else \
	  echo "  no SKOS engine at $(SKOS_ENGINE) — skipping upstream validation"; \
	fi

# Mirrors the PUBLISHED vocabulary rather than the export, so the stubs carry
# URIs and dates that actually resolve. Deliberately not a dependency of `all`:
# it writes outside this repo, into a vault that syncs to a public site, so it
# stays an explicit action. Stale stubs are pruned; run with --dry-run first if
# the vocabulary has had terms renamed.
notes:
	$(VOCAB) notes vocab/pkm-vocab.ttl --out $(NOTES_OUT)

# The hub note one level above the stubs, which `notes` does not write: it is
# hand-written, and only its facts are generated -- counts, version, top
# concepts, collection membership -- into three named marker blocks. Prose
# around them is left alone. Fails with the markers to paste if they are absent,
# rather than appending a block to the end of someone's page.
#
# Like `notes` and `vault`, deliberately not part of `all`: it writes outside
# this repo, into a vault with Sync and Publish both enabled. `make hub DRY=-n`
# reports without writing.
hub:
	$(VOCAB) hub vocab/pkm-vocab.ttl --out $(HUB_OUT) $(if $(DRY),--dry-run,)

# Puts the generated Obsidian tree where Obsidian can actually open it, which is
# the only way to find out whether a Base renders: the templates are YAML that
# looks right and fails in the app, which is how the groupBy defect survived a
# reading. Depends on `artifacts` because mirroring a stale generated/ tree is
# the failure this is meant to catch, and regenerating costs nothing.
#
# Like `notes`, deliberately not part of `all`: it writes outside this repo,
# into a vault with Sync and Publish both enabled. Dry run first --
# `make vault DRY=-n` -- to see what would be pruned.
#
# rsync per leaf directory rather than one pass over the tree, because --delete
# is scoped to what it is given: a single pass at $(VAULT_OUT) would prune any
# hand-written file that had been added alongside, and the three leaves are the
# generator's own. Blank templates land under templates/Seed to match the layout
# already in the vault; note that Obsidian's Templates plugin reads x/Templates,
# so these are reference scaffolds rather than templates the picker will offer.
vault: artifacts
	@test -d $(GEN)/obsidian || { echo "no $(GEN)/obsidian — run make artifacts"; exit 1; }
	@mkdir -p "$(VAULT_OUT)/bases" "$(VAULT_OUT)/notes" "$(VAULT_OUT)/templates/Seed"
	@rsync -a $(DRY) -i --delete $(GEN)/obsidian/bases/     "$(VAULT_OUT)/bases/"
	@rsync -a $(DRY) -i --delete $(GEN)/obsidian/notes/     "$(VAULT_OUT)/notes/"
	@rsync -a $(DRY) -i --delete $(GEN)/obsidian/templates/ "$(VAULT_OUT)/templates/Seed/"
	@echo "  $(VAULT_OUT)"

# One-time, and after any change to the Gemfile. Needs `brew install ruby@3.3`.
gems:
	$(BUNDLE) install

# Builds the site the way Pages builds it, then checks the one thing no other
# target can: that each term page's `permalink` really does land at
# vocab/{Term}/index.html, and that the Turtle is still served from
# vocab/terms/{Term}.ttl. Those two are exactly "a browser gets a readable page"
# and "an RDF client still gets Turtle" -- the whole point of the term URIs.
#
# Deliberately not part of `all`: like notes and vault, it needs something this
# repo does not install.
site:
	$(BUNDLE) exec jekyll build
	@built=$$(ls -d _site/vocab/*/ 2>/dev/null | grep -cvE '/(terms|browse)/$$'); \
	 want=$$(ls vocab/terms/*.md | wc -l | tr -d ' '); \
	 test "$$built" = "$$want" || \
	   { echo "  $$built term pages built, expected $$want"; exit 1; }; \
	 test -f _site/vocab/terms/DayMealPlan.ttl || \
	   { echo "  per-term Turtle missing from _site"; exit 1; }; \
	 echo "  _site ok: $$built term pages, per-term Turtle intact"

# Serves what `make site` builds. The `/pkm/` is `baseurl`, which Pages sets for
# a project site and the local build has to match or the CSS 404s -- which is
# also why the built site cannot be browsed by opening files from _site, and why
# a Markdown preview shows neither the A-Z anchors (kramdown generates those
# heading ids) nor working term links (they are relative to /vocab/). This target
# is the only way to see what a reader sees, so it prints where to go.
#
# The one thing worth clicking is a term URI, /pkm/vocab/DayMealPlan/, since that
# path exists only because of `permalink`.
#
# The ports are checked before anything is printed, because printing them first
# is how this went wrong: 4000 is Jekyll's default and therefore contended, and
# on this machine an Apollo Router `rover dev` session holds it. Jekyll could not
# bind, the browser reached the router instead, and the router's CSRF protection
# answered "Access denied" -- under a list of five URLs this target had just
# promised. A wrong URL list is worse than none, because it sends the reader to
# another program's error page and hides the real failure below the invitation.
serve:
	@if command -v lsof >/dev/null 2>&1; then 	  for spec in "$(PORT):PORT" "$(LIVERELOAD_PORT):LIVERELOAD_PORT"; do 	    port=$${spec%%:*}; var=$${spec##*:}; 	    held=$$(lsof -nP -iTCP:$$port -sTCP:LISTEN 2>/dev/null | awk 'NR==2 {print $$1" (pid "$$2")"}'); 	    if [ -n "$$held" ]; then 	      echo "  port $$port is already held by $$held"; 	      echo "  retry with a free one:  make serve $$var=$$(($$port+1))"; 	      exit 1; 	    fi; 	  done; 	fi
	@echo "  vocabulary   http://127.0.0.1:$(PORT)/pkm/vocab/"
	@echo "  map          http://127.0.0.1:$(PORT)/pkm/vocab/browse/map/"
	@echo "  hierarchy    http://127.0.0.1:$(PORT)/pkm/vocab/browse/hierarchy/"
	@echo "  collections  http://127.0.0.1:$(PORT)/pkm/vocab/browse/collections/"
	@echo "  all terms    http://127.0.0.1:$(PORT)/pkm/vocab/browse/all/"
	@echo "  a term       http://127.0.0.1:$(PORT)/pkm/vocab/DayMealPlan/"
	@echo ""
	$(BUNDLE) exec jekyll serve --livereload --port $(PORT) \
	  --livereload-port $(LIVERELOAD_PORT)

clean:
	rm -rf _site .jekyll-cache .sass-cache
