from datetime import datetime
from configuration import API_KEY, AIRLABS_URL, ORION_URL, SUPPORTED_FLIGHTS
from airlabs.utility import format_datetime
from loguru import logger
import requests
import json

# read json file
with open("example\schedule-CDG-JFK.json", "r") as f:
    flights = json.load(f)


def get_all_flights(dep_iata_code: str, arr_iata_code: str) -> list:
    """Get flight information from airlabs API.

    Args:
        dep_iata_code (str): Departure airport IATA code.
        arr_iata_code (str): Arrival airport IATA code.

    Returns:
        list: List of all flights following Flight Datamodel.
    """
    to_import = []
    params = {"api_key": API_KEY, "dep_iata": dep_iata_code, "arr_iata": arr_iata_code}
    logger.debug(f"{dep_iata_code=} - {arr_iata_code=}")
    flights = requests.get(url=f"{AIRLABS_URL}/schedules", params=params).json()
    for flight in flights.get("response", []):

        logger.debug(f"{flight.get('flight_number')=}")
        _ = {
            "id": f"flight-{flight.get('flight_number')}",
            "type": "Flight",
            "flightNumber": {"type": "Text", "value": flight.get("flight_number")},
            "flightNumberIATA": {"type": "Text", "value": flight.get("flight_iata")},
            "flightNumberICAO": {"type": "Text", "value": flight.get("flight_icao")},
            "flightType": {"type": "Text", "value": "G"},
            "state": {"type": "Text", "value": flight.get("status")},
            "dateDeparture": {
                "type": "DateTime",
                "value": format_datetime(flight.get("dep_time")),
                "metadata": {
                    "description": {"type": "Text", "value": "Departure date"}
                },
            },
            "dateArrival": {
                "type": "DateTime",
                "value": format_datetime(flight.get("arr_time")),
                "metadata": {"description": {"type": "Text", "value": "Arrival time"}},
            },
            "dateSTOT": {  # Scheduled Take Off Time
                "type": "DateTime",
                "value": format_datetime(flight.get("dep_time")),
                "metadata": {
                    "description": {"type": "Text", "value": "Scheduled Take Off Time"}
                },
            },
            "dateETOT": {  # Estimated Take Off Time
                "type": "DateTime",
                "value": format_datetime(
                    flight.get("dep_estimated", flight.get("dep_time"))
                ),  # if no estimated time, use scheduled time
                "metadata": {
                    "description": {"type": "Text", "value": "Estimated arrival time"}
                },
            },
            "dateELDT": {  # Estimated Landing Time
                "type": "DateTime",
                "value": format_datetime(flight.get("arr_estimated")),
                "metadata": {
                    "description": {"type": "Text", "value": "Estimated Landing Time"}
                },
            },
            "dateSLDT": {  # Scheduled Landing Time
                "type": "DateTime",
                "value": format_datetime(flight.get("arr_time")),
                "metadata": {
                    "description": {"type": "Text", "value": "Scheduled Landing Time"}
                },
            },
            "hasAircraft": {
                "type": "Relationship",
                "value": f"aircraft-{flight.get('aircraft_icao', 'NotFound')}",
            },
            "departsFromAirport": {
                "type": "Relationship",
                "value": f"airport-{flight.get('dep_icao')}",
            },
            "arrivesToAirport": {
                "type": "Relationship",
                "value": f"airport-{flight.get('arr_icao')}",
            },
            "belongsToAirline": {
                "type": "Relationship",
                "value": f"airline-{flight.get('airline_icao')}",
            },
            "delayed": {
                "type": "Integer",
                "value": flight.get("delayed", 0),
                "metadata": {
                    "unit": {
                        "type": "Text",
                        "value": "minutes",
                    }
                },
            },
            "duration": {
                "type": "Integer",
                "value": flight.get("duration", 0),
                "metadata": {"unit": {"type": "Text", "value": "minutes"}},
            },
            "country": {
                "type": "Text",
                "value": flight.get("flag"),
            },
            "airline_iata": {
                "type": "Text",
                "value": f"{flight.get('airline_iata')}",
            },
            "airline_icao": {
                "type": "Text",
                "value": f"{flight.get('airline_icao')}",
            },
            "last_update": {
                "type": "DateTime",
                "value": f"{datetime.now().isoformat()}Z",
            },
        }
        to_import.append(_)
    return to_import


def import_flights(flights: list) -> bool:
    """Import flights into the ORION database.

    Args:
        flights (list): List of flights to import.

    Returns:
        bool: True if the flights were imported successfully.
    """
    if not flights:
        logger.warning("No flights to import.")
        return False
    params = {"actionType": "append", "entities": flights}
    res = requests.post(url=f"{ORION_URL}/op/update", json=params)
    if res.ok:
        logger.success(f"{len(flights)} flights imported successfully.")
        return True
    else:
        logger.error(f"{len(flights)} flights could not be imported.")
        logger.info(res.text)
        return False


def update_flights_information() -> None:
    """Update data in orion with the supported flights"""
    for i, flight in enumerate(SUPPORTED_FLIGHTS):
        temp = flight.get(str(i))
        logger.info(f"Updating flights {temp.get('description')}")
        flights = get_all_flights(temp.get("dep_iata"), temp.get("arr_iata"))
        import_flights(flights)
