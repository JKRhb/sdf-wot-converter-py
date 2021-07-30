from converter import convert_sdf_to_wot_tm
from jsonschema import validate
from converter.schemas.tm_schema import tm_schema
from converter.schemas.sdf_validation_schema import sdf_validation_schema

def perform_conversion_test(input, expected_result, conversion_function):
    actual_result = conversion_function(input)

    assert actual_result == expected_result

def sdf_tm_helper(input):
    validate(input, sdf_validation_schema)
    output = convert_sdf_to_wot_tm(input)
    validate(output, tm_schema)
    return output


def test_empty_sdf_tm_conversion():
    input = {}

    expected_result = {
        "@context": [
            "http://www.w3.org/ns/td",
            {"sdf": "https://example.com/sdf"}
        ],
        "@type": "tm:ThingModel"
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)


def test_sdf_tm_type_conversion():
    input = {
        "sdfProperty": {
            "foo": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9002,
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 9000,
                "multipleOf": 2
            },
            "bar": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 9002.0,
                "exclusiveMinimum": 0.0,
                "exclusiveMaximum": 9000.0,
                "multipleOf": 2.0
            },
            "baz": {
                "type": "string",
                "minLength": 3,
                "maxLength": 5,
                "pattern": "email",
                "format": "uri-reference"
            },
            "foobar": {
                "type": "array",
                "minItems": 2,
                "maxItems": 5
            },
            "barfoo": {
                "type": "object",
                "required": ["foo"]
            }
        }
    }

    expected_result = {
        "@context": [
            "http://www.w3.org/ns/td",
            {"sdf": "https://example.com/sdf"}
        ],
        "@type": "tm:ThingModel",
        "properties": {
            "foo": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9002,
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 9000,
                "multipleOf": 2,
                'sdf:jsonPointer': '#/sdfProperty/foo',
            },
            "bar": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 9002.0,
                "exclusiveMinimum": 0.0,
                "exclusiveMaximum": 9000.0,
                "multipleOf": 2.0,
                'sdf:jsonPointer': '#/sdfProperty/bar',
            },
            "baz": {
                "type": "string",
                "minLength": 3,
                "maxLength": 5,
                "pattern": "email",
                "format": "uri-reference",
                'sdf:jsonPointer': '#/sdfProperty/baz',
            },
            "foobar": {
                "type": "array",
                "minItems": 2,
                "maxItems": 5,
                'sdf:jsonPointer': '#/sdfProperty/foobar',
            },
            "barfoo": {
                "type": "object",
                "required": ["foo"],
                'sdf:jsonPointer': '#/sdfProperty/barfoo',
            }
        }
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)


def test_sdf_tm_action_conversion():
    input = {
        "sdfAction": {
            "foobar": {
                "sdfInputData": {
                    "type": "string"
                },
                "sdfOutputData": {
                    "type": "string"
                }
            }
        }
    }
    expected_result = {
        "@context": [
            "http://www.w3.org/ns/td",
            {"sdf": "https://example.com/sdf"}
        ],
        "@type": "tm:ThingModel",
        "actions": {
            "foobar": {
                "input": {
                    "type": "string"
                },
                "output": {
                    "type": "string"
                }
            }
        }
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)
