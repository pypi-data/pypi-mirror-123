from typing import Any, Dict
from urllib.parse import quote_plus

import dacite
import requests

from gopos.models import GoposAddress, HealthResponse, TimezoneResponse

# Public interface.
__all__ = ["GoposClient"]


class GoposClient:
    def __init__(self, base: str):
        """
        GoposClient constructor.

        :param base: url at which the Gopos server is running
        """
        self._base = base

    def _call(self, endpoint: str) -> Dict[str, Any]:
        """
        Calls the service.

        :param endpoint: the endpoint to call
        :return: the response parsed as JSON
        """
        # Send the request.
        url = f"{self._base}{endpoint}"
        request = requests.get(url)

        # Error handling.
        request.raise_for_status()

        # Parse the response.
        return request.json()

    def get_health(self) -> bool:
        """
        Gets the health check response.

        :return: true if the service is healthy
        """
        # Send the request.
        data = self._call("/health")
        parsed = dacite.from_dict(HealthResponse, data)

        # Extract the status.
        return parsed.status

    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Gets the details of the given Google Place ID.

        :param place_id: the ID to lookup
        :return: the details
        """
        # Send the request.
        return self._call(f"/google/place/{place_id}")

    def get_timezone(self, latitude: float, longitude: float) -> str:
        """
        Gets the timezone for the given coordinate pair.

        :param latitude: the latitude coordinate
        :param longitude: the longitude coordinate
        :return: the timezone
        """
        # Send the request.
        data = self._call(f"/timezone?latitude={latitude}&longitude={longitude}")
        parsed = dacite.from_dict(TimezoneResponse, data)

        # Extract the timezone.
        return parsed.timezone

    def parse_address(self, query: str, country: str = None) -> GoposAddress:
        """
        Parses the address for the given query.

        :param query: the address to parse
        :param country: (optional) if passed, this will help the address parser
               to obtain more accurate results
        :return: the address
        """
        # Build the endpoint.
        endpoint = f"/address/parse?query={quote_plus(query)}"
        if country:
            endpoint = f"{endpoint}&country={country}"

        # Send the request.
        data = self._call(endpoint)
        return dacite.from_dict(GoposAddress, data)
