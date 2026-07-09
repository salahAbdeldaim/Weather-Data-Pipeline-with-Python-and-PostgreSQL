# 🚀 خارطة طريق التطوير وزيادة قيمة المشروع (Future Enhancements & Value-Add Roadmap)
### مشروع تخرج مبادرة رواد مصر الرقمية (DEPI) — مسار Microsoft Data Engineer

تعتبر هذه الوثيقة **خارطة طريق هندسية وتصميمية (Blueprint)** تحتوي على جميع التعديلات البرمجية، واستعلامات الـ SQL، وأفكار لوحات التحكم التي تم الاتفاق عليها لرفع قيمة منصة طقس مصر وتحويلها إلى **منصة متكاملة لذكاء الأعمال وهندسة البيانات (Enterprise-Grade Data Platform)** جاهزة للتطبيق في أي وقت تتطلب فيه تطوير المشروع قبل مناقشة التخرج.

---

## 🌟 ملخص التطويرات الأربعة المقترحة:
1. **إثراء البيانات (Data Enrichment):** إضافة حقول جديدة (الحرارة المحسوسة، مؤشر UV، الأمطار، الضغط الجوي) من Open-Meteo API.
2. **لوحات تحكم تخصصية (Domain-Specific BI):** إنشاء داشبوردات لقطاع السياحة وقطاع الطاقة المتجددة والزراعة.
3. **نظام الإنذار المبكر (Automated Weather Alerts):** ربط قاعدة البيانات بـ n8n وبوت تليجرام لإرسال تحذيرات فورية عند ارتفاع الحرارة أو الرياح.
4. **التحليلات التاريخية والمتقدمة (Historical Trends & Window Functions):** بناء استعلامات تجميعية لتتبع تغير المناخ.

---

## 💡 التطوير الأول: إثراء البيانات من واجهة Open-Meteo API (Data Enrichment)

لجعل البيانات أكثر ثراءً وفائدة لصناع القرار، سنقوم بسحب 4 متغيرات إضافية مجانية من API الطقس:
*   **`apparent_temperature` (الحرارة المحسوسة / RealFeel):** تعكس الشعور الحقيقي بالحرارة في ظل الرطوبة والرياح.
*   **`uv_index` (مؤشر الأشعة فوق البنفسجية):** ضروري لقطاع السياحة والصحة العامة.
*   **`precipitation` (معدل هطول الأمطار مم):** مهم لنظام التنبؤ بالسيول والأمطار.
*   **`surface_pressure` (الضغط الجوي هكتوباسكال):** يستخدم في التنبؤات الجوية وحركة الرياح.

### 🛠️ التعديل المطلوب في ملف `api/extractor.py`:
يتم تحديث رابط الـ API ونموذج الـ Pydantic بالشكل التالي:

```python
# 1. تحديث نموذج Pydantic
class WeatherRecord(BaseModel):
    province: str
    city: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    temperature: float = Field(..., ge=-10, le=60)
    apparent_temperature: float = Field(..., ge=-10, le=65) # [جديد]
    humidity: float = Field(..., ge=0, le=100)
    wind_speed: float = Field(..., ge=0)
    uv_index: float = Field(..., ge=0)                      # [جديد]
    precipitation: float = Field(..., ge=0)                 # [جديد]
    surface_pressure: float = Field(..., ge=0)              # [جديد]
    weather_code: int
    ingestion_time: str

# 2. تحديث الرابط واستخراج المتغيرات داخل دالة start_extraction
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lat}&longitude={lon}"
    f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m,uv_index"
    f"&timezone=Africa%2FCairo"
)

# 3. إضافتهم للقاموس (row)
row = {
    "province": loc['province'],
    "city": loc['city'],
    "latitude": float(loc['lat']),
    "longitude": float(loc['lon']),
    "temperature": c.get('temperature_2m'),
    "apparent_temperature": c.get('apparent_temperature'), # [جديد]
    "humidity": c.get('relative_humidity_2m'),
    "wind_speed": c.get('wind_speed_10m'),
    "uv_index": c.get('uv_index'),                         # [جديد]
    "precipitation": c.get('precipitation'),               # [جديد]
    "surface_pressure": c.get('surface_pressure'),         # [جديد]
    "weather_code": c.get('weather_code'),
    "ingestion_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
```

### 🛠️ التعديل المطلوب في ملف `api/loader.py`:
يتم إضافة الأعمدة الجديدة تلقائياً في قاعدة البيانات عبر دالة `ensure_table_schema`:

```python
def ensure_table_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS apparent_temperature FLOAT;
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS uv_index FLOAT;
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS precipitation FLOAT;
            ALTER TABLE weather_readings ADD COLUMN IF NOT EXISTS surface_pressure FLOAT;
        """)
    conn.commit()
```

---

## 📊 التطوير الثاني: لوحات تحكم تخصصية في Metabase (Domain-Specific BI)

بدل عرض البيانات الأولية فقط، يمكنك إنشاء لوحات تحكم تخدم وزارات وقطاعات محددة في الدولة:

### 1️⃣ مؤشر الجذب السياحي (Tourism Weather Index):
لوحة مخصصة لوزارة السياحة تقارن المدن السياحية (الغردقة، شرم الشيخ، الأقصر، أسوان، العلمين الجديدة، سانت كاترين):
```sql
SELECT DISTINCT ON (city)
    city AS "المدينة السياحية",
    temperature AS "درجة الحرارة (°C)",
    humidity AS "الرطوبة (%)",
    wind_speed AS "سرعة الرياح (كم/س)",
    CASE 
        WHEN temperature BETWEEN 20 AND 30 AND wind_speed < 25 THEN '🌟 طقس مثالي للسياحة'
        WHEN temperature > 38 THEN '⚠️ حار جداً - يفضل الأنشطة المسائية'
        ELSE '🌤️ طقس معتدل'
    END AS "تقييم الطقس السياحي"
FROM weather_readings
WHERE city IN ('Hurghada', 'Sharm El Sheikh', 'Luxor', 'Aswan', 'New Alamein City', 'Saint Catherine')
ORDER BY city, ingestion_time DESC;
```

