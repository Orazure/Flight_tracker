from configuration import ORION_URL
from typing import List
import requests


class FlightDAL:
    """Flight Data Access Layer."""

    def __init__(self):
        self.orion_url = f"{ORION_URL}/entities"

    def get_all_flights(self):
        """Get all flights."""
        params = {"type": "Flight"}
        return requests.get(f"{self.orion_url}", params=params).json()

    def get_flight_from_id(self, flight_id: str) -> dict:
        """Get flight from its id.

        Args:
            flight_id (str): Id of the flight.

        Returns:
            dict: The flight.
        """
        params = {"type": "Flight"}
        return requests.get(f"{self.orion_url}/{flight_id}", params=params).json()

    def get_flights_from_icao(self, dep_icao: str, arr_icao: str) -> List[dict]:
        """Get flight from departure and arrival ICAO codes.

        Args:
            dep_icao (str): ICAO code of the departure airport.
            arr_icao (str): ICAO code of the arrival airport.

        Returns:
            List[dict]: The flights.

        Example:
            >>> dal = FlightDAL()
            >>> dal.get_flights_from_icao('LFPG', 'KJFK')
            [{'id': 'Flight_1', 'departsFromAirport.value': 'LFPG', ...]
        """
        params = {
            "type": "Flight",
            "q": f"departsFromAirport==airport-{dep_icao};arrivesToAirport==airport-{arr_icao}",
        }
        return requests.get(f"{self.orion_url}", params=params).json()
