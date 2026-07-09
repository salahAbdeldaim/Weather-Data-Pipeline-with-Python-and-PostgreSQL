import json
import logging
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def enrich_egypt_cities(excel_path="worldcities.xlsx", json_path="cities.json"):
    if not os.path.exists(excel_path):
        logging.error(f"❌ Excel file '{excel_path}' not found in current directory!")
        return

    logging.info(f"📂 Reading Excel file '{excel_path}'...")
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        logging.error(f"❌ Failed to read Excel file. Please ensure 'openpyxl' is installed (pip install openpyxl): {e}")
        return

    # Filter for Egypt (checking country column or iso2 column)
    egypt_df = df[(df['country'] == 'Egypt') | (df['iso2'] == 'EG')].copy()
    logging.info(f"🇪🇬 Found {len(egypt_df)} Egyptian cities/towns in the Excel database!")

    # Load existing cities.json
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            existing_cities = json.load(f)
    else:
        existing_cities = []

    logging.info(f"📋 Current '{json_path}' contains {len(existing_cities)} cities.")

    # Create a set of lowercase city names to avoid duplicate insertions
    existing_names = {item['city'].strip().lower() for item in existing_cities}

    added_count = 0
    for _, row in egypt_df.iterrows():
        # Get city ascii name or regular city name
        city_name = str(row['city_ascii']).strip() if pd.notna(row['city_ascii']) else str(row['city']).strip()
        
        # Get province/admin_name
        province_name = str(row['admin_name']).strip() if pd.notna(row['admin_name']) and str(row['admin_name']).strip() != "" else "Egypt"
        
        try:
            lat = float(row['lat'])
            lon = float(row['lng'])
        except (ValueError, TypeError):
            continue

        # If city not already in our JSON, add it!
        if city_name.lower() not in existing_names:
            new_entry = {
                "province": province_name,
                "city": city_name,
                "lat": round(lat, 4),
                "lon": round(lon, 4)
            }
            existing_cities.append(new_entry)
            existing_names.add(city_name.lower())
            added_count += 1

    # Save back to cities.json with pretty formatting
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(existing_cities, f, indent=2, ensure_ascii=False)

    logging.info(f"🎉 Success! Extracted and added {added_count} NEW Egyptian cities/towns!")
    logging.info(f"📊 Total Egyptian cities in '{json_path}' is now: {len(existing_cities)}!")

if __name__ == "__main__":
    logging.info("=== Starting Egypt Cities Enrichment Script ===")
    enrich_egypt_cities()
