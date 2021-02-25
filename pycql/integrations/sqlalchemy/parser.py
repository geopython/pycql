
import logging
import re

from ...parser import parse as _plain_parse
from ...util import parse_duration
from dateparser import parse as parse_datetime
from sqlalchemy import func

LOGGER = logging.getLogger(__name__)


def parse_geometry(geom):
    LOGGER.debug(f"PARSE GEOM: {geom}")
    search = re.search(r"SRID=(\d+);", geom)

    sridtxt = "" if search else "SRID=4326;"
    LOGGER.debug(f"{sridtxt}{geom}")

    return func.ST_GeomFromEWKT(f"{sridtxt}{geom}")


def parse_bbox(box, srid: int=4326):
    LOGGER.debug("PARSE BBOX: {type(box)}, {box}")
    minx, miny, maxx, maxy = box
    return func.ST_GeomFromEWKT(
        f"SRID={srid};POLYGON(("
        f"{minx} {miny}, {minx} {maxy}, "
        f"{maxx} {maxy}, {maxx} {miny}, "
        f"{minx} {miny}))"
    )


def parse(cql):
    """ Shorthand for the :func:`pycql.parser.parse` function with
        the required factories set up.

        :param cql: the CQL expression string to parse
        :type cql: str
        :return: the parsed CQL expression as an AST
        :rtype: ~pycql.ast.Node
    """
    return _plain_parse(
        cql,
        geometry_factory=parse_geometry,
        bbox_factory=parse_bbox,
        time_factory=parse_datetime,
        duration_factory=parse_duration,
    )
