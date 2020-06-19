#!/bin/bash
docker build -t redoc-cli -f redoc_cli/Dockerfile .
# options:
# https://github.com/Redocly/redoc#redoc-options-object
# theme options:
# https://github.com/Redocly/redoc/blob/master/src/theme.ts

# imsig colors:
#	--options.theme.colors.primary.main=#3377b2 \
#	--options.theme.rightPanel.backgroundColor=#3377b2 \

./clean_spec.py reference/krs-rdf/openapi.v1.yaml > \
	reference/krs-rdf/.cleaned.yaml
docker run --rm -it  -v $PWD:/data redoc-cli bundle \
	--options.noAutoAuth \
	--options.theme.colors.primary.main=#2C669A \
	--options.theme.rightPanel.backgroundColor=#2C669A \
	--options.theme.logo.gutter=20px \
	reference/krs-rdf/.cleaned.yaml
rm -f reference/krs-rdf/.cleaned.yaml
