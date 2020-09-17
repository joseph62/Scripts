#! /usr/bin/env python3

import re
import json
import argparse

parser = argparse.ArgumentParser(
    description="Parse default Tomcat access log into JSON"
)
parser.add_argument("path", help="The path to the Tomcat access log")
args = parser.parse_args()

until_space = "([^ ]+)"
quoted = '"([^"]+)"'
pattern = f"({until_space}|[^,]+(, [^,]+)*) {until_space} {until_space} {until_space} {until_space} \\[([^\\]]+)\\] {quoted} {until_space} {until_space} {quoted} {quoted} (.*)"
keys = (
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

print(f"Reading {args.path}")
with open(args.path) as f:
    raw_traffic_lines = [line for line in f]
print(f"Done reading {args.path}")

print(f"Parsing {len(raw_traffic_lines)} lines")
traffic_groups = [(line, re.match(pattern, line)) for line in raw_traffic_lines]
print(f"Done parsing lines")

failed_traffic = [line for line, match in traffic_groups if match is None]


if failed_traffic:
    print(f"Writing {len(failed_traffic)} lines that failed to parse")

    with open(f"{args.path}.failed", "w") as f:
        f.writelines(failed_traffic)

    print(f"Transforming successful matches into json")

successful_traffic = [
    dict(zip(keys, match.groups())) for _, match in traffic_groups if match is not None
]

print("Writing jsonified traffic")

with open(f"{args.path}.json", "w") as f:
    json.dump(successful_traffic, f)

print("DONE!")
