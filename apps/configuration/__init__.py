API_KEY = "9a00f99a-81f1-4a9b-a2f0-53c1d6f30d14"
AIRLABS_URL = "https://airlabs.co/api/v9"
ORION_URL = "http://orion:1026/v2"
# ORION_URL = "http://impossibly.fr:1026/v2"
databaseMysql = "draco-db"
userMysql="root"
passwordMysql="6L?op69RSYhT6a7ni?P6"
hostMysql="impossibly.fr"
# We choose only five flights to limit api calls.
SUPPORTED_FLIGHTS = [
    {
        "0": {
            "dep_iata": "CDG",
            "arr_iata": "JFK",
            "description": "from Paris to New York",
            "dep_icao": "LFPG",
            "arr_icao": "KJFK",
        }
    },
    {
        "1": {
            "dep_iata": "CDG",
            "arr_iata": "MLA",
            "description": "from Paris to Malte",
            "dep_icao": "LFPG",
            "arr_icao": "LMML",
        }
    },
    {
        "2": {
            "dep_iata": "CDG",
            "arr_iata": "MRS",
            "description": "from Paris to Marseille",
            "dep_icao": "LFPG",
            "arr_icao": "LFML",
        }
    },
    {
        "3": {
            "dep_iata": "IBZ",
            "arr_iata": "BCN",
            "description": "from Ibiza to Barcelona",
            "dep_icao": "LEIB",
            "arr_icao": "LEBL",
        }
    },
    {
        "4": {
            "dep_iata": "OTP",
            "arr_iata": "PMO",
            "description": "from Bucarest to Palermo",
            "dep_icao": "LROP",
            "arr_icao": "LICJ",
        }
    },
]
# We choose only a few airports to limit the number of requests to airlabs API
SUPPORTED_AIRPORTS = ["CDG", "JFK", "MLA", "MRS", "BCN", "OTP", "PMO"]
