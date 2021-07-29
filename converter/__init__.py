import json
from pprint import pprint
from pathlib import Path
from jsonschema import validate
from typing import Dict
from .sdf_to_wot import convert_sdf_to_wot_tm


def validate_model(jso_path: str, model: Dict):
    path = Path(__file__).parent / jso_path
    file = open(path)
    validation_syntax = json.load(file)
    validate(model, validation_syntax)


def validate_sdf(sdf_model: Dict):
    validate_model("JSO/sdf-framework.jso.json", sdf_model)


def validate_wot_tm(sdf_model: Dict):
    validate_model("JSO/tm-json-schema-validation.json", sdf_model)


def validate_wot_td(sdf_model: Dict):
    validate_model("JSO/td-json-schema-validation.json", sdf_model)


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
