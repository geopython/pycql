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
# The above copyright notice and this permission notice shall be included in
# all copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------


from datetime import datetime, timedelta
from functools import reduce
from inspect import signature
from typing import List, Any
from sqlalchemy import and_, func, not_, or_


# ------------------------------------------------------------------------------
# Filters
# ------------------------------------------------------------------------------
class Operator(object):

    OPERATORS = {
        "is_null": lambda f: f.is_(None),
        "is_not_null": lambda f: f.isnot(None),
        "==": lambda f, a: f == a,
        "=": lambda f, a: f == a,
        "eq": lambda f, a: f == a,
        "!=": lambda f, a: f != a,
        "ne": lambda f, a: f != a,
        ">": lambda f, a: f > a,
        "gt": lambda f, a: f > a,
        "<": lambda f, a: f < a,
        "lt": lambda f, a: f < a,
        ">=": lambda f, a: f >= a,
        "ge": lambda f, a: f >= a,
        "<=": lambda f, a: f <= a,
        "le": lambda f, a: f <= a,
        "like": lambda f, a: f.like(a),
        "ilike": lambda f, a: f.ilike(a),
        "not_ilike": lambda f, a: ~f.ilike(a),
        "in": lambda f, a: f.in_(a),
        "not_in": lambda f, a: ~f.in_(a),
        "any": lambda f, a: f.any(a),
        "not_any": lambda f, a: func.not_(f.any(a)),
        "INTERSECTS": lambda f, a: f.ST_Contains(a),
        "DISJOINT": lambda f, a: f.ST_Disjoint(a),
        "CONTAINS": lambda f, a: f.ST_Contains(a),
        "WITHIN": lambda f, a: f.ST_Within(a),
        "TOUCHES": lambda f, a: f.ST_Touches(a),
        "CROSSES": lambda f, a: f.ST_Crosses(a),
        "OVERLAPS": lambda f, a: f.ST_Overlaps(a),
        "EQUALS": lambda f, a: f.ST_Equals(a),
        "RELATE": lambda f, a, pattern: f.ST_Relate(a, pattern),
        "DWITHIN": lambda f, a, distance: f.ST_Dwithin(a, distance),
        "BEYOND": lambda f, a, distance: ~f.ST_Dwithin(a, distance),
        "+": lambda f, a: f + a,
        "-": lambda f, a: f - a,
        "*": lambda f, a: f * a,
        "/": lambda f, a: f / a,
    }

    def __init__(self, operator: str = None):
        if not operator:
            operator = "=="

        if operator not in self.OPERATORS:
            raise Exception("Operator `{}` not valid.".format(operator))

        self.operator = operator
        self.function = self.OPERATORS[operator]
        self.arity = len(signature(self.function).parameters)


def combine(
    sub_filters: List[Any], combinator: str = "AND"
) -> Any:
    """ Combine filters using a logical combinator

        :param sub_filters: the filters to combine
        :param combinator: a string: "AND" / "OR"
        :return: the combined filter
    """
    assert combinator in ("AND", "OR")
    op = and_ if combinator == "AND" else or_
    print(type(sub_filters))

    def test(acc, q):
        print(type(acc), type(q))
        return op(acc, q)

    return reduce(test, sub_filters)


def negate(sub_filter):
    """ Negate a filter, opposing its meaning.

        :param sub_filter: the filter to negate
        :return: the negated filter
    """
    return not_(sub_filter)


def compare(
    lhs, rhs, op: str
):
    """ Compare a filter with an expression using a comparison operation

        :param lhs: the field to compare
        :param rhs: the filter expression
        :param op: a string denoting the operation. one of ``"<"``, ``"<="``,
                   ``">"``, ``">="``, ``"<>"``, ``"="``
        :return: a comparison expression object
    """
    _op = Operator(op)
    print(type(lhs), type(rhs))

    if _op.arity > 1:
        return _op.function(lhs, rhs)
    else:
        return _op.function(lhs)


def between(lhs, low, high, negate=False):
    """ Create a filter to match elements that have a value within a certain
        range.

        :param lhs: the field to compare
        :type lhs: :class:`django.db.models.F`
        :param low: the lower value of the range
        :type low:
        :param high: the upper value of the range
        :type high:
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :return: a comparison expression object
        :rtype: :class:`django.db.models.Q`
    """
    l_op = Operator("<=")
    g_op = Operator(">=")
    if negate:
        return not_(and_(g_op.function(lhs, low), l_op.function(lhs, high)))
    return and_(g_op.function(lhs, low), l_op.function(lhs, high))


def like(lhs, rhs, case=False, negate=False, mapping_choices=None):
    """ Create a filter to filter elements according to a string attribute using
        wildcard expressions.

        :param lhs: the field to compare
        :type lhs: :class:`django.db.models.F`
        :param rhs: the wildcard pattern: a string containing any number of '%'
                    characters as wildcards.
        :type rhs: str
        :param case: whether the lookup shall be done case sensitively or not
        :type case: bool
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :param mapping_choices: a dict to lookup potential choices for a
                                certain field.
        :type mapping_choices: dict[str, str]
        :return: a comparison expression object
        :rtype: :class:`django.db.models.Q`
    """
    if case:
        op = Operator("like")
    else:
        op = Operator("ilike")

    if negate:
        return not_(op.function(lhs, rhs))
    return op.function(lhs, rhs)


