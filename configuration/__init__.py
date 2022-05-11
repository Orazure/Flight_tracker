API_KEY = "9a00f99a-81f1-4a9b-a2f0-53c1d6f30d14"
AIRLABS_URL = "https://airlabs.co/api/v9"
ORION_URL = "http://localhost:1026/v2"
# We choose only five flights to limit api calls.
SUPPORTED_FLIGHTS = [
    {'dep_iata': 'CDG', 'arr_iata': 'JFK', 'description': 'from Paris to New York'}, 
    {'dep_iata': 'CDG', 'arr_iata': 'MLA', 'description': 'from Paris to Malte'}, 
    {'dep_iata': 'CDG', 'arr_iata': 'MRS', 'description': 'from Paris to Marseille'}, 
    {'dep_iata': 'IBZ', 'arr_iata': 'BCN', 'description': 'from Ibiza to Barcelona'}, 
    {'dep_iata': 'OTP', 'arr_iata': 'PMO', 'description': 'from Bucarest to Palermo'},
]
# We choose only a few airports to limit the number of requests to airlabs API
SUPPORTED_AIRPORTS = ['CDG', 'JFK', 'MLA', 'MRS', 'BCN', 'OTP', 'PMO']

