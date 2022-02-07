import json
import os
import sys
from collections import defaultdict

import yaml

filePath = sys.argv[1]

with open(filePath) as openapiJson:
    jsonFile = json.load(openapiJson)

wantedPaths = defaultdict(dict)
for path, methods in jsonFile["paths"].items():
    for method, endpoint in methods.items():
        if "internal" not in endpoint["tags"] \
          and "admin" not in endpoint["tags"]:
            wantedPaths[path][method] = endpoint

openapiFile = jsonFile
openapiFile["paths"] = wantedPaths

with open('reference/openapi.json', 'w') as jf:
    json.dump(openapiFile, jf)

with open("reference/openapi.json") as jf, \
  open("reference/openapi.yaml", "w") as yf:
    jsonObj = json.load(jf)
    yaml.dump(jsonObj, yf, sort_keys=False)

# if os.path.exists("files/new_openapi.json"):
#     os.remove("files/new_openapi.json")
