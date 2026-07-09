# Weather Data Extraction Layer 🇪🇬
# طبقة استخراج بيانات الطقس

This module represents the **Extraction and Validation** phase (Milestone 1) of the Weather Data Pipeline project. It retrieves real-time weather data for 81 Egyptian cities using the Open-Meteo API.
تمثل هذه الوحدة مرحلة **استخراج والتحقق من البيانات** للمشروع. تقوم الوحدة بجلب بيانات الطقس اللحظية لـ 71 مدينة مصرية باستخدام واجهة برمجة تطبيقات Open-Meteo.

## Features | الميزات التقنية
- **Data Fetching:** Synchronous HTTP requests targeting Open-Meteo API with strict timeout handling.
- **Data Validation:** Runtime data validation and type checking using `Pydantic` models to ensure data integrity before downstream processing.
- **Logging:** Comprehensive event logging (INFO, WARNING, ERROR) outputted to both the terminal and a `pipeline.log` file.
- **Rate Limiting:** Managed request execution to comply with API constraints.

## Prerequisites | المتطلبات
Ensure you have the required Python packages installed:
تأكد من تثبيت المكتبات التالية:
```bash
pip install -r requirements.txt