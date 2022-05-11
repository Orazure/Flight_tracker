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

    def get_flights_from_iata(self, dep_iata: str, arr_iata: str) -> List[dict]:
        """Get flight from departure and arrival IATA codes.

        Args:
            dep_iata (str): IATA code of the departure airport.
            arr_iata (str): IATA code of the arrival airport.

        Returns:
            List[dict]: The flights.

        Example:
            >>> dal = FlightDAL()
            >>> dal.get_flights_from_iata('LHR', 'CDG')
            [{'id': 'Flight_1', 'dep_iata': 'LHR', 'arr_iata': 'CDG'...]
        """
        params = {
            "type": "Flight",
            "q": f"dep_iata=={dep_iata} AND arr_iata=={arr_iata}",
        }
        return requests.get(f"{self.orion_url}", params=params).json()
