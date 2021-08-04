tm_schema = {
    "title": "Thing Model",
    "version": "1.1-04-June-2021",
    "description": "JSON Schema for validating Thing Models. This is automatically generated from the WoT TD Schema.",
    "$schema ": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "anyUri": {"type": "string"},
        "description": {"type": "string"},
        "descriptions": {"type": "object", "additionalProperties": {"type": "string"}},
        "title": {"type": "string"},
        "titles": {"type": "object", "additionalProperties": {"type": "string"}},
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
        "thing-context-w3c-uri": {
            "type": "string",
            "enum": ["https://www.w3.org/2019/wot/td/v1", "http://www.w3.org/ns/td"],
        },
        "thing-context": {
            "oneOf": [
                {
                    "type": "array",
                    "items": [{"$ref": "#/definitions/thing-context-w3c-uri"}],
                    "additionalItems": {
                        "anyOf": [{"$ref": "#/definitions/anyUri"}, {"type": "object"}]
                    },
                },
                {"$ref": "#/definitions/thing-context-w3c-uri"},
            ]
        },
        "type_declaration": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dataSchema": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "title": {"$ref": "#/definitions/title"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "titles": {"$ref": "#/definitions/titles"},
                "writeOnly": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
                "readOnly": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
                "oneOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/dataSchema"},
                },
                "unit": {"type": "string"},
                "enum": {"type": "array", "minItems": 1, "uniqueItems": True},
                "format": {"type": "string"},
                "const": {},
                "contentEncoding": {"type": "string"},
                "contentMediaType": {"type": "string"},
                "type": {
                    "type": "string",
                    "enum": [
                        "boolean",
                        "integer",
                        "number",
                        "string",
                        "object",
                        "array",
                        "null",
                    ],
                },
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
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "minItems": {
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "minimum": {"anyOf": [{"type": "number"}, {"type": "string"}]},
                "maximum": {"anyOf": [{"type": "number"}, {"type": "string"}]},
                "minLength": {
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "maxLength": {
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "multipleOf": {
                    "anyOf": [
                        {"type": "integer", "exclusiveMinimum": 0},
                        {"type": "number", "exclusiveMinimum": 0},
                    ]
                },
                "properties": {
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"}
                },
                "required": {"type": "array", "items": {"type": "string"}},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
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
        "form_element_property": {
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "enum": [
                                "readproperty",
                                "writeproperty",
                                "observeproperty",
                                "unobserveproperty",
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "readproperty",
                                    "writeproperty",
                                    "observeproperty",
                                    "unobserveproperty",
                                ],
                            },
                        },
                    ]
                },
                "href": {"$ref": "#/definitions/anyUri"},
                "contentType": {"type": "string"},
                "contentCoding": {"type": "string"},
                "subprotocol": {"$ref": "#/definitions/subprotocol"},
                "security": {"$ref": "#/definitions/security"},
                "scopes": {"$ref": "#/definitions/scopes"},
                "response": {
                    "type": "object",
                    "properties": {"contentType": {"type": "string"}},
                },
                "additionalResponses": {
                    "$ref": "#/definitions/additionalResponsesDefinition"
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
        },
        "form_element_action": {
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {"type": "string", "enum": ["invokeaction"]},
                        {
                            "type": "array",
                            "items": {"type": "string", "enum": ["invokeaction"]},
                        },
                    ]
                },
                "href": {"$ref": "#/definitions/anyUri"},
                "contentType": {"type": "string"},
                "contentCoding": {"type": "string"},
                "subprotocol": {"$ref": "#/definitions/subprotocol"},
                "security": {"$ref": "#/definitions/security"},
                "scopes": {"$ref": "#/definitions/scopes"},
                "response": {
                    "type": "object",
                    "properties": {"contentType": {"type": "string"}},
                },
                "additionalResponses": {
                    "$ref": "#/definitions/additionalResponsesDefinition"
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
        },
        "form_element_event": {
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "enum": ["subscribeevent", "unsubscribeevent"],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["subscribeevent", "unsubscribeevent"],
                            },
                        },
                    ]
                },
                "href": {"$ref": "#/definitions/anyUri"},
                "contentType": {"type": "string"},
                "contentCoding": {"type": "string"},
                "subprotocol": {"$ref": "#/definitions/subprotocol"},
                "security": {"$ref": "#/definitions/security"},
                "scopes": {"$ref": "#/definitions/scopes"},
                "response": {
                    "type": "object",
                    "properties": {"contentType": {"type": "string"}},
                },
                "additionalResponses": {
                    "$ref": "#/definitions/additionalResponsesDefinition"
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
        },
        "form_element_root": {
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "enum": [
                                "readallproperties",
                                "writeallproperties",
                                "readmultipleproperties",
                                "writemultipleproperties",
                                "observeallproperties",
                                "unobserveallproperties",
                                "subscribeallevents",
                                "unsubscribeallevents",
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "readallproperties",
                                    "writeallproperties",
                                    "readmultipleproperties",
                                    "writemultipleproperties",
                                    "observeallproperties",
                                    "unobserveallproperties",
                                    "subscribeallevents",
                                    "unsubscribeallevents",
                                ],
                            },
                        },
                    ]
                },
                "href": {"$ref": "#/definitions/anyUri"},
                "contentType": {"type": "string"},
                "contentCoding": {"type": "string"},
                "subprotocol": {"$ref": "#/definitions/subprotocol"},
                "security": {"$ref": "#/definitions/security"},
                "scopes": {"$ref": "#/definitions/scopes"},
                "response": {
                    "type": "object",
                    "properties": {"contentType": {"type": "string"}},
                },
                "additionalResponses": {
                    "$ref": "#/definitions/additionalResponsesDefinition"
                },
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
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
                },
                "observable": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
                "writeOnly": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
                "readOnly": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
                "oneOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/dataSchema"},
                },
                "unit": {"type": "string"},
                "enum": {"type": "array", "minItems": 1, "uniqueItems": True},
                "format": {"type": "string"},
                "const": {},
                "type": {
                    "type": "string",
                    "enum": [
                        "boolean",
                        "integer",
                        "number",
                        "string",
                        "object",
                        "array",
                        "null",
                    ],
                },
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
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "minItems": {
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "minimum": {"anyOf": [{"type": "number"}, {"type": "string"}]},
                "maximum": {"anyOf": [{"type": "number"}, {"type": "string"}]},
                "minLength": {
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "maxLength": {
                    "minimum": 0,
                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                },
                "multipleOf": {
                    "anyOf": [
                        {"type": "integer", "exclusiveMinimum": 0},
                        {"type": "number", "exclusiveMinimum": 0},
                    ]
                },
                "properties": {
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"}
                },
                "required": {"type": "array", "items": {"type": "string"}},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
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
                },
                "input": {"$ref": "#/definitions/dataSchema"},
                "output": {"$ref": "#/definitions/dataSchema"},
                "safe": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
                "idempotent": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
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
                },
                "subscription": {"$ref": "#/definitions/dataSchema"},
                "data": {"$ref": "#/definitions/dataSchema"},
                "cancellation": {"$ref": "#/definitions/dataSchema"},
                "tm:ref": {"$ref": "#/definitions/tm_ref"},
            },
            "additionalProperties": True,
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
                        "properties": {"rel": {"enum": ["icon"]}},
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
        "securityScheme": {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "@type": {"$ref": "#/definitions/type_declaration"},
                        "description": {"$ref": "#/definitions/description"},
                        "descriptions": {"$ref": "#/definitions/descriptions"},
                        "proxy": {"$ref": "#/definitions/anyUri"},
                        "scheme": {"type": "string", "enum": ["nosec"]},
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
                        "scheme": {"type": "string", "enum": ["combo"]},
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
                        "scheme": {"type": "string", "enum": ["combo"]},
                        "allOf": {
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
                        "scheme": {"type": "string", "enum": ["basic"]},
                        "in": {
                            "type": "string",
                            "enum": ["header", "query", "body", "cookie"],
                        },
                        "name": {"type": "string"},
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
                        "scheme": {"type": "string", "enum": ["digest"]},
                        "qop": {"type": "string", "enum": ["auth", "auth-int"]},
                        "in": {
                            "type": "string",
                            "enum": ["header", "query", "body", "cookie"],
                        },
                        "name": {"type": "string"},
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
                        "scheme": {"type": "string", "enum": ["apikey"]},
                        "in": {
                            "type": "string",
                            "enum": ["header", "query", "body", "cookie"],
                        },
                        "name": {"type": "string"},
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
                        "scheme": {"type": "string", "enum": ["bearer"]},
                        "authorization": {"$ref": "#/definitions/anyUri"},
                        "alg": {"type": "string"},
                        "format": {"type": "string"},
                        "in": {
                            "type": "string",
                            "enum": ["header", "query", "body", "cookie"],
                        },
                        "name": {"type": "string"},
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
                        "scheme": {"type": "string", "enum": ["psk"]},
                        "identity": {"type": "string"},
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
                        "scheme": {"type": "string", "enum": ["oauth2"]},
                        "authorization": {"$ref": "#/definitions/anyUri"},
                        "token": {"$ref": "#/definitions/anyUri"},
                        "refresh": {"$ref": "#/definitions/anyUri"},
                        "scopes": {
                            "oneOf": [
                                {"type": "array", "items": {"type": "string"}},
                                {"type": "string"},
                            ]
                        },
                        "flow": {"type": "string", "enum": ["code"]},
                        "tm:ref": {"$ref": "#/definitions/tm_ref"},
                    },
                },
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
        },
        "actions": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/action_element"},
        },
        "events": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/event_element"},
        },
        "description": {"$ref": "#/definitions/description"},
        "descriptions": {"$ref": "#/definitions/descriptions"},
        "version": {"type": "object", "properties": {"instance": {"type": "string"}}},
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
        },
        "schemaDefinitions": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {"$ref": "#/definitions/dataSchema"},
        },
        "support": {"$ref": "#/definitions/anyUri"},
        "created": {"type": "string"},
        "modified": {"type": "string"},
        "security": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "minItems": 1, "items": {"type": "string"}},
            ]
        },
        "@type": {"$ref": "#/definitions/tm_type_declaration"},
        "@context": {"$ref": "#/definitions/thing-context"},
        "tm:required": {"$ref": "#/definitions/tm_required"},
    },
    "additionalProperties": True,
    "required": ["@context", "@type"],
}
