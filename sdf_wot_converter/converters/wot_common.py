import os
from typing import Any, Dict, List, Optional
import urllib.parse
import urllib.request
import json_merge_patch
import json
import copy
from jsonpointer import resolve_pointer
from ..validation import validate_thing_model


class PlaceholderException(Exception):
    """Raised when an error occurs during the placeholder replacement process."""

    pass


def _retrieve_thing_model_from_url(tm_url: str):
    with urllib.request.urlopen(tm_url) as url:
        retrieved_thing_model = json.loads(url.read().decode())
        return retrieved_thing_model


def _retrieve_thing_model_from_file_path(file_path: str):
    with open(file_path) as json_file:
        read_thing_model = json.load(json_file)
        return read_thing_model


def retrieve_thing_model(tm_url: str, thing_collection=None):
    url_scheme = urllib.parse.urlparse(tm_url).scheme

    if url_scheme.startswith("http"):
        thing_model = _retrieve_thing_model_from_url(tm_url)
    elif tm_url.startswith("#/") and thing_collection is not None:
        thing_model = resolve_pointer(thing_collection, tm_url[1:])
    else:
        thing_model = _retrieve_thing_model_from_file_path(tm_url)

    validate_thing_model(thing_model)
    return thing_model


def _perform_extension(
    partial_td: Dict,
    extension_href: str,
    extension_link_list: List[str],
    resolve_relative_pointers: bool,
    thing_collection=None,
):
    retrieved_thing_model = retrieve_thing_model(
        extension_href, thing_collection=thing_collection
    )
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
        partial_td = _perform_extension(
            partial_td, extension_href, extension_link_list, resolve_relative_pointers
        )

    return partial_td


def _stringify_boolean(boolean: bool) -> str:
    if boolean:
        return "true"
    else:
        return "false"


def _has_placeholders(serialized_thing_model: str) -> bool:
    return "{{" in serialized_thing_model


def _format_placeholder_value(placeholer_value) -> str:
    if isinstance(placeholer_value, bool):
        return _stringify_boolean(placeholer_value)

    if isinstance(placeholer_value, str):
        return f'"{placeholer_value}"'

    return str(placeholer_value)


def _format_placeholder_key(placeholder_key: str) -> str:
    prefix = "{{"
    suffix = "}}"
    return f'"{prefix}{placeholder_key}{suffix}"'


def _replace_placeholder(
    serialized_thing_model: str, placeholder: str, value: Any
) -> str:
    value = _format_placeholder_value(value)
    placeholder = _format_placeholder_key(placeholder)

    return serialized_thing_model.replace(placeholder, value)


def replace_placeholders(thing_model: dict, placeholders: Optional[Dict[str, Any]]):
    if placeholders is None:
        return thing_model

    serialized_thing_model = json.dumps(thing_model)

    for placeholder, value in placeholders.items():
        serialized_thing_model = _replace_placeholder(
            serialized_thing_model,
            placeholder,
            value,
        )

    if _has_placeholders(serialized_thing_model):
        raise PlaceholderException("Not all placeholders have been replaced!")

    return json.loads(serialized_thing_model)


def _resolve_tm_ref(
    partial_td,
    current_definition,
    resolve_relative_pointers,
    pointer_list=None,
    thing_collection=None,
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
            retrieved_thing_model = retrieve_thing_model(
                root, thing_collection=thing_collection
            )
            original = resolve_pointer(retrieved_thing_model, pointer)
        elif resolve_relative_pointers:
            original = resolve_pointer(partial_td, pointer)

        if original:
            del result["tm:ref"]
            result = json_merge_patch.merge(original, result)

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


def is_thing_collection(thing_collection: Optional[Dict]) -> bool:
    """Determines if a dictionary should be treated as Thing Collection by checking
    a JSON-LD @context is present.

    If Thing Collections should become formally specified, this check needs to be
    reworked.
    """
    return thing_collection is not None and "@context" not in thing_collection


def resolve_sub_things(
    thing_model: Dict, thing_collection=None, placeholder_map=None, replace_href=False
):
    sub_models: Dict = {}

    for link in thing_model.get("links", []):
        if link.get("rel") == "tm:submodel":
            sub_model = retrieve_thing_model(
                link["href"], thing_collection=thing_collection
            )
            replace_placeholders(sub_model, placeholder_map)
            key = _get_submodel_key_from_link(link)
            sub_models[key] = sub_model
            if replace_href:
                link["href"] = f"#/{key}"

    return sub_models


def _get_submodel_key_from_link(link: Dict) -> str:
    key = link.get("instanceName")
    if key is None:
        href: str = link["href"]
        if href.startswith("#/"):
            href = href[1:]
        parsed_href = urllib.parse.urlparse(href)
        key = parsed_href.path
        key = os.path.split(key)[1]
        for file_extension in ["jsonld", "json", "tm", "td"]:
            key = key.replace(f".{file_extension}", "")
    return key
