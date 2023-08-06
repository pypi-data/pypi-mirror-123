# d2b-asl

Plugin for the d2b package to handle configuration files written in YAML.

[![PyPI Version](https://img.shields.io/pypi/v/d2b-yaml.svg)](https://pypi.org/project/d2b-yaml/)

## Installation

```bash
pip install d2b-yaml
```

## User Guide

This package adds support for configuration files written in YAML. Once this package is installed one can then run something like:

```bash
d2b run \
  --config="d2b-config.yaml" \
  --participant="01" \
  --session="001"
  --out-dir="my/bids/dataset/dir/" \
  "my/input/dir/"
```

See [`examples/d2b-config.yaml`](https://github.com/d2b-dev/d2b-yaml/blob/master/examples/d2b-config.yaml). The Schema for YAML configuration files is exactly the same as for JSON configuration files ([JSON Schema](https://github.com/d2b-dev/d2b/blob/master/json-schemas/schema.json))
