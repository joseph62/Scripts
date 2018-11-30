import argparse
import os
import sys
import json

def valid_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'"{path}" is not a valid path.')
    return path

def get_all_subpaths(path):
    for root, directories, filenames in os.walk(path):
        root = root.replace(path, '', 1).lstrip('/')
        for directory in directories:
            yield os.path.join(root, directory) + os.sep
        for filename in filenames:
            yield os.path.join(root, filename)

def get_arguments(args):
    parser = argparse.ArgumentParser('Find the difference in structure'
                                        ' between two paths.')
    parser.add_argument('left', type=valid_path,
                        help='A path to compare structure')
    parser.add_argument('right', type=valid_path,
                        help='A path to compare structure')
    return parser.parse_args(args)

def compare_sets(left, right):
    left_only = left - right
    right_only = right - left
    both = left & right
    return left_only, both, right_only

def main(args):
    args = get_arguments(args)

    left_paths = set(get_all_subpaths(args.left))
    right_paths = set(get_all_subpaths(args.right))
    left_only, both, right_only = compare_sets(left_paths, right_paths)
    print(json.dumps({
        'only_left' : sorted(left_only),
        'only_right' : sorted(right_only),
        'both' : sorted(both),
    }))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
