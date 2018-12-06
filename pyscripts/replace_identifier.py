#! /usr/bin/env python3

import argparse
import os
import sys

def get_arguments(args):
    parser = argparse.ArgumentParser(
        description='Expand appname identifier into the application name'
    )

    parser.add_argument('-p', '--path', default=os.getcwd(),
        help='The path to work with. Current working directory by default'
    )

    parser.add_argument('-i', '--identifier', required=True,
        help='The identifier to substitute.'
    )

    parser.add_argument('-s', '--substitute', required=True,
        help='The value to replace the identifier with.'
    )

    parser.add_argument('--dry-run', default=False, action='store_true',
        help='Print changes that would be made without making them'
    )

    return parser.parse_args(args)

def replace_identifier(path, identifier, substitute, dry_run=False):
    files = os.listdir(path)
    replace_pairs = []

    for file in files:
        new_file = file.replace(identifier, substitute)
        old_path = os.path.join(path, file)
        new_path = os.path.join(path, new_file)
        if not dry_run:
            os.replace(old_path, new_path)
        replace_pairs.append((file, new_file))

    return replace_pairs

def main(args):
    args = get_arguments(args)
    output = replace_identifier(args.path, args.identifier,
                                args.substitute, args.dry_run)

    for old_file, new_file in output:
        print(f'"{old_file}" -> "{new_file}"')

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
