import json
import argparse
import sys
from jsonschema import validate
from typing import Dict, Callable
from . import sdf_to_wot
from . import wot_to_sdf

from .schemas.sdf_validation_schema import sdf_validation_schema
from .schemas.td_schema import td_schema
from .schemas.tm_schema import tm_schema


def load_model(input_path: str) -> Dict:  # pragma: no cover
    file = open(input_path)
    return json.load(file)


def save_model(output_path: str, model: Dict, indent=4):  # pragma: no cover
    file = open(output_path, "w")
    json.dump(model, file, indent=indent)


def convert_and_validate(
    from_model: Dict,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
):
    validate(from_model, from_schema)
    to_model = converter_function(from_model)
    validate(to_model, to_schema)
    return to_model


def convert_model_from_path(
    from_path: str,
    to_path: str,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
):  # pragma: no cover
    from_model = load_model(from_path)
    to_model = convert_and_validate(
        from_model, from_schema, to_schema, converter_function
    )
    save_model(to_path, to_model)


def convert_model_from_json(
    from_model_json: str,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
    indent=4,
):  # pragma: no cover
    from_model = json.loads(from_model_json)
    to_model = convert_and_validate(
        from_model, from_schema, to_schema, converter_function
    )
    return json.dumps(to_model, indent=indent)


def convert_sdf_to_wot_tm(input: Dict):
    return convert_and_validate(
        input, sdf_validation_schema, tm_schema, sdf_to_wot.convert_sdf_to_wot_tm
    )


def convert_wot_tm_to_sdf(input: Dict):
    return convert_and_validate(
        input, tm_schema, sdf_validation_schema, wot_to_sdf.convert_wot_tm_to_sdf
    )


def convert_sdf_to_wot_tm_from_path(from_path: str, to_path: str):
    return convert_model_from_path(
        from_path,
        to_path,
        sdf_validation_schema,
        tm_schema,
        sdf_to_wot.convert_sdf_to_wot_tm,
    )


def convert_wot_tm_to_sdf_from_path(from_path: str, to_path: str):
    return convert_model_from_path(
        from_path,
        to_path,
        tm_schema,
        sdf_validation_schema,
        wot_to_sdf.convert_wot_tm_to_sdf,
    )


def convert_sdf_to_wot_tm_from_json(input: str):
    return convert_model_from_json(
        input, sdf_validation_schema, tm_schema, sdf_to_wot.convert_sdf_to_wot_tm
    )


def convert_wot_tm_to_sdf_from_json(input: str):

    return convert_model_from_json(
        input, tm_schema, sdf_validation_schema, wot_to_sdf.convert_wot_tm_to_sdf
    )


def parse_arguments(args):
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
        "--to-sdf", metavar="SDF", dest="to_sdf", help="SDF output file"
    )

    return parser.parse_args(args)


def use_converter_cli(args):  # pragma: no cover
    if args.from_sdf and args.to_tm:
        convert_sdf_to_wot_tm_from_path(args.from_sdf, args.to_tm)
    elif args.from_tm and args.to_sdf:
        convert_wot_tm_to_sdf_from_path(args.from_tm, args.to_sdf)


def main():  # pragma: no cover
    args = parse_arguments(sys.argv[1:])
    use_converter_cli(args)
