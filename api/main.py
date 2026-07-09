import logging
from extractor import start_extraction
from loader import load_weather_data

if __name__ == "__main__":
    logging.info("=== Starting Weather ETL Pipeline ===")
    
    # 1. Extraction & Validation Phase
    logging.info("--- Phase 1: Extraction & Validation ---")
    weather_df = start_extraction('cities.json')
    
    if weather_df is not None and not weather_df.empty:
        # Save a backup CSV locally
        csv_filename = "egypt_weather_full.csv"
        weather_df.to_csv(csv_filename, index=False)
        logging.info(f"Backup CSV saved to '{csv_filename}'")
        
        # 2. Loading Phase
        logging.info("--- Phase 2: Loading to PostgreSQL ---")
        load_weather_data(weather_df)
        
        logging.info("=== ETL Pipeline Completed Successfully! ===")
    else:
        logging.error("❌ Pipeline stopped: Extracted DataFrame is empty or None.")
