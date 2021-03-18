#!/bin/bash -e
./swagger-bundle.sh

./redoc-bundle.sh

rm -f openapi-bundle-cleaned.v1.yaml
