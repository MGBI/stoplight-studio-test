#!/bin/bash -e
sudo chgrp docker openapi-bundle.yaml || true
sudo chgrp docker-root openapi-bundle.yaml || true
docker run --rm --volume $PWD:/mnt --workdir /mnt mgbi/swagger-cli bundle \
  --dereference \
  --type yaml \
  --outfile openapi-bundle.yaml \
  reference/openapi.yaml

wget http://szczur41.mgbi.pl:8080/openapi.json -O iapi.json
./merge_spec.py openapi-bundle.yaml iapi.json > openapi-bundle.iapi.yaml

mkdir backup 2> /dev/null && true
cp -r reference "backup/reference-`date +'%Y-%m-%d_%H-%M-%S'`"
./save_spec.py openapi-bundle.iapi.yaml reference/

./clean_spec.py openapi-bundle.iapi.yaml > openapi-bundle-cleaned.yaml