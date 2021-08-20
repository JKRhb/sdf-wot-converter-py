from typing import (
    Dict,
)
import json


def replace_type(thing_description: Dict):
    json_ld_type = thing_description["@type"]
    if json_ld_type == "tm:ThingModel":
        json_ld_type = "Thing"
    else:
        json_ld_type = ["Thing" if x == "tm:ThingModel" else x for x in json_ld_type]
    thing_description["@type"] = json_ld_type


def convert_tm_to_td(thing_model: Dict, placeholder_map=None) -> Dict:
    partial_td: Dict = thing_model.copy()

    replace_type(partial_td)

    return partial_td
