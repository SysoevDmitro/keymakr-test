import os
import json
import logging

from .celery_app import celery_app
from .utils import normalize_city, fetch_weather_data, classify_region, validate_temperature


# Set up logging
logging.basicConfig(level=logging.INFO)


@celery_app.task(bind=True)
def process_weather_task(self, cities):
    """
    Processes the list of cities:
      - Normalizes city names,
      - Calls the weather API,
      - Validates and filters data,
      - Classifies data by region,
      - Saves results into per-region files.
    Returns a dict mapping regions to a URL (or file link) for that task’s results.
    """
    # Normalize the city names (e.g., "Киев" → "Kyiv", "Londn" → "London")
    normalized_cities = [normalize_city(city) for city in cities]
    results_by_region = {}
    task_id = self.request.id  # Unique ID for this task

    for city in normalized_cities:
        try:
            # Fetch weather data from an unreliable external API.
            data = fetch_weather_data(city)
            temperature = data.get("temperature")
            # Filter out invalid data (e.g., missing or out-of-range temperature)
            if temperature is None or not validate_temperature(temperature):
                logging.error(f"Invalid temperature for {city}: {temperature}")
                continue  # Skip this city

            # Determine geographic region (e.g., "Europe", "America", "Asia")
            region = classify_region(city)
            if region not in results_by_region:
                results_by_region[region] = []
            results_by_region[region].append(data)
        except Exception as e:
            # Log API errors with details
            logging.error(f"Error processing city {city}: {str(e)}")
            continue

    # Save results for each region in the appropriate folder
    for region, data in results_by_region.items():
        dir_path = os.path.join("weather_data", region)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"task_{task_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Return a mapping of region to a link (for example purposes)
    # (In a real app, you might generate absolute URLs.)
    return {region: f"/results/{region}?task_id={task_id}" for region in results_by_region}
