from configuration import ORION_URL
import requests


class FlightDAL:
    def __init__(self):
        self.orion_url = f"{ORION_URL}/entities"

    def get_all_flights(self):
        params = {'type': 'Flight'}
        flights = requests.get(f"{self.orion_url}", params=params).json()
        return flights

    def get_flight(self, flight_id):
        params = {'type': 'Flight', 'id': flight_id}
        flight = requests.get(f"{self.orion_url}", params=params).json()
        return flight

    
