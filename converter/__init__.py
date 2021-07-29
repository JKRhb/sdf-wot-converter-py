import json
from pprint import pprint
from pathlib import Path
from jsonschema import validate
from typing import Dict
from .sdf_to_wot import convert_sdf_to_wot_tm

from .schemas.sdf_framework_schema import sdf_framework_schema
from .schemas.td_schema import td_schema
from .schemas.tm_schema import tm_schema


def validate_sdf(sdf_model: Dict):
    validate(sdf_model, sdf_framework_schema)


def validate_wot_tm(thing_model: Dict):
    validate(thing_model, tm_schema)


def validate_wot_td(thing_description: Dict):
    validate(thing_description, td_schema)


def load_model(input_path: str) -> Dict:
    path = Path(__file__).parent / input_path
    file = open(path)
    return json.load(file)


def main():
    sdf_model = load_model("examples/sdf/sdfobject-level.sdf.json")
    # sdf_model = load_model("examples/sdf/example.sdf.json")
    validate_sdf(sdf_model)
    thing_model = convert_sdf_to_wot_tm(sdf_model)
    validate_wot_tm(thing_model)
    pprint(thing_model)
