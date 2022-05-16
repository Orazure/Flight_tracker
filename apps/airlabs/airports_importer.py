import requests
from time import time
from typing import List
from loguru import logger
from apps.configuration import ORION_URL, API_KEY, AIRLABS_URL, SUPPORTED_AIRPORTS
from apps.airlabs.utility import replace_illegal_characters


def get_all_airports() -> List[dict]:
    """Get all airports from airlabs API and format them to a list of dict following the airport data model.
        We ongly get the supported airports to limit api calls.
    Returns:
        List[dict]: A list of dict following the orion airport data model.
    """
    # string with supported airports comma separated
    supported_airports_str = ",".join(SUPPORTED_AIRPORTS)
    logger.debug(f"Getting following airports {supported_airports_str}...")
    params = {"api_key": API_KEY, "iata_code": supported_airports_str}
    airports = requests.get(url=f"{AIRLABS_URL}/airports", params=params).json()
    imported_airports = []
    for airport in airports.get("response", []):
        airport_model = {
            "id": f"airport-{airport.get('icao_code')}",
            "type": "Airport",
            "codeIATA": {"type": "Text", "value": airport.get("iata_code")},
            "codeICAO": {"type": "Text", "value": airport.get("icao_code")},
            "name": {
                "type": "Text",
                # replace illegal characters
                "value": replace_illegal_characters(airport.get("name")),
            },
            "address": {
                "type": "PostalAddress",
                "value": {
                    "addressCountry": airport.get("country_code"),
                    # get first word of airport name
                    "addressLocality": replace_illegal_characters(
                        airport.get("name").split(" ")[0]
                    ),
                },
            },
            "location": {
                "type": "geo:json",
                "value": {
                    "type": "Point",
                    "coordinates": [airport.get("lng"), airport.get("lat")],
                },
            },
        }
        imported_airports.append(airport_model)
    return imported_airports


def import_to_orion(airports: List[dict]) -> None:
    """Import all airports to Orion.
    Args:
        airports (List[dict]): A list of dict following the orion airport data model.

    Returns:
        None

    Take about 16 minutes to import 20k airports.
    """
    if not airports:
        logger.error("No airports to import.")
        return
    params = {"actionType": "append", "entities": airports}
    logger.info(f"Importing {len(airports)} airports...")
    res = requests.post(url=f"{ORION_URL}/op/update", json=params)
    if res.ok:
        logger.success("Successfully imported airports to Orion.")
    else:
        logger.error("Failed to import airports to Orion.")
        logger.info(res.text)


def update_airports_info() -> None:
    """Update information in orion with the supported airports"""
    logger.debug("Start importing airports...")
    start_time = time()
    airports = get_all_airports()
    import_to_orion(airports)
    logger.debug(f"Finished importing airports in {time() - start_time} seconds.")
    logger.success("ENDING.")


if __name__ == "__main__":
    update_airports_info()
