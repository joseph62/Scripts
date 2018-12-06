#! /usr/bin/env python3
"""
Read stdin, turn input into 8 bit binary, output binary to stdout
"""

import sys
import itertools

def chunks(iterable, size):
    return iter(itertools.zip_longest(*([iter(iterable)] * size)))

def main(argv):
    # Reading stdin and encoding in bytes
    bytes_ = sys.stdin.read().encode()
    # format each byte as a length 8 binary number
    binary = chunks((f'{byte:08b}' for byte in bytes_), 8)
    sys.stdout.write(
        '\n'.join(
            ' '.join(col for col in row if col) for row in binary
        )
    )
    sys.stdout.write('\n')
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
