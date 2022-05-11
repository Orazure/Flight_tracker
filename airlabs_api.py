from airlabs.airports_importer import update_airports_info
from airlabs.flight_importer import update_flights_information
from airlabs.live_flight_importer import update_live_flights


def main() -> None:
    """Main function."""
    # update_airports_info()
    update_flights_information()
    update_live_flights()


if __name__ == "__main__":
    main()
