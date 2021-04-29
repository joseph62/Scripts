#! /usr/bin/env python3

import re
import sys
import csv
import json
import logging
import argparse

UNTIL_SPACE = "([^ ]+)"
QUOTED = '"([^"]+)"'
PATTERN = f"([^,]+(?:, [^,]+)*|[^ ]+).*?{UNTIL_SPACE}.*?{UNTIL_SPACE}.*?{UNTIL_SPACE}.*?{UNTIL_SPACE}.*?\\[([^\\]]+)\\].*?{QUOTED}.*?{UNTIL_SPACE}.*?{UNTIL_SPACE}.*?{QUOTED}.*?{QUOTED}(.*)"
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
    parser.add_argument("paths", help="The path to the Tomcat access log", nargs="+")
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument(
        "--json", help="Format the output as JSON", action="store_true"
    )
    format_group.add_argument(
        "--csv", help="Format the output as CSV", action="store_true"
    )
    return parser.parse_args(args)


def write_as_json(path, traffic):
    logging.info("Writing jsonified traffic")

    with open(f"{path}.json", "w") as f:
        json.dump(traffic, f)


def write_as_csv(path, traffic, fieldnames=KEYS):
    logging.info("Writing csv traffic")

    with open(f"{path}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(traffic)


def write_failed_traffic(path, failed_traffic):
    logging.warning(f"Writing {len(failed_traffic)} lines that failed to parse")

    with open(f"{path}.failed", "w") as f:
        f.writelines(failed_traffic)


def parse_tomcat_log_file(path, succeeded_formatter, failed_formatter):
    logging.info(f"Reading {path}")
    with open(path) as f:
        raw_traffic_lines = [line for line in f]
    logging.info(f"Done reading {path}")

    logging.info(f"Parsing {len(raw_traffic_lines)} lines")
    traffic_groups = [(line, re.match(PATTERN, line)) for line in raw_traffic_lines]
    logging.info(f"Done parsing lines")

    failed_traffic = [line for line, match in traffic_groups if match is None]

    if failed_traffic:
        failed_formatter(path, failed_traffic)

    succeeded_traffic = [
        dict(zip(KEYS, match.groups()))
        for _, match in traffic_groups
        if match is not None
    ]

    succeeded_formatter(path, succeeded_traffic)


def main(args):
    logging.basicConfig(level=logging.INFO)
    succeeded_formatter = write_as_csv if args.csv else write_as_json

    for path in args.paths:
        try:
            parse_tomcat_log_file(path, succeeded_formatter, write_failed_traffic)
        except FileNotFoundError as e:
            logging.error(e)

    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args(sys.argv[1:])))
