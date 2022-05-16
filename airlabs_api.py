from airlabs.airports_importer import update_airports_info
from airlabs.flight_importer import update_flights_information
from airlabs.live_flight_importer import update_live_flights
from airlabs.airlines_importer import add_airline_information


def main() -> None:
    """Main function."""
    # update_airports_info()
    # add_airline_information() # One shot function the data will not be often updated.
    update_flights_information()
    update_live_flights()


if __name__ == "__main__":
    main()
