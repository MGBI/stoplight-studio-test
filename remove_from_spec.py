#!/usr/bin/python3

import sys
import yaml


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

    # dump to file
    save(file_path, context)



if __name__ == "__main__":
    if len(sys.argv) == 2:
        remove_from_spec(sys.argv[1])
    else:
        sys.stderr.write(
            "USAGE: %s file_path\n" % sys.argv[0]
        )