def contains(lhs, items, not_=False, mapping_choices=None):
    """ Create a filter to match elements attribute to be in a list of choices.

        :param lhs: the field to compare
        :type lhs: :class:`django.db.models.F`
        :param items: a list of choices
        :type items: list
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :param mapping_choices: a dict to lookup potential choices for a
                                certain field.
        :type mapping_choices: dict[str, str]
        :return: a comparison expression object
        :rtype: :class:`django.db.models.Q`
    """
    op = Operator("in")
    if negate:
        return not_(op.function(lhs, items))
    return op.function(lhs, items)


def null(lhs, not_=False):
    """ Create a filter to match elements whose attribute is (not) null

        :param lhs: the field to compare
        :type lhs: :class:`django.db.models.F`
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :return: a comparison expression object
        :rtype: :class:`django.db.models.Q`
    """

    op = Operator("is_null")
    if negate:
        return not_(op.function(lhs))
    return op.function(lhs)


def temporal(lhs, time_or_period, op):
    """ Create a temporal filter for the given temporal attribute.

        :param lhs: the field to compare
        :type lhs: :class:`django.db.models.F`
        :param time_or_period: the time instant or time span to use as a filter
        :type time_or_period: :class:`datetime.datetime` or a tuple of two
                              datetimes or a tuple of one datetime and one
                              :class:`datetime.timedelta`
        :param op: the comparison operation. one of ``"BEFORE"``,
                   ``"BEFORE OR DURING"``, ``"DURING"``, ``"DURING OR AFTER"``,
                   ``"AFTER"``.
        :type op: str
        :return: a comparison expression object
        :rtype: :class:`django.db.models.Q`
    """
    low = None
    high = None
    if op in ("BEFORE", "AFTER"):
        assert isinstance(time_or_period, datetime)
        if op == "BEFORE":
            high = time_or_period
        else:
            low = time_or_period
    else:
        low, high = time_or_period
        assert isinstance(low, datetime) or isinstance(high, datetime)

        if isinstance(low, timedelta):
            low = high - low
        if isinstance(high, timedelta):
            high = low + high

    if low and high:
        return between(lhs, low, high)
    elif low:
        return compare(lhs, low, ">=")
    else:
        return compare(lhs, high, "<=")


UNITS_LOOKUP = {"kilometers": "km", "meters": "m"}


def spatial(lhs, rhs, op, pattern=None, distance=None, units=None):
    """ Create a spatial filter for the given spatial attribute.

        :param lhs: the field to compare
        :type lhs: :class:`django.db.models.F`
        :param rhs: the time instant or time span to use as a filter
        :type rhs:
        :param op: the comparison operation. one of ``"INTERSECTS"``,
                   ``"DISJOINT"``, `"CONTAINS"``, ``"WITHIN"``,
                   ``"TOUCHES"``, ``"CROSSES"``, ``"OVERLAPS"``,
                   ``"EQUALS"``, ``"RELATE"``, ``"DWITHIN"``, ``"BEYOND"``
        :type op: str
        :param pattern: the spatial relation pattern
        :type pattern: str
        :param distance: the distance value for distance based lookups:
                         ``"DWITHIN"`` and ``"BEYOND"``
        :type distance: float
        :param units: the units the distance is expressed in
        :type units: str
        :return: a comparison expression object
        :rtype: :class:`django.db.models.Q`
    """

    op_ = Operator(op)
    if op == "RELATE":
        return op_.function(lhs, rhs, pattern)
    elif op in ("DWITHIN", "BEYOND"):
        if units == "kilometers":
            distance = distance / 1000
        elif units == "miles":
            distance = distance / 1609
        return op_.function(lhs, rhs, distance)
    else:
        return op_.function(lhs, rhs)


def bbox(lhs, minx, miny, maxx, maxy, crs=4326, bboverlaps=True):
    """ Create a bounding box filter for the given spatial attribute.

        :param lhs: the field to compare
        :param minx: the lower x part of the bbox
        :type minx: float
        :param miny: the lower y part of the bbox
        :type miny: float
        :param maxx: the upper x part of the bbox
        :type maxx: float
        :param maxy: the upper y part of the bbox
        :type maxy: float
        :param crs: the CRS the bbox is expressed in
        :type crs: str
        :type lhs: :class:`django.db.models.F`
        :return: a comparison expression object
        :rtype: :class:`django.db.models.Q`
    """

    return lhs.ST_Intersects(
        func.ST_MakeEnvelope(minx, miny, maxx, maxy, crs).ST_Transform(4326)
    )


def attribute(name, model=None, field_mapping=None):
    """ Create an attribute lookup expression using a field mapping dictionary.

        :param name: the field filter name
        :type name: str
        :param field_mapping: the dictionary to use as a lookup.
        :type mapping_choices: dict[str, str]
        :rtype: :class:`django.db.models.F`
    """
    if field_mapping:
        field = field_mapping.get(name, name)
    else:
        field = name
    return getattr(model, field)


def literal(value):
    return value


def arithmetic(lhs, rhs, op):
    """ Create an arithmetic filter

        :param lhs: left hand side of the arithmetic expression. either a
                    scalar or a field lookup or another type of expression
        :param rhs: same as `lhs`
        :param op: the arithmetic operation. one of
         ``"+"``, ``"-"``, ``"*"``, ``"/"``
        :rtype: :class:`django.db.models.F`
    """

    op_ = Operator(op)
    return op_.function(lhs, rhs)
