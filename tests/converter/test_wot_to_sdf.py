from sdf_wot_converter import convert_wot_tm_to_sdf


def perform_conversion_test(input, expected_result):
    actual_result = convert_wot_tm_to_sdf(input)

    assert actual_result == expected_result


def test_empty_tm_sdf_conversion():

    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
    }

    expected_result = {}

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
        "info": {
            "title": "Lamp Thing Model",
            "copyright": "",
            "license": "",
            "version": "",
        },
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
                "sdf:jsonPointer": "#/sdfProduct/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfProperty/foo",
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
            "foobar": {"type": "array", "minItems": 2, "maxItems": 5},
            "barfoo": {"type": "object", "required": ["foo"]},
            "fizzbuzz": {},
        },
    }

    expected_result = {
        "sdfProduct": {
            "blah": {
                "sdfThing": {
                    "foo": {
                        "sdfThing": {
                            "bar": {
                                "sdfObject": {
                                    "baz": {
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
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "sdfProperty": {
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
            "foobar": {"type": "array", "minItems": 2, "maxItems": 5},
            "barfoo": {"type": "object", "required": ["foo"]},
            "fizzbuzz": {},
        },
    }

    perform_conversion_test(input, expected_result)


def test_tm_sdf_link_conversion():
    # TODO: Check how links should be mapped

    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "links": [{"href": "https://example.org"}],
    }

    expected_result = {}

    perform_conversion_test(input, expected_result)


def test_tm_sdf_schema_definition_conversion():
    # TODO: Check how links should be mapped

    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "schemaDefinitions": {"foobar": {"type": "string"}},
    }

    expected_result = {
        "sdfData": {"foobar": {"type": "string"}},
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
        "sdfData": {"foobar": {"type": "string"}},
        "sdfAction": {"toggle": {"sdfInputData": {"sdfRef": "#/sdfData/foobar"}}},
    }

    perform_conversion_test(input, expected_result)
