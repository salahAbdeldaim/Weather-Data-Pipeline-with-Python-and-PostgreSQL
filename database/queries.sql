-- ==============================================================================
-- Weather Data Pipeline - Useful SQL Queries for Verification & Presentation
-- استعلامات SQL هامة لاختبار البيانات وعرضها أثناء المناقشة والتقييم
-- ==============================================================================

-- 1. Check total number of weather readings recorded so far
-- التحقق من إجمالي عدد القراءات المسجلة في قاعدة البيانات
SELECT COUNT(*) AS total_weather_records FROM weather_readings;

-- 2. View the top 20 most recent weather readings across all cities
-- عرض أحدث 20 قراءة مسجلة في قاعدة البيانات
SELECT 
    province AS المحافظة,
    city AS المدينة,
    ROUND(temperature::numeric, 1) || ' °C' AS درجة_الحرارة,
    ROUND(humidity::numeric, 1) || ' %' AS الرطوبة,
    ROUND(wind_speed::numeric, 1) || ' km/h' AS سرعة_الرياح,
    TO_CHAR(ingestion_time, 'YYYY-MM-DD HH24:MI:SS') AS وقت_التسجيل
FROM weather_readings
ORDER BY ingestion_time DESC
LIMIT 20;

-- 3. Top 10 Hottest Cities in the latest batch of readings
-- أعلى 10 مدن في درجة الحرارة من أحدث البيانات
SELECT 
    province AS المحافظة,
    city AS المدينة,
    temperature AS درجة_الحرارة,
    humidity AS نسبة_الرطوبة
FROM view_latest_weather_per_city
ORDER BY temperature DESC
LIMIT 10;

-- 4. Top 10 Coldest Cities in the latest batch of readings
-- أبرد 10 مدن في درجة الحرارة حالياً
SELECT 
    province AS المحافظة,
    city AS المدينة,
    temperature AS درجة_الحرارة,
    humidity AS نسبة_الرطوبة
FROM view_latest_weather_per_city
ORDER BY temperature ASC
LIMIT 10;

-- 5. Average Weather Conditions per Province (Summary Analytics)
-- متوسط درجات الحرارة والرطوبة لكل محافظة (لشاشات العرض Metabase)
SELECT 
    province AS المحافظة,
    COUNT(DISTINCT city) AS عدد_المدن,
    ROUND(AVG(temperature)::numeric, 2) AS متوسط_الحرارة,
    ROUND(AVG(humidity)::numeric, 2) AS متوسط_الرطوبة,
    ROUND(AVG(wind_speed)::numeric, 2) AS متوسط_سرعة_الرياح
FROM view_latest_weather_per_city
GROUP BY province
ORDER BY متوسط_الحرارة DESC;

-- 6. Check data distribution across dates/time (Validate Ingestion Frequency)
-- التحقق من انتظام سحب وتخزين البيانات عبر الوقت
SELECT 
    DATE(ingestion_time) AS تاريخ_القراءة,
    COUNT(*) AS عدد_السجلات,
    MIN(ingestion_time) AS أول_قراءة_في_اليوم,
    MAX(ingestion_time) AS آخر_قراءة_في_اليوم
FROM weather_readings
GROUP BY DATE(ingestion_time)
ORDER BY تاريخ_القراءة DESC;
