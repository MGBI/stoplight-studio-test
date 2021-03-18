#!/bin/bash -e
sudo chgrp docker-root openapi-bundle.v1.yaml
docker run --rm -v $PWD:/mnt mgbi/swagger-cli bundle \
  --dereference \
  --type yaml \
  --outfile openapi-bundle.v1.yaml \
  /mnt/$1

./clean_spec.py openapi-bundle.v1.yaml > openapi-bundle-cleaned.v1.yaml
