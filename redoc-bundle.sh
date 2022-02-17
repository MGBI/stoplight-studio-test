#!/bin/bash -e
# options:
# https://github.com/Redocly/redoc#redoc-options-object
# theme options:
# https://github.com/Redocly/redoc/blob/master/src/theme.ts

# imsig colors:
#	--options.theme.colors.primary.main=#3377b2 \
#	--options.theme.rightPanel.backgroundColor=#3377b2 \

sudo chgrp docker-root redoc-static.html || true
docker run --rm -it --volume $PWD:/mnt --workdir /mnt mgbi/redoc-cli bundle \
	--options.noAutoAuth \
	--options.theme.colors.primary.main=#2C669A \
	--options.theme.rightPanel.backgroundColor=#2C669A \
	--options.theme.logo.gutter=20px \
  openapi-bundle-cleaned.yaml
