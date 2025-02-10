import random
import time

# --- City Normalization ---
# A simple mapping for common cases and typos.
CITY_NORMALIZATION_MAP = {
    "Киев": "Kyiv",
    "Лондон": "London",
    "Londn": "London",
    "Токио": "Tokyo",
    # Add more mappings as needed.
}


def normalize_city(city_name: str) -> str:
    """
    Normalize city names using a simple mapping.
    """
    return CITY_NORMALIZATION_MAP.get(city_name, city_name)


# --- API Keys for Multiple External Services ---
# In a real scenario, these would be kept secret (e.g. in environment variables)
API_KEYS = {
    "service1": "YOUR_API_KEY_1",
    "service2": "YOUR_API_KEY_2",
}


# --- Simulated External Weather API Call ---
def fetch_weather_data(city: str) -> dict:
    """
    Simulate calling an external weather API for the given city.
    This function randomly introduces delays and occasional errors.
    The returned data has ambiguous labels (assumes temperature is in Celsius).
    """
    # Simulate network delay
    time.sleep(random.uniform(0.5, 2.0))
    # Randomly simulate an API error (~33% chance)
    if random.choice([True, False, False]):
        raise Exception("External API error")
    # Simulated raw weather data
    simulated_data = {
        "city": city,
        "temperature": round(random.uniform(-10, 40), 1),  # Celsius
        "description": random.choice(["clear sky", "rain", "snow"])
    }
    return simulated_data


# --- Data Validation ---
def validate_temperature(temperature: float) -> bool:
    """
    Checks if the temperature is within a plausible range.
    """
    return -50 <= temperature <= 50


# --- Region Classification ---
# A simple mapping from normalized city names to regions.
CITY_REGION_MAP = {
    "Kyiv": "Europe",
    "London": "Europe",
    "New York": "America",
    "Tokyo": "Asia",
    # Add more mappings as needed.
}


def classify_region(city: str) -> str:
    """
    Returns the geographic region for the given city.
    If the city is not found, returns "Unknown".
    """
    return CITY_REGION_MAP.get(city, "Unknown")
