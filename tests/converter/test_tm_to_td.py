from sdf_wot_converter import convert_wot_tm_to_td


def perform_conversion_test(input, expected_result, placeholder_map=None):
    actual_result = convert_wot_tm_to_td(input, placeholder_map=placeholder_map)

    assert actual_result == expected_result


def test_empty_tm_td_conversion():
    # TODO: Handle case of TMs without title or security
    input = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": ["tm:ThingModel", "test"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": ["Thing", "test"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_with_placeholder_conversion():
    # TODO: Handle case of TMs without forms
    input = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "properties": {
            "temperature": {
                "description": "Shows the current temperature value",
                "type": "number",
                "minimum": -20,
                "maximum": "{{THERMOSTATE_TEMPERATURE_MAXIMUM}}",
                "observable": "{{THERMOSTATE_TEMPERATURE_OBSERVABLE}}",
                "readOnly": "{{THERMOSTATE_TEMPERATURE_READ_ONLY}}",
                "forms": [{"href": "coap://example.org"}],
            }
        },
    }

    placeholder_map = {
        "THERMOSTATE_NUMBER": 4,
        "THERMOSTATE_TEMPERATURE_MAXIMUM": 47.7,
        "THERMOSTATE_TEMPERATURE_OBSERVABLE": False,
        "THERMOSTATE_TEMPERATURE_READ_ONLY": True,
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "Thing",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "properties": {
            "temperature": {
                "description": "Shows the current temperature value",
                "type": "number",
                "minimum": -20,
                "maximum": 47.7,
                "observable": False,
                "readOnly": True,
                "forms": [{"href": "coap://example.org"}],
            }
        },
    }

    perform_conversion_test(input, expected_result, placeholder_map=placeholder_map)
