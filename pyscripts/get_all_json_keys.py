#! /usr/bin/env python3

import sys
import click
import signal
import json


def get_dict_keys_recursive(obj):
    keys = set()
    if isinstance(obj, dict):
        for key in obj.keys():
            keys.add(key)
        for value in obj.values():
            keys = keys.union(get_dict_keys_recursive(value))
    elif isinstance(obj, list):
        for value in obj:
            keys = keys.union(get_dict_keys_recursive(value))

    return keys


@click.command()
@click.argument("json_file", type=click.File("r"))
def test_script(json_file):
    """
    A script that uses click
    """
    json_obj = json.load(json_file)
    keys = get_dict_keys_recursive(json_obj)
    for key in keys:
        print(key)


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    test_script()
    sys.exit(0)
