#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse
from datetime import datetime
from urllib.parse import urlencode

API_BASE = "http://api.open-notify.org"
API_CURR_LOC = f"{API_BASE}/iss-now.json"
API_PASS_TIME = f"{API_BASE}/iss-pass.json?"
API_PEOPLE = f"{API_BASE}/astros.json"


def get_location(args):
    req = requests.get(API_CURR_LOC)
    if req.status_code == 200:
        data = req.json()
        time_iso = datetime.fromtimestamp(data["timestamp"]).isoformat(" ")
        position = data["iss_position"]
        print(
            f"The ISS current location at {time_iso} is {position['latitude']}, {position['longitude']}"
        )


def get_people(args):
    req = requests.get(API_PEOPLE)
    if req.status_code == 200:
        data = req.json()
        print(f"There are currently {data['number']} humans in space. They are:")
        for person in data["people"]:
            print(f" * {person['name']}")


def get_pass_time(args):
    if not (-80 <= args.lat <= 80) or not (-180 <= args.lon <= 180):
        print(
            "Invalid position! LATITUDE must be -80..80 and LONGITUDE must be -180..180"
        )
        return

    url_params = {"lat": args.lat, "lon": args.lon}
    if args.n is not None:
        if 1 <= args.n <= 100:
            url_params["n"] = args.n
        else:
            print("Invalid value for n, must be between 1..100")
            return
    if args.alt is not None:
        if 0 < args.alt <= 10000:  # the API says 0..10,000 but 0 returns error
            url_params["alt"] = args.alt
        else:
            print("Invalid value for alt, must be between 0..10,000")
            return

    url = API_PASS_TIME + urlencode(url_params)
    req = requests.get(url)
    if req.status_code == 200:
        req = requests.get(url)
        data = req.json()
        req_info = data["request"]
        msg = f"{req_info['passes']} upcoming passes for {req_info['latitude']},{req_info['longitude']}"
        if args.alt:
            msg += f" at altitude {args.alt}m"
        print(msg)

        for iss_pass in data["response"]:
            time_iso = datetime.fromtimestamp(iss_pass["risetime"]).isoformat(" ")
            print(f"* {time_iso} for {iss_pass['duration']}s")
    else:
        print(f"Something went wrong: {req.json()['reason']}")


parser = argparse.ArgumentParser(prog="issnow")
subparsers = parser.add_subparsers()

parser_curr_loc = subparsers.add_parser("loc", help="Current Location of the ISS")
parser_curr_loc.set_defaults(func=get_location)

parser_people = subparsers.add_parser("people", help="")
parser_people.set_defaults(func=get_people)

parser_pass = subparsers.add_parser("pass")
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
