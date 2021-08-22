from typing import (
    Dict,
)
import copy
import json_merge_patch
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


def _replace_meta_data(partial_td, meta_data) -> Dict:
    if meta_data is None:
        return partial_td

    return json_merge_patch.merge(partial_td, meta_data)


def _replace_bindings(partial_td, bindings) -> Dict:
    if bindings is None:
        return partial_td

    return json_merge_patch.merge(partial_td, bindings)


def convert_tm_to_td(
    thing_model: Dict, placeholder_map=None, meta_data=None, bindings=None
) -> Dict:
    partial_td: Dict = copy.deepcopy(thing_model)

    partial_td = wot_common.resolve_extension(partial_td)
    partial_td = _replace_meta_data(partial_td, meta_data)
    partial_td = _replace_bindings(partial_td, bindings)

    replace_type(partial_td)

    partial_td = wot_common.replace_placeholders(partial_td, placeholder_map)

    assert_tm_required(partial_td)

    return partial_td
