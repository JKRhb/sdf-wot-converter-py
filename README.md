[![Build Status](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml/badge.svg)](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml)
[![PyPI version](https://badge.fury.io/py/sdf-wot-converter.svg)](https://badge.fury.io/py/sdf-wot-converter)
[![codecov](https://codecov.io/gh/JKRhb/sdf-wot-converter-py/branch/main/graph/badge.svg?token=AWAN1GHKD8)](https://codecov.io/gh/JKRhb/sdf-wot-converter-py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# SDF-WoT-Converter (Python Edition)

This repository provides a Python-based converter from [SDF](https://datatracker.ietf.org/doc/html/draft-ietf-asdf-sdf-05) to [WoT TD](https://www.w3.org/TR/wot-thing-description/) including Thing Models.

The converter is both usable as a library and a command line tool. It is based on my [Rust implementation](https://github.com/JKRhb/sdf-wot-converter) but is (when it comes to the conversion from SDF to Thing Models) already more mature as development in Python turned out to be much faster. The final version of this converter, however, will be reimplemented in Rust once it is finished to also support more constrained environments.

The CI pipeline is set up to automatically convert all (valid) models from the [oneDM playground](https://github.com/one-data-model/playground) to WoT Thing Models and upload to the results to [this repository](https://github.com/JKRhb/onedm-playground-wot-tm).

## Installation

You can install the converter using pip:

```sh
pip install sdf-wot-converter
```

Afterwards, it can be used both as a command line tool and a library.

## Using the command line tool

After installing the libary you should be able to call the converter in your terminal using `sdf-wot-converter`. You can display available parameters by typing `sdf-wot-converter --help`. So far, you can convert from SDF to WoT Thing Models and vice versa. Thing Descriptions are supposed to be added soon.

### Example

```bash
# Convert an SDF model to a WoT Thing Model
sdf-wot-converter --from-sdf examples/sdf/example.sdf.json --to-tm converted-example.tm.json

# Convert a WoT Thing Model to an SDF model
sdf-wot-converter --from-tm examples/wot/example.tm.json --to-sdf converted-example.sdf.json
```

## Using the library

With the converter installed, you can use also use it as a library in your own projects. Below you can see examples for how to convert an SDF model to a WoT Thing Model and back again. As you can see, nested definitions from `sdfObject`s or `sdfThing`s a prefixed with the respective object or thing names. Moreover, an `sdf:jsonPointer` field is added to each affordance to enable roundtripping. More detailed mapping tables will be added to this readme soon.

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
        "http://www.w3.org/ns/td",
        {"cap": "https://example.com/capability/cap", "sdf": "https://example.com/sdf"},
    ],
    "@type": "tm:ThingModel",
    "title": "Example file for OneDM Semantic Definition Format",
    "description": "Copyright 2019 Example Corp. All rights reserved.",
    "links": [{"href": "https://example.com/license", "rel": "license"}],
    "version": {"model": "2019-04-24"},
    "sdf:defaultNamespace": "cap",
    "actions": {
        "Switch_on": {
            "sdf:jsonPointer": "#/sdfObject/Switch/sdfAction/on",
            "description": "Turn the switch on; equivalent to setting value to true.",
        },
        "Switch_off": {
            "sdf:jsonPointer": "#/sdfObject/Switch/sdfAction/off",
            "description": "Turn the switch off; equivalent to setting value to false.",
        },
        "Switch_toggle": {
            "sdf:jsonPointer": "#/sdfObject/Switch/sdfAction/toggle",
            "description": "Toggle the switch; equivalent to setting value to its complement.",
        },
    },
    "properties": {
        "Switch_value": {
            "sdf:jsonPointer": "#/sdfObject/Switch/sdfProperty/value",
            "description": "The state of the switch; false for off and true for on.",
            "type": "boolean",
        }
    },
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
