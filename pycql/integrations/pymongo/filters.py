# ------------------------------------------------------------------------------
#
# Project: pycql <https://github.com/geopython/pycql>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
# Copyright (C) 2019 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

import re

import geodaisy

from ...values import Geometry
from ...ast import (
    NotConditionNode, CombinationConditionNode, ComparisonPredicateNode,
    BetweenPredicateNode, BetweenPredicateNode, LikePredicateNode,
    InPredicateNode, NullPredicateNode, TemporalPredicateNode,
    SpatialPredicateNode, BBoxPredicateNode, AttributeExpression,
    LiteralExpression, ArithmeticExpressionNode,
)


def negate(expr, not_=True):
    if not_:
        return {'$not': expr}
    return expr

def combine(sub_exprs, op):
    op = op.lower()
    assert op in ('and', 'or')
    assert isinstance(sub_exprs, (list, tuple))
    return {'$%s' % op: sub_exprs}


OP_TO_COMP = {
    "<": "$lt",
    "<=": "$lte",
    ">": "$gt",
    ">=": "$gte",
    "<>": "$ne",
    "=": "$eq"
}


def compare(lhs, rhs, op, mapping_choices=None):
    assert isinstance(lhs, str)
    return {lhs: {OP_TO_COMP[op]: rhs}}


def between(lhs, low, high, not_=False):
    return negate({lhs: {'$lte': high, '$gte': low}}, not_)


def like(lhs, rhs, case=False, not_=False, mapping_choices=None):
    assert isinstance(lhs, str)
    assert isinstance(rhs, str)
    return negate({
        lhs: {
            '$regex': re.compile(".*".join(rhs.split('%')), re.IGNORECASE if not case else 0)
        }
    }, not_)


def contains(lhs, rhs, not_=False, mapping_choices=None):
    assert isinstance(lhs, str)
    assert isinstance(rhs, list)
    return negate({
        lhs: {
            '$in': rhs
        }
    }, not_)


def null(lhs, not_=False):
    assert isinstance(lhs, str)
    return negate({
        lhs: {
            '$type': 'null'
        }
    }, not_)

def attribute(lhs, field_mapping=None):
    if field_mapping:
        return field_mapping[lhs]
    return lhs


# feet, meters,  statute miles, nautical miles, kilometers

UNIT_FACTORS = {
    'feet': 0.3048,
    'meters': 1,
    'statute miles': 1609.344,
    'nautical miles': 1852,
    'kilometers': 1000,
}

def _to_meters(amount, units):
    return amount * UNIT_FACTORS[units]


def spatial(lhs, rhs, op, pattern, distance, units):
    assert isinstance(lhs, str)
    assert isinstance(rhs, Geometry)
    assert op in (
        "INTERSECTS", "DISJOINT", "CONTAINS", "WITHIN", "TOUCHES", "CROSSES",
        "OVERLAPS", "EQUALS", "RELATE", "DWITHIN", "BEYOND"
    )
    
    if op not in ("WITHIN", "INTERSECTS", "DWITHIN", "BEYOND"):
        raise Exception('Spatial operation %s is not supported' % op)

    if op == "WITHIN":
        return {
            lhs: {
                '$geoWithin': {
                    '$geometry': geodaisy.converters.wkt_to_geo_interface(rhs.value)
                }
            }
        }

    elif op == "INTERSECTS":
        return {
            lhs: {
                '$geoIntersects': {
                    '$geometry': geodaisy.converters.wkt_to_geo_interface(rhs.value)
                }
            }
        }

    elif op == "DWITHIN":
        return {
            lhs: {
                '$nearSphere': {
                    '$geometry': geodaisy.converters.wkt_to_geo_interface(rhs.value),
                    '$maxDistance': _to_meters(distance, units)
                }
            }
        }

    elif op == "BEYOND":
        return {
            lhs: {
                '$nearSphere': {
                    '$geometry': geodaisy.converters.wkt_to_geo_interface(rhs.value),
                    '$minDistance': _to_meters(distance, units)
                }
            }
        }

def bbox(lhs, minx, miny, maxx, maxy, crs):
    assert isinstance(lhs, str)
    return {
        lhs: {
            '$geoIntersects': {
                '$geometry': {
                    'type': 'Polygon',
                    'coordinates': [[
                        [minx, miny], [minx, maxy],
                        [maxx, maxy], [maxx, miny],
                        [minx, miny]
                    ]]
                }
            }
        }
    }
