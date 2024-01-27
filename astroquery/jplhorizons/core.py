# Licensed under a 3-clause BSD style license - see LICENSE.rst

__all__ = ["Horizons", "HorizonsClass"]

from typing import Dict, Optional, Union

# import numpy as np
import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table
from astrpy.time import Time

from ..query import BaseQuery
from ..utils import commons
from ..utils import prepend_docstr_nosections
from ..utils import async_to_sync
from . import conf

@async_to_sync
class HorizonsClass(BaseQuery):
    """
    Query the `JPL Horizons <https://ssd.jpl.nasa.gov/horizons/>`_ service.
    """

    URL: str = conf.server
    TIMEOUT: int = conf.timeout

    def _get_command(self,
                     object_name: str,
                     query_type: Union[str, None],
                     closest_apparition: bool,
                     fragments: bool
                    ) -> str:
        query_type_to_command_prefix: Dict[str, str] = {
            "designation": "DES=",
            "name": "NAME=",
            "asteroid name": "ASTNAM=",
            "comet name": "COMNAM=",
            "small body": "",
            None: "",
            # legacy compatibility:
            "asteroid_name": "ASTNAM=",
            "smallbody": "",
            "comet_name": "COMNAM=",
        }

        query_type_to_command_suffix: Dict[str, str] = {
            "designation": ";",
            "name": ";",
            "asteroid name": ";",
            "comet name": ";",
            "small body": ";",
            None: "",
            # legacy compatibility:
            "asteroid_name": ";",
            "smallbody": ";",
            "comet_name": ";",
        }

        try:
            prefix: str = query_type_to_command_prefix[query_type]
        except KeyError as exc:
            raise KeyError("Invalid query_type") from exc
        
        suffix: str = query_type_to_command_suffix[query_type]

        cap: str = ""
        if query_type in ["designation", "name", "comet name", "comet_name"]:
            if closest_apparition is True:
                cap = "CAP;"
            elif isinstance(closest_apparition, Time):
                cap = "CAP<{:.1f};".format(closest_apparition.jd)

        fragments: str = "NOFRAG;" if fragments is False else ""

    def query_observer_async(self,
                             query: str,
                             *,
                             query_type: Optional[str] = None,
                             closest_apparition: Optional[Union[bool, float]] = None,
                             fragments: bool = True,
                             center: Optional[str] = None,
                             get_query_payload: bool = False,
                             cache: bool = True,
                             **kwargs
                            ) -> None:
        """
        Query for an object's observables.

        
        Parameters
        ----------
        query : string
            The target query string.

        query_type : string, optional
            The type of target query: "designation", "name", "asteroid name",
            "comet name", or "small body".

        closest_apparition : bool or `~astropy.time.Time`, optional
            For comet queries.  If `True`, match the last apparition before the
            current date.  If a `Time` object, match the last apparition before
            the specified date.

        fragments : bool, optional
            If `False`, exclude (cometary) fragments from object query.

        center : string or `~astropy.coordinates.EarthLocation`, optional
            The coordinate origin.  If given as an `EarthLocation`, then API
            parameters `coord_type` and `site_coord` will be automatically set.

        **kwargs
            Additional keyword arguments are passed on as API parameters.  Some
            parameters may be given as `~astropy.time.Time` or
            `~astropy.units.Quantity` objects.

        
        Returns
        -------
        response : `requests.Response`
            The HTTP response returned from the service.


        Examples
        --------

        Object specifications:

        >>> from astroquery.jplhorizons import Horizons
        >>> Horizons.query_observer("Jupiter")
        >>>
        >>> Horizons.query_observer("1", center="568")
        >>>
        >>> Horizons.query_observer("europa", center="I41", id_type="name")
        >>>
        >>> Horizons.query_observer("2P", id_type="designation")
        >>> Horizons.query_observer("2P",
        ...                          id_type="designation",
        ...                          closest_apparition=True)
        >>>
        >>> Horizons.query_observer("73P",
        ...                          id_type="designation",
        ...                          closest_apparition=True,
        ...                          fragments=False)
        >>>
        >>> tab = Horizons.query_observer(
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
        >>> tab = Horizons.query_observer("Jupiter", center=college_park)

        Specifying time:

        >>> from astropy.time import Time
        >>> import astropy.units as u
        >>> tab = Horizons.query_observer("Jupiter",
        ...                                start_time=Time("2023-12-11"),
        ...                                stop_time=Time("2023-12-12"),
        ...                                step_size=1 * u.hr)
        >>>
        >>> times = Time(["2023-12-11", "2023-12-20", "2024-01-08"])
        >>> tab = Horizons.query_observer("Jupiter", tlist=times)

        """
        
        request_payload = dict()

        request_payload["command"] = self.get_command(
            query,
            id_type,
            closest_apparition,
            fragments,
        )


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

        >>> Horizons.query_vectors("Jupiter", "@0")

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

        >>> Horizons.query_elements("3200", "@0")

        See :meth:`.query_observer` for examples specifying the object, center,
        and time.

        """
        pass
        

# the default tool for users to interact with is an instance of the Class
Horizons = HorizonsClass()
