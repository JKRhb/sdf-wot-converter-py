import json
from jsonschema import validate
from typing import Dict, Callable
from .sdf_to_wot import convert_sdf_to_wot_tm
from .wot_to_sdf import convert_wot_tm_to_sdf

from .schemas.sdf_framework_schema import sdf_framework_schema
from .schemas.td_schema import td_schema
from .schemas.tm_schema import tm_schema


def load_model(input_path: str) -> Dict:
    file = open(input_path)
    return json.load(file)


def save_model(output_path: str, model: Dict, indent=4):
    file = open(output_path, "w")
    json.dump(model, file,  indent=indent)


def convert_model(from_path: str, to_path: str, from_schema: Dict, to_schema: Dict, converter_function: Callable):
    from_model = load_model(from_path)
    validate(from_model, from_schema)
    to_model = converter_function(from_model)
    validate(to_model, to_schema)
    save_model(to_path, to_model)


def main(args):
    if args.from_sdf and args.to_tm:
        convert_model(args.from_sdf, args.to_tm,
                      sdf_framework_schema, tm_schema,
                      convert_sdf_to_wot_tm)
    elif args.from_tm and args.to_sdf:
        convert_model(args.from_tm, args.to_sdf,
                      tm_schema, sdf_framework_schema,
                      convert_wot_tm_to_sdf)
