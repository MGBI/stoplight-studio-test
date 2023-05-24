#!/usr/bin/python3

import os
import sys
import yaml

INTERNAL_DOCS = bool(int(os.getenv("INTERNAL_DOCS", 0)))
print(f"Internal docs: {INTERNAL_DOCS}")

def load(file_path):
    with open(file_path) as file:
        return yaml.safe_load(file)

def save(file_path, context):
    with open(file_path, "w") as file:
        return yaml.safe_dump(context, file, sort_keys=False)

def remove_from_spec(file_path):
    # load content from file
    context = load(file_path)

    # looking for `update_first_id` parameter & delete that
    for index in range(len(context["paths"]["/v2/announcements"]["get"]["parameters"])):
        if context["paths"]["/v2/announcements"]["get"]["parameters"][index]["name"] == "first_update_id":
            del context["paths"]["/v2/announcements"]["get"]["parameters"][index]
            break

    # looking for "X-Vendor-Authorization" or "authorized_vendors" and removing them
    if not INTERNAL_DOCS:
        for path in context["paths"].values():
            for method in path.values():
                for parameter in method.get("parameters", []):
                    if parameter.get("name") == "X-Vendor-Authorization":
                        method["parameters"].remove(parameter)
                        break
                for model in method.get("components", {}).get("schemas", {}).values():
                    model.get("properties", {}).pop("authorized_vendors", None)
                    model.get("example", {}).pop("authorized_vendors", None)
                    for requirement in model.get("required", []):
                        if requirement == "authorized_vendors":
                            model["required"].remove("authorized_vendors")
        
        for model in context.get("components", {}).get("schemas", {}).values():
            for requirement in model.get("required", []):
                if requirement == "authorized_vendors":
                    model["required"].remove("authorized_vendors")
                    break
            for property in model.get("properties", {}):
                if property == "authorized_vendors":
                    model["properties"].pop("authorized_vendors")
                    break
            model.get("example", {}).pop("authorized_vendors", None)

    # dump to file
    save(file_path, context)



if __name__ == "__main__":
    if len(sys.argv) == 2:
        remove_from_spec(sys.argv[1])
    else:
        sys.stderr.write(
            "USAGE: %s file_path\n" % sys.argv[0]
        )
