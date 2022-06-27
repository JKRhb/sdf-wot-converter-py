from jsonschema import ValidationError
import pytest
from sdf_wot_converter import convert_wot_tm_to_sdf
from sdf_wot_converter.converters.tm_to_sdf import convert_wot_tm_collection_to_sdf


def perform_conversion_test(input, expected_result, **kwargs):
    actual_result = convert_wot_tm_to_sdf(input, **kwargs)

    assert actual_result == expected_result


def test_empty_tm_sdf_conversion():

    input = {
        "@context": "https://www.w3.org/2022/wot/td/v1.1",
        "@type": "tm:ThingModel",
    }

    expected_result = (
        {"sdfObject": {"sdfObject0": {}}},
        {
            "map": {
                "#/sdfObject/sdfObject0": {
                    "@context": "https://www.w3.org/2022/wot/td/v1.1",
                }
            }
        },
    )

    perform_conversion_test(input, expected_result)


def test_wot_tm_to_sdf_conversion():

    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Lamp Thing Model",
        "version": {
            "instance": "1.0.0",
        },
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

    expected_result = (
        {
            "sdfObject": {
                "sdfObject0": {
                    "label": "Lamp Thing Model",
                    "sdfAction": {
                        "toggle": {"description": "Turn " "the " "lamp " "on or " "off"}
                    },
                    "sdfEvent": {
                        "overheating": {
                            "description": "Lamp "
                            "reaches "
                            "a "
                            "critical "
                            "temperature "
                            "(overheating)",
                            "sdfOutputData": {"type": "string"},
                        }
                    },
                    "sdfProperty": {
                        "status": {
                            "description": "current "
                            "status "
                            "of "
                            "the "
                            "lamp "
                            "(on|off)",
                            "observable": False,
                            "type": "string",
                            "writable": False,
                        }
                    },
                }
            },
        },
        {
            "map": {
                "#/sdfObject/sdfObject0": {
                    "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
                    "version": {"instance": "1.0.0"},
                }
            },
        },
    )

    perform_conversion_test(input, expected_result)


def test_tm_sdf_namespace_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {
                "sdf": "https://example.com/sdf",
                "foo": "https://example.com/foo",
            },
        ],
        "sdf:defaultNamespace": "foo",
        "@type": "tm:ThingModel",
    }

    expected_result = (
        {
            "defaultNamespace": "foo",
            "namespace": {"foo": "https://example.com/foo"},
            "sdfObject": {"sdfObject0": {}},
        },
        {
            "defaultNamespace": "foo",
            "map": {
                "#/sdfObject/sdfObject0": {
                    "@context": [
                        "https://www.w3.org/2022/wot/td/v1.1",
                        {
                            "foo": "https://example.com/foo",
                            "sdf": "https://example.com/sdf",
                        },
                    ]
                }
            },
            "namespace": {"foo": "https://example.com/foo"},
        },
    )

    perform_conversion_test(input, expected_result)


def test_tm_sdf_property_conversion():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "properties": {
            "boo": {"type": "boolean", "const": True, "default": True},
            "foo": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9001,
                "exclusiveMaximum": 9002,
                "exclusiveMinimum": 1,
                "multipleOf": 1,
                "const": 5,
                "default": 5,
            },
            "bar": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 9001.0,
                "exclusiveMaximum": 9002.0,
                "exclusiveMinimum": 1.0,
                "multipleOf": 1.0,
                "const": 5.0,
                "default": 5.0,
            },
            "baz": {
                "type": "string",
                "minLength": 3,
                "maxLength": 5,
                "pattern": "email",
            },
            "foobar": {
                "type": "array",
                "minItems": 2,
                "maxItems": 5,
                "items": {"type": "string"},
            },
            "barfoo": {
                "type": "object",
                "properties": {"foo": {"type": "string"}},
                "required": ["foo"],
            },
            "fizzbuzz": {},
        },
    }

    expected_result = (
        {
            "sdfObject": {
                "sdfObject0": {
                    "sdfProperty": {
                        "bar": {
                            "const": 5.0,
                            "default": 5.0,
                            "exclusiveMaximum": 9002.0,
                            "exclusiveMinimum": 1.0,
                            "maximum": 9001.0,
                            "minimum": 0.0,
                            "multipleOf": 1.0,
                            "observable": False,
                            "type": "number",
                        },
                        "barfoo": {
                            "observable": False,
                            "properties": {"foo": {"type": "string"}},
                            "required": ["foo"],
                            "type": "object",
                        },
                        "baz": {
                            "maxLength": 5,
                            "minLength": 3,
                            "observable": False,
                            "pattern": "email",
                            "type": "string",
                        },
                        "boo": {
                            "const": True,
                            "default": True,
                            "observable": False,
                            "type": "boolean",
                        },
                        "fizzbuzz": {"observable": False},
                        "foo": {
                            "const": 5,
                            "default": 5,
                            "exclusiveMaximum": 9002,
                            "exclusiveMinimum": 1,
                            "maximum": 9001,
                            "minimum": 0,
                            "multipleOf": 1,
                            "observable": False,
                            "type": "integer",
                        },
                        "foobar": {
                            "items": {"type": "string"},
                            "maxItems": 5,
                            "minItems": 2,
                            "observable": False,
                            "type": "array",
                        },
                    }
                }
            }
        },
        {
            "map": {
                "#/sdfObject/sdfObject0": {
                    "@context": ["https://www.w3.org/2022/wot/td/v1.1"]
                }
            }
        },
    )

    perform_conversion_test(input, expected_result)


