# ------------------------------------------------------------------------------
#
# Project: pycql <http://github.com/constantinius/pycql>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
# Copyright (C) 2017 EOX IT Services GmbH
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

from pycql import parse, get_repr
from pycql.ast import *


def test_attribute_eq_literal():
    ast = parse('attr = "A"')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression('A'),
        '='
    )

def test_attribute_lt_literal():
    ast = parse('attr < 5')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression(5.0),
        '<'
    )

def test_attribute_lte_literal():
    ast = parse('attr <= 5')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression(5.0),
        '<='
    )

def test_attribute_gt_literal():
    ast = parse('attr > 5')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression(5.0),
        '>'
    )

def test_attribute_gte_literal():
    ast = parse('attr >= 5')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression(5.0),
        '>='
    )

def test_attribute_ne_literal():
    ast = parse('attr <> 5')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression(5),
        '<>'
    )

def test_attribute_between():
    ast = parse('attr BETWEEN 2 AND 5')
    assert ast == BetweenPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression(2),
        LiteralExpression(5),
        False,
    )

def test_attribute_not_between():
    ast = parse('attr NOT BETWEEN 2 AND 5')
    assert ast == BetweenPredicateNode(
        AttributeExpression('attr'),
        LiteralExpression(2),
        LiteralExpression(5),
        True,
    )

def test_string_like():
    ast = parse('attr LIKE "some%"')
    assert ast == LikePredicateNode(
        AttributeExpression('attr'),
        LiteralExpression('some%'),
        True,
        False,
    )

def test_string_ilike():
    ast = parse('attr ILIKE "some%"')
    assert ast == LikePredicateNode(
        AttributeExpression('attr'),
        LiteralExpression('some%'),
        False,
        False,
    )

def test_string_not_like():
    ast = parse('attr NOT LIKE "some%"')
    assert ast == LikePredicateNode(
        AttributeExpression('attr'),
        LiteralExpression('some%'),
        True,
        True,
    )

def test_string_not_ilike():
    ast = parse('attr NOT ILIKE "some%"')
    assert ast == LikePredicateNode(
        AttributeExpression('attr'),
        LiteralExpression('some%'),
        False,
        True,
    )

def test_attribute_in_list():
    ast = parse('attr IN (1, 2, 3, 4)')
    assert ast == InPredicateNode(
        AttributeExpression('attr'), [
            LiteralExpression(1),
            LiteralExpression(2),
            LiteralExpression(3),
            LiteralExpression(4),
        ],
        False
    )

def test_attribute_not_in_list():
    ast = parse('attr NOT IN ("A", "B", \'C\', \'D\')')
    assert ast == InPredicateNode(
        AttributeExpression('attr'), [
            LiteralExpression("A"),
            LiteralExpression("B"),
            LiteralExpression("C"),
            LiteralExpression("D"),
        ],
        True
    )

def test_attribute_is_null():
    ast = parse('attr IS NULL')
    assert ast == NullPredicateNode(
        AttributeExpression('attr'), False
    )

def test_attribute_is_not_null():
    ast = parse('attr IS NOT NULL')
    assert ast == NullPredicateNode(
        AttributeExpression('attr'), True
    )

# Temporal predicate

# Spatial predicate

# BBox prediacte

def test_attribute_arithmetic_add():
    ast = parse('attr = 5 + 2')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        ArithmeticExpressionNode(
            LiteralExpression(5),
            LiteralExpression(2),
            '+',
        ),
        '=',
    )

def test_attribute_arithmetic_sub():
    ast = parse('attr = 5 - 2')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        ArithmeticExpressionNode(
            LiteralExpression(5),
            LiteralExpression(2),
            '-',
        ),
        '=',
    )

def test_attribute_arithmetic_mul():
    ast = parse('attr = 5 * 2')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        ArithmeticExpressionNode(
            LiteralExpression(5),
            LiteralExpression(2),
            '*',
        ),
        '=',
    )

def test_attribute_arithmetic_div():
    ast = parse('attr = 5 / 2')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        ArithmeticExpressionNode(
            LiteralExpression(5),
            LiteralExpression(2),
            '/',
        ),
        '=',
    )


def test_attribute_arithmetic_add_mul():
    ast = parse('attr = 3 + 5 * 2')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        ArithmeticExpressionNode(
            LiteralExpression(3),
            ArithmeticExpressionNode(
                LiteralExpression(5),
                LiteralExpression(2),
                '*',
            ),
            '+',
        ),
        '=',
    )

def test_attribute_arithmetic_div_sub():
    ast = parse('attr = 3 / 5 - 2')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        ArithmeticExpressionNode(
            ArithmeticExpressionNode(
                LiteralExpression(3),
                LiteralExpression(5),
                '/',
            ),
            LiteralExpression(2),
            '-',
        ),
        '=',
    )

def test_attribute_arithmetic_div_sub_bracketted():
    ast = parse('attr = 3 / (5 - 2)')
    assert ast == ComparisonPredicateNode(
        AttributeExpression('attr'),
        ArithmeticExpressionNode(
            LiteralExpression(3),
            ArithmeticExpressionNode(
                LiteralExpression(5),
                LiteralExpression(2),
                '-',
            ),
            '/',
        ),
        '=',
    )
