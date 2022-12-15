from jsonschema import ValidationError
import pytest
from sdf_wot_converter import convert_wot_tm_to_wot_td
from sdf_wot_converter.converters.wot_common import PlaceholderException


def perform_conversion_test(input, expected_result, **kwargs):
    actual_result = convert_wot_tm_to_wot_td(input, **kwargs)

    assert actual_result == expected_result


def test_empty_tm_td_conversion():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": ["tm:ThingModel", "test"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": ["test"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_with_meta_data_and_bindings_conversion():
    input = {
        "@context": "https://www.w3.org/2022/wot/td/v1.1",
        "@type": "tm:ThingModel",
        "title": "Lamp Thing Model",
        "properties": {
            "status": {
                "description": "current status of the lamp (on|off)",
                "type": "string",
                "readOnly": True,
            }
        },
        "actions": {"toggle": {"description": "Turn the lamp on or off"}},
        "events": {
            "overheating": {
                "description": "Lamp reaches a critical temperature (overheating)",
                "data": {"type": "string"},
            }
        },
    }

    meta_data = {
        "title": "MyLampThing",
        "id": "urn:dev:ops:32473-WoTLamp-1234",
    }

    bindings = {
        "securityDefinitions": {"basic_sc": {"scheme": "basic", "in": "header"}},
        "security": "basic_sc",
        "properties": {
            "status": {
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "actions": {
            "toggle": {"forms": [{"href": "https://mylamp.example.com/toggle"}]}
        },
        "events": {
            "overheating": {
                "forms": [
                    {"href": "https://mylamp.example.com/oh", "subprotocol": "longpoll"}
                ],
            }
        },
    }

    expected_result = {
        "@context": "https://www.w3.org/2022/wot/td/v1.1",
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "title": "MyLampThing",
        "securityDefinitions": {"basic_sc": {"scheme": "basic", "in": "header"}},
        "security": "basic_sc",
        "properties": {
            "status": {
                "description": "current status of the lamp (on|off)",
                "type": "string",
                "readOnly": True,
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "actions": {
            "toggle": {
                "description": "Turn the lamp on or off",
                "forms": [{"href": "https://mylamp.example.com/toggle"}],
            }
        },
        "events": {
            "overheating": {
                "description": "Lamp reaches a critical temperature (overheating)",
                "data": {"type": "string"},
                "forms": [
                    {"href": "https://mylamp.example.com/oh", "subprotocol": "longpoll"}
                ],
            }
        },
    }

    perform_conversion_test(
        input, expected_result, meta_data=meta_data, bindings=bindings
    )


def test_tm_td_with_placeholder_conversion():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
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
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
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


def test_tm_td_with_unreplaced_placeholders():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "id": "{{UNREPLACED_PLACEHOLDER}}",
    }

    placeholder_map = {}

    with pytest.raises(PlaceholderException):
        convert_wot_tm_to_wot_td(input, placeholder_map=placeholder_map)


def test_tm_td_extension():
    extension_url = (
        "https://raw.githubusercontent.com/JKRhb/"
        "sdf-wot-converter-py/main/examples/wot/example-with-bindings.tm.jsonld"
    )
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "links": [
            {
                "href": extension_url,
                "rel": "tm:extends",
            }
        ],
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "title": "Thing Title",
        "securityDefinitions": {
            "basic_sc": {"scheme": "basic", "in": "header"},
            "nosec_sc": {"scheme": "nosec"},
        },
        "security": ["nosec_sc"],
        "properties": {
            "status": {
                "@type": "saref:OnOffState",
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "actions": {
            "toggle": {
                "@type": "saref:ToggleCommand",
                "forms": [{"href": "https://mylamp.example.com/toggle"}],
            }
        },
        "events": {
            "overheating": {
                "data": {"type": "string"},
                "forms": [
                    {"href": "https://mylamp.example.com/oh", "subprotocol": "longpoll"}
                ],
            }
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_recursive_extension():
    extension_url = (
        "https://raw.githubusercontent.com/JKRhb/"
        "sdf-wot-converter-py/main/examples/wot/example-with-tm-extends.tm.jsonld"
    )

    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "links": [
            {
                "href": extension_url,
                "rel": "tm:extends",
            }
        ],
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "title": "MyLampThing",
        "securityDefinitions": {
            "basic_sc": {"scheme": "basic", "in": "header"},
        },
        "security": "basic_sc",
        "properties": {
            "status": {
                "@type": "saref:OnOffState",
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "actions": {
            "toggle": {
                "@type": "saref:ToggleCommand",
                "forms": [{"href": "https://mylamp.example.com/toggle"}],
            }
        },
        "events": {
            "overheating": {
                "data": {"type": "string"},
                "forms": [
                    {"href": "https://mylamp.example.com/oh", "subprotocol": "longpoll"}
                ],
            }
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_link_preservation():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "links": [{"href": "https://example.org"}],
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "securityDefinitions": {
            "nosec_sc": {"scheme": "nosec"},
        },
        "security": ["nosec_sc"],
        "links": [{"href": "https://example.org"}],
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_tm_ref():
    tm_ref_url = (
        "https://raw.githubusercontent.com/JKRhb/sdf-wot-converter-py/"
        "main/examples/wot/example-with-tm-ref.tm.jsonld#/properties/status"
    )

    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "properties": {
            "status": {
                "tm:ref": tm_ref_url,
                "readOnly": True,
            },
            "anotherStatus": {"tm:ref": "#/properties/status"},
        },
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "securityDefinitions": {
            "nosec_sc": {"scheme": "nosec"},
        },
        "security": ["nosec_sc"],
        "properties": {
            "status": {
                "@type": "saref:OnOffState",
                "type": "boolean",
                "readOnly": True,
                "forms": [{"href": "https://mylamp.example.com/status"}],
            },
            "anotherStatus": {
                "@type": "saref:OnOffState",
                "type": "boolean",
                "readOnly": True,
                "forms": [{"href": "https://mylamp.example.com/status"}],
            },
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_tm_required():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "properties": {
            "status": {
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "tm:required": ["#/properties/status"],
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "securityDefinitions": {
            "nosec_sc": {"scheme": "nosec"},
        },
        "security": ["nosec_sc"],
        "properties": {
            "status": {
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_illegal_input():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": 42,
    }

    with pytest.raises(ValidationError):
        convert_wot_tm_to_wot_td(input)


def test_tm_td_with_submodel():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"saref": "https://w3id.org/saref#"},
        ],
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "title": "MyLampThing",
        "@type": ["tm:ThingModel", "saref:LightSwitch"],
        "securityDefinitions": {"basic_sc": {"scheme": "basic", "in": "header"}},
        "security": "basic_sc",
        "properties": {
            "status": {
                "@type": "saref:OnOffState",
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "actions": {
            "toggle": {
                "@type": "saref:ToggleCommand",
                "forms": [{"href": "https://mylamp.example.com/toggle"}],
            }
        },
        "events": {
            "overheating": {
                "data": {"type": "string"},
                "forms": [
                    {"href": "https://mylamp.example.com/oh", "subprotocol": "longpoll"}
                ],
            },
            "overheating2": {"tm:ref": "#/events/overheating"},
        },
        "links": [
            {
                "href": "./examples/wot/example-with-bindings.tm.jsonld",
                "rel": "tm:submodel",
            }
        ],
    }

    expected_result = {
        "example-with-bindings": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"saref": "https://w3id.org/saref#"},
            ],
            "@type": ["saref:LightSwitch"],
            "actions": {
                "toggle": {
                    "@type": "saref:ToggleCommand",
                    "forms": [{"href": "https://mylamp.example.com/toggle"}],
                }
            },
            "events": {
                "overheating": {
                    "data": {"type": "string"},
                    "forms": [
                        {
                            "href": "https://mylamp.example.com/oh",
                            "subprotocol": "longpoll",
                        }
                    ],
                }
            },
            "id": "urn:dev:ops:32473-WoTLamp-1234",
            "properties": {
                "status": {
                    "@type": "saref:OnOffState",
                    "forms": [{"href": "https://mylamp.example.com/status"}],
                    "type": "string",
                }
            },
            "security": "basic_sc",
            "securityDefinitions": {"basic_sc": {"in": "header", "scheme": "basic"}},
            "title": "MyLampThing",
        },
        "root": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"saref": "https://w3id.org/saref#"},
            ],
            "@type": ["saref:LightSwitch"],
            "actions": {
                "toggle": {
                    "@type": "saref:ToggleCommand",
                    "forms": [{"href": "https://mylamp.example.com/toggle"}],
                }
            },
            "events": {
                "overheating": {
                    "data": {"type": "string"},
                    "forms": [
                        {
                            "href": "https://mylamp.example.com/oh",
                            "subprotocol": "longpoll",
                        }
                    ],
                },
                "overheating2": {
                    "data": {"type": "string"},
                    "forms": [
                        {
                            "href": "https://mylamp.example.com/oh",
                            "subprotocol": "longpoll",
                        }
                    ],
                },
            },
            "id": "urn:dev:ops:32473-WoTLamp-1234",
            "links": [{"href": "#/example-with-bindings", "rel": "item"}],
            "properties": {
                "status": {
                    "@type": "saref:OnOffState",
                    "forms": [{"href": "https://mylamp.example.com/status"}],
                    "type": "string",
                }
            },
            "security": "basic_sc",
            "securityDefinitions": {"basic_sc": {"in": "header", "scheme": "basic"}},
            "title": "MyLampThing",
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_with_nesting():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"saref": "https://w3id.org/saref#"},
        ],
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "title": "MyLampThing",
        "@type": ["tm:ThingModel", "saref:LightSwitch"],
        "securityDefinitions": {"basic_sc": {"scheme": "basic", "in": "header"}},
        "security": "basic_sc",
        "properties": {
            "status": {
                "@type": "saref:OnOffState",
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "actions": {
            "toggle": {
                "@type": "saref:ToggleCommand",
                "forms": [{"href": "https://mylamp.example.com/toggle"}],
            }
        },
        "events": {
            "overheating": {
                "data": {"type": "string"},
                "forms": [
                    {"href": "https://mylamp.example.com/oh", "subprotocol": "longpoll"}
                ],
            },
            "overheating2": {"tm:ref": "#/events/overheating"},
        },
        "links": [
            {
                "href": "./examples/wot/example-with-bindings.tm.jsonld",
                "rel": "tm:submodel",
            }
        ],
    }

    expected_result = {
        "example-with-bindings": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"saref": "https://w3id.org/saref#"},
            ],
            "@type": ["saref:LightSwitch"],
            "actions": {
                "toggle": {
                    "@type": "saref:ToggleCommand",
                    "forms": [{"href": "https://mylamp.example.com/toggle"}],
                }
            },
            "events": {
                "overheating": {
                    "data": {"type": "string"},
                    "forms": [
                        {
                            "href": "https://mylamp.example.com/oh",
                            "subprotocol": "longpoll",
                        }
                    ],
                }
            },
            "id": "urn:dev:ops:32473-WoTLamp-1234",
            "properties": {
                "status": {
                    "@type": "saref:OnOffState",
                    "forms": [{"href": "https://mylamp.example.com/status"}],
                    "type": "string",
                }
            },
            "security": "basic_sc",
            "securityDefinitions": {"basic_sc": {"in": "header", "scheme": "basic"}},
            "title": "MyLampThing",
        },
        "root": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"saref": "https://w3id.org/saref#"},
            ],
            "@type": ["saref:LightSwitch"],
            "actions": {
                "toggle": {
                    "@type": "saref:ToggleCommand",
                    "forms": [{"href": "https://mylamp.example.com/toggle"}],
                }
            },
            "events": {
                "overheating": {
                    "data": {"type": "string"},
                    "forms": [
                        {
                            "href": "https://mylamp.example.com/oh",
                            "subprotocol": "longpoll",
                        }
                    ],
                },
                "overheating2": {
                    "data": {"type": "string"},
                    "forms": [
                        {
                            "href": "https://mylamp.example.com/oh",
                            "subprotocol": "longpoll",
                        }
                    ],
                },
            },
            "id": "urn:dev:ops:32473-WoTLamp-1234",
            "links": [{"href": "#/example-with-bindings", "rel": "item"}],
            "properties": {
                "status": {
                    "@type": "saref:OnOffState",
                    "forms": [{"href": "https://mylamp.example.com/status"}],
                    "type": "string",
                }
            },
            "security": "basic_sc",
            "securityDefinitions": {"basic_sc": {"in": "header", "scheme": "basic"}},
            "title": "MyLampThing",
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_td_tm_required_removal():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "properties": {
            "status": {
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            },
            "removedStatus": {"type": "string"},
        },
        "tm:required": ["#/properties/status"],
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "securityDefinitions": {
            "nosec_sc": {"scheme": "nosec"},
        },
        "security": ["nosec_sc"],
        "properties": {
            "status": {
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
    }

    perform_conversion_test(
        input, expected_result, remove_not_required_affordances=True
    )