### 2️⃣ لوحة دعم الطاقة المتجددة والزراعة (Renewable Energy & Agriculture):
مقارنة بين أقاليم مصر (الدلتا مقابل الصعيد) لتحديد أفضل الأماكن لمزارع الرياح والطاقة الشمسية:
```sql
SELECT 
    CASE 
        WHEN province IN ('Aswan', 'Luxor', 'Qena', 'Sohag', 'Asyut', 'Minya', 'Beni Suef', 'Faiyum') THEN 'إقليم الصعيد (Upper Egypt)'
        WHEN province IN ('Cairo', 'Giza', 'Qalyubia', 'Alexandria', 'Beheira', 'Dakahlia', 'Sharqia', 'Monufia', 'Gharbia', 'Kafr El Sheikh', 'Damietta') THEN 'إقليم الدلتا والقاهرة الكبير'
        ELSE 'إقليم سيناء والقناة والحدود'
    END AS "الإقليم الجغرافي",
    ROUND(AVG(temperature)::numeric, 1) AS "متوسط الحرارة",
    ROUND(AVG(wind_speed)::numeric, 1) AS "متوسط سرعة الرياح (كم/س)",
    ROUND(AVG(humidity)::numeric, 1) AS "متوسط الرطوبة (%)"
FROM weather_readings
WHERE ingestion_time >= NOW() - INTERVAL '24 hours'
GROUP BY 1
ORDER BY "متوسط سرعة الرياح (كم/س)" DESC;
```

---

## 🤖 التطوير الثالث: نظام الإنذار المبكر عبر n8n وبوت تليجرام (Automated Weather Alerts)

توضيح كيفية استخدام أداة الأتمتة **n8n** لإرسال إنذارات جوية ذكية على قناة التليجرام:

1.  **إضافة عقدة Postgres (Postgres Node) في n8n:**
    *   تقوم بتنفيذ استعلام يفحص المدن التي تتخطى فيها الحرارة 41 درجة أو الرياح 35 كم/ساعة:
    ```sql
    SELECT city, province, temperature, wind_speed, ingestion_time
    FROM weather_readings
    WHERE (temperature >= 41 OR wind_speed >= 35)
      AND ingestion_time >= NOW() - INTERVAL '2 hours';
    ```
2.  **إضافة عقدة شرطية (IF Node):**
    *   الشرط: `if items.length > 0` (يعني لو الاستعلام رجع مدن فيها طقس متطرف).
3.  **إضافة عقدة تليجرام (Telegram Node):**
    *   إرسال رسالة تحذيرية عاجلة على جروب فريق العمل:
    > ⚠️ **إنذار جوي عاجل — منصة طقس مصر (DEPI):**
    > تم رصد ارتفاع شديد في درجات الحرارة/الرياح في المحافظات التالية:
    > 📍 **المدينة:** {{ $json.city }} (محافظة {{ $json.province }})
    > 🌡️ **درجة الحرارة:** {{ $json.temperature }}°C
    > 💨 **سرعة الرياح:** {{ $json.wind_speed }} كم/ساعة
    > 🕒 **وقت الرصد:** {{ $json.ingestion_time }}
    > *يرجى اتخاذ التدابير اللازمة وتحذير المواطنين في هذه النطاقات الجغرافية.*

---

## 📈 التطوير الرابع: التحليلات التاريخية (Historical Trends & Window Functions)

بعد تشغيل البايبلاين لعدة أيام، يمكنك استخدام دوال النوافذ (Window Functions) في PostgreSQL لعرض تغير المناخ:

### تقرير أحر وأبرد قراءة أسبوعية لكل محافظة (Weekly Temperature Extremes):
```sql
WITH RankedWeather AS (
    SELECT 
        province,
        city,
        temperature,
        ingestion_time,
        ROW_NUMBER() OVER(PARTITION BY province ORDER BY temperature DESC) as max_temp_rank,
        ROW_NUMBER() OVER(PARTITION BY province ORDER BY temperature ASC) as min_temp_rank
    FROM weather_readings
    WHERE ingestion_time >= NOW() - INTERVAL '7 days'
)
SELECT 
    province AS "المحافظة",
    MAX(CASE WHEN max_temp_rank = 1 THEN city || ' (' || temperature || '°C)' END) AS "أحر مدينة هذا الأسبوع",
    MAX(CASE WHEN min_temp_rank = 1 THEN city || ' (' || temperature || '°C)' END) AS "أبرد مدينة هذا الأسبوع"
FROM RankedWeather
GROUP BY province
ORDER BY province;
```

---

## 🏆 خاتمة: أثر هذه التطويرات على تقييم المشروع
تنفيذ أي من هذه التطويرات أو إدراجها في العرض التقديمي (Presentation) يثبت للمقيّمين في وزارة الاتصالات ومايكروسوفت أن المنصة ليست مجرد مشروع تخرج تدريبي، بل هي **نظام مؤسسي متكامل (Production-Ready System)** قادر على:
1.  التعامل مع البيانات الضخمة والتاريخية (Scalability & Time-Series Modeling).
2.  تقديم قيمة أعمال حقيقية لمتخذي القرار (Business Intelligence & Data Governance).
3.  الأتمتة الكاملة والمراقبة الحية وبث الإنذارات (DataOps, DevOps & Real-time Alerting).
