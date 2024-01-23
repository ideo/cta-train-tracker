import sys
import pprint

from src.locations import get_cta_train_locations
from src import utils

def main(simplify):
    locations = get_cta_train_locations(simplify=simplify)
    return locations



if __name__ == "__main__":
    simplify = "--simplify" in sys.argv
    locations = main(simplify)

    if "--json" in sys.argv:
        # Write to json
        utils.write_to_json(locations, "train_locations.json")

    else:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(locations)