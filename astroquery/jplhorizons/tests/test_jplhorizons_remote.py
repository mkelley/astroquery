# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest

from astropy.time import Time
import astropy.units as u

from ... import jplhorizons as jh

class TestMultipleTargetMatches:
    def test_major_body(self):
        result = jh.Horizons.query_observer("Jupiter")

