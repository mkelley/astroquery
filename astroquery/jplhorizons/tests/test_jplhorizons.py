# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest

from astropy.time import Time
import astropy.units as u

from astroquery.utils.mocks import MockResponse
# from ...query import AstroQuery
from ... import jplhorizons as jh

@pytest.mark.parametrize(
    ["target", "query_type", "closest_apparition", "fragments", "expected"],
    (
        ["Jupiter", None, None, True, "Jupiter"],
        ["Io", "small body", None, True, "Io;"],
        ["Io", "name", None, True, "NAME=Io;"],
        ["Io", "asteroid name", None, True, "ASTNAM=Io;"],
        ["2P", "designation", None, True, "DES=2P;"],
        ["2P", "designation", True, True, "DES=2P;CAP;"],
        ["2P", "designation", Time("2003-11-20"), True, "DES=2P;CAP<2452963.5;"],
        ["73P", "designation", True, False, "DES=73P;CAP;NOFRAG;"]
    )
)
def test_format_command(target, query_type, closest_apparition, fragments, expected):
    command = jh.Horizons._format_command(target, query_type, closest_apparition, fragments)
    assert command == expected
