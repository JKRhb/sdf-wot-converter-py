[![Build Status](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml/badge.svg)](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml)
[![PyPI version](https://badge.fury.io/py/sdf-wot-converter.svg)](https://badge.fury.io/py/sdf-wot-converter)
[![codecov](https://codecov.io/gh/JKRhb/sdf-wot-converter-py/branch/main/graph/badge.svg?token=AWAN1GHKD8)](https://codecov.io/gh/JKRhb/sdf-wot-converter-py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# SDF-WoT-Converter

This repository provides a Python-based converter from [SDF](https://datatracker.ietf.org/doc/html/draft-ietf-asdf-sdf-05) to [WoT TD](https://www.w3.org/TR/wot-thing-description/) including Thing Models.

The converter is both usable as a library and a command line tool. It provides
conversion functions between WoT Thing Descriptions, WoT Thing Models and SDF
Models (one for each combination). You can find a number of examples for the
usage of the converter down below.

The CI pipeline is set up to automatically convert all (valid) models from the [oneDM playground](https://github.com/one-data-model/playground) to WoT Thing Models and upload to the results to [this repository](https://github.com/JKRhb/onedm-playground-wot-tm).

## Installation

You can install the converter using pip:

```sh
pip install sdf-wot-converter
```

Afterwards, it can be used both as a command line tool and a library.

## Using the command line tool

After installing the libary you should be able to call the converter in your terminal using `sdf-wot-converter` and one of the six available subcommands:

* `sdf-to-tm`
* `sdf-to-td`
* `td-to-tm`
* `td-to-sdf`
* `tm-to-td`
* `tm-to-sdf`

You can display available parameters by typing `sdf-wot-converter --help`.
A usage example for each subcommand can be found below.

### Examples

```bash
# Convert an SDF model to a WoT Thing Model
sdf-wot-converter sdf-to-tm -i examples/sdf/example.sdf.json -o converted-example.tm.jsonld

# Convert an SDF model to a WoT Thing Description
sdf-wot-converter sdf-to-td -i examples/sdf/example.sdf.json --mapping-files examples/sdf/example.sdf-mapping.json -o converted-example.td.jsonld

# Convert a WoT Thing Model to an SDF model
sdf-wot-converter tm-to-sdf -i examples/wot/example.tm.jsonld -o converted-example.sdf.json

# Convert a WoT Thing Model to a WoT Thing Description
sdf-wot-converter tm-to-td -i examples/wot/example-with-bindings.tm.jsonld -o converted-example.td.jsonld

# Convert a WoT Thing Description to an SDF model and a mapping file
sdf-wot-converter td-to-sdf -i examples/wot/example.td.jsonld -o converted-example.sdf.json --mapping-file-output converted-example.sdf-mapping.json

# Convert a WoT Thing Description to a WoT Thing Model
sdf-wot-converter td-to-tm -i examples/wot/example.td.jsonld -o converted-example.tm.jsonld
```

## Using the library

With the converter installed, you can use also use it as a library in your own projects. Below you can see examples for how to convert an SDF model to a WoT Thing Model and back again. As you can see, nested definitions from `sdfObject`s or `sdfThing`s are prefixed with the respective object or thing names.

```python
from sdf_wot_converter import (
    convert_sdf_to_wot_tm,
    convert_wot_tm_to_sdf,
)

sdf_model = {
    "info": {
        "title": "Example file for OneDM Semantic Definition Format",
        "version": "2019-04-24",
        "copyright": "Copyright 2019 Example Corp. All rights reserved.",
        "license": "https://example.com/license",
    },
    "namespace": {"cap": "https://example.com/capability/cap"},
    "defaultNamespace": "cap",
    "sdfObject": {
        "Switch": {
            "sdfProperty": {
                "value": {
                    "description": "The state of the switch; false for off and true for on.",
                    "type": "boolean",
                    "observable": False,
                }
            },
            "sdfAction": {
                "on": {
                    "description": "Turn the switch on; equivalent to setting value to true."
                },
                "off": {
                    "description": "Turn the switch off; equivalent to setting value to false."
                },
                "toggle": {
                    "description": "Toggle the switch; equivalent to setting value to its complement."
                },
            },
        }
    },
}

thing_model = convert_sdf_to_wot_tm(sdf_model)

expected_thing_model = {
    "@context": [
        "https://www.w3.org/2022/wot/td/v1.1",
        {
            "cap": "https://example.com/capability/cap",
            "sdf": "https://example.com/sdf",
        },
    ],
    "@type": "tm:ThingModel",
    "sdf:title": "Example file for OneDM Semantic Definition Format",
    "sdf:copyright": "Copyright 2019 Example Corp. All rights reserved.",
    "links": [{"href": "https://example.com/license", "rel": "license"}],
    "version": {"model": "2019-04-24"},
    "sdf:defaultNamespace": "cap",
    "actions": {
        "on": {
            "description": "Turn the switch on; equivalent to setting value to true.",
        },
        "off": {
            "description": "Turn the switch off; equivalent to setting value to false.",
        },
        "toggle": {
            "description": "Toggle the switch; equivalent to setting value to its complement.",
        },
    },
    "properties": {
        "value": {
            "description": "The state of the switch; false for off and true for on.",
            "type": "boolean",
            "observable": False,
        }
    },
    "sdf:objectKey": "Switch",
}

assert thing_model == expected_thing_model

sdf_roundtrip_model = convert_wot_tm_to_sdf(thing_model)

assert sdf_model == sdf_roundtrip_model
```

## License

This project is licensed under the MIT license.

```
SPDX-License-Identifier: MIT
```
