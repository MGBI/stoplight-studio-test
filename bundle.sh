#!/bin/bash -e
./swagger-bundle.sh

./redoc-bundle.sh

rm -f openapi-bundle.yaml
rm -f iapi.json
rm -f openapi-bundle.iapi.yaml
