import dataclasses

# Public interface.
__all__ = ["TimezoneResponse"]


@dataclasses.dataclass
class TimezoneResponse:
    """
    Response of a request to the `GET /timezone` route.
    """

    latitude: float
    longitude: float
    timezone: str
