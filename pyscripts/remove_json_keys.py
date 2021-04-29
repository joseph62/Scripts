#! /usr/bin/env python3

import sys
import click
import signal
import json
from pprint import pprint


def remove_dict_keys_recursive(obj, keys_to_remove):
    if isinstance(obj, dict):
        return {
            key: remove_dict_keys_recursive(value, keys_to_remove)
            for key, value in obj.items()
            if key not in keys_to_remove
        }
    elif isinstance(obj, list):
        return [remove_dict_keys_recursive(value, keys_to_remove) for value in obj]
    else:
        return obj


@click.command()
@click.argument("json_file", type=click.File("r"))
@click.argument("keys_file", type=click.File("r"))
def remove_json_keys(json_file, keys_file):
    """
    Remove specified keys from json file
    """
    obj = json.load(json_file)
    keys = {key.strip() for key in keys_file}
    print(json.dumps(remove_dict_keys_recursive(obj, keys), indent=2))


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    remove_json_keys()
    sys.exit(0)
