#!/bin/bash -e
./swagger-bundle.sh reference/openapi.v1.yaml

./redoc-bundle.sh openapi-bundle-cleaned.v1.yaml

rm -f openapi-bundle-cleaned.v1.yaml
