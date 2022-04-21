from sdf_wot_converter.converters.wot_to_sdf import convert_wot_tm_to_sdf
from sdf_wot_converter.converters.wot_to_sdf import convert_wot_tm_collection_to_sdf


def perform_conversion_test(input, expected_result):
    actual_result = convert_wot_tm_to_sdf(input)

    assert actual_result == expected_result


def test_empty_tm_sdf_conversion():

    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
    }

    expected_result = {"sdfObject": {"sdfObject0": {}}}

    perform_conversion_test(input, expected_result)


def test_wot_tm_to_sdf_conversion():

    input = {
        "@context": ["http://www.w3.org/ns/td"],
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

    expected_result = {
        "sdfObject": {
            "sdfObject0": {
                "label": "Lamp Thing Model",
                "sdfProperty": {
                    "status": {
                        "description": "current status of the lamp (on|off)",
                        "type": "string",
                        "writable": False,
                    }
                },
                "sdfAction": {"toggle": {"description": "Turn the lamp on or off"}},
                "sdfEvent": {
                    "overheating": {
                        "description": "Lamp reaches a critical temperature (overheating)",
                        "sdfOutputData": {"type": "string"},
                    }
                },
            },
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_namespace_conversion():
    input = {
        "@context": [
            "https://www.w3.org/2019/wot/td/v1",
            {
                "sdf": "https://example.com/sdf",
                "foo": "https://example.com/foo",
            },
        ],
        "sdf:defaultNamespace": "foo",
        "@type": "tm:ThingModel",
    }

    expected_result = {
        "namespace": {"foo": "https://example.com/foo"},
        "defaultNamespace": "foo",
        "sdfObject": {"sdfObject0": {}},
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_property_conversion():
    input = {
        "@context": ["https://www.w3.org/2019/wot/td/v1"],
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

    expected_result = {
        "sdfObject": {
            "sdfObject0": {
                "sdfProperty": {
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
                    "boo": {"type": "boolean", "const": True, "default": True},
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
        }
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_link_conversion():
    # TODO: Check how links should be mapped

    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "links": [{"href": "https://example.org"}],
    }

    expected_result = {"sdfObject": {"sdfObject0": {}}}

    perform_conversion_test(input, expected_result)


def test_tm_sdf_schema_definition_conversion():
    # TODO: Check how links should be mapped

    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
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
                    "foobar": {"type": "string"},
                    "barfoo": {"type": "integer"},
                }
            }
        }
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_relative_tm_ref_conversion():
    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "schemaDefinitions": {"foobar": {"type": "string"}},
        "actions": {"toggle": {"input": {"tm:ref": "#/schemaDefinitions/foobar"}}},
    }

    expected_result = {
        "sdfObject": {
            "sdfObject0": {
                "sdfData": {"foobar": {"type": "string"}},
                "sdfAction": {
                    "toggle": {
                        "sdfInputData": {
                            "sdfRef": "#/sdfObject/sdfObject0/sdfData/foobar"
                        }
                    }
                },
            }
        }
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_composited_conversion():
    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "links": [
            {
                "href": "./examples/wot/example.tm.jsonld",
                "rel": "tm:submodel",
            }
        ],
    }

    expected_result = {
        "sdfThing": {
            "sdfThing0": {
                "sdfObject": {
                    "example": {
                        "label": "MyLampThing",
                        "sdfAction": {"toggle": {}},
                        "sdfEvent": {
                            "overheating": {"sdfOutputData": {"type": "string"}}
                        },
                        "sdfProperty": {"status": {"type": "string"}},
                    }
                }
            }
        }
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_composited_conversion_with_affordance():
    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "title": "Top Level Lamp Thing",
        "links": [
            {
                "href": "./examples/wot/example.tm.jsonld",
                "rel": "tm:submodel",
                "instanceName": "smartlamp",
            }
        ],
        "properties": {"status": {"type": "string"}},
    }

    expected_result = {
        "sdfThing": {
            "sdfThing0": {
                "label": "Top Level Lamp Thing",
                "sdfProperty": {"status": {"type": "string"}},
                "sdfObject": {
                    "smartlamp": {
                        "label": "MyLampThing",
                        "sdfAction": {"toggle": {}},
                        "sdfEvent": {
                            "overheating": {"sdfOutputData": {"type": "string"}}
                        },
                        "sdfProperty": {"status": {"type": "string"}},
                    },
                },
            }
        }
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
            "properties": {"status": {"type": "string"}},
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
                        "sdfProperty": {"status": {"type": "string"}},
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
    }

    result = convert_wot_tm_collection_to_sdf(input)

    assert result == expected_result
