#!/bin/bash -e
sudo chgrp docker openapi-bundle.v1.yaml || true
sudo chgrp docker-root openapi-bundle.v1.yaml || true
docker run --rm --volume $PWD:/mnt --workdir /mnt mgbi/swagger-cli bundle \
  --dereference \
  --type yaml \
  --outfile openapi-bundle.v1.yaml \
  reference/openapi.v1.yaml

./new_clean_spec.py openapi-bundle.v1.yaml reference/openapi.json > openapi-bundle.v2.yaml

./clean_spec.py openapi-bundle.v2.yaml > openapi-bundle-cleaned.v2.yaml
