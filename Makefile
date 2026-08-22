# Build glue for the PKM namespace.
#
# Not published (excluded in _config.yml). No Python package lives in this repo —
# invoke LinkML from whatever environment has it installed, e.g. the pkm-neo4j-services
# virtualenv, or `pipx install linkml`.
#
#   make shapes     regenerate SHACL + JSON Schema from schema/pkm.yaml
#   make validate   parse-check every published Turtle file
#   make serve      preview the site locally
#   make clean      remove build output

SCHEMA  := schema/pkm.yaml
SHAPES  := shapes
TTL     := ontology/pkm.ttl vocab/pkm-vocab.ttl taxonomy/pkm-taxonomy.ttl void.ttl

.PHONY: all shapes validate serve clean

all: shapes validate

shapes:
	gen-shacl $(SCHEMA)      > $(SHAPES)/pkm.shacl.ttl
	gen-json-schema $(SCHEMA) > $(SHAPES)/pkm.schema.json

# Requires Apache Jena (`brew install jena`). rdflib is a fine substitute:
#   python -c "import rdflib,sys; [rdflib.Graph().parse(f) for f in sys.argv[1:]]" $(TTL)
validate:
	riot --validate $(TTL) $(SHAPES)/*.ttl

serve:
	bundle exec jekyll serve --livereload

clean:
	rm -rf _site .jekyll-cache
