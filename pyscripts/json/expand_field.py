#! /usr/bin/env python3
import argparse
import json
import sys


def get_arguments(args):
    parser = argparse.ArgumentParser(description="Expand a field from the given JSON")
    parser.add_argument("-k", "--key", help="The key to expand", required=True)
    json_input = parser.add_mutually_exclusive_group(required=True)
    json_input.add_argument("--stdin", help="Read JSON from stdin", action="store_true")
    json_input.add_argument("--json", help="JSON string", type=str)
    json_input.add_argument("--file", help="JSON file", type=argparse.FileType("r"))

    args = parser.parse_args(args)

    if args.stdin:
        args.json = json.loads(sys.stdin.read())
    elif args.file:
        args.json = json.load(args.file)
    else:
        args.json = json.loads(args.json)

    return args


def expand_dict_key(key, dict_):
    return dict_.get(key) if isinstance(dict_, dict) else None


def main(args):
    args = get_arguments(args)
    result = expand_dict_key(args.key, args.json)
    if not result:
        return 1
    else:
        print(json.dumps(result, indent=2))
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
