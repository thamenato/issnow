#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from api import get_location, get_pass_time, get_people

parser = argparse.ArgumentParser(prog="issnow")
subparsers = parser.add_subparsers()

parser_curr_loc = subparsers.add_parser("loc", help="Current ISS location over Earth")
parser_curr_loc.set_defaults(func=get_location)

parser_people = subparsers.add_parser(
    "people", help="The number of people in space at this moment"
)
parser_people.set_defaults(func=get_people)

parser_pass = subparsers.add_parser(
    "pass", help="Predictions when the ISS will fly over a particular location"
)
parser_pass.add_argument(
    "lat", help="The latitude of the place to predict passes", type=float
)
parser_pass.add_argument(
    "lon", help="The longitude of the place to predict passes", type=float
)
parser_pass.add_argument(
    "--alt", help="The altitude of the place to predict passes", type=float
)
parser_pass.add_argument("--n", help="The number of passes to return", type=int)
parser_pass.set_defaults(func=get_pass_time)


if __name__ == "__main__":
    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        print("Missing argument...")
        parser.print_usage()
