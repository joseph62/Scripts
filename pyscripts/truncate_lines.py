#! /usr/bin/env python3

import sys
import argparse
import signal

DEFAULT_LINE_LENGTH = 80


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description="Trucate incoming lines to a specified length with an optional suffix"
    )

    parser.add_argument(
        "-l", "--length", help="The maximum length of each line", type=int, default=80
    )
    parser.add_argument(
        "-s",
        "--suffix",
        help="A suffix to add to the end of truncated lines",
        default="",
    )

    return parser.parse_args(args)


def truncate_lines_from_handle(handle, length, suffix):
    for line in handle:
        if len(line) > length:
            yield f"{line[:length-len(suffix)]}{suffix}"
        else:
            yield line


def main(args):
    args = parse_arguments(args)
    for line in truncate_lines_from_handle(sys.stdin, args.length, args.suffix):
        print(line)
    return 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main(sys.argv[1:]))
