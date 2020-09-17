#! /usr/bin/env python3

import re
import sys
import csv
import json
import argparse

UNTIL_SPACE = "([^ ]+)"
QUOTED = '"([^"]+)"'
PATTERN = f"([^,]+(?:, [^,]+)*|[^ ]+) {UNTIL_SPACE} {UNTIL_SPACE} {UNTIL_SPACE} {UNTIL_SPACE} \\[([^\\]]+)\\] {QUOTED} {UNTIL_SPACE} {UNTIL_SPACE} {QUOTED} {QUOTED} (.*)"
KEYS = (
    "x-forwarded-for",
    "remote-hostname",
    "local-ip",
    "username",
    "authenticated-user",
    "timestamp",
    "request",
    "status-code",
    "bytes-sent",
    "user-agent",
    "referer",
    "time-to-process",
)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Parse default Tomcat access log")
    parser.add_argument("path", help="The path to the Tomcat access log")
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument(
        "--json", help="Format the output as JSON", action="store_true"
    )
    format_group.add_argument(
        "--csv", help="Format the output as CSV", action="store_true"
    )
    return parser.parse_args(args)


def write_as_json(path, traffic):
    print("Writing jsonified traffic")

    with open(path, "w") as f:
        json.dump(traffic, f)


def write_as_csv(path, traffic, fieldnames=KEYS):
    print("Writing csv traffic")

    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(traffic)


def main(args):
    print(f"Reading {args.path}")
    with open(args.path) as f:
        raw_traffic_lines = [line for line in f]
    print(f"Done reading {args.path}")

    print(f"Parsing {len(raw_traffic_lines)} lines")
    traffic_groups = [(line, re.match(PATTERN, line)) for line in raw_traffic_lines]
    print(f"Done parsing lines")

    failed_traffic = [line for line, match in traffic_groups if match is None]

    if failed_traffic:
        print(f"Writing {len(failed_traffic)} lines that failed to parse")

        with open(f"{args.path}.failed", "w") as f:
            f.writelines(failed_traffic)

        print(f"Transforming successful matches into json")

    successful_traffic = [
        dict(zip(KEYS, match.groups()))
        for _, match in traffic_groups
        if match is not None
    ]

    if args.csv:
        write_as_csv(f"{args.path}.csv", successful_traffic)
    else:
        write_as_json(f"{args.path}.json", successful_traffic)

    print("DONE!")
    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args(sys.argv[1:])))
