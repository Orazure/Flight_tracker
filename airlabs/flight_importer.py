from configuration import API_KEY, AIRLABS_URL, ORION_URL
import requests

def get_all_flights(country_code: str) -> list:
    """Get all flights from a specific country.

    Args:
        country_code (str): The ISO 2 Code of the country.

    Returns:
        list: List of all flights from the country following Flight Datamodel.
    """
    params = {'api_key': API_KEY, 'flag': country_code}
    flights = requests.get(url=f"{AIRLABS_URL}/flights", params=params).json()
    return flights.get('response', [])


def import_flights(flights: list) -> bool:
    """Import flights into the ORION database.

    Args:
        flights (list): List of flights to import.

    Returns:
        bool: True if the flights were imported successfully.
    """
    return True


def main() -> None:
    """Main function."""
    flights = get_all_flights('FR')