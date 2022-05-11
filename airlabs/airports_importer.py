import requests
from time import time
from typing import List
from loguru import logger
from configuration import ORION_URL, API_KEY, AIRLABS_URL


def replace_illegal_characters(string: str) -> str:
    """Replace characters that are not allowed in the orion data model.

    Args:
        string (str): The string that need to be sanitized.

    Returns:
        str: The sanitized string.
    """
    return string.replace('"', ' ').replace("'", ' ').replace('(', '').replace(')', '')


def get_all_airports(country_code: str) -> List[dict]:
    """Get all airports from airlabs API and format them to a list of dict following the airport data model.
    Args:
        country_code (str): The country code to filter the airports.
    Returns:
        List[dict]: A list of dict following the orion airport data model.
    """
    logger.debug(f"Getting all airports from {country_code}...")
    params = {'api_key': API_KEY, 'country_code': country_code}
    airports = requests.get(url=f"{AIRLABS_URL}/airports", params=params).json()
    imported_airports = []
    for airport in airports.get('response', []):
        airport_model = {
            "id": f"airport-{airport.get('icao_code')}",
            "type": "Airport",
            "codeIATA": {
                "type": "Text",
                "value": airport.get('iata_code')
            },
            "codeICAO": {
                "type": "Text",
                "value": airport.get('icao_code')
            },
            "name": {
                "type": "Text",
                # replace illegal characters
                "value": replace_illegal_characters(airport.get('name'))
            },
            "address": {
                "type": "PostalAddress",
                "value": {
                    "addressCountry": airport.get('country_code'),
                    # get first word of airport name
                    "addressLocality": replace_illegal_characters(airport.get('name').split(' ')[0])
                }
            },
            "location": {
                "type": "geo:json",
                "value": {
                    "type": "Point",
                    "coordinates": [airport.get('lng'), airport.get('lat')]
                }
            }
        }
        imported_airports.append(airport_model)
    return imported_airports


def import_to_orion(airports: List[dict]) -> None:
    """Import all airports to Orion.
    Args:
        airports (List[dict]): A list of dict following the orion airport data model.

    Take about 16 minutes to import 20k airports.
    """
    # split airports to respect the max size of the payload : 1048576
    airports_chunks = [airports[i:i + 2000] for i in range(0, len(airports), 2000)]
    for chunk in airports_chunks:
        params = {'actionType':'append', 'entities': chunk}
        print(f"Importing {len(chunk)} airports...")
        res = requests.post(url=f"{ORION_URL}/op/update", json=params)
        if res.ok:
            logger.success("Successfully imported airports to Orion.")
        else:
            logger.error("Failed to import airports to Orion.")
            logger.info(res.text)


def main() -> None:
    logger.debug("Start importing airports...")
    # time execution
    start_time = time()
    FR_airports = get_all_airports('FR')
    end_time = time()
    logger.debug(f"Query all airports took {end_time - start_time} seconds.")
    start_time = time()
    import_to_orion(FR_airports)
    end_time = time()
    logger.debug(f"Import all airports from France took {(end_time - start_time)/60} minutes.")
    UK_airports = get_all_airports('GB')
    start_time = time()
    import_to_orion(UK_airports)
    end_time = time()
    logger.debug(f"Import all airports from UK took {(end_time - start_time)/60} minutes.")


if __name__ == "__main__":
    main()