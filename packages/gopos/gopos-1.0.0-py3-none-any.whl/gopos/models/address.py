import dataclasses

# Public interface.
__all__ = ["GoposAddress"]

from typing import Optional


@dataclasses.dataclass
class GoposAddress:
    """
    Response of a request to the `GET /address/parse` route.

    Definition of the fields is available at:
    https://github.com/openvenues/libpostal#parser-labels.
    """

    category: Optional[str] = None
    city: Optional[str] = None
    city_district: Optional[str] = None
    country: Optional[str] = None
    country_region: Optional[str] = None
    entrance: Optional[str] = None
    house: Optional[str] = None
    house_number: Optional[str] = None
    island: Optional[str] = None
    level: Optional[str] = None
    near: Optional[str] = None
    po_box: Optional[str] = None
    postcode: Optional[str] = None
    road: Optional[str] = None
    staircase: Optional[str] = None
    state: Optional[str] = None
    state_district: Optional[str] = None
    suburb: Optional[str] = None
    unit: Optional[str] = None
    world_region: Optional[str] = None
