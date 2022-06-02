from typing import Dict
import copy

from .utility import (
    initialize_list_field,
    validate_thing_description,
    validate_thing_model,
)


def _replace_type(thing_model: Dict):

    thing_model_type = "tm:ThingModel"

    if "@type" not in thing_model:
        thing_model["@type"] = thing_model_type
        return

    json_ld_type = thing_model["@type"]

    if isinstance(json_ld_type, list) and thing_model_type not in json_ld_type:
        thing_model["@type"].append(thing_model_type)
    elif isinstance(json_ld_type, str) and json_ld_type != thing_model_type:
        thing_model["@type"] = [json_ld_type, thing_model_type]


def convert_td_to_tm(thing_description: Dict) -> Dict:
    validate_thing_description(thing_description)
    thing_model: Dict = copy.deepcopy(thing_description)

    _replace_type(thing_model)
    validate_thing_model(thing_model)

    return thing_model
