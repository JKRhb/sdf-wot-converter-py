from typing import Dict, List, Optional
import urllib.request
import json_merge_patch
import json
import copy
from jsonpointer import resolve_pointer
from ..validation import validate_thing_model


def _retrieve_thing_model_from_url(tm_url: str):
    with urllib.request.urlopen(tm_url) as url:
        retrieved_thing_model = json.loads(url.read().decode())
        validate_thing_model(retrieved_thing_model)
        return retrieved_thing_model


def _retrieve_thing_model_from_file_path(file_path: str):
    with open(file_path) as json_file:
        read_thing_model = json.load(json_file)
        validate_thing_model(read_thing_model)
        return read_thing_model


def retrieve_thing_model(tm_url: str, thing_collection=None):
    url_scheme = urllib.parse.urlparse(tm_url).scheme

    if url_scheme.startswith("http"):
        return _retrieve_thing_model_from_url(tm_url)
    elif tm_url.startswith("#/") and thing_collection is not None:
        return resolve_pointer(thing_collection, tm_url[1:])
    else:
        return _retrieve_thing_model_from_file_path(tm_url)


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


def replace_placeholders(thing_model, placeholders):
    if placeholders is None:
        return thing_model

    thing_model_as_string = json.dumps(thing_model)

    for placeholder, value in placeholders.items():
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


def is_thing_collection(thing_collection: Optional[Dict]) -> bool:
    """Determines if a dictionary should be treated as Thing Collection by checking
    a JSON-LD @context is present.

    If Thing Collections should become formally specified, this check needs to be
    reworked.
    """
    return thing_collection is not None and "@context" not in thing_collection
