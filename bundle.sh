#!/bin/bash
docker build -t redoc-cli -f redoc_cli/Dockerfile .
# options:
# https://github.com/Redocly/redoc#redoc-options-object
# theme options:
# https://github.com/Redocly/redoc/blob/master/src/theme.ts
docker run --rm -it  -v $PWD:/data redoc-cli bundle \
	--options.noAutoAuth \
	--options.theme.colors.primary.main=black \
	/data/reference/krs-rdf/openapi.v1.yaml
