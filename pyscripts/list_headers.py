#! /usr/bin/env python3
import argparse
import sys
import os
import csv

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='list headers for all given csv files')
    parser.add_argument('files',nargs='+',help='a csv file to read')
    return parser.parse_args(argv[1:])

def get_header(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames

def main(argv):
    args = get_arguments(argv)
    for filename in args.files:
        fieldnames = get_header(filename)
        print(f'{filename}:')
        for name in fieldnames:
            print(f'\t"{name}"')
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
