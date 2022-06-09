from typing import Dict
from jsonschema import Draft7Validator
from .sdf_validation_schema import sdf_validation_schema
from .td_schema import td_schema
from .tm_schema import tm_schema


def validate_sdf_model(sdf_model: Dict):
    Draft7Validator(sdf_validation_schema).validate(sdf_model)


def validate_thing_model(thing_model: Dict):
    Draft7Validator(tm_schema).validate(thing_model)


def validate_thing_description(thing_description: Dict):
    Draft7Validator(td_schema).validate(thing_description)
