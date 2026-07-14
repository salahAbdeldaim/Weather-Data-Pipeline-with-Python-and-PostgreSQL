"""
==============================================================================
PostgreSQL Data Loader
==============================================================================
Overview:
This script manages database connection and loads weather data into PostgreSQL:
1. Connects to the database using credentials loaded from the .env file.
2. Automatically checks and creates the 'weather_readings' table and latitude/longitude columns if they don't exist.
3. Inserts records in bulk using execute_values for fast performance.
4. Handles duplicates using Upsert (ON CONFLICT DO UPDATE) so existing records are updated instead of duplicated.
"""

import os
import logging
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from dotenv import load_dotenv

# Load environment variables (such as DB username, password, and port) from .env file
load_dotenv()

def get_db_connection():
    """
    Create and return an active PostgreSQL database connection.
    
    Returns:
        psycopg2.extensions.connection: Active database connection object.
    """
    # Read database connection settings from .env with default fallback values
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "32770"),
        dbname=os.getenv("DB_NAME", "project"),
        user=os.getenv("DB_USER", "salah_depi"),
        password=os.getenv("DB_PASSWORD")
    )

def ensure_table_schema(conn):
    """
    Check if 'weather_readings' table exists, and create it automatically if missing.
    
    Args:
        conn: Database connection object.
    """
    with conn.cursor() as cur:
        # Create table if not exists, with a UNIQUE constraint on (city, ingestion_time)
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
            -- Add latitude and longitude columns if the table was created before
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS latitude FLOAT;
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS longitude FLOAT;
        """)
    # Save (commit) schema changes to the database
    conn.commit()

def load_weather_data(df: pd.DataFrame):
    """
    Load weather DataFrame into PostgreSQL table 'weather_readings'.
    Uses Upsert (ON CONFLICT DO UPDATE) to update existing records cleanly without duplicates.
    
    Args:
        df (pd.DataFrame): DataFrame containing validated weather records.
    """
    # Check if DataFrame is empty before opening a database connection
    if df.empty:
        logging.warning("DataFrame is empty. No data to load into PostgreSQL.")
        return

    # Insert query with conflict handling (Upsert Query)
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
    
    # Convert DataFrame rows into tuples for fast bulk insertion
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
        # Open database connection using a context manager
        with get_db_connection() as conn:
            # Ensure table and columns exist before inserting
            ensure_table_schema(conn)
            with conn.cursor() as cur:
                # Use execute_values to insert all rows in one single batch request
                execute_values(cur, insert_query, data_tuples)
            # Commit the changes to the database
            conn.commit()
        logging.info(f"✅ Successfully loaded/updated {len(data_tuples)} records in PostgreSQL table 'weather_readings'!")
    except Exception as e:
        # Log error and raise exception if insertion fails
        logging.error(f"❌ Failed to load data into PostgreSQL: {e}")
        raise e


