import requests
from functools import lru_cache

# ==========================================================
# District Geocoding using OpenStreetMap (Nominatim)
# ==========================================================

BASE_URL = "https://nominatim.openstreetmap.org/search"

@lru_cache(maxsize=500)
def get_coordinates(state, district):
    """
    Returns latitude and longitude for the selected district and state.
    Uses OpenStreetMap Nominatim API.
    """

    query = f"{district}, {state}, India"

    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "UZHU-AI/1.0 (Smart Agriculture)"
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if len(data) == 0:

            # Fallback to state search
            return get_state_coordinates(state)

        return {
            "lat": float(data[0]["lat"]),
            "lon": float(data[0]["lon"])
        }

    except Exception as e:

        print("Location Error:", e)

        return get_state_coordinates(state)


# ==========================================================
# State Fallback
# ==========================================================

STATE_COORDINATES = {

    "Tamil Nadu": (13.0827, 80.2707),
    "Karnataka": (12.9716, 77.5946),
    "Kerala": (8.5241, 76.9366),
    "Andhra Pradesh": (15.9129, 79.7400),
    "Telangana": (17.3850, 78.4867),
    "Maharashtra": (19.0760, 72.8777),
    "Gujarat": (22.2587, 71.1924),
    "Punjab": (31.1471, 75.3412),
    "Rajasthan": (27.0238, 74.2179),
    "Odisha": (20.9517, 85.0985),
    "Bihar": (25.0961, 85.3131),
    "Assam": (26.2006, 92.9376),
    "West Bengal": (22.5726, 88.3639),
    "Madhya Pradesh": (23.4733, 77.9470),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Chhattisgarh": (21.2787, 81.8661),
    "Jharkhand": (23.6102, 85.2799),
    "Goa": (15.2993, 74.1240),
    "Delhi": (28.6139, 77.2090),
    "Haryana": (29.0588, 76.0856),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Uttarakhand": (30.0668, 79.0193),
    "Tripura": (23.9408, 91.9882),
    "Nagaland": (26.1584, 94.5624),
    "Meghalaya": (25.4670, 91.3662),
    "Mizoram": (23.1645, 92.9376),
    "Manipur": (24.6637, 93.9063),
    "Arunachal Pradesh": (28.2180, 94.7278),
    "Sikkim": (27.5330, 88.5122),
    "Jammu and Kashmir": (33.7782, 76.5762),
    "Ladakh": (34.1526, 77.5771),
    "Andaman and Nicobar Island": (11.6234, 92.7265),
    "Lakshadweep": (10.5667, 72.6417),
    "Puducherry": (11.9416, 79.8083),
    "Chandigarh": (30.7333, 76.7794),
    "Dadra and Nagar Haveli": (20.1809, 73.0169),
    "Daman and Diu": (20.4283, 72.8397),
}


def get_state_coordinates(state):
    """
    Returns fallback coordinates for the selected state.
    """

    lat, lon = STATE_COORDINATES.get(
        state,
        (22.9734, 78.6569)   # Center of India
    )

    return {
        "lat": lat,
        "lon": lon
    }