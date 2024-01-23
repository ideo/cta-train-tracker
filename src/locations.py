from datetime import datetime

from .cta_api import CTA_API

import pprint
pp = pprint.PrettyPrinter(indent=4)


def get_cta_train_locations(simplify=False):
    response = get_locations()
    train_locations = parse_response(response, simplify=simplify)
    return train_locations


def get_locations():
    cta_api = CTA_API()
    response = cta_api.get_locations()
    return response


def parse_response(response, simplify=False):
    # Parse response
    train_locations = []
    for packet in response["ctatt"]["route"]:
        line = {}
        line["name"] = packet["@name"]
        line["trains"] = []
        if "train" in packet:
            for train in packet["train"]:
                line["trains"].append(clean_train_packet(train))
        train_locations.append(line)

    if simplify:
        train_locations = simplify_response(train_locations)

    return train_locations


def simplify_response(train_locations):
    for line in train_locations:
        if "trains" in line:
            line["trains"] = [(pkt["lat"], pkt["lon"]) for pkt in line["trains"]]
    return train_locations
    

def clean_train_packet(train):
    _format = "%Y-%m-%dT%H:%M:%S"
    try:
        cleaned_packet = {
            "lat":                      float(train["lat"]),
            "lon":                      float(train["lon"]),
            "is_delayed":               train["isDly"],
            "is_approaching":           train["isApp"],
            "heading":                  int(train["heading"]),
            "destination":              train["destNm"],
            "destination_id":           train["destSt"],
            "next_station":             train["nextStaNm"],
            "next_station_id":          int(train["nextStaId"]),
            "next_stop_id":             int(train["nextStpId"]),
            "train_route_code":         int(train["trDr"]),
            "run_number":               int(train["rn"]),
            "predicted_arrival_time":   datetime.strptime(train["arrT"], _format),
            "time_of_prediction":       datetime.strptime(train["prdt"], _format),
        }
    except TypeError:
        cleaned_packet = train
        print("train: ", train)

    # if cleaned_packet["lat"] == 0:
    #     print("Latitude is null.")

    return cleaned_packet