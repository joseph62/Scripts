#! /usr/bin/env python3
"""
Read stdin, turn input into 8 bit binary, output binary to stdout
"""

import sys
import argparse
import itertools
import signal


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


def chunks(iterable, size):
    return iter(itertools.zip_longest(*([iter(iterable)] * size)))


def byte_to_binary(byte):
    return f"{byte:08b}"


def byte_stream_iter(input_stream, chunk_size=8):
    b = input_stream.buffer.read(chunk_size)
    while b:
        yield b
        b = input_stream.buffer.read(chunk_size)


def bytes_to_binary(input_stream, output_stream, width):
    for bytes_ in byte_stream_iter(input_stream, width):
        output_stream.write(" ".join(byte_to_binary(byte) for byte in bytes_))
        output_stream.write("\n")


def main(argv):
    args = parse_arguments(argv[1:])
    bytes_to_binary(args.in_file, args.out_file, args.width)
    return 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main(sys.argv))
