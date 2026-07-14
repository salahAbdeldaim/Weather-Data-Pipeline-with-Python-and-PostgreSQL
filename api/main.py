"""
==============================================================================
ETL Pipeline Main Script
==============================================================================
Overview:
This script controls and runs the complete ETL (Extract, Transform, Load) pipeline:
1. Extract & Validate: Get weather readings for cities from Open-Meteo API and check data quality using Pydantic.
2. Local Backup: Save the extracted data into a local CSV file (egypt_weather_full.csv) to prevent data loss.
3. Load to Database: Insert or update the records into PostgreSQL (using Upsert to avoid duplicates).
"""

import logging
from extractor import start_extraction
from loader import load_weather_data

if __name__ == "__main__":
    # Start the ETL pipeline and log the start time
    logging.info("=== Starting Weather ETL Pipeline ===")
    
    # --------------------------------------------------------------------------
    # Phase 1: Extraction & Validation
    # --------------------------------------------------------------------------
    logging.info("--- Phase 1: Extraction & Validation ---")
    
    # Call start_extraction to get weather data for all cities in 'cities.json'
    weather_df = start_extraction('cities.json')
    
    # Check if the returned DataFrame is valid and not empty
    if weather_df is not None and not weather_df.empty:
        # ----------------------------------------------------------------------
        # Step 1.5: Save a local backup CSV
        # ----------------------------------------------------------------------
        csv_filename = "egypt_weather_full.csv"
        weather_df.to_csv(csv_filename, index=False)
        logging.info(f"Backup CSV saved to '{csv_filename}'")
        
        # ----------------------------------------------------------------------
        # Phase 2: Loading to PostgreSQL Database
        # ----------------------------------------------------------------------
        logging.info("--- Phase 2: Loading to PostgreSQL ---")
        
        # Call load_weather_data to insert/upsert records into 'weather_readings' table
        load_weather_data(weather_df)
        
        logging.info("=== ETL Pipeline Completed Successfully! ===")
    else:
        # If no data was extracted or an error occurred, stop the pipeline
        logging.error("❌ Pipeline stopped: Extracted DataFrame is empty or None.")

