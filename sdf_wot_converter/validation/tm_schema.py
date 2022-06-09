tm_schema = {
    "title": "Thing Model",
    "version": "1.1-28-January-2022",
    "description": "JSON Schema for validating Thing Models. This is automatically generated from the WoT TD Schema.",
    "$schema ": "http://json-schema.org/draft-07/schema#",
    "$id": "https://raw.githubusercontent.com/w3c/wot-thing-description/main/validation/tm-json-schema-validation.json",
    "definitions": {
        "anyUri": {"type": "string"},
        "description": {"type": "string"},
        "descriptions": {
            "type": "object",
            "additionalProperties": {"type": "string"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "title": {"type": "string"},
        "titles": {
            "type": "object",
            "additionalProperties": {"type": "string"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "security": {
            "oneOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "scopes": {
            "oneOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "subprotocol": {"type": "string", "examples": ["longpoll", "websub", "sse"]},
        "thing-context-td-uri-v1": {
            "type": "string",
            "const": "https://www.w3.org/2019/wot/td/v1",
        },
        "thing-context-td-uri-v1.1": {
            "type": "string",
            "const": "https://www.w3.org/2022/wot/td/v1.1",
        },
        "thing-context-td-uri-temp": {
            "type": "string",
            "const": "http://www.w3.org/ns/td",
        },
        "thing-context": {
            "anyOf": [
                {
                    "$comment": "New context URI with other vocabularies after it but not the old one",
                    "type": "array",
                    "items": [{"$ref": "#/definitions/thing-context-td-uri-v1.1"}],
                    "additionalItems": {
                        "anyOf": [{"$ref": "#/definitions/anyUri"}, {"type": "object"}],
                        "not": {"$ref": "#/definitions/thing-context-td-uri-v1"},
                    },
                },
                {
                    "$comment": "Only the new context URI",
                    "$ref": "#/definitions/thing-context-td-uri-v1.1",
                },
                {
                    "$comment": "Old context URI, followed by the new one and possibly other vocabularies. minItems and contains are required since prefixItems does not say all items should be provided",
                    "type": "array",
                    "prefixItems": [
                        {"$ref": "#/definitions/thing-context-td-uri-v1"},
                        {"$ref": "#/definitions/thing-context-td-uri-v1.1"},
                    ],
                    "minItems": 2,
                    "contains": {"$ref": "#/definitions/thing-context-td-uri-v1.1"},
                    "additionalItems": {
                        "anyOf": [{"$ref": "#/definitions/anyUri"}, {"type": "object"}]
                    },
                },
            ]
        },
        "type_declaration": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dataSchema-type": {
            "type": "string",
            "anyOf": [
                {
                    "enum": [
                        "boolean",
                        "integer",
                        "number",
                        "string",
                        "object",
                        "array",
                        "null",
                    ]
                },
                {"$ref": "#/definitions/placeholder-pattern"},
            ],
        },
        "dataSchema": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "title": {"$ref": "#/definitions/title"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "titles": {"$ref": "#/definitions/titles"},
                "writeOnly": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "readOnly": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "oneOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/dataSchema"},
                },
                "unit": {"type": "string"},
                "enum": {"type": "array", "minItems": 1, "uniqueItems": True},
                "format": {"type": "string"},
                "const": {},
                "default": {},
                "contentEncoding": {"type": "string"},
                "contentMediaType": {"type": "string"},
                "type": {"$ref": "#/definitions/dataSchema-type"},
                "items": {
                    "oneOf": [
                        {"$ref": "#/definitions/dataSchema"},
                        {
                            "type": "array",
                            "items": {"$ref": "#/definitions/dataSchema"},
                        },
                    ]
                },
                "maxItems": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "minItems": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "minimum": {
                    "anyOf": [
                        {"type": "number"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "maximum": {
                    "anyOf": [
                        {"type": "number"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "exclusiveMinimum": {"type": "number"},
                "exclusiveMaximum": {"type": "number"},
                "minLength": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "maxLength": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "multipleOf": {"$ref": "#/definitions/multipleOfDefinition"},
                "properties": {
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"}
                },
                "required": {"type": "array", "items": {"type": "string"}},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "additionalResponsesDefinition": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "contentType": {"type": "string"},
                    "schema": {"type": "string"},
                    "success": {"type": "boolean"},
                },
            },
        },
        "multipleOfDefinition": {
            "anyOf": [
                {"type": ["integer", "number"], "exclusiveMinimum": 0},
                {"$ref": "#/definitions/placeholder-pattern"},
            ]
        },
        "expectedResponse": {
            "type": "object",
            "properties": {"contentType": {"type": "string"}},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "form_element_base": {
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}},
                    ]
                },
                "href": {"$ref": "#/definitions/anyUri"},
                "contentType": {"type": "string"},
                "contentCoding": {"type": "string"},
                "subprotocol": {"$ref": "#/definitions/subprotocol"},
                "security": {"$ref": "#/definitions/security"},
                "scopes": {"$ref": "#/definitions/scopes"},
                "response": {"$ref": "#/definitions/expectedResponse"},
                "additionalResponses": {
                    "$ref": "#/definitions/additionalResponsesDefinition"
                },
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "form_element_property": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "anyOf": [
                                {
                                    "enum": [
                                        "readproperty",
                                        "writeproperty",
                                        "observeproperty",
                                        "unobserveproperty",
                                    ]
                                },
                                {"$ref": "#/definitions/placeholder-pattern"},
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "anyOf": [
                                    {
                                        "enum": [
                                            "readproperty",
                                            "writeproperty",
                                            "observeproperty",
                                            "unobserveproperty",
                                        ]
                                    },
                                    {"$ref": "#/definitions/placeholder-pattern"},
                                ],
                            },
                        },
                    ]
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "form_element_action": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "anyOf": [
                                {
                                    "enum": [
                                        "invokeaction",
                                        "queryaction",
                                        "cancelaction",
                                    ]
                                },
                                {"$ref": "#/definitions/placeholder-pattern"},
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "anyOf": [
                                    {
                                        "enum": [
                                            "invokeaction",
                                            "queryaction",
                                            "cancelaction",
                                        ]
                                    },
                                    {"$ref": "#/definitions/placeholder-pattern"},
                                ],
                            },
                        },
                    ]
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "form_element_event": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "anyOf": [
                                {"enum": ["subscribeevent", "unsubscribeevent"]},
                                {"$ref": "#/definitions/placeholder-pattern"},
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "anyOf": [
                                    {"enum": ["subscribeevent", "unsubscribeevent"]},
                                    {"$ref": "#/definitions/placeholder-pattern"},
                                ],
                            },
                        },
                    ]
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "form_element_root": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "anyOf": [
                                {
                                    "enum": [
                                        "readallproperties",
                                        "writeallproperties",
                                        "readmultipleproperties",
                                        "writemultipleproperties",
                                        "observeallproperties",
                                        "unobserveallproperties",
                                        "queryallactions",
                                        "subscribeallevents",
                                        "unsubscribeallevents",
                                    ]
                                },
                                {"$ref": "#/definitions/placeholder-pattern"},
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "anyOf": [
                                    {
                                        "enum": [
                                            "readallproperties",
                                            "writeallproperties",
                                            "readmultipleproperties",
                                            "writemultipleproperties",
                                            "observeallproperties",
                                            "unobserveallproperties",
                                            "queryallactions",
                                            "subscribeallevents",
                                            "unsubscribeallevents",
                                        ]
                                    },
                                    {"$ref": "#/definitions/placeholder-pattern"},
                                ],
                            },
                        },
                    ]
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "form": {
            "$comment": "This is NOT for validation purposes but for automatic generation of TS types. For more info, please see: https://github.com/w3c/wot-thing-description/pull/1319#issuecomment-994950057",
            "oneOf": [
                {"$ref": "#/definitions/form_element_property"},
                {"$ref": "#/definitions/form_element_action"},
                {"$ref": "#/definitions/form_element_event"},
                {"$ref": "#/definitions/form_element_root"},
            ],
        },
        "property_element": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "title": {"$ref": "#/definitions/title"},
                "titles": {"$ref": "#/definitions/titles"},
                "forms": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/form_element_property"},
                },
                "uriVariables": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"},
                    "propertyNames": {
                        "not": {"$ref": "#/definitions/placeholder-pattern"}
                    },
                },
                "observable": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "writeOnly": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "readOnly": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "oneOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/dataSchema"},
                },
                "unit": {"type": "string"},
                "enum": {"type": "array", "minItems": 1, "uniqueItems": True},
                "format": {"type": "string"},
                "const": {},
                "default": {},
                "type": {"$ref": "#/definitions/dataSchema-type"},
                "items": {
                    "oneOf": [
                        {"$ref": "#/definitions/dataSchema"},
                        {
                            "type": "array",
                            "items": {"$ref": "#/definitions/dataSchema"},
                        },
                    ]
                },
                "maxItems": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "minItems": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "minimum": {
                    "anyOf": [
                        {"type": "number"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "maximum": {
                    "anyOf": [
                        {"type": "number"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "exclusiveMinimum": {"type": "number"},
                "exclusiveMaximum": {"type": "number"},
                "minLength": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "maxLength": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "multipleOf": {"$ref": "#/definitions/multipleOfDefinition"},
                "properties": {
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"}
                },
                "required": {"type": "array", "items": {"type": "string"}},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "action_element": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "title": {"$ref": "#/definitions/title"},
                "titles": {"$ref": "#/definitions/titles"},
                "forms": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/form_element_action"},
                },
                "uriVariables": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"},
                    "propertyNames": {
                        "not": {"$ref": "#/definitions/placeholder-pattern"}
                    },
                },
                "input": {"$ref": "#/definitions/dataSchema"},
                "output": {"$ref": "#/definitions/dataSchema"},
                "safe": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "idempotent": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ]
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "event_element": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "title": {"$ref": "#/definitions/title"},
                "titles": {"$ref": "#/definitions/titles"},
                "forms": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/form_element_event"},
                },
                "uriVariables": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"},
                    "propertyNames": {
                        "not": {"$ref": "#/definitions/placeholder-pattern"}
                    },
                },
                "subscription": {"$ref": "#/definitions/dataSchema"},
                "data": {"$ref": "#/definitions/dataSchema"},
                "dataResponse": {"$ref": "#/definitions/dataSchema"},
                "cancellation": {"$ref": "#/definitions/dataSchema"},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "base_link_element": {
            "type": "object",
            "properties": {
                "href": {"$ref": "#/definitions/anyUri"},
                "type": {"type": "string"},
                "rel": {"type": "string"},
                "anchor": {"$ref": "#/definitions/anyUri"},
            },
            "additionalProperties": True,
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "link_element": {
            "allOf": [
                {"$ref": "#/definitions/base_link_element"},
                {
                    "not": {
                        "description": "A basic link element should not contain sizes",
                        "type": "object",
                        "properties": {"sizes": {}},
                        "required": ["sizes"],
                    }
                },
                {
                    "not": {
                        "description": "A basic link element should not contain icon",
                        "properties": {
                            "rel": {
                                "anyOf": [
                                    {"enum": ["icon"]},
                                    {"$ref": "#/definitions/placeholder-pattern"},
                                ]
                            }
                        },
                        "required": ["rel"],
                    }
                },
            ]
        },
        "icon_link_element": {
            "allOf": [
                {"$ref": "#/definitions/base_link_element"},
                {
                    "properties": {
                        "rel": {"const": "icon"},
                        "sizes": {"type": "string", "pattern": "[0-9]*x[0-9]+"},
                    },
                    "required": ["rel"],
                },
            ]
        },
        "noSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["nosec"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "autoSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["auto"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "comboSecurityScheme": {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "@type": {"$ref": "#/definitions/type_declaration"},
                        "description": {"$ref": "#/definitions/description"},
                        "descriptions": {"$ref": "#/definitions/descriptions"},
                        "proxy": {"$ref": "#/definitions/anyUri"},
                        "scheme": {
                            "type": "string",
                            "anyOf": [
                                {"enum": ["combo"]},
                                {"$ref": "#/definitions/placeholder-pattern"},
                            ],
                        },
                        "oneOf": {
                            "type": "array",
                            "minItems": 2,
                            "items": {"type": "string"},
                        },
                        "tm:ref": {"$ref": "#/definitions/tm_ref"},
                    },
                },
                {
                    "type": "object",
                    "properties": {
                        "@type": {"$ref": "#/definitions/type_declaration"},
                        "description": {"$ref": "#/definitions/description"},
                        "descriptions": {"$ref": "#/definitions/descriptions"},
                        "proxy": {"$ref": "#/definitions/anyUri"},
                        "scheme": {
                            "type": "string",
                            "anyOf": [
                                {"enum": ["combo"]},
                                {"$ref": "#/definitions/placeholder-pattern"},
                            ],
                        },
                        "allOf": {
                            "type": "array",
                            "minItems": 2,
                            "items": {"type": "string"},
                        },
                        "tm:ref": {"$ref": "#/definitions/tm_ref"},
                    },
                },
            ]
        },
        "basicSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["basic"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "in": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["header", "query", "body", "cookie", "auto"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "name": {"type": "string"},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "digestSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["digest"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "qop": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["auth", "auth-int"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "in": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["header", "query", "body", "cookie", "auto"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "name": {"type": "string"},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "apiKeySecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["apikey"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "in": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["header", "query", "body", "cookie"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "name": {"type": "string"},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "bearerSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["bearer"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "authorization": {"$ref": "#/definitions/anyUri"},
                "alg": {"type": "string"},
                "format": {"type": "string"},
                "in": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["header", "query", "body", "cookie", "auto"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "name": {"type": "string"},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "pskSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["psk"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "identity": {"type": "string"},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "oAuth2SecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {
                    "type": "string",
                    "anyOf": [
                        {"enum": ["oauth2"]},
                        {"$ref": "#/definitions/placeholder-pattern"},
                    ],
                },
                "authorization": {"$ref": "#/definitions/anyUri"},
                "token": {"$ref": "#/definitions/anyUri"},
                "refresh": {"$ref": "#/definitions/anyUri"},
                "scopes": {
                    "oneOf": [
                        {"type": "array", "items": {"type": "string"}},
                        {"type": "string"},
                    ]
                },
                "flow": {
                    "anyOf": [
                        {"type": "string"},
                        {
                            "type": "string",
                            "anyOf": [
                                {"enum": ["code", "client", "device"]},
                                {"$ref": "#/definitions/placeholder-pattern"},
                            ],
                        },
                    ]
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "securityScheme": {
            "anyOf": [
                {"$ref": "#/definitions/noSecurityScheme"},
                {"$ref": "#/definitions/autoSecurityScheme"},
                {"$ref": "#/definitions/comboSecurityScheme"},
                {"$ref": "#/definitions/basicSecurityScheme"},
                {"$ref": "#/definitions/digestSecurityScheme"},
                {"$ref": "#/definitions/apiKeySecurityScheme"},
                {"$ref": "#/definitions/bearerSecurityScheme"},
                {"$ref": "#/definitions/pskSecurityScheme"},
                {"$ref": "#/definitions/oAuth2SecurityScheme"},
            ]
        },
        "tm_type_declaration": {
            "oneOf": [
                {"type": "string", "const": "tm:ThingModel"},
                {
                    "type": "array",
                    "items": {"type": "string"},
                    "contains": {"const": "tm:ThingModel"},
                },
            ]
        },
        "placeholder-pattern": {
            "type": "string",
            "pattern": "^.*[{]{2}[ -~]+[}]{2}.*$",
        },
        "tm_required": {
            "type": "array",
            "items": {"type": "string", "format": "json-pointer"},
        },
        "tm_ref": {"type": "string", "format": "uri-reference"},
    },
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "title": {"$ref": "#/definitions/title"},
        "titles": {"$ref": "#/definitions/titles"},
        "properties": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/property_element"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "actions": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/action_element"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "events": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/event_element"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "description": {"$ref": "#/definitions/description"},
        "descriptions": {"$ref": "#/definitions/descriptions"},
        "version": {
            "type": "object",
            "properties": {"instance": {"type": "string"}},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "links": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"$ref": "#/definitions/link_element"},
                    {"$ref": "#/definitions/icon_link_element"},
                ]
            },
        },
        "forms": {
            "type": "array",
            "minItems": 1,
            "items": {"$ref": "#/definitions/form_element_root"},
        },
        "base": {"$ref": "#/definitions/anyUri"},
        "securityDefinitions": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {"$ref": "#/definitions/securityScheme"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "schemaDefinitions": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {"$ref": "#/definitions/dataSchema"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "support": {"$ref": "#/definitions/anyUri"},
        "created": {"type": "string"},
        "modified": {"type": "string"},
        "profile": {
            "oneOf": [
                {"$ref": "#/definitions/anyUri"},
                {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/anyUri"},
                },
            ]
        },
        "security": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "minItems": 1, "items": {"type": "string"}},
            ]
        },
        "uriVariables": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/dataSchema"},
            "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
        },
        "@type": {"$ref": "#/definitions/tm_type_declaration"},
        "@context": {"$ref": "#/definitions/thing-context"},
        "tm:required": {"$ref": "#/definitions/tm_required"},
    },
    "additionalProperties": True,
    "propertyNames": {"not": {"$ref": "#/definitions/placeholder-pattern"}},
    "required": ["@context", "@type"],
}
