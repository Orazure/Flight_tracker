from apps.configuration import ORION_URL
from typing import List
import requests

# Live Flight containt the live position of a plane.
class LiveFlightDAL:
    """Live Flight Data Access Layer."""

    def __init__(self):
        self.orion_url = f"{ORION_URL}/entities"

    def get_all_flights(self):
        """Get all flights."""
        params = {"type": "LiveFlight"}
        return requests.get(f"{self.orion_url}", params=params).json()

    def get_flights_from_iata_dest(self, dep_iata: str, arr_iata: str) -> List[dict]:
        """Get flight from departure and arrival IATA codes.

        Args:
            dep_iata (str): IATA code of the departure airport.
            arr_iata (str): IATA code of the arrival airport.

        Returns:
            List[dict]: The flights.

        Example:
            >>> dal = FlightDAL()
            >>> dal.get_flights_from_iata('CDG', 'JFK')
            [{'id': 'LiveFlight-1', 'departure': 'CDG', 'arrival': 'JFK', 'location':...}...]
        """
        params = {
            "type": "LiveFlight",
            "q": f"departure=={dep_iata};arrival=={arr_iata}",
        }
        return requests.get(f"{self.orion_url}", params=params).json()

    def get_flight_from_iata(self, flight_iata_code: str) -> dict:
        """Get flight from its iata code.

        Args:
            flight_iata_code (str): IATA code of the flight.

        Returns:
            dict: The flight.

        Example:
            >>> dal = FlightDAL()
            >>> dal.get_flight_from_iata('AF22')
            {'id': 'Flight_1', 'flightNumberIATA': 'LHR'...}
        """
        params = {"type": "LiveFlight", "q": f"flightNumberIATA=={flight_iata_code}"}
        return requests.get(f"{self.orion_url}", params=params).json()

    def get_flight_from_number(self, flight_number: str) -> dict:
        """Get flight from its number.

        Args:
            flight_number (str): Number of the flight.

        Returns:
            dict: The flight.

        Example:
            >>> dal = FlightDAL()
            >>> dal.get_flight_from_number('22')
            {'id': 'Flight_1', 'flightNumberIATA': 'LHR'...}
        """
        params = {"type": "LiveFlight", "q": f"flightNumber=={flight_number}"}
        return requests.get(f"{self.orion_url}", params=params).json()
