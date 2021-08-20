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


def _stringify_boolean(boolean: bool) -> str:
    if boolean:
        return "true"
    else:
        return "false"


def replace_placeholders(thing_model, placeholders):
    if placeholders is None:
        return thing_model
    import re

    thing_model_as_string = json.dumps(thing_model)

    for placeholder, value in placeholders.items():
        # TODO: Placeholder pattern should be validated

        # assert isinstance(placeholder, str)
        # assert re.fullmatch('[A-Z0-9_]+',
        #                     placeholder), "Placeholders must follow the pattern \"PLACEHOLDER_IDENTIFIER\""
        # assert isinstance(value, str)

        if isinstance(value, bool):
            value = _stringify_boolean(value)

        thing_model_as_string = thing_model_as_string.replace(
            '"{{' + placeholder + '}}"', str(value)
        )

    # TODO: Raise exception instead
    assert "{{" not in thing_model_as_string, "Not all placeholders have been replaced!"

    return json.loads(thing_model_as_string)


def convert_tm_to_td(thing_model: Dict, placeholder_map=None) -> Dict:
    partial_td: Dict = thing_model.copy()

    replace_type(partial_td)

    partial_td = replace_placeholders(partial_td, placeholder_map)

    return partial_td
