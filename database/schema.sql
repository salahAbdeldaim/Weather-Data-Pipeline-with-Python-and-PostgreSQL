-- ==============================================================================
-- Weather Data Pipeline - Database Schema Definition (PostgreSQL)
-- ==============================================================================

-- 1. Create the main table for storing historical and real-time weather readings
CREATE TABLE IF NOT EXISTS weather_readings (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100) NOT NULL,            -- Province name (e.g., Cairo, Alexandria, Aswan)
    city VARCHAR(100) NOT NULL,                -- City or town name (e.g., Nasr City, Mansoura)
    latitude FLOAT,                            -- Geographic latitude coordinate
    longitude FLOAT,                           -- Geographic longitude coordinate
    temperature FLOAT NOT NULL,                -- Temperature in Celsius (°C)
    humidity FLOAT NOT NULL,                   -- Relative humidity percentage (%)
    wind_speed FLOAT NOT NULL,                 -- Wind speed (km/h or m/s)
    weather_code INT NOT NULL,                 -- WMO weather condition code
    ingestion_time TIMESTAMP NOT NULL,         -- Timestamp when data was fetched from API
    
    -- Constraint: Prevent duplicate readings for the exact same city and timestamp (Upsert Target)
    CONSTRAINT unique_city_ingestion UNIQUE(city, ingestion_time)
);

-- 2. Create Indexes to optimize query speed and Metabase BI dashboard performance
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_readings(city);
CREATE INDEX IF NOT EXISTS idx_weather_province ON weather_readings(province);
CREATE INDEX IF NOT EXISTS idx_weather_ingestion_time ON weather_readings(ingestion_time DESC);
CREATE INDEX IF NOT EXISTS idx_weather_temp ON weather_readings(temperature);

-- ==============================================================================
-- 3. Helpful Database Views (Optional: pre-made views for analytical reporting)
-- ==============================================================================

-- View: Latest weather reading per city
CREATE OR REPLACE VIEW view_latest_weather_per_city AS
SELECT 
    DISTINCT ON (city)
    id,
    province,
    city,
    latitude,
    longitude,
    temperature,
    humidity,
    wind_speed,
    weather_code,
    ingestion_time
FROM weather_readings
ORDER BY city, ingestion_time DESC;

-- View: Daily summary statistics per province
CREATE OR REPLACE VIEW view_province_daily_stats AS
SELECT 
    province,
    DATE(ingestion_time) AS reading_date,
    COUNT(id) AS total_readings,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
    ROUND(MAX(temperature)::numeric, 2) AS max_temperature,
    ROUND(MIN(temperature)::numeric, 2) AS min_temperature,
    ROUND(AVG(humidity)::numeric, 2) AS avg_humidity
FROM weather_readings
GROUP BY province, DATE(ingestion_time)
ORDER BY reading_date DESC, avg_temperature DESC;

