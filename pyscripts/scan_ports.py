#! /usr/bin/env python3

import socket
import argparse
import sys

def port_number(number):
    number = int(number)
    if number < 0 or number > 65535:
        raise argparse.ArgumentTypeError(f'{port} must be in range 0-65535')
    return number

def get_arguments(args):
    parser = argparse.ArgumentParser(description="Scan ports for a given host in a given range")
    parser.add_argument("-t", "--target", help="The address of the machine to scan",
                            required=True)
    parser.add_argument("-v", "--verbose", default=0, action="count",
            help="Specify level of verbosity. Can be specified multiple times.")
    parser.add_argument("--timeout", help="Set the timeout per request in seconds",
                            default=0.3, type=float)
    port_group = parser.add_mutually_exclusive_group(required=True)
    port_group.add_argument("-r", "--range", help="The port range to scan",
                                nargs=2, type=port_number, metavar=('START','END'))
    port_group.add_argument("-p", "--port", help="The port to scan", type=port_number)
    port_group.add_argument("--all", help="Scan ports range 0-65535",
                                action='store_true')
    args = parser.parse_args(args)

    if args.all:
        args.start, args.end = (0, 65535)
    elif args.range:
        args.start, args.end = args.range
        if args.start > args.end:
            args.end, args.start = (args.start, args.end)
    else:
        args.start, args.end = (args.port, args.port)
    args.end += 1

    return args

def scan_port(target, port):
    s = socket.socket()
    try:
        s.connect((target,port))
        return True
    except ConnectionRefusedError as e:
        return False
    except socket.timeout as e:
        return False

def scan_ports(target, range_):
    return ((scan_port(target, port), port) for port in range_)

def main(args):
    args = get_arguments(args)
    socket.setdefaulttimeout(args.timeout)

    for success, port in scan_ports(args.target, range(args.start, args.end)):
        if success:
            if args.verbose > 0:
                print(f"Port {port} is open for tcp traffic")
            else:
                print(f"{port}")
        elif not success and args.verbose > 1:
            print(f"Port {port} is closed for tcp traffic")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
