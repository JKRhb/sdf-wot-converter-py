from typing import (
    Dict,
)
import copy
from jsonpointer import resolve_pointer
from . import wot_common


def replace_type(thing_description: Dict):
    json_ld_type = thing_description["@type"]
    if json_ld_type == "tm:ThingModel":
        json_ld_type = "Thing"
    else:
        json_ld_type = ["Thing" if x == "tm:ThingModel" else x for x in json_ld_type]
    thing_description["@type"] = json_ld_type


def assert_tm_required(partial_td):
    if "tm:required" not in partial_td:
        return

    for required_affordance_pointer in partial_td["tm:required"]:
        root, pointer = tuple(required_affordance_pointer.split("#", 1))
        assert root == ""
        assert resolve_pointer(partial_td, pointer, None) is not None

    del partial_td["tm:required"]


def convert_tm_to_td(thing_model: Dict, placeholder_map=None) -> Dict:
    partial_td: Dict = copy.deepcopy(thing_model)

    partial_td = wot_common.resolve_extension(partial_td)

    replace_type(partial_td)

    partial_td = wot_common.replace_placeholders(partial_td, placeholder_map)

    assert_tm_required(partial_td)

    return partial_td