def test_tm_sdf_link_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "links": [{"href": "https://example.org"}],
    }

    expected_result = (
        {"sdfObject": {"sdfObject0": {}}},
        {
            "map": {
                "#/sdfObject/sdfObject0": {
                    "@context": [
                        "https://www.w3.org/2022/wot/td/v1.1",
                        {"sdf": "https://example.com/sdf"},
                    ],
                    "links": [{"href": "https://example.org"}],
                }
            }
        },
    )

    perform_conversion_test(input, expected_result)


def test_tm_sdf_schema_definition_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "schemaDefinitions": {
            "foobar": {"type": "string"},
            "barfoo": {"type": "integer"},
        },
    }

    expected_result = {
        "sdfObject": {
            "sdfObject0": {
                "sdfData": {
                    "barfoo": {"type": "integer"},
                    "foobar": {"type": "string"},
                }
            }
        }
    }, {
        "map": {
            "#/sdfObject/sdfObject0": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    {"sdf": "https://example.com/sdf"},
                ]
            }
        }
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_relative_tm_ref_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf", "test": "https://example.org/test"},
        ],
        "@type": "tm:ThingModel",
        "schemaDefinitions": {"foobar": {"type": "string"}},
        "actions": {"toggle": {"input": {"tm:ref": "#/schemaDefinitions/foobar"}}},
        "properties": {
            "status1": {"type": "string", "observable": False},
            "status2": {
                "tm:ref": "#/properties/status1",
                "observable": False,
                "test:foo": "test",
            },
        },
    }

    expected_result = {
        "namespace": {"test": "https://example.org/test"},
        "sdfObject": {
            "sdfObject0": {
                "sdfAction": {
                    "toggle": {
                        "sdfInputData": {
                            "sdfRef": "#/sdfObject/sdfObject0/sdfData/foobar"
                        }
                    }
                },
                "sdfProperty": {
                    "status1": {"type": "string", "observable": False},
                    "status2": {
                        "observable": False,
                        "sdfRef": "#/sdfObject/sdfObject0/sdfProperty/status1",
                    },
                },
                "sdfData": {"foobar": {"type": "string"}},
            }
        },
    }, {
        "namespace": {"test": "https://example.org/test"},
        "map": {
            "#/sdfObject/sdfObject0": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    {
                        "sdf": "https://example.com/sdf",
                        "test": "https://example.org/test",
                    },
                ]
            },
            "#/sdfObject/sdfObject0/sdfProperty/status2": {"test:foo": "test"},
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_composited_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "links": [
            {
                "href": "./examples/wot/example.tm.jsonld",
                "rel": "tm:submodel",
            }
        ],
    }

    expected_result = {
        "namespace": {"saref": "https://w3id.org/saref#"},
        "sdfThing": {
            "sdfThing0": {
                "sdfObject": {
                    "example": {
                        "label": "MyLampThing",
                        "sdfAction": {"toggle": {}},
                        "sdfEvent": {
                            "overheating": {"sdfOutputData": {"type": "string"}}
                        },
                        "sdfProperty": {
                            "status": {"observable": False, "type": "string"}
                        },
                    }
                }
            }
        },
    }, {
        "map": {
            "#/sdfThing/sdfThing0": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    {"sdf": "https://example.com/sdf"},
                ]
            },
            "#/sdfThing/sdfThing0/sdfObject/example": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    {"saref": "https://w3id.org/saref#"},
                ],
                "@type": ["saref:LightSwitch"],
                "id": "urn:dev:ops:32473-WoTLamp-1234",
            },
            "#/sdfThing/sdfThing0/sdfObject/example/sdfAction/toggle": {
                "@type": "saref:ToggleCommand"
            },
            "#/sdfThing/sdfThing0/sdfObject/example/sdfProperty/status": {
                "@type": "saref:OnOffState"
            },
        },
        "namespace": {"saref": "https://w3id.org/saref#"},
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_composited_conversion_with_affordance():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "title": "Top Level Lamp Thing",
        "links": [
            {
                "href": "./examples/wot/example.tm.jsonld",
                "rel": "tm:submodel",
                "instanceName": "smartlamp",
            }
        ],
        "properties": {"status": {"type": "string", "observable": False}},
    }

    expected_result = {
        "namespace": {"saref": "https://w3id.org/saref#"},
        "sdfThing": {
            "sdfThing0": {
                "label": "Top Level Lamp Thing",
                "sdfProperty": {"status": {"type": "string", "observable": False}},
                "sdfObject": {
                    "smartlamp": {
                        "label": "MyLampThing",
                        "sdfAction": {"toggle": {}},
                        "sdfEvent": {
                            "overheating": {"sdfOutputData": {"type": "string"}}
                        },
                        "sdfProperty": {
                            "status": {"type": "string", "observable": False}
                        },
                    },
                },
            }
        },
    }, {
        "namespace": {"saref": "https://w3id.org/saref#"},
        "map": {
            "#/sdfThing/sdfThing0": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    {"sdf": "https://example.com/sdf"},
                ]
            },
            "#/sdfThing/sdfThing0/sdfObject/smartlamp": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    {"saref": "https://w3id.org/saref#"},
                ],
                "@type": ["saref:LightSwitch"],
                "id": "urn:dev:ops:32473-WoTLamp-1234",
            },
            "#/sdfThing/sdfThing0/sdfObject/smartlamp/sdfAction/toggle": {
                "@type": "saref:ToggleCommand"
            },
            "#/sdfThing/sdfThing0/sdfObject/smartlamp/sdfProperty/status": {
                "@type": "saref:OnOffState"
            },
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_collection_sdf_conversion():
    input = {
        "baseModel": {
            "@context": "https://www.w3.org/2022/wot/td/v1.1",
            "@type": "tm:ThingModel",
            "title": "Smart Ventilator Thing Model",
            "links": [
                {
                    "rel": "tm:submodel",
                    "href": "#/ventilation",
                    "type": "application/tm+json",
                    "instanceName": "ventilation",
                },
                {
                    "rel": "tm:submodel",
                    "href": "#/LED",
                    "type": "application/tm+json",
                    "instanceName": "led",
                },
            ],
        },
        "ventilation": {
            "@context": "https://www.w3.org/2022/wot/td/v1.1",
            "@type": "tm:ThingModel",
            "title": "Ventilator Thing Model",
            "links": [
                {
                    "rel": "tm:submodel",
                    "href": "#/ventilationSubmodel",
                    "type": "application/tm+json",
                }
            ],
        },
        "LED": {
            "@context": "https://www.w3.org/2022/wot/td/v1.1",
            "@type": "tm:ThingModel",
            "title": "LED Thing Model",
            "properties": {"status": {"type": "string", "observable": False}},
            "actions": {"toggle": {}},
            "events": {"overheating": {"data": {"type": "string"}}},
        },
        "ventilationSubmodel": {
            "@context": "https://www.w3.org/2022/wot/td/v1.1",
            "@type": "tm:ThingModel",
            "title": "Submodel of a Ventilator",
        },
    }

    expected_result = {
        "sdfThing": {
            "baseModel": {
                "label": "Smart Ventilator Thing Model",
                "sdfObject": {
                    "led": {
                        "label": "LED Thing Model",
                        "sdfAction": {"toggle": {}},
                        "sdfEvent": {
                            "overheating": {"sdfOutputData": {"type": "string"}}
                        },
                        "sdfProperty": {
                            "status": {"type": "string", "observable": False}
                        },
                    }
                },
                "sdfThing": {
                    "ventilation": {
                        "label": "Ventilator Thing Model",
                        "sdfObject": {
                            "ventilationSubmodel": {"label": "Submodel of a Ventilator"}
                        },
                    },
                },
            }
        }
    }, {
        "map": {
            "#/sdfThing/baseModel": {"@context": "https://www.w3.org/2022/wot/td/v1.1"},
            "#/sdfThing/baseModel/sdfObject/led": {
                "@context": "https://www.w3.org/2022/wot/td/v1.1"
            },
            "#/sdfThing/baseModel/sdfThing/ventilation": {
                "@context": "https://www.w3.org/2022/wot/td/v1.1"
            },
            "#/sdfThing/baseModel/sdfThing/ventilation/sdfObject/ventilationSubmodel": {
                "@context": "https://www.w3.org/2022/wot/td/v1.1"
            },
        }
    }

    result = convert_wot_tm_collection_to_sdf(input)

    assert result == expected_result


def test_mapping_file_conversion():

    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "titles": {"de": "Lampending"},
    }

    expected_result = {"sdfObject": {"sdfObject0": {}}}, {
        "map": {
            "#/sdfObject/sdfObject0": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    {"sdf": "https://example.com/sdf"},
                ],
                "titles": {"de": "Lampending"},
            }
        }
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_illegal_input():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": 42,
    }

    with pytest.raises(ValidationError):
        convert_wot_tm_to_sdf(input)


def test_tm_to_sdf_context_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            "https://example.org",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
    }

    expected_result = {"sdfObject": {"sdfObject0": {}}}, {
        "map": {
            "#/sdfObject/sdfObject0": {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1",
                    "https://example.org",
                    {"sdf": "https://example.com/sdf"},
                ],
            }
        }
    }

    perform_conversion_test(input, expected_result)


def test_tm_to_sdf_suppressed_context_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            "https://example.org",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
    }

    expected_result = {"sdfObject": {"sdfObject0": {}}}

    perform_conversion_test(input, expected_result, suppress_roundtripping=True)
