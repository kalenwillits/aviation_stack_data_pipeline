import os
from enum import Enum
import logging
from http import HTTPStatus
import requests

from .error import Misconfigured
from .error import InvalidParameterError
from .error import ApiError
from .error import MalformedResponse


class IcaoType(Enum):
    DEPARTURE: int = 1
    ARRIVAL: int = 2


class AviationStackApiClient:
    """
    Aviation Stack api wrapper for  https://aviationstack.com.

    :api_key:
        Aviation Stack API key.
    :https:
        Toggle https encryption,
    :threshold:
        Maxiumum number of flights to gather before stopping pull. If -1, then
        no limit is set.

    Notes:
    - Free accounts do not support https.
    """
    def __init__(self, api_key: str = None, https: bool = False, threshold: int = 100):
        self._https = https
        self._threshold = threshold
        if api_key is None:
            logging.info("No api_key parameter found, using \"AVIATION_STACK_API_KEY\" environment variable instead.")
            self._api_key = os.environ.get("AVIATION_STACK_API_KEY")
        else:
            self._api_key = api_key
        if self._api_key is None:
            raise Misconfigured("Missing Aviation Stack API Key.")

    @property
    def protocol(self) -> str:
        if self._https:
            return "https"
        return "http"

    def get(self, endpoint: str, params: dict = {}) -> requests.Request:
        params.update({"access_key": self._api_key})
        return requests.get(f"{self.protocol}://api.aviationstack.com/v1/{endpoint}", params=params)

    def get_flights_by_icao(self, icao: str, icao_type: IcaoType, offset: int = 0):
        """
        https://aviationstack.com/documentation -> Real Time Flights
        """
        params = {"flight_status": "active", "offset": offset}

        match icao_type:
            case IcaoType.DEPARTURE:
                params["dep_icao"] = icao.upper()
            case IcaoType.ARRIVAL:
                params["arr_icao"] = icao.upper()
            case _:
                logging.critical("Crashing application due to invalid parameters passed for icao_type")
                raise InvalidParameterError("Invalid icao_type passed!")

        match (response := self.get("flights")).status_code:
            case HTTPStatus.OK:
                logging.info("Aviation Stack API successfully obtained data from the flights endpoint")
                return response
            case HTTPStatus.UNAUTHORIZED:
                logging.warning("Unauthorized request to Aviation Stack API, check the access credentials")
                return response
            case _:
                logging.error(f"Uncaught response from Aviation Stack API {response.status_code}")
        return response

    def validate_payload(self, payload: dict):
        if payload.get("data") is None or payload.get("pagination") is None:
            logging.error("Payload from Aviation Stack responded with a malformed response")
            raise MalformedResponse("payload is malformed and contains no 'data' key")

    def payload_has_more_results(self, payload: dict) -> bool:
        pagination = payload.get("pagination", {})
        offset = pagination.get("offset")
        count = pagination.get("count")
        total = pagination.get("total")
        if offset is None or count is None or total is None:
            logging.warning("Payload from Aviation Stack is missing pagination information, \
                            possible malformed response.")
            return False

        if self._threshold > 0:
            if (offset + count) > self._threshold:
                return False

        if (offset + count) < total:
            return True

        return False

    def get_all_flights(self, icao: str) -> list[dict, ...]:
        logging.info(f"Requesting all arriving and departing flights for {icao}.")
        for icao_type in (IcaoType.DEPARTURE, IcaoType.ARRIVAL):
            logging.info(f"Requesting all {icao_type} flights...")
            pagination_left: bool = True
            offset: int = 0
            while pagination_left:
                response = self.get_flights_by_icao(icao, icao_type, offset)
                if response.status_code == HTTPStatus.OK:
                    payload = response.json()
                    self.validate_payload(payload)
                    yield payload["data"]
                    pagination_left = self.payload_has_more_results(payload)
                else:
                    raise ApiError("Failed to load")
