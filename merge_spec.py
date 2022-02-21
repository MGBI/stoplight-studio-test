#!/usr/bin/python
# This script tries to merge two schemas, existing yaml one, and online
# generated json schema. It copies missing tags and descriptions into endpoints,
# and then overwrite endpoints
import json
import yaml
import sys
import os
from collections import defaultdict


V_SUFFIX = "_iapi"
OLD_API_ROOT_PATH = "/v2/"
NEW_API_ROOT_PATH = "/v2/"


def load(file_path):
    loader = {".yaml": yaml.safe_load, ".json": json.load}
    with open(file_path) as f:
        return loader[os.path.splitext(file_path)[-1]](f)


def transformation_of_openapi_v2(old_file_path, new_file_path):
    old_openapi = load(old_file_path)
    new_openapi = load(new_file_path)

    old_api = {}
    for path, methods in old_openapi["paths"].items():
        for method, endpoint in methods.items():
            old_api[method + " " + path.replace(OLD_API_ROOT_PATH, "", 1)] = endpoint

    new_api = {}
    for path, methods in new_openapi["paths"].items():
        for method, endpoint in methods.items():
            new_api[method + " " + path.replace(NEW_API_ROOT_PATH, "", 1)] = endpoint

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
            endpoint["tags"] = [tag + V_SUFFIX for tag in endpoint["tags"]]

    new_openapi["paths"] = wanted_paths

    # appending new paths and components to existing ones
    old_openapi["paths"].update(new_openapi["paths"])

    # components
    for name, component in new_openapi.get("components", {}).items() :
        if name in old_openapi["components"]:
            old_component = old_openapi["components"][name]
            for field in component:
                if field == "example":
                    for f in component[field]:
                        component[field][f] = old_component[field].get(f, component[field][f])
                if field == "properties":
                    for p in component[field]:
                        for pname in old_component[field].get(p, []):
                            component[field][p][pname] = old_component[field][p][pname]
            for field in old_component:
                if field not in ["example", "properties"]:
                    component[field] = old_component[field]
        old_openapi["components"][name] = component

    # adding tags from path to set without public, internal and admin
    tags = set()
    for path, methods in new_openapi["paths"].items():
        for method, endpoint in methods.items():
            tags = tags.union(endpoint["tags"])
    tags = tags.difference(["public" + V_SUFFIX, "internal" + V_SUFFIX, "admin" + V_SUFFIX])

    # adding new values to tags field without duplicates
    for tag in tags.difference({tag["name"] for tag in old_openapi["tags"]}):
        old_openapi["tags"].append(
          {"name": tag, "x-displayName": tag.replace(V_SUFFIX, "").capitalize()}
        )

    # adding tags from set to tags in x-tagGroups
    for tag_group in old_openapi["x-tagGroups"]:
        if tag_group["name"] == "MSIG API V2":
           old_openapi["x-tagGroups"].pop(old_openapi["x-tagGroups"].index(tag_group))
           break
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
