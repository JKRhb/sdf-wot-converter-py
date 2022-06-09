from typing import Dict
from jsonschema import Draft7Validator
from .sdf_validation_schema import sdf_validation_schema
from .td_schema import td_schema
from .tm_schema import tm_schema
from .sdf_framework_schema import sdf_framework_schema


sdf_framework_validator = Draft7Validator(sdf_framework_schema)

sdf_validator = Draft7Validator(sdf_validation_schema)

tm_validator = Draft7Validator(tm_schema)

td_validator = Draft7Validator(td_schema)


def validate_sdf_model(sdf_model: Dict, framework=False):
    if framework:
        sdf_framework_validator.validate(sdf_model)
    else:
        sdf_validator.validate(sdf_model)


def validate_thing_model(thing_model: Dict):
    tm_validator.validate(thing_model)


def validate_thing_description(thing_description: Dict):
    td_validator.validate(thing_description)
