from converter import convert_wot_tm_to_sdf
from jsonschema import validate
from converter.schemas.tm_schema import tm_schema
from converter.schemas.sdf_validation_schema import sdf_validation_schema


def perform_conversion_test(input, expected_result, conversion_function):
    actual_result = conversion_function(input)

    assert actual_result == expected_result


def tm_sdf_helper(input):
    validate(input, tm_schema)
    output = convert_wot_tm_to_sdf(input)
    validate(output, sdf_validation_schema)
    return output


def test_empty_sdf_tm_conversion():

    input = {
        "@context": [
            "http://www.w3.org/ns/td",
            {"sdf": "https://example.com/sdf"}
        ],
        "@type": "tm:ThingModel"
    }

    expected_result = {}

    perform_conversion_test(input, expected_result, tm_sdf_helper)
