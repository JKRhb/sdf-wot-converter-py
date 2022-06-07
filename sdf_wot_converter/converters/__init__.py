from typing import Dict, List, Optional, Tuple, Union

from .tm_to_td import convert_tm_to_td as _convert_tm_to_td
from .td_to_tm import convert_td_to_tm as _convert_td_to_tm
from .tm_to_sdf import convert_wot_tm_to_sdf as _convert_wot_tm_to_sdf
from .sdf_to_tm import convert_sdf_to_wot_tm as _convert_sdf_to_wot_tm

ThingCollection = Dict[str, Dict]


def convert_wot_td_to_wot_tm(input: Union[Dict, ThingCollection]):
    return _convert_td_to_tm(input)


def convert_wot_td_to_sdf(input: Union[Dict, ThingCollection]):
    thing_model = convert_wot_td_to_wot_tm(input)
    return convert_wot_tm_to_sdf(thing_model)


def convert_sdf_to_wot_tm(
    sdf_model: Dict,
    sdf_mapping_files: Optional[List[Dict]] = None,
    origin_url=None,
    set_instance_version=False,
    suppress_roundtripping=False,
):
    return _convert_sdf_to_wot_tm(
        sdf_model,
        origin_url=origin_url,
        sdf_mapping_files=sdf_mapping_files,
        set_instance_version=set_instance_version,
        suppress_roundtripping=suppress_roundtripping,
    )


def convert_sdf_to_wot_td(
    sdf_model: Dict,
    sdf_mapping_files: Optional[List[Dict]] = None,
    origin_url: Optional[str] = None,
    suppress_roundtripping=False,
) -> Dict:
    """Converts an SDF model and one or more SDF mapping files to a Thing Description or Thing Description collection.

    Args:
        sdf_model (Dict): An SDF model.
        sdf_mapping_files (Optional[Union[Dict, List[Dict]]], optional): One or more SDF mapping files. Defaults to None.
        origin_url (str, optional): The URL the SDF model originated from. Defaults to None.

    Returns:
        Dict: A Thing Description or Thing Description collection that is equivalent to the input SDF model and (optional)
                SDF mapping file(s).
    """

    wot_tm = convert_sdf_to_wot_tm(
        sdf_model,
        sdf_mapping_files=sdf_mapping_files,
        origin_url=origin_url,
        set_instance_version=True,
        suppress_roundtripping=suppress_roundtripping,
    )

    # TODO: Deal with Thing Collections
    return convert_wot_tm_to_wot_td(wot_tm)


def convert_wot_tm_to_sdf(
    thing_models: Union[Dict, ThingCollection],
    placeholder_map: Optional[Dict] = None,
) -> Union[Dict, Tuple[Dict, Dict]]:
    # TODO: Also deal with bindings and metadata

    return _convert_wot_tm_to_sdf(
        thing_models,
        placeholder_map=placeholder_map,
    )


def convert_wot_tm_to_wot_td(
    thing_models: Union[Dict, ThingCollection],
    placeholder_map: Optional[Dict] = None,
    meta_data: Optional[Dict] = None,
    bindings: Optional[Dict] = None,
):
    # TODO: Also deal with extensions

    return _convert_tm_to_td(
        thing_models,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
    )
