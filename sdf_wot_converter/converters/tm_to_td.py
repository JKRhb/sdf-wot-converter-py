from typing import (
    Dict,
    List,
)
import copy
import json_merge_patch
from jsonpointer import resolve_pointer
from jsonschema import ValidationError

from .utility import ensure_value_is_list
from ..validation import validate_thing_description, validate_thing_model
from .wot_common import (
    is_thing_collection,
    replace_placeholders,
    resolve_extension,
    resolve_sub_things,
)


def replace_type(thing_description: Dict):
    json_ld_type = ensure_value_is_list(thing_description["@type"])
    result = list(filter(lambda item: item != "tm:ThingModel", json_ld_type))
    if len(result) == 0:
        del thing_description["@type"]
        return

    thing_description["@type"] = result


def _replace_version(partial_td):
    version = partial_td.get("version")

    if version is None:
        return

    if "model" in version and "instance" not in version:
        version["instance"] = version["model"]


def _assert_tm_optional(partial_td: Dict, remove_not_required_affordances: bool):
    if "tm:optional" not in partial_td:
        return

    optional_affordances = partial_td["tm:optional"]

    all_affordances = set()
    for affordance_type in ["actions", "properties", "events"]:
        affordances = [
            f"/{affordance_type}/{affordance}"
            for affordance in partial_td.get(affordance_type, dict()).keys()
        ]
        all_affordances.update(affordances)

    tm_required = list(all_affordances.difference(optional_affordances))

    for required_affordance_pointer in list(tm_required):
        assert (
            resolve_pointer(partial_td, required_affordance_pointer, None) is not None
        )

    if remove_not_required_affordances:
        for affordance_type in ["properties", "actions", "events"]:
            affordances = partial_td.get(affordance_type, {})
            not_required_affordance_keys: List[str] = []
            for affordance_key in affordances:
                affordance_pointer = f"/{affordance_type}/{affordance_key}"
                if affordance_pointer not in tm_required:
                    not_required_affordance_keys.append(affordance_key)
            for affordance_key in not_required_affordance_keys:
                del affordances[affordance_key]

    del partial_td["tm:optional"]


def _prevent_required_tm_field_removal(document_to_apply: dict):
    """Checks that none of the values within the dictionary is `None` to prevent the
    JSON Merge Patch algorithm from removing any fields, which is forbidden during the
    TM -> TD derivation process.
    """
    for key, value in document_to_apply.items():
        if value is None:
            raise ValidationError(
                "All required fields in a TM MUST be taken over into the resulting TD."
                "Applying th additional information to the TD would have resulted in"
                f'the removal the field "{key}", which is not allowed.'
            )

        if isinstance(value, dict):
            _prevent_required_tm_field_removal(value)


def _replace_meta_data(partial_td, meta_data) -> Dict:
    if meta_data is None:
        return partial_td

    _prevent_required_tm_field_removal(meta_data)

    return json_merge_patch.merge(partial_td, meta_data)


def _replace_bindings(partial_td: dict, bindings: dict) -> Dict:
    if bindings is None:
        return partial_td

    _prevent_required_tm_field_removal(bindings)

    return json_merge_patch.merge(partial_td, bindings)


def _resolve_submodels(thing_model: dict, thing_collection: dict):
    links = thing_model.get("links")

    if links is None:
        return

    for link in links:
        if link.get("rel") == "tm:submodel":
            # TODO: Apply proper mapping
            link["rel"] = "item"


def convert_tm_collection_to_td_collection(
    thing_collection, remove_not_required_affordances=False
):
    result = {}

    for key, value in thing_collection.items():
        _resolve_submodels(value, result)
        result[key] = convert_tm_to_td(
            value, remove_not_required_affordances=remove_not_required_affordances
        )

    return result


def convert_tm_to_td(
    thing_model: Dict,
    placeholder_map=None,
    meta_data=None,
    bindings=None,
    root_model_key="root",
    remove_not_required_affordances=False,
) -> Dict:
    if is_thing_collection(thing_model):
        return convert_tm_collection_to_td_collection(
            thing_model, remove_not_required_affordances=remove_not_required_affordances
        )

    sub_models = resolve_sub_things(thing_model, replace_href=True)
    if len(sub_models) > 0:
        sub_models[root_model_key] = thing_model
        for key, value in sub_models.items():
            sub_models[key] = resolve_extension(value, resolve_relative_pointers=True)
        return convert_tm_collection_to_td_collection(
            sub_models, remove_not_required_affordances=remove_not_required_affordances
        )

    validate_thing_model(thing_model)
    partial_td: Dict = copy.deepcopy(thing_model)

    partial_td = resolve_extension(partial_td)
    partial_td = _replace_meta_data(partial_td, meta_data)
    partial_td = _replace_bindings(partial_td, bindings)

    replace_type(partial_td)

    partial_td = replace_placeholders(partial_td, placeholder_map)

    _replace_version(partial_td)

    _assert_tm_optional(partial_td, remove_not_required_affordances)

    validate_thing_description(partial_td)

    return partial_td
