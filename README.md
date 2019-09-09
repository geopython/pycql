# pycql

[![Build Status](https://travis-ci.org/EOxServer/pycql.svg?branch=master)](https://travis-ci.org/EOxServer/pycql)

A pure python CQL parser.

## Installation

```bash
pip install pycql
```

## Usage

The basic functionality parses the input string to an abstract syntax tree (AST) representation.
This AST can then be used to build database filters or similar functionality.

```python
import pycql

ast = pycql.parse(filter_expression)
```

## Testing

The basic functionality can be tested using `pytest`.

```bash
python -m pytest
```

There is a test project/app to test the Django integration. This is tested using the following
command:

```bash
python manage.py test testapp
```


## Django integration

For Django there is a default bridging implementation, where all the filters are translated to the
Django ORM. In order to use this integration, we need two dictionaries, one mapping the available
fields to the Django model fields, and one to map the fields that use `choices`. Consider the
following example models:

```python
from django.contrib.gis.db import models


optional = dict(null=True, blank=True)

class Record(models.Model):
    identifier = models.CharField(max_length=256, unique=True, null=False)
    geometry = models.GeometryField()

    float_attribute = models.FloatField(**optional)
    int_attribute = models.IntegerField(**optional)
    str_attribute = models.CharField(max_length=256, **optional)
    datetime_attribute = models.DateTimeField(**optional)
    choice_attribute = models.PositiveSmallIntegerField(choices=[
                                                                 (1, 'ASCENDING'),
                                                                 (2, 'DESCENDING'),],
                                                        **optional)


class RecordMeta(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='record_metas')

    float_meta_attribute = models.FloatField(**optional)
    int_meta_attribute = models.IntegerField(**optional)
    str_meta_attribute = models.CharField(max_length=256, **optional)
    datetime_meta_attribute = models.DateTimeField(**optional)
    choice_meta_attribute = models.PositiveSmallIntegerField(choices=[
                                                                      (1, 'X'),
                                                                      (2, 'Y'),
                                                                      (3, 'Z')],
                                                             **optional)
```

Now we can specify the field mappings and mapping choices to be used when applying the filters:

```python
FIELD_MAPPING = {
    'identifier': 'identifier',
    'geometry': 'geometry',
    'floatAttribute': 'float_attribute',
    'intAttribute': 'int_attribute',
    'strAttribute': 'str_attribute',
    'datetimeAttribute': 'datetime_attribute',
    'choiceAttribute': 'choice_attribute',

    # meta fields
    'floatMetaAttribute': 'record_metas__float_meta_attribute',
    'intMetaAttribute': 'record_metas__int_meta_attribute',
    'strMetaAttribute': 'record_metas__str_meta_attribute',
    'datetimeMetaAttribute': 'record_metas__datetime_meta_attribute',
    'choiceMetaAttribute': 'record_metas__choice_meta_attribute',
}

MAPPING_CHOICES = {
    'choiceAttribute': dict(Record._meta.get_field('choice_attribute').choices),
    'choiceMetaAttribute': dict(RecordMeta._meta.get_field('choice_meta_attribute').choices),
}
```

Finally we are able to connect the CQL AST to the Django database models. We also provide factory
functions to parse the timestamps, durations, geometries and envelopes, so that they can be used
with the ORM layer:

```python
from pycql.integrations.django import to_filter

cql_expr = 'strMetaAttribute LIKE "%parent%" AND datetimeAttribute BEFORE 2000-01-01T00:00:01Z'

ast = pycql.parse(
    cql_expr, GEOSGeometry, Polygon.from_bbox, parse_datetime,
    parse_duration
)
filters = to_filter(ast, mapping, mapping_choices)

qs = Record.objects.filter(**filters)
```
