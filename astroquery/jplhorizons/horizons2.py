# Licensed under a 3-clause BSD style license - see LICENSE.rst

__all__ = ["Horizons2", "Horizons2Class"]

import numpy as np

import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table

from ..query import BaseQuery
from ..utils import commons
from ..utils import prepend_docstr_nosections
from ..utils import async_to_sync
from . import conf


@async_to_sync
class Horizons2Class(BaseQuery):
    """
    Query the `JPL Horizons <https://ssd.jpl.nasa.gov/horizons/>`_ service.
    """

    URL = conf.horizons_server
    TIMEOUT = conf.timeout

    def query_observer_async(self,
                             obj,
                             *,
                             id_type=None,
                             closest_apparition=False,
                             fragments=True,
                             get_query_payload=False,
                             cache=True,
                             **kwargs):
        """
        Query for an object's observables.

        
        Parameters
        ----------
        obj : string
            The object query string.

        center : string or `~astropy.coordinates.EarthLocation`, optional
            The coordinate origin.  If given as an ``EarthLocation``, then API
            parameters ``coord_type`` and ``site_coord`` will be automatically
            set.

        **kwargs
            Additional keyword arguments are passed on as API parameters.  Some
            parameters may be given as `~astropy.time.Time` or
            `~astropy.units.Quantity` objects.

        Examples
        --------

        Object specifications:

        >>> from astroquery.jplhorizons import Horizons2
        >>> Horizons2.query_observer("Jupiter")
        >>>
        >>> Horizons2.query_observer("1", center="568")
        >>>
        >>> Horizons2.query_observer("europa", center="I41", id_type="name")
        >>>
        >>> Horizons2.query_observer("2P", id_type="designation")
        >>> Horizons2.query_observer("2P",
        ...                          id_type="designation",
        ...                          closest_apparition=True)
        >>>
        >>> Horizons2.query_observer("73P",
        ...                          id_type="designation",
        ...                          closest_apparition=True,
        ...                          fragments=False)
        >>>
        >>> tab = Horizons2.query_observer(
        ...     "comet",
        ...     id_type="orbit",
        ...     epoch=Time(2450200.5, scale="tdb", format="jd"),
        ...     ec=0.8241907231263196,
        ...     qr=0.532013766859137 * u.au,
        ...     tp=Time(2450077.480966184235, scale="tdb", format="jd"),
        ...     om=89.14262290335057 * u.deg,
        ...     w=326.0591239257098 * u.deg,
        ...     in=4.247821264821585 * u.deg,
        ...     a1=-5.113711376907895D-10 * u.au / u.d**2,
        ...     a2=-6.288085687976327D-10 * u.au / u.d**2)

        The observer (ephemeris center) can also be an
        `~astropy.coordinates.EarthLocation`:

        >>> from astropy.coordinates import EarthLocation
        >>> college_park = EarthLocation.from_geodetic(-76.9378 * u.deg,
        ...                                            38.9897 * u.deg,
        ...                                            21 * u.m)
        >>> tab = Horizons2.query_observer("Jupiter", center=college_park)

        Specifying time:

        >>> from astropy.time import Time
        >>> import astropy.units as u
        >>> tab = Horizons2.query_observer("Jupiter",
        ...                                start_time=Time("2023-12-11"),
        ...                                stop_time=Time("2023-12-12"),
        ...                                step_size=1 * u.hr)
        >>>
        >>> times = Time(["2023-12-11", "2023-12-20", "2024-01-08"])
        >>> tab = Horizons2.query_observer("Jupiter", tlist=times)

        """
        pass

    def query_vectors_async(self,
                            obj,
                            center,
                            *,
                            id_type=None,
                            closest_apparition=False,
                            fragments=True,
                            get_query_payload=False,
                            cache=True,
                            **kwargs):
        """
        Query for an object's Cartesian state vectors.

        
        Parameters
        ----------
        

        Examples
        --------

        >>> Horizons2.query_vectors("Jupiter", "@0")

        See :meth:`.query_observer` for examples specifying the object, center,
        and time.

        """
        pass

    def query_elements_async(self,
                             obj,
                             *,
                             id_type=None,
                             closest_apparition=False,
                             fragments=True,
                             get_query_payload=False,
                             cache=True,
                             **kwargs):
        """
        Query for an object's orbital elements.

        
        Parameters
        ----------
        

        Examples
        --------

        >>> Horizons2.query_elements("3200", "@0")

        See :meth:`.query_observer` for examples specifying the object, center,
        and time.

        """
        pass
        