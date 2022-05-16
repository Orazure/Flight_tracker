from configuration import API_KEY, AIRLABS_URL, ORION_URL, SUPPORTED_FLIGHTS
from airlabs.utility import replace_illegal_characters
from loguru import logger
from typing import List
import requests

# One shot function we import all information from airlabs API.
def get_all_airlines() -> List[dict]:
    """Get airline information from airlabs API.

    Returns:
        List[dict]: List of all airlines following Airline Datamodel.

    """
    to_import = []
    params = {"api_key": API_KEY}
    airlines = requests.get(url=f"{AIRLABS_URL}/airlines", params=params).json()
    for airline in airlines.get("response", []):
        _ = {
            "id": f"airline-{airline.get('icao_code')}",
            "type": "Airline",
            "codeIATA": {"type": "Text", "value": airline.get("iata_code")},
            "codeICAO": {"type": "Text", "value": airline.get("icao_code")},
            "name": {
                "type": "Text",
                "value": replace_illegal_characters(airline.get("name")),
            },
        }
        to_import.append(_)
    return to_import


def import_airlines(airlines: List[dict]) -> None:
    """Import all airlines to Orion.

    Args:
        airlines (List[dict]): List of all airlines following Airline Datamodel.

    Returns:
        None
    """
    if not airlines:
        logger.warning("No airlines to import.")
        return
    # chunk data by 2000 elements
    for chunk in [airlines[i : i + 2000] for i in range(0, len(airlines), 2000)]:
        params = {"actionType": "append", "entities": chunk}
        logger.info(f"Importing {len(chunk)} airlines...")
        response = requests.post(url=f"{ORION_URL}/op/update", json=params)
        if response.ok:
            logger.success("Successfully imported airlines to Orion.")
        else:
            logger.error("Failed to import airlines to Orion.")
            logger.info(response.text)


def add_airline_information() -> None:
    """Add airline_information to Orion.
    One shot function the data will not be often updated."""
    airlines = get_all_airlines()
    import_airlines(airlines)
