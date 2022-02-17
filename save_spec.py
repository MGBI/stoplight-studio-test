#!/usr/bin/python3
# This script tries to merge two schemas, existing yaml one, and online
# generated json schema. It copies missing tags and descriptions into endpoints,
# and then overwrite endpoints
import os
import re
import sys
import json
import yaml
from collections import defaultdict

SAVE_ROOT_PATH = None
CONFIG_FILE = "config.yaml"
OPENAPI_KEYS_ORDER = ["openapi", "info", "tags", "x-tagGroups", "paths", "components"]

def str_representer(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


yaml.add_representer(str, str_representer)
yaml.representer.SafeRepresenter.add_representer(str, str_representer)
yaml.add_representer(defaultdict, dict_representer)
yaml.representer.SafeRepresenter.add_representer(defaultdict, dict_representer)


def load(file_path):
    loader = {".yaml": yaml.safe_load, ".json": json.load}
    with open(file_path) as f:
        return loader[os.path.splitext(file_path)[-1]](f)


def save(file_path, data, root_path=True):
    """Save data and return yaml reference"""
    dumper = {
        ".yaml": lambda d, f: yaml.safe_dump(d, f, sort_keys=False, default_flow_style=False, allow_unicode=True),
        ".json": json.dump,
        ".md": lambda d, f: f.write(d),
    }
    if root_path is True:
        dest_path = os.path.join(SAVE_ROOT_PATH, file_path)
    else:
        dest_path = os.path.join(root_path, file_path) if root_path else file_path

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        dumper[os.path.splitext(file_path)[-1]](data, f)
    return {"$ref": file_path}


def normalize_operation_name(operation_id, method=""):
    operation_id = re.sub(r"_+", "-", operation_id.lower())
    operation_id = re.sub(r"^" + method + r"-+", "", operation_id)
    return "-".join([re.sub(r"-+" + method + r"$", "", operation_id), method.upper()])


def get_path_for_path(config, path, method, endpoint):
    directory = config["path-to-directory"]["*"]
    for p, d in config["path-to-directory"].items():
        if path.startswith(p):
            directory = d
            break
    return os.path.join(directory, "paths", normalize_operation_name(endpoint["operationId"], method)) + ".yaml"


def get_path_for_tag(config, tag_name: str):
    directory = config["tag-to-directory"]["*"]
    for t, d in config["tag-to-directory"].items():
        if tag_name == t:
            directory = d
            break
        elif t.startswith("*") and tag_name.endswith(t[1:]):
            directory = d
            tag_name = tag_name[:-len(t)+1]
            break
        elif t.endswith("*") and tag_name.startswith(t[:-1]):
            directory = d
            tag_name = tag_name[len(t) - 1:]
            break
    return os.path.join(directory, "descriptions", f"tag_{tag_name}.md")


def get_path_for_common(config, *args, directory="common"):
    args = [re.sub(r"([A-Z].)", r"-\1", arg).lower() for arg in args]
    return os.path.join(directory, *args)


def save_spec(api_file_path, spec_directory):
    global SAVE_ROOT_PATH
    api = load(api_file_path)
    config = load(os.path.join(spec_directory, CONFIG_FILE))
    SAVE_ROOT_PATH = spec_directory
    SAVE_ROOT_PATH = "save_test"
    # Created properly sorted base dict (order matters!)
    spec = {}
    for key in OPENAPI_KEYS_ORDER:
        spec[key] = api[key]
    # just in case add other keys on the end of the file
    for key in api.keys():
        if key not in spec:
            spec[key] = api[key]


    # INFO (description and version increment)
    file_path = os.path.join("common", "info_description.md")
    spec["info"]["description"] = save(file_path, spec["info"]["description"])
    pre, post = spec["info"]["version"].rsplit('.', 1)
    spec["info"]["version"] = '.'.join([pre, str(int(post) + 1)])

    # PATHS
    spec["paths"] = defaultdict(lambda: defaultdict(dict), api["paths"])
    for path in api["paths"]:
        for method, endpoint in api["paths"][path].items():
            file_path = get_path_for_path(config, path, method, endpoint)
            spec["paths"][path][method] = save(file_path, endpoint)
            # TODO components at endpoints
            # TODO Save components

    # TAGS
    spec["tags"] = []
    for tag in api["tags"]:
        file_path = get_path_for_tag(config, tag["name"])
        tag["description"] = save(file_path, tag.get("description", ""))
        spec["tags"].append(tag)

    # COMPONENTS
    for key, value in spec["components"].items():
        file_path = get_path_for_common(config, key + ".yaml")
        spec["components"][key] = save(file_path, spec["components"][key])
        # TODO Save individual components (schemas in directory)

    # FINALLY
    save(config["spec"], spec)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        save_spec(sys.argv[1], sys.argv[2])
    else:
        sys.stderr.write(
          "USAGE: %s spec.yaml spec/reference/directory\n" % sys.argv[0]
        )
