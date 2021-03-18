#!/bin/bash -e
exec docker run --rm -it -p 8001:8080 \
  -v $PWD/openapi-bundle-cleaned.v1.yaml:/mnt/swagger.yaml:ro mgbi/redoc-cli serve \
	--options.noAutoAuth \
	--options.theme.colors.primary.main=#2C669A \
	--options.theme.rightPanel.backgroundColor=#2C669A \
	--options.theme.logo.gutter=20px \
	--watch \
  /mnt/swagger.yaml
