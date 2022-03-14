#!/bin/bash -e
exec docker run --rm -it -v $PWD:/mnt -p 8001:8080 mgbi/redoc-cli serve \
	--options.noAutoAuth \
	--options.theme.colors.primary.main=#2C669A \
	--options.theme.rightPanel.backgroundColor=#2C669A \
	--options.theme.logo.gutter=20px \
	--watch \
  /mnt/openapi-bundle-cleaned.yaml
