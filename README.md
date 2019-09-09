# pycql

[![Build Status](https://travis-ci.org/EOxServer/pycql.svg?branch=master)](https://travis-ci.org/EOxServer/pycql)

A pure python CQL parser.

## Installation

```bash
pip install pycql
```

## Usage

```python
import pycql

ast = pycql.parse(filter_expression)
```

## Testing

```bash
python -m pytest
```