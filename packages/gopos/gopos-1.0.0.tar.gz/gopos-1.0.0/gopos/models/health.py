import dataclasses

# Public interface.
__all__ = ["HealthResponse"]


@dataclasses.dataclass
class HealthResponse:
    """
    Response of a request to the `GET /health` route.
    """

    status: bool
