from configuration import ORION_URL
from typing import List
import requests


class AirportDAL:
    """Data Access Layer for flights."""

    def __init__(self):
        self.orion_url = f"{ORION_URL}/entities"

    def get_all_airports(self):
        """Get all airports."""
        params = {"type": "Airport"}
        return requests.get(f"{self.orion_url}", params=params).json()

    def get_airports_from_country(self, country_code: str) -> List[dict]:
        """Get all airports from a specific country.

        Args:
            country_code (str): ISO 2 Code of the country

        Returns:
            List[dict]: All airports from the country.
        """
        params = {"type": "Airport", "q": f"address.addressCountry=={country_code}"}
        return requests.get(f"{self.orion_url}", params=params).json()

    def get_airport_from_iata(self, iata_code: str) -> dict:
        """Get an airport from its IATA code.

        Args:
            iata_code (str): IATA code of the airport.

        Returns:
            dict: The airport.
        """
        params = {"type": "Airport", "q": f"codeIATA=={iata_code}"}
        return requests.get(f"{self.orion_url}", params=params).json()

    def get_airport_from_icao(self, icao_code: str) -> dict:
        """Get an airport from its ICAO code.

        Args:
            icao_code (str): ICAO code of the airport.

        Returns:
            dict: The airport.
        """
        params = {"type": "Airport", "q": f"codeICAO=={icao_code}"}
        return requests.get(f"{self.orion_url}", params=params).json()
