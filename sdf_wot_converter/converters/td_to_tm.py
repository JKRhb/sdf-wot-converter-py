from typing import Dict
import copy

from .utility import ensure_value_is_list
from .wot_common import is_thing_collection

from ..validation import (
    validate_thing_description,
    validate_thing_model,
)


def _replace_type(thing_model: Dict):

    thing_model_type = "tm:ThingModel"

    if "@type" not in thing_model:
        thing_model["@type"] = thing_model_type
        return

    json_ld_type = ensure_value_is_list(thing_model["@type"])
    json_ld_type.append(thing_model_type)
    thing_model["@type"] = json_ld_type


def convert_td_collection_to_tm_collection(
    thing_collection: Dict[str, Dict]
) -> Dict[str, Dict]:
    result = {}

    for key, value in thing_collection.items():
        result[key] = convert_td_to_tm(value)

    return result


def convert_td_to_tm(thing_description: Dict) -> Dict:
    if is_thing_collection(thing_description):
        return convert_td_collection_to_tm_collection(thing_description)

    validate_thing_description(thing_description)
    thing_model: Dict = copy.deepcopy(thing_description)
    # TODO: Deal with item links

    _replace_type(thing_model)
    validate_thing_model(thing_model)

    return thing_model
