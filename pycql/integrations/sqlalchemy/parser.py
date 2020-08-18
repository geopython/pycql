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

from django.contrib.gis.geos import Polygon, MultiPolygon, GEOSGeometry
from django.utils.dateparse import parse_datetime

from ...parser import parse as _plain_parse
from ...util import parse_duration


def parse(cql):
    """ Shorthand for the :func:`pycql.parser.parse` function with
        the required factories set up.

        :param cql: the CQL expression string to parse
        :type cql: str
        :return: the parsed CQL expression as an AST
        :rtype: ~pycql.ast.Node 
    """
    return _plain_parse(
        cql, GEOSGeometry, Polygon.from_bbox, parse_datetime,
        parse_duration
    )
