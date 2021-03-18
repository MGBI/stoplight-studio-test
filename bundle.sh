#!/bin/bash -e
sudo chgrp docker-root openapi-bundle.v1.yaml
docker run --rm -v $PWD:/mnt mgbi/swagger-cli bundle \
  --dereference \
  --type yaml \
  --outfile openapi-bundle.v1.yaml \
  /mnt/reference/openapi.v1.yaml

docker build -t redoc-cli -f redoc_cli/Dockerfile .
# options:
# https://github.com/Redocly/redoc#redoc-options-object
# theme options:
# https://github.com/Redocly/redoc/blob/master/src/theme.ts

# imsig colors:
#	--options.theme.colors.primary.main=#3377b2 \
#	--options.theme.rightPanel.backgroundColor=#3377b2 \

./clean_spec.py openapi-bundle.v1.yaml > openapi-bundle-cleaned.v1.yaml
sudo chgrp docker-root redoc-static.html
docker run --rm -it -v $PWD:/data redoc-cli bundle \
	--options.noAutoAuth \
	--options.theme.colors.primary.main=#2C669A \
	--options.theme.rightPanel.backgroundColor=#2C669A \
	--options.theme.logo.gutter=20px \
  openapi-bundle-cleaned.v1.yaml
rm -f openapi-bundle-cleaned.v1.yaml
