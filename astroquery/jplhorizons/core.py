# Licensed under a 3-clause BSD style license - see LICENSE.rst

__all__ = ["Horizons", "HorizonsClass"]

from typing import Dict, Optional, Union

from requests import Response
import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table
from astropy.time import Time
from astropy.coordinates.earth import EarthLocation, GeodeticLocation

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

    def _format_command(self,
                     target: str,
                     query_type: Union[str, None],
                     closest_apparition: Union[bool, Time],
                     fragments: bool
                    ) -> str:
        """Form the COMMAND parameter."""

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

        return "".join([prefix, target, suffix, cap, fragments])

    def _format_center(self, center: Union[str, EarthLocation]) -> Dict[str, str]:
        """Form the CENTER parameter.
        
        GEODETIC (generally this means map coordinates)
            E-long - Geodetic east longitude (DEGREES)
            lat    - Geodetic latitude  (DEGREES)
            h      - Altitude above reference ellipsoid (km)

        Comma separated values.

        """

        if isinstance(center, str):
            return {"center": center}
        elif isinstance(center, EarthLocation):
            loc: GeodeticLocation = center.to_geodetic("WGS84")

            site_coord: str = (
                f"{loc.lon.deg},{loc.lat.deg},{loc.height.to_value('km')}"
            )

            return {
                "center": "coord@399",
                "coord_type": "geodetic",
                "site_coord": site_coord,
            }
        
        raise TypeError("center must be a string or `EarthLocation`")
        
        

    def query_observer_async(self,
                             target: str,
                             *,
                             query_type: Optional[str] = None,
                             closest_apparition: Union[bool, Time] = False,
                             fragments: bool = True,
                             center: Optional[Union[str, EarthLocation]] = None,
                             get_query_payload: bool = False,
                             cache: bool = True,
                             **kwargs
                            ) -> Response:
        """
        Query for an object's observables.

        
        Parameters
        ----------
        target : string
            The target query string.

        query_type : string, optional
            The type of target query: "designation", "name", "asteroid name",
            "comet name", "small body"

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

        >>> from astropy.time import Time
        >>> import astropy.units as u
        >>> from astroquery.jplhorizons import Horizons
        >>>
        >>> tab = Horizons.query_observer("Jupiter")
        >>>
        >>> tab = Horizons.query_observer("1", center="568")
        >>>
        >>> tab = Horizons.query_observer("europa", center="I41", query_type="name")
        >>>
        >>> tab = Horizons.query_observer("2P", query_type="designation")
        >>>
        >>> tab = Horizons.query_observer("2P",
        ...                               query_type="designation",
        ...                               closest_apparition=True)
        >>>
        >>> tab = Horizons.query_observer("2P",
        ...                               query_type="designation",
        ...                               closest_apparition=Time("2003-11-20"))
        >>>
        >>> tab = Horizons.query_observer("73P",
        ...                               query_type="designation",
        ...                               closest_apparition=True,
        ...                               fragments=False)
        >>>

        Any target query supported by Horizons is possible, simply format the
        target string according to the documentation.  For example, to search
        for all S-type small-bodies with semi-major axis less than 2.5 au and
        inclination greater than 7.8 degrees with a known (non-zero) GM:

        >>> tab = Horizons.query_observer("A < 2.5; IN > 7.8; STYP = S, GM <> 0;"

        Or, to specify the orbital elements:

        >>> tab = Horizons.query_observer(
        ...     "object=comet "
        ...     "epoch=2450200.5 "
        ...     "ec=0.8241907231263196 "
        ...     "qr=0.532013766859137 "
        ...     "tp=2450077.480966184235 "
        ...     "om=89.14262290335057 "
        ...     "w=326.0591239257098 "
        ...     "in=4.247821264821585 "
        ...     "a1=-5.113711376907895D-10 "
        ...     "a2=-6.288085687976327D-10"
        ... )

        The observer (ephemeris center) can also be an
        `~astropy.coordinates.EarthLocation`:

        >>> from astropy.coordinates import EarthLocation
        >>> college_park = EarthLocation.from_geodetic(76.935 * u.deg,
        ...                                            38.9867 * u.deg,
        ...                                            0 * u.km)
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

        request_payload["command"] = self._format_command(target,
                                                       query_type,
                                                       closest_apparition,
                                                       fragments)

        request_payload.update(self._format_center(center))

        if get_query_payload:
            return request_payload

        response: Response = self._request("GET",
                                           self.URL,
                                           params=request_payload,
                                           timeout=self.TIMEOUT,
                                           cache=cache)
        return response

    def query_vectors_async(self,
                            obj,
                            center,
                            *,
                            query_type=None,
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
                             query_type=None,
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
