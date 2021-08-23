from typing import (
    Dict,
    List,
)
import urllib.request
import json_merge_patch
import jsonschema
import json
from ..schemas import tm_schema
import copy
from jsonpointer import resolve_pointer


def _retrieve_thing_model(tm_url: str):
    with urllib.request.urlopen(tm_url) as url:
        retrieved_thing_model = json.loads(url.read().decode())
        jsonschema.validate(retrieved_thing_model, tm_schema.tm_schema)
        return retrieved_thing_model


def perform_extension(
    partial_td: Dict,
    extension_href: str,
    extension_link_list: List[str],
    resolve_relative_pointers: bool,
):
    retrieved_thing_model = _retrieve_thing_model(extension_href)
    merged_partial_td = json_merge_patch.merge(retrieved_thing_model, partial_td)
    return resolve_extension(
        merged_partial_td,
        resolve_relative_pointers=resolve_relative_pointers,
        extension_link_list=extension_link_list,
    )


def resolve_extension(
    partial_td: Dict, resolve_relative_pointers=True, extension_link_list=None
):
    partial_td = _resolve_tm_ref(partial_td, partial_td, resolve_relative_pointers)

    if "links" not in partial_td:
        return partial_td

    if extension_link_list is None:
        extension_link_list = []

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
        assert extension_href not in extension_link_list
        extension_link_list.append(extension_href)
        partial_td = perform_extension(
            partial_td, extension_href, extension_link_list, resolve_relative_pointers
        )

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
        elif isinstance(value, str):
            value = f'"{value}"'

        thing_model_as_string = thing_model_as_string.replace(
            '"{{' + placeholder + '}}"', str(value)
        )

    # TODO: Raise exception instead
    assert "{{" not in thing_model_as_string, "Not all placeholders have been replaced!"

    return json.loads(thing_model_as_string)


def _resolve_tm_ref(
    partial_td, current_definition, resolve_relative_pointers, pointer_list=None
):
    result = copy.deepcopy(current_definition)

    if pointer_list is None:
        pointer_list = []

    if "tm:ref" in result:
        retrieved_thing_model = None
        tm_ref = result["tm:ref"]
        assert tm_ref not in pointer_list
        pointer_list.append(tm_ref)
        root, pointer = tuple(tm_ref.split("#", 1))
        original = None
        if root:
            retrieved_thing_model = _retrieve_thing_model(root)
            original = resolve_pointer(retrieved_thing_model, pointer)
        elif resolve_relative_pointers:
            original = resolve_pointer(partial_td, pointer)

        if original:
            del result["tm:ref"]
            result = json_merge_patch.merge(original, result)

            # TODO: Check if this is actually working
            if "tm:ref" in result:
                if root:
                    result = _resolve_tm_ref(
                        retrieved_thing_model,
                        result,
                        resolve_relative_pointers,
                        pointer_list=pointer_list,
                    )
                else:
                    result = _resolve_tm_ref(
                        partial_td,
                        result,
                        True,
                        pointer_list=pointer_list,
                    )

    for key, value in result.items():
        if isinstance(value, dict):
            result[key] = _resolve_tm_ref(partial_td, value, resolve_relative_pointers)

    return result
