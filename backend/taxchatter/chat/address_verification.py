import json
import os

import googlemaps
from dotenv import load_dotenv

load_dotenv()


GMAPS = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(f"{FILE_DIR}/../data/urzedy_loc.json") as f:
    all_urzedy = json.load(f)


def get_closest_urzad(client, customer_addr: str):
    geocode_result = client.geocode(customer_addr)
    addr_loc = geocode_result[0]["geometry"]["location"]
    closest_urzad = None
    urzedy_distances = []
    for urzad in all_urzedy:
        dist = (urzad["lat"] - addr_loc["lat"]) ** 2 + (urzad["lon"] - addr_loc["lng"]) ** 2
        urzedy_distances.append(dist)

    # get 3 closest indexes
    closest_indexes = sorted(range(len(urzedy_distances)), key=lambda i: urzedy_distances[i])[:3]
    closest_urzad = [all_urzedy[i] for i in closest_indexes]
    return closest_urzad


def determine_if_address_valid(client, addr: str):
    addressvalidation_result = client.addressvalidation(
        [addr],
        regionCode="PL",
        enableUspsCass=False,
    )
    _ = addressvalidation_result["result"]["address"]["addressComponents"]
    if "hasUnconfirmedComponents" in addressvalidation_result["result"]["verdict"]:
        return False
    else:
        addres_formatted = addressvalidation_result["result"]["address"]["formattedAddress"]
        print(addres_formatted)
        return True


def get_address_components(client, addr: str):
    geocode_result = client.geocode(addr)
    addr_comps = {}
    for comp in geocode_result[0]["address_components"]:
        addr_comps[comp["types"][0]] = comp["short_name"]
    map_key = {
        "administrative_area_level_2": "powiat",
        "administrative_area_level_1": "województwo",
        "locality": "miasto",
        "route": "ulica",
    }
    # rename keys
    remapped_addr_comps = {}
    for k, v in addr_comps.items():
        if k in map_key:
            remapped_addr_comps[map_key[k]] = v
        else:
            remapped_addr_comps[k] = v
    return remapped_addr_comps
