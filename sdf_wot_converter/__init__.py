import json
import argparse
import sys
from jsonschema import validate
from typing import Dict, Callable, Optional
from .converters import (
    sdf_to_wot,
    wot_to_sdf,
    tm_to_td,
)

from .schemas.sdf_validation_schema import sdf_validation_schema
from .schemas.td_schema import td_schema
from .schemas.tm_schema import tm_schema


def _load_model(input_path: str) -> Dict:  # pragma: no cover
    file = open(input_path)
    return json.load(file)


def _save_model(output_path: str, model: Dict, indent=4):  # pragma: no cover
    file = open(output_path, "w")
    json.dump(model, file, indent=indent)


def _load_optional_json_file(path: Optional[str]) -> Optional[Dict]:
    json_data = None
    if path:
        json_data = _load_model(path)

    return json_data


def _load_optional_json(json_string: Optional[str]) -> Optional[Dict]:
    json_data = None
    if json_string:
        json_data = json.loads(json_string)

    return json_data


def _convert_and_validate(
    from_model: Dict,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
    **kwargs,
):
    validate(from_model, from_schema)
    to_model = converter_function(from_model, **kwargs)
    validate(to_model, to_schema)
    return to_model


def _convert_model_from_path(
    from_path: str,
    to_path: str,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
    **kwargs,
):  # pragma: no cover
    from_model = _load_model(from_path)
    to_model = _convert_and_validate(
        from_model,
        from_schema,
        to_schema,
        converter_function,
        **kwargs,
    )
    _save_model(to_path, to_model)


def _convert_model_from_json(
    from_model_json: str,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
    indent=4,
    **kwargs,
):  # pragma: no cover
    from_model = json.loads(from_model_json)
    to_model = _convert_and_validate(
        from_model,
        from_schema,
        to_schema,
        converter_function,
        **kwargs,
    )
    return json.dumps(to_model, indent=indent)


def convert_sdf_to_wot_tm(input: Dict):
    return _convert_and_validate(
        input, sdf_validation_schema, tm_schema, sdf_to_wot.convert_sdf_to_wot_tm
    )


def convert_wot_tm_to_sdf(input: Dict, placeholder_map=None):
    return _convert_and_validate(
        input,
        tm_schema,
        sdf_validation_schema,
        wot_to_sdf.convert_wot_tm_to_sdf,
        placeholder_map=placeholder_map,
    )


def convert_wot_tm_to_td(
    input: Dict, placeholder_map=None, meta_data=None, bindings=None
):
    return _convert_and_validate(
        input,
        tm_schema,
        td_schema,
        tm_to_td.convert_tm_to_td,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
    )


def convert_sdf_to_wot_tm_from_path(from_path: str, to_path: str):
    return _convert_model_from_path(
        from_path,
        to_path,
        sdf_validation_schema,
        tm_schema,
        sdf_to_wot.convert_sdf_to_wot_tm,
    )


def convert_wot_tm_to_sdf_from_path(
    from_path: str, to_path: str, placeholder_map_path=None
):
    placeholder_map = _load_optional_json_file(placeholder_map_path)
    return _convert_model_from_path(
        from_path,
        to_path,
        tm_schema,
        sdf_validation_schema,
        wot_to_sdf.convert_wot_tm_to_sdf,
        placeholder_map=placeholder_map,
    )


def convert_wot_tm_to_wot_td_from_path(
    from_path: str,
    to_path: str,
    placeholder_map_path=None,
    meta_data_path=None,
    bindings_path=None,
):
    placeholder_map = _load_optional_json_file(placeholder_map_path)
    meta_data = _load_optional_json_file(meta_data_path)
    bindings = _load_optional_json_file(bindings_path)
    return _convert_model_from_path(
        from_path,
        to_path,
        tm_schema,
        td_schema,
        tm_to_td.convert_tm_to_td,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
    )


def convert_sdf_to_wot_tm_from_json(input: str, indent=4):
    return _convert_model_from_json(
        input,
        sdf_validation_schema,
        tm_schema,
        sdf_to_wot.convert_sdf_to_wot_tm,
        indent=indent,
    )


def convert_wot_tm_to_sdf_from_json(input: str, indent=4):

    return _convert_model_from_json(
        input,
        tm_schema,
        sdf_validation_schema,
        wot_to_sdf.convert_wot_tm_to_sdf,
        indent=indent,
    )


def convert_wot_tm_to_wot_td_from_json(
    input: str,
    indent=4,
    placeholder_map_json=None,
    meta_data_json=None,
    bindings_json=None,
):
    placeholder_map = _load_optional_json(placeholder_map_json)
    meta_data = _load_optional_json(meta_data_json)
    bindings = _load_optional_json(bindings_json)
    return _convert_model_from_json(
        input,
        tm_schema,
        td_schema,
        tm_to_td.convert_tm_to_td,
        indent=indent,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
    )


def _parse_arguments(args):
    parser = argparse.ArgumentParser(
        description="Convert from SDF to WoT and vice versa."
    )

    from_group = parser.add_mutually_exclusive_group(required=True)
    from_group.add_argument(
        "--from-sdf", metavar="SDF", dest="from_sdf", help="SDF input JSON file"
    )
    from_group.add_argument(
        "--from-tm", metavar="TM", dest="from_tm", help="WoT TM input JSON file"
    )

    to_group = parser.add_mutually_exclusive_group(required=True)
    to_group.add_argument(
        "--to-tm", metavar="TM", dest="to_tm", help="WoT TM output file"
    )
    to_group.add_argument(
        "--to-td", metavar="TD", dest="to_td", help="WoT TD output file"
    )
    to_group.add_argument(
        "--to-sdf", metavar="SDF", dest="to_sdf", help="SDF output file"
    )

    parser.add_argument(
        "--placeholder",
        dest="placeholder_map",
        help="Optional placeholder map for TM-to-TD conversion",
    )

    parser.add_argument(
        "--meta-data",
        dest="meta_data",
        help="Additional meta-data for TM-to-TD conversion",
    )

    parser.add_argument(
        "--bindings",
        dest="bindings",
        help="Additional bindings information for TM-to-TD conversion",
    )

    return parser.parse_args(args)


def _use_converter_cli(args):  # pragma: no cover
    if args.from_sdf and args.to_tm:
        convert_sdf_to_wot_tm_from_path(args.from_sdf, args.to_tm)
    elif args.from_tm:
        if args.to_sdf:
            convert_wot_tm_to_sdf_from_path(
                args.from_tm, args.to_sdf, placeholder_map_path=args.placeholder_map
            )
        elif args.to_td:
            convert_wot_tm_to_wot_td_from_path(
                args.from_tm,
                args.to_td,
                placeholder_map_path=args.placeholder_map,
                meta_data_path=args.meta_data,
                bindings_path=args.bindings,
            )


def main():  # pragma: no cover
    args = _parse_arguments(sys.argv[1:])
    _use_converter_cli(args)
