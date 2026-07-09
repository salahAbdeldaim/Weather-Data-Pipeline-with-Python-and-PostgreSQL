-- ==============================================================================
-- Weather Data Pipeline - Database Schema Definition (PostgreSQL)
-- مرحلة تعريف جداول قاعدة البيانات - مشروع بيانات الطقس في مصر
-- ==============================================================================

-- 1. Create the main table for storing historical and real-time weather readings
CREATE TABLE IF NOT EXISTS weather_readings (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100) NOT NULL,            -- المحافظة (e.g., Cairo, Alexandria, Aswan)
    city VARCHAR(100) NOT NULL,                -- المدينة / المركز (e.g., Nasr City, Mansoura)
    latitude FLOAT,                            -- خط العرض الجغرافي
    longitude FLOAT,                           -- خط الطول الجغرافي
    temperature FLOAT NOT NULL,                -- درجة الحرارة (بالمقياس المئوي Celsius)
    humidity FLOAT NOT NULL,                   -- نسبة الرطوبة (بالمائة %)
    wind_speed FLOAT NOT NULL,                 -- سرعة الرياح (كم / ساعة أو متر/ثانية)
    weather_code INT NOT NULL,                 -- كود حالة الطقس (وفقاً لتصنيف WMO Weather Codes)
    ingestion_time TIMESTAMP NOT NULL,         -- وقت وتاريخ قراءة البيانات من الـ API
    
    -- Constraint: Prevent duplicate readings for the exact same city and timestamp
    -- منع تكرار نفس البيانات لنفس المدينة في نفس اللحظة الزمنيّة (Upsert Target)
    CONSTRAINT unique_city_ingestion UNIQUE(city, ingestion_time)
);

-- 2. Create Indexes to optimize analytical queries and Metabase BI dashboard performance
-- إنشاء فهارس لتحسين سرعة الاستعلامات ولوحات بيانات Metabase
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_readings(city);
CREATE INDEX IF NOT EXISTS idx_weather_province ON weather_readings(province);
CREATE INDEX IF NOT EXISTS idx_weather_ingestion_time ON weather_readings(ingestion_time DESC);
CREATE INDEX IF NOT EXISTS idx_weather_temp ON weather_readings(temperature);

-- ==============================================================================
-- 3. Helpful Database Views (اختياري: عروض جاهزة لتسهيل التحليلات)
-- ==============================================================================

-- View: Latest weather reading per city (أحدث قراءة للطقس لكل مدينة)
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

-- View: Daily summary statistics per province (إحصائيات الطقس اليومية لكل محافظة)
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
