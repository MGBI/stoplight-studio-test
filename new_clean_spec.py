#!/usr/bin/python
import json
import sys
from collections import defaultdict

import yaml

SUFFIX = "_V2"


def transformation_of_openapi_v2(old_file_path, new_file_path):

    with open(new_file_path) as openapiJson:
        new_openapi = json.load(openapiJson)

    with open(old_file_path) as yamlFile:
        old_openapi = yaml.safe_load(yamlFile)

    old_api = {}
    for path, methods in old_openapi["paths"].items():
        for method, endpoint in methods.items():
            old_api[method + " " + path.split("msig", 1)[-1]] = endpoint

    new_api = {}
    for path, methods in new_openapi["paths"].items():
        for method, endpoint in methods.items():
            new_api[method + " " + path.split("msig", 1)[-1]] = endpoint

    # here we are taking description and other useful info from old endpoints
    # to our new
    for endpoint, new_values in new_api.items():
        old_values = old_api.get(endpoint, None)
        if old_values is not None:
            if "description" not in new_values and "description" in old_values:
                new_values["description"] = old_values["description"]
            if "parameters" in new_values:
                for new_item in new_values["parameters"]:
                    new_name = new_item.get("name")
                    for old_item in new_item and old_values["parameters"] or []:
                        if new_name == old_item["name"]:
                            if new_item["schema"].get("description") is None \
                              and old_item["schema"].get(
                              "description") is not None:
                                new_item["schema"]["description"] = old_item[
                                  "schema"]["description"]
                            if new_item["schema"].get("example") is None and \
                              old_item["schema"].get("example") is not None:
                                new_item["schema"]["example"] = old_item["schema"][
                                  "example"]
                            if new_item.get("description") is None and old_item.get(
                              "description") is not None:
                                new_item["description"] = old_item["description"]

    # here we remove admin and internal tags from paths field in new_openapi
    wanted_paths = defaultdict(dict)
    for path, methods in new_openapi["paths"].items():
        for method, endpoint in methods.items():
            if "internal" not in endpoint["tags"] \
              and "admin" not in endpoint["tags"]:
                wanted_paths[path][method] = endpoint
            endpoint["tags"] = [tag + SUFFIX for tag in endpoint["tags"]]

    new_openapi["paths"] = wanted_paths

    # the api version is overwritten in the info field
    info_section = defaultdict(dict)
    for info, fields in new_openapi["info"].items():
        info_section[info] = fields
    old_openapi["info"]["version"] = info_section["version"]

    # appending new paths and components to existing ones
    old_openapi["paths"].update(new_openapi["paths"])
    old_openapi["components"].update(new_openapi["components"])

    # adding tags from path to set without public, internal and admin
    tags = set()
    for path, methods in new_openapi["paths"].items():
        for method, endpoint in methods.items():
            tags = tags.union(endpoint["tags"])
    tags = tags.difference(["public_V2", "internal_V2", "admin_V2"])

    # adding new values to tags field without duplicates
    for tag in tags.difference({tag["name"] for tag in old_openapi["tags"]}):
        old_openapi["tags"].append(
          {"name": tag, "x-displayName": tag.replace("_V2", "").capitalize()}
        )

    # adding tags from set to tags in x-tagGroups
    old_openapi["x-tagGroups"].append(
      {"name": "MSIG API V2", "tags": list(tags)})

    # at the end we dump changes to old openapi
    yaml.safe_dump(old_openapi, sys.stdout, sort_keys=False)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        transformation_of_openapi_v2(sys.argv[1], sys.argv[2])
    else:
        sys.stderr.write(
          "USAGE: %s old_file_path new_file_path\n" % sys.argv[0]
        )
