"""
==============================================================================
Weather Data Extractor & Validator
==============================================================================
Overview:
This script does the following:
1. Connects to Open-Meteo API to get current weather readings (temperature, humidity, wind speed, weather code).
2. Validates data quality using Pydantic to make sure values are within logical ranges.
3. Groups valid records into a Pandas DataFrame ready for loading into PostgreSQL or saving as a CSV file.
"""

import requests
import pandas as pd
import json
import time
import logging
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError

# Configure logging to write logs to both a file and the terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", encoding='utf-8'),  # Save log events to a file
        logging.StreamHandler()                                 # Print log events to the terminal screen
    ]
)

class WeatherRecord(BaseModel):
    """
    Pydantic Data Validation Model:
    Ensures every weather record from the API matches correct data types and ranges
    before inserting it into the database (prevents corrupted or invalid data).
    """
    province: str
    city: str
    latitude: float = Field(..., ge=-90, le=90)      # Latitude must be between -90 and +90
    longitude: float = Field(..., ge=-180, le=180)   # Longitude must be between -180 and +180
    temperature: float = Field(..., ge=-10, le=60)   # Temperature must be between -10 and 60 °C
    humidity: float = Field(..., ge=0, le=100)       # Humidity percentage between 0% and 100%
    wind_speed: float = Field(..., ge=0)             # Wind speed must be a positive number or zero
    weather_code: int                                # WMO weather condition code
    ingestion_time: str                              # Timestamp when data was fetched

def get_weather_data(lat, lon):
    """
    Connect to the API and fetch weather data for a specific city using its coordinates.
    
    Args:
        lat (float): City latitude.
        lon (float): City longitude.
        
    Returns:
        dict | None: Weather data dictionary from API, or None if connection fails.
    """
    # Build API request URL to get current temperature, humidity, wind speed, and weather code
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    try:
        # Send HTTP GET request with a 15-second timeout
        res = requests.get(url, timeout=15)
        res.raise_for_status()  # Check that the request was successful (not 404 or 500)
        return res.json()       # Parse JSON response into a Python dictionary
    except Exception as e:
        # Log error if request fails
        logging.error(f"Failed to fetch data: {e}")
        return None

def start_extraction(file_path):
    """
    Run extraction pipeline for all cities listed in the JSON file.
    
    Args:
        file_path (str): Path to JSON file with city names and coordinates (e.g., cities.json).
        
    Returns:
        pd.DataFrame: DataFrame containing all validated weather records.
    """
    # Read city locations from JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        locations = json.load(f)
    
    final_list = []
    total = len(locations)
    logging.info(f"Starting Extraction Pipeline for {total} cities...")

    # Loop through each city and fetch its weather data
    for index, loc in enumerate(locations, 1):
        logging.info(f"[{index}/{total}] Processing: {loc['city']}, {loc['province']}...")
        
        # Fetch current weather reading
        data = get_weather_data(loc['lat'], loc['lon'])
        
        # Check if response is valid and contains 'current' weather data
        if data and 'current' in data:
            c = data['current']
            # Prepare row dictionary with extracted data
            row = {
                "province": loc['province'],
                "city": loc['city'],
                "latitude": float(loc['lat']),
                "longitude": float(loc['lon']),
                "temperature": c.get('temperature_2m'),
                "humidity": c.get('relative_humidity_2m'),
                "wind_speed": c.get('wind_speed_10m'),
                "weather_code": c.get('weather_code'),
                "ingestion_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            try:
                # Validate values using WeatherRecord class (Pydantic Validation)
                validated = WeatherRecord(**row)
                # Add valid record to final list
                final_list.append(validated.model_dump())
            except ValidationError as ve:
                # If validation fails, skip record and log warning
                logging.warning(f"Validation failed for {loc['city']}")
        
        # Pause for 0.5 seconds (Rate Limiting) to avoid overloading the API server
        time.sleep(0.5) 

    # Convert final list into Pandas DataFrame
    df = pd.DataFrame(final_list)
    return df

if __name__ == "__main__":
    # Run extraction phase independently for testing
    weather_df = start_extraction('cities.json')
    logging.info("Extraction Phase Completed Successfully!")
    
    # Save results to a local CSV file
    weather_df.to_csv("egypt_weather_full.csv", index=False)
    logging.info("Results saved to 'egypt_weather_full.csv'")

