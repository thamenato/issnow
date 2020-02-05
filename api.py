from datetime import datetime
from urllib.parse import urlencode

import requests

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
            f"The ISS current location at {time_iso} is "
            f"{position['latitude']}, {position['longitude']}"
        )
    else:
        print(f"Something went wrong: {req.json()['reason']}")


def get_people(args):
    req = requests.get(API_PEOPLE)
    if req.status_code == 200:
        data = req.json()
        print(f"There are currently {data['number']} humans in space. They are:")
        for person in data["people"]:
            print(f" * {person['name']}")
    else:
        print(f"Something went wrong: {req.json()['reason']}")


def get_pass_time(args):
    url = _get_pass_time_url(args)
    if not url:
        return
    req = requests.get(url)
    if req.status_code == 200:
        req = requests.get(url)
        data = req.json()
        req_info = data["request"]
        msg = (
            f"{req_info['passes']} upcoming passes for "
            f"{req_info['latitude']},{req_info['longitude']}"
        )
        if args.alt:
            msg += f" at altitude {args.alt}m"
        print(msg)

        for iss_pass in data["response"]:
            time_iso = datetime.fromtimestamp(iss_pass["risetime"]).isoformat(" ")
            print(f"* {time_iso} for {iss_pass['duration']}s")
    else:
        print(f"Something went wrong: {req.json()['reason']}")


def _get_pass_time_url(args):
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

    return API_PASS_TIME + urlencode(url_params)
