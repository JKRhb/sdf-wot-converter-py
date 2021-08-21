from typing import (
    Dict,
)
import json
import copy
import urllib.request
import json_merge_patch
import jsonschema
from ..schemas import tm_schema


def replace_type(thing_description: Dict):
    json_ld_type = thing_description["@type"]
    if json_ld_type == "tm:ThingModel":
        json_ld_type = "Thing"
    else:
        json_ld_type = ["Thing" if x == "tm:ThingModel" else x for x in json_ld_type]
    thing_description["@type"] = json_ld_type


def _retrieve_thing_model(tm_url: str):
    with urllib.request.urlopen(tm_url) as url:
        retrieved_thing_model = json.loads(url.read().decode())
        jsonschema.validate(retrieved_thing_model, tm_schema.tm_schema)
        return retrieved_thing_model


def perform_extension(partial_td, extension_href):
    retrieved_thing_model = _retrieve_thing_model(extension_href)
    merged_partial_td = json_merge_patch.merge(retrieved_thing_model, partial_td)
    return resolve_extension(merged_partial_td)


def resolve_extension(partial_td: Dict):
    if "links" not in partial_td:
        return partial_td

    extension_href = None
    new_links = []

    for link in partial_td.get("links", []):
        if "tm:extends" == link.get("rel"):
            extension_href = link["href"]
        else:
            new_links.append(link)

    if new_links:
        partial_td["links"] = new_links
    else:
        del partial_td["links"]

    if extension_href:
        partial_td = perform_extension(partial_td, extension_href)

    return partial_td


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
    partial_td: Dict = copy.deepcopy(thing_model)

    partial_td = resolve_extension(partial_td)

    replace_type(partial_td)

    partial_td = replace_placeholders(partial_td, placeholder_map)

    return partial_td
