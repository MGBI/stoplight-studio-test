#!/bin/bash -e
sudo chgrp docker openapi-bundle.yaml || true
sudo chgrp docker-root openapi-bundle.yaml || true
docker run --rm --volume $PWD:/mnt --workdir /mnt mgbi/swagger-cli bundle \
  --type yaml \
  --outfile openapi-bundle.yaml \
  reference/openapi.yaml
  # --outfile openapi-bundle.iapi.yaml \

# wget https://nornik51.mgbi.pl/openapi.json -O iapi.json
# ./merge_spec.py openapi-bundle.yaml iapi.json > openapi-bundle.iapi.yaml

mkdir backup 2> /dev/null && true
cp -r reference "backup/reference-`date +'%Y-%m-%d_%H-%M-%S'`"
# ./save_spec.py openapi-bundle.iapi.yaml reference/
./save_spec.py openapi-bundle.yaml reference/
# ./remove_from_spec.py openapi-bundle.iapi.yaml
./remove_from_spec.py openapi-bundle.yaml
# ./clean_spec.py openapi-bundle.iapi.yaml > openapi-bundle-cleaned.yaml
./clean_spec.py openapi-bundle.yaml > openapi-bundle-cleaned.yaml
