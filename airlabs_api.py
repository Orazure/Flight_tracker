import requests


API_KEY = "9a00f99a-81f1-4a9b-a2f0-53c1d6f30d14"
BASE_URL = "https://airlabs.co/api/v9"

def get_all_flights() -> list:
    params = {'api_key': API_KEY}
    flights = requests.get(f"{BASE_URL}/flights", params=params).json()
    print(len(flights.get('response', [])))
    # for flight in flights.get('response', []):
    #     print(flight)


def main() -> None:
    get_all_flights()

if __name__ == "__main__":
    main()