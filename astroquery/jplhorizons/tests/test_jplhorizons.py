# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest

from astropy.time import Time
import astropy.units as u
from astropy.coordinates.earth import EarthLocation

from astroquery.utils.mocks import MockResponse
# from ...query import AstroQuery
from ... import jplhorizons as jh

@pytest.mark.parametrize(
    ["target", "query_type", "closest_apparition", "fragments", "expected"],
    (
        ["Jupiter", None, False, True, "Jupiter"],
        ["Io", "small body", False, True, "Io;"],
        ["Io", "smallbody", False, True, "Io;"],
        ["Io", "name", False, True, "NAME=Io;"],
        ["Io", "asteroid name", False, True, "ASTNAM=Io;"],
        ["Io", "asteroid_name", False, True, "ASTNAM=Io;"],
        ["2P", "designation", False, True, "DES=2P;"],
        ["2P", "designation", True, True, "DES=2P;CAP;"],
        ["2P", "designation", Time("2003-11-20"), True, "DES=2P;CAP<2452963.5;"],
        ["73P", "designation", True, False, "DES=73P;CAP;NOFRAG;"],
        ["encke", "comet name", False, True, "COMNAM=encke;"],
    )
)
def test_format_command(target, query_type, closest_apparition, fragments, expected):
    command = jh.Horizons._format_command(target, query_type, closest_apparition, fragments)
    assert command == expected


def test_format_command_invalid_query_type():
    with pytest.raises(KeyError, match="Invalid query_type"):
        jh.Horizons._format_command("2P", "asdf", False, True)

def test_format_center_strng():
    payload = jh.Horizons._format_center("I41")
    assert payload == {"center": "I41"}


def test_format_center_earth_location():
    college_park = EarthLocation.from_geodetic(76.935 * u.deg, 38.9867 * u.deg, 0 * u.km)
    payload = jh.Horizons._format_center(college_park)
    assert payload == {
        "center": "coord@399",
        "coord_type": "geodetic",
        "site_coord": "76.935,38.98669999999999,0.0"
    }

def test_format_center_type_error():
    with pytest.raises(TypeError):
        jh.Horizons._format_center(568)
