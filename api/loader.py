import os
import logging
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Create and return a PostgreSQL database connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "32770"),
        dbname=os.getenv("DB_NAME", "project"),
        user=os.getenv("DB_USER", "salah_depi"),
        password=os.getenv("DB_PASSWORD")
    )

def ensure_table_schema(conn):
    """Ensure table exists and has latitude/longitude columns."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_readings (
                id SERIAL PRIMARY KEY,
                province VARCHAR(100),
                city VARCHAR(100),
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                humidity FLOAT,
                wind_speed FLOAT,
                weather_code INT,
                ingestion_time TIMESTAMP,
                UNIQUE(city, ingestion_time)
            );
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS latitude FLOAT;
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS longitude FLOAT;
        """)
    conn.commit()

def load_weather_data(df: pd.DataFrame):
    """
    Load weather DataFrame into PostgreSQL table 'weather_readings'.
    Uses ON CONFLICT DO UPDATE (Upsert) to prevent duplicate records.
    """
    if df.empty:
        logging.warning("DataFrame is empty. No data to load into PostgreSQL.")
        return

    insert_query = """
        INSERT INTO weather_readings 
        (province, city, latitude, longitude, temperature, humidity, wind_speed, weather_code, ingestion_time)
        VALUES %s
        ON CONFLICT (city, ingestion_time) 
        DO UPDATE SET 
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            temperature = EXCLUDED.temperature,
            humidity = EXCLUDED.humidity,
            wind_speed = EXCLUDED.wind_speed,
            weather_code = EXCLUDED.weather_code;
    """
    
    # Convert DataFrame rows into tuples for bulk insertion
    data_tuples = [
        (
            row['province'], 
            row['city'], 
            float(row['latitude']),
            float(row['longitude']),
            float(row['temperature']), 
            float(row['humidity']), 
            float(row['wind_speed']), 
            int(row['weather_code']), 
            row['ingestion_time']
        )
        for _, row in df.iterrows()
    ]

    try:
        logging.info("Connecting to PostgreSQL database...")
        with get_db_connection() as conn:
            ensure_table_schema(conn)
            with conn.cursor() as cur:
                execute_values(cur, insert_query, data_tuples)
            conn.commit()
        logging.info(f"✅ Successfully loaded/updated {len(data_tuples)} records in PostgreSQL table 'weather_readings'!")
    except Exception as e:
        logging.error(f"❌ Failed to load data into PostgreSQL: {e}")
        raise e
