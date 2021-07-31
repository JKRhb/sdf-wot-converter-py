from converter import convert_sdf_to_wot_tm
from jsonschema import validate
from converter.schemas.tm_schema import tm_schema
from converter.schemas.sdf_validation_schema import sdf_validation_schema
import pytest


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
                "$comment": "This is a comment!",
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
                "sdf:$comment": "This is a comment!",
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


def test_sdf_tm_nested_model():
    input = {
        "sdfThing": {
            "foo": {
                "sdfRequired": [
                    "#/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfProperty/foobar",
                    "#/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfAction/foobar",
                    "#/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfEvent/foobar",
                ],
                "sdfThing": {
                    "bar": {
                        "sdfObject": {
                            "baz": {
                                "sdfProperty": {
                                    "foobar": {
                                        "label": "hi"
                                    },
                                },
                                "sdfAction": {
                                    "foobar": {
                                        "label": "hi"
                                    },
                                },
                                "sdfEvent": {
                                    "foobar": {
                                        "label": "hi"
                                    },
                                }
                            }
                        }
                    }
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
            "foo_bar_baz_foobar": {
                "sdf:jsonPointer": "#/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfAction/foobar",
                "title": "hi"
            },
        },
        "properties": {
            "foo_bar_baz_foobar": {
                "sdf:jsonPointer": "#/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfProperty/foobar",
                "title": "hi"
            },
        },
        "events": {
            "foo_bar_baz_foobar": {
                "sdf:jsonPointer": "#/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfEvent/foobar",
                "title": "hi"
            },
        },
        "tm:required": [
            "#/actions/foo_bar_baz_foobar",
            "#/properties/foo_bar_baz_foobar",
            "#/events/foo_bar_baz_foobar",
        ]
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)


def test_sdf_tm_looping_sdf_ref():
    input = {
        "sdfProperty": {
            "foo": {
                "sdfRef": "#/sdfProperty/bar"
            },
            "bar": {
                "sdfRef": "#/sdfProperty/foo"
            },
        },
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result, sdf_tm_helper)

    assert str(e_info.value) == "Encountered a looping sdfRef: #/sdfProperty/bar"


def test_sdf_tm_unparsabable_sdf_ref():
    input = {
        "sdfProperty": {
            "foo": {
                "sdfRef": "bla/sdfProperty/bar"
            },
        },
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result, sdf_tm_helper)

    assert str(e_info.value) == "sdfRef bla/sdfProperty/bar could not be resolved"


def test_sdf_tm_failing_URL_sdf_ref():
    input = {
        "namespace": {
            "bla": "https://example.org"
        },
        "sdfProperty": {
            "foo": {
                "sdfRef": "bla:/sdfProperty/bar"
            },
        },
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result, sdf_tm_helper)

    error_message = "No valid SDF model could be retrieved from https://example.org"

    assert str(e_info.value) == error_message


def test_sdf_tm_succeeding_URL_sdf_ref():
    input = {
        "namespace": {
            "test": "https://raw.githubusercontent.com/one-data-model/playground/master/sdfObject/sdfobject-accelerometer.sdf.json"
        },
        "sdfProperty": {
            "foo": {
                "sdfRef": "test:/sdfObject/Accelerometer/sdfProperty/X_Value"
            },
        },
    }

    expected_result = {
        "@context": [
            "http://www.w3.org/ns/td",
            {
                "sdf": "https://example.com/sdf",
                "test": "https://raw.githubusercontent.com/one-data-model/playground/master/sdfObject/sdfobject-accelerometer.sdf.json"
            }
        ],
        "@type": "tm:ThingModel",
        "properties": {
            "foo": {
                "title": "X Value",
                "description": "The measured value along the X axis.",
                "readOnly": True,
                "type": "number",
                "sdf:jsonPointer": "#/sdfProperty/foo"
            },
        },
    }

    perform_conversion_test(input, expected_result, sdf_tm_helper)
