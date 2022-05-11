from configuration import API_KEY, AIRLABS_URL, ORION_URL, SUPPORTED_FLIGHTS
from airlabs.utility import format_datetime
from loguru import logger
from typing import List
import requests


def get_all_flights(dep_iata_code: str, arr_iata_code: str) -> list:
    """Get flight information from airlabs API.

    Args:
        dep_iata_code (str): Departure airport IATA code.
        arr_iata_code (str): Arrival airport iata code.

    Returns:
        list: List of all flights from the country following Flight Datamodel.

    """
    to_import = []
    params = {"api_key": API_KEY, "dep_iata": dep_iata_code, "arr_iata": arr_iata_code}
    flights = requests.get(url=f"{AIRLABS_URL}/flights", params=params).json()
    for flight in flights.get("response", []):
        _ = {
            "id": f"live_flight-{flight.get('flight_number')}",
            "type": "LiveFlight",
            "flightNumber": {"type": "Text", "value": flight.get("flight_number")},
            "flightNumberIATA": {"type": "Text", "value": flight.get("flight_iata")},
            "flightNumberICAO": {"type": "Text", "value": flight.get("flight_icao")},
            "flightType": {"type": "Text", "value": "G"},
            "state": {"type": "Text", "value": flight.get("status")},
            "location": {
                "type": "GeoJson:Point",
                "value": [flight.get("lat"), flight.get("lng")],
                "metadata": {
                    "description": {
                        "type": "Text",
                        "value": "Postion with the Latitude and Longitude",
                    }
                },
            },
            "speed": {"type": "Number", "value": flight.get("speed")},
            "altitude": {
                "type": "Number",
                "value": flight.get("alt"),
                "metadata": {"unit": {"type": "Text", "value": "meters"}},
            },
            "departure": {"type": "Text", "value": flight.get("dep_iata")},
            "arrival": {"type": "Text", "value": flight.get("arr_iata")},
            "aircraft_icao": {"type": "Text", "value": flight.get("aircraft_icao")},
            "aircraft_iata": {"type": "Text", "value": flight.get("aircraft_iata")},
            "airline_iata": {"type": "Text", "value": flight.get("airline_iata")},
            "direction": {
                "type": "Number",
                "value": flight.get("dir"),
                "metadata": {"unit": {"type": "Text", "value": "degrees"}},
            },
        }
        to_import.append(_)
    return to_import


def import_flights(flights: List[dict]) -> None:
    """Import flights to ORION.

    Args:
        flights (list): List of flights to import.
    """
    if not flights:
        logger.warning("No flights to import.")
        return
    params = {"actionType": "append", "entities": flights}
    res = requests.post(url=f"{ORION_URL}/op/update", json=params)
    if res.ok:
        logger.success(f"{len(flights)} flights imported.")
    else:
        logger.error(f"{len(flights)} flights not imported.")
        logger.info(res.text)


def update_live_flights() -> None:
    """Update live flights in ORION."""
    for flight in SUPPORTED_FLIGHTS:
        logger.info(f"Updating live flights {flight.get('description')}")
        flights = get_all_flights(
            dep_iata_code=flight.get("dep_iata"), arr_iata_code=flight.get("arr_iata")
        )
        import_flights(flights)
