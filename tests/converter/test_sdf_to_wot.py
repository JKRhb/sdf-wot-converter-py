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


def test__sdf_tm_infoblock_conversion():
    input = {
        "info": {
            "title": "Test",
            "version": "2021-07-31",
            "copyright": "Copyright (c) 2021 Example Corp",
            "license": "https://example.com/LICENSE"
        }
    }

    expected_result = {
        "@context": [
            "http://www.w3.org/ns/td",
            {"sdf": "https://example.com/sdf"}
        ],
        "@type": "tm:ThingModel",
        "title": "Test",
        "description": "Copyright (c) 2021 Example Corp",
        "version": {
            "instance": "2021-07-31",
        },
        "links": [{
            "href": "https://example.com/LICENSE",
            "rel": "license"
        }]
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)


def test_sdf_tm_type_conversion():
    input = {
        "sdfProperty": {
            "foo": {
                "type": "integer",
                "readable": True,
                "minimum": 0,
                "maximum": 9002,
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 9000,
                "multipleOf": 2
            },
            "bar": {
                "type": "number",
                "writable": True,
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
                "format": "uri-reference",
                "contentFormat": "audio/mpeg"
            },
            "foobar": {
                "type": "array",
                "minItems": 2,
                "maxItems": 5,
                "items": {
                    "type": "string"
                }
            },
            "barfoo": {
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string"
                    }
                },
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
                "writeOnly": False,
                "type": "integer",
                "minimum": 0,
                "maximum": 9002,
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 9000,
                "multipleOf": 2,
                'sdf:jsonPointer': '#/sdfProperty/foo',
            },
            "bar": {
                "readOnly": False,
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
                "contentMediaType": "audio/mpeg",
                'sdf:jsonPointer': '#/sdfProperty/baz',
            },
            "foobar": {
                "type": "array",
                "minItems": 2,
                "maxItems": 5,
                "items": {
                    "type": "string"
                },
                'sdf:jsonPointer': '#/sdfProperty/foobar',
            },
            "barfoo": {
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string"
                    }
                },
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
                'sdf:jsonPointer': '#/sdfAction/foobar',
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


def test_sdf_tm_event_conversion():
    input = {
        "sdfEvent": {
            "foobar": {
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
        "events": {
            "foobar": {
                "data": {
                    "type": "string"
                },
                "sdf:jsonPointer": "#/sdfEvent/foobar"
            }
        }
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)


def test_sdf_tm_sdf_ref_conversion():
    input = {
        "sdfAction": {
            "foobar": {
                "label": "hi"
            },
            "foobaz": {
                "sdfRef": "#/sdfAction/foobar"
            }
        },
        "sdfEvent": {
            "foobar": {
                "label": "hi"
            },
            "foobaz": {
                "sdfRef": "#/sdfEvent/foobar"
            }
        },
        "sdfProperty": {
            "foobar": {
                "label": "hi"
            },
            "foobaz": {
                "sdfRef": "#/sdfProperty/foobar"
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
                "sdf:jsonPointer": "#/sdfAction/foobar",
                "title": "hi"
            },
            "foobaz": {
                "sdf:jsonPointer": "#/sdfAction/foobaz",
                "title": "hi"
            }
        },
        "properties": {
            "foobar": {
                "sdf:jsonPointer": "#/sdfProperty/foobar",
                "title": "hi"
            },
            "foobaz": {
                "sdf:jsonPointer": "#/sdfProperty/foobaz",
                "title": "hi"
            }
        },
        "events": {
            "foobar": {
                "sdf:jsonPointer": "#/sdfEvent/foobar",
                "title": "hi"
            },
            "foobaz": {
                "sdf:jsonPointer": "#/sdfEvent/foobaz",
                "title": "hi"
            }
        }
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)
