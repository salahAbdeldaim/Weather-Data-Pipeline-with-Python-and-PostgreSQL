import requests
import pandas as pd
import json
import time
import logging
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", encoding='utf-8'), 
        logging.StreamHandler() 
    ]
)

class WeatherRecord(BaseModel):
    province: str
    city: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    temperature: float = Field(..., ge=-10, le=60)
    humidity: float = Field(..., ge=0, le=100)
    wind_speed: float = Field(..., ge=0)
    weather_code: int
    ingestion_time: str

def get_weather_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")
        return None

def start_extraction(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        locations = json.load(f)
    
    final_list = []
    total = len(locations)
    logging.info(f"Starting Extraction Pipeline for {total} cities...")

    for index, loc in enumerate(locations, 1):
        logging.info(f"[{index}/{total}] Processing: {loc['city']}, {loc['province']}...")
        data = get_weather_data(loc['lat'], loc['lon'])
        
        if data and 'current' in data:
            c = data['current']
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
                validated = WeatherRecord(**row)
                final_list.append(validated.model_dump())
            except ValidationError as ve:
                logging.warning(f"Validation failed for {loc['city']}")
        
        time.sleep(0.5) 

    df = pd.DataFrame(final_list)
    return df

if __name__ == "__main__":
    weather_df = start_extraction('cities.json')
    logging.info("Extraction Phase Completed Successfully!")
    
    weather_df.to_csv("egypt_weather_full.csv", index=False)
    logging.info("Results saved to 'egypt_weather_full.csv'")