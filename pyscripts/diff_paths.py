#! /usr/bin/env python3

import argparse
import os
import sys
import json


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        "Find the difference in structure" " between two paths."
    )
    parser.add_argument(
        "left", type=valid_path, help="The left path operand to compare"
    )
    parser.add_argument(
        "right", type=valid_path, help="The right path operand to compare"
    )
    return parser.parse_args(args)


def valid_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'"{path}" is not a valid path.')
    return path


def get_all_subpaths(path):
    for root, directories, filenames in os.walk(path):
        root = root.replace(path, "", 1).lstrip(os.sep)
        for directory in directories:
            yield os.path.join(root, directory) + os.sep
        for filename in filenames:
            yield os.path.join(root, filename)


def compare_sets(left, right):
    left_only = left - right
    right_only = right - left
    both = left & right
    return left_only, both, right_only


def diff_paths(left_path, right_path):

    left_paths = set(get_all_subpaths(left_path))
    right_paths = set(get_all_subpaths(right_path))
    left_only, both, right_only = compare_sets(left_paths, right_paths)

    print(
        json.dumps(
            {
                "both": sorted(both),
                "left": sorted(left_only),
                "right": sorted(right_only),
            },
            indent=2,
        )
    )


def main(args):
    args = parse_arguments(args)
    try:
        diff_paths(args.left, args.right)
    except Exception as e:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
