# tools/ functions moved in this tools.py
from datetime import datetime
import json
import urllib.request
import urllib.parse


# --- the real functions (the model NEVER touches these) ---

def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculator(expression: str) -> str:
    # NOTE: eval() is a deliberate security hole — Week 10 fixes it properly.
    return str(eval(expression))

def get_weather(location: str) -> str:
    # Open-Meteo's geocoder wants a bare place name or zip, not "City, ST".
    # Take the part before the first comma; the geocoder resolves the city.
    location = location.split(",")[0].strip()
    
    """Get current weather for a US city/state (e.g. 'Atlanta, GA') or zip code.
    Two-step: geocode the location to lat/lon, then fetch current conditions."""
    # --- step 1: geocode (name or zip -> coordinates) ---
    geo_url = "https://geocoding-api.open-meteo.com/v1/search?" + urllib.parse.urlencode({
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json",
    })
    with urllib.request.urlopen(geo_url, timeout=10) as r:
        geo = json.loads(r.read())

    if not geo.get("results"):
        return f"ERROR: could not find a location matching '{location}'"

    place = geo["results"][0]
    lat, lon = place["latitude"], place["longitude"]
    name = place.get("name", location)
    print("Name of the location ", name)
    admin = place.get("admin1", "")   # state/region
    print("Name of the admin ", admin)

    # --- step 2: current weather at those coordinates ---
    wx_url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
    })
    with urllib.request.urlopen(wx_url, timeout=10) as r:
        wx = json.loads(r.read())

    cur = wx["current"]
    return (
        f"Weather for {name}, {admin}: "
        f"{cur['temperature_2m']}°F, "
        f"humidity {cur['relative_humidity_2m']}%, "
        f"wind {cur['wind_speed_10m']} mph "
        f"(weather_code {cur['weather_code']})"
    )

# --- their schemas (what the model sees INSTEAD of the code) ---

TOOLS = [
    {
        "name": "get_current_time",
        "description": "Returns the current local date and time.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "calculator",
        "description": "Evaluates a basic arithmetic expression, e.g. '2 + 2 * 10'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The arithmetic expression to evaluate."}
            },
            "required": ["expression"],
        },
    },
    {
        "name": "get_weather",
        "description": "Get current weather conditions for a US location. "
                    "Accepts a city and state (e.g. 'Atlanta GA') or a zip code(e.g. '30301').",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "US city and state, or a US zip code.",
                }
            },
            "required": ["location"],
        }
    }
]

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculator": calculator,
    "get_weather": get_weather
}