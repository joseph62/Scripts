#! /usr/bin/env python3

import sys
import signal
import argparse


def parse_arguments(args):
    parser = argparse.ArgumentParser(description="Convert an input stream into binary")
    parser.add_argument(
        "in_file",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Input file (default stdin)",
    )
    parser.add_argument(
        "out_file",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file (default stdout)",
    )
    parser.add_argument(
        "-w", "--width", type=int, default=8, help="Number of columns (default 8)"
    )
    return parser.parse_args(args)


def dos_to_unix(input_stream, output_stream):
    output_stream.writelines(
        line.replace("\n", "\r\n") for line in input_stream.readlines
    )


def main(args):
    args = parse_arguments(args)
    try:
        dos_to_unix(args.in_file, args.out_file)
    except Exception as e:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
