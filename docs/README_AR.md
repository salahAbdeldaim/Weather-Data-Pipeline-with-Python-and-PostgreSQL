# 🌤️ Egypt Weather Data Engineering & BI Platform 🇪🇬

### منصة هندسة بيانات الطقس وذكاء الأعمال - متكاملة بمعايير الشركات العالمية

**🎓 مشروع تخرج مبادرة رواد مصر الرقمية (DEPI)**
\*وزارة الاتصالات وتكنولوجيا المعلومات المصرية (MCIT) — **مسار هندسة البيانات (Microsoft Data Engineer Track)\***

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED.svg?logo=docker&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Workflow_Automation-EA4B71.svg?logo=n8n&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-BI_Dashboard-509EE3.svg?logo=metabase&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Alert_Bot-2CA5E0.svg?logo=telegram&logoColor=white)

---

## 📑 فهرس المحتويات | Table of Contents

1. [نبذة عامة عن المشروع | Executive Summary](#1-نبذة-عامة-عن-المشروع--executive-summary)
2. [هيكل الفريق والمسؤوليات | Team Structure & Roles](#2-هيكل-الفريق-والمسؤوليات--team-structure--roles)
3. [المعمارية الهندسية ومخطط تدفق البيانات | System Architecture](#3-المعمارية-الهندسية-ومخطط-تدفق-البيانات--system-architecture)
4. [التقنيات المستخدمة | Technology Stack](#4-التقنيات-المستخدمة--technology-stack)
5. [شرح المراحل الهندسية بالتفصيل | Detailed Engineering Stages](#5-شرح-المراحل-الهندسية-بالتفصيل--detailed-engineering-stages)
   - [المرحلة الأولى: استخراج البيانات والتحقق من جودتها (Pydantic & Pandas)](#المرحلة-الأولى-استخراج-البيانات-والتحقق-من-جودتها-pydantic--pandas)
   - [المرحلة الثانية: بناء قاعدة البيانات ومنع التكرار (Idempotent Upsert)](#المرحلة-الثانية-بناء-قاعدة-البيانات-ومنع-التكرار-idempotent-upsert)
   - [المرحلة الثالثة: الـ DevOps والحاويات (Docker & Cloud VPS)](#المرحلة-الثالثة-الـ-devops-والحاويات-docker--cloud-vps)
   - [المرحلة الرابعة: أتمتة التشغيل والإنذارات (n8n & Telegram Bot)](#المرحلة-الرابعة-أتمتة-التشغيل-والإنذارات-n8n--telegram-bot)
   - [المرحلة الخامسة: ذكاء الأعمال وصلاحيات الوصول (Metabase & RBAC)](#المرحلة-الخامسة-ذكاء-الأعمال-وصلاحيات-الوصول-metabase--rbac)
6. [دليل التشغيل السريع | Quick Start Guide](#6-دليل-التشغيل-السريع--quick-start-guide)
7. [دليل وصول فريق الداشبورد والتحليل | BI & Analytics Team Access Guide](#7-دليل-وصول-فريق-الداشبورد-والتحليل--bi--analytics-team-access-guide)
8. [الخطوات المستقبلية | Future Roadmap](#8-الخطوات-المستقبلية--future-roadmap)

---

## 1. نبذة عامة عن المشروع | Executive Summary

منصة **Egypt Weather Data Engineering & BI Platform** هي مشروع تخرج متكامل (Capstone Project) تم تطويره ضمن **مبادرة رواد مصر الرقمية (DEPI)** التابعة لـ **وزارة الاتصالات وتكنولوجيا المعلومات المصرية (MCIT)** في مسار **مهندس بيانات مايكروسوفت (Microsoft Data Engineer Track)**.

النظام يعمل بشكل مؤتمت بالكامل لاستخراج، تنظيف، التحقق من جودة، تخزين، ومراقبة بيانات الطقس اللحظية لـ **71 مدينة ومحافظة مصرية** من واجهة Open-Meteo API. تم تصميم المشروع وفقاً لأحدث معايير الـ **DataOps** والـ **DevOps** في الشركات العالمية، حيث يعمل ذاتياً على سيرفر سحابي (Cloud VPS) بدون أي تدخل بشري. يضمن النظام نقاء البيانات بنسبة 100% عبر الفحص الصارم (Pydantic Validation)، ويمنع تكرار البيانات في قاعدة البيانات عبر هندسة الـ Idempotent Upsert، كما يوفر نظام إنذارات لحظي للفريق عبر تطبيق تليجرام، ويطبق مبدأ الصلاحية الأدنى (RBAC) لحماية السيرفر أثناء ربطه بأدوات ذكاء الأعمال (Metabase BI) ولمحللي البيانات (Data Analysts).

---

## 2. هيكل الفريق والمسؤوليات | Team Structure & Roles

يحاكي هذا المشروع فريق هندسة بيانات محترف في شركة عالمية ضمن تخصصات مسار Microsoft Data Engineer، حيث ينقسم العمل إلى 5 أدوار تخصصية متكاملة:

| الدور الهندسي (Role)                             | المسؤوليات والإنجازات الفعليّة في المشروع                                                                                                                  | التقنيات والمكتبات المستخدمة                  |
| :----------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------- |
| 🐍 **1. Data Extraction & Quality Engineer**     | بناء محرك سحب البيانات لـ 71 مدينة مصرية (`cities.json`). تصميم معايير الفحص والتحقق الصارمة بـ Pydantic لرفض أي قراءات شاذة أو تالفة قبل تخزينها.         | Python, Pandas, Pydantic, Requests            |
| 🐘 **2. Database Architect & Load Engineer**     | تصميم قاعدة بيانات العلاقات PostgreSQL وجدول `weather_readings`. هندسة منطق الإدخال الذكي (`ON CONFLICT DO UPDATE`) لمنع تكرار السطور عند التشغيل المتكرر. | PostgreSQL, SQL, psycopg2, SQLAlchemy         |
| 🐳 **3. DevOps & Cloud Infrastructure Engineer** | تغليف المشروع والداتابيز في حاويات Docker & Docker Compose. إعداد وإدارة السيرفر السحابي (Hostinger VPS) وضبط جدار الحماية (Firewall) والمنافذ.            | Docker, Docker Compose, Linux, UFW/Firewall   |
| ⚡ **4. DataOps & Automation Engineer**          | أتمتة التشغيل اليومي ذاتياً باستخدام أداة n8n السحابية عبر اتصال SSH. تطوير بوت تليجرام (`@wether_app_bot`) لإرسال إشعارات لحظية بنجاح أو فشل البايبلاين.  | n8n Workflow, Telegram Bot API, SSH/Bash      |
| 📊 **5. BI Developer & Data Governance Lead**    | تشغيل منصة Metabase لذكاء الأعمال وإعداد رسوم X-Ray البيانية. تطبيق نظام حماية الصلاحيات (RBAC) عبر إنشاء حساب قراءة فقط (`team_view`) للتيم.              | Metabase BI, PostgreSQL RBAC, Data Governance |

---

## 3. المعمارية الهندسية ومخطط تدفق البيانات | System Architecture

يعمل النظام عبر عدة طبقات هندسية معزولة لضمان الأمان، الاستمرارية، وسرعة المعالجة:

```mermaid
graph TD
    subgraph External Sources ["🌐 External Data Sources"]
        API["Open-Meteo Weather API<br/>(71 Egyptian Cities)"]
    end

    subgraph Cloud VPS ["☁️ Hostinger Cloud VPS Infrastructure (Dockerized)"]
        subgraph Orchestration Layer ["⚡ DataOps & Orchestration"]
            N8N["n8n Cloud Orchestrator<br/>(Daily Cron Trigger)"]
            TBOT["Telegram Alert Bot<br/>(@wether_app_bot)"]
        end

        subgraph Ingestion & Processing Layer ["🐍 Python ETL Container"]
            EXT["Extractor Module<br/>(Requests + Pandas)"]
            VAL["Validator Module<br/>(Pydantic Schema Guard)"]
            LOAD["Loader Module<br/>(psycopg2 Upsert Engine)"]
        end

        subgraph Storage & Governance Layer ["🐘 Relational Storage"]
            DB[(PostgreSQL 15 Database<br/>weather_db / project)]
            RBAC["RBAC Security Role<br/>(Read-Only: team_view)"]
        end

        subgraph BI & Analytics Layer ["📊 Business Intelligence"]
            META["Metabase BI Platform<br/>(Port: 3000)"]
            DASH["Interactive Dashboards<br/>& X-Ray Analytics"]
        end
    end

    subgraph End Users ["👥 Team & Stakeholders"]
        BI_TEAM["BI / PowerBI / Tableau Analysts"]
        DATA_TEAM["Python Data Analysts / Reports"]
    end

    %% Flow Connections
    N8N -->|1. SSH Execution Trigger| EXT
    EXT -->|2. Fetch Telemetry| API
    API -->|3. Raw JSON| EXT
    EXT -->|4. Clean DataFrame| VAL
    VAL -->|5. Validated Telemetry| LOAD
    LOAD -->|6. Idempotent Upsert| DB
    LOAD -->|7. Execution Status| N8N
    N8N -->|8. Success / Failure Alert| TBOT

    %% Governance & BI Flow
    DB --- RBAC
    RBAC -->|Secure Read Access| META
    META --> DASH
    RBAC -->|Direct SQL / Connect| BI_TEAM
    RBAC -->|Pandas / SQL Queries| DATA_TEAM
```

### 3.1 هيكل المجلدات وتنظيم المشروع (`Clean Modular Architecture`)

لضمان تنظيم الأكواد وتسهيل العمل المشترك بين أعضاء فريق هندسة البيانات وتقسيم المسؤوليات (استخراج البيانات، تصميم قاعدة البيانات، إدارة الحاويات والدوكر، ولوحات التحليلات BI)، تم تنظيم المشروع في مجلدات منفصلة واضحة ومستقلة:

```text
depi_project/
├── 📁 api/                   # 🐍 طبقة استخراج البيانات بالبايثون (Python ETL Extraction Layer & Pydantic)
│   ├── main.py               # نقطة الانطلاق الرئيسية لتشغيل البايبلين
│   ├── extractor.py          # جلب البيانات من الـ API وتحويلها لجداول Pandas
│   ├── loader.py             # محرك الـ Upsert لتحميل البيانات في PostgreSQL دون تكرار
│   ├── cities.json           # ملف إحداثيات 71 مدينة ومحافظة مصرية
│   └── Dockerfile            # ملف بناء حاوية بايثون الخاصة بالبايبلين
│
├── 📁 database/              # 🐘 طبقة قواعد البيانات (Database Architecture & SQL Layer)
│   ├── schema.sql            # هيكل الجداول (DDL)، القيود (Unique Constraints)، والفهارس (Indexes)
│   ├── queries.sql           # استعلامات SQL هامة وجاهزة لاختبار الأداء ومقارنة البيانات أثناء المناقشة
│   └── README.md             # دليل الاتصال بقاعدة البيانات مباشرة من اللاب توب (عبر DBeaver أو VS Code)
│
├── 📁 docker/                # 🐳 طبقة الدوكر وإدارة الحاويات (DevOps & Containerization Layer)
│   ├── docker-compose.yml    # ملف تعريف خدمات الحاويات المنفصل
│   ├── start_services.bat    # سكريبت تشغيل جميع الحاويات والخدمات بضغطة زر واحدة (Windows)
│   ├── stop_services.bat     # سكريبت إيقاف وتنظيف الحاويات بأمان
│   ├── run_pipeline_now.bat  # سكريبت تشغيل بايبلين استخراج الطقس فوراً لسحب أحدث قراءة
│   └── README.md             # دليل شرح الحاويات والشبكات والربط المنافذ
│
├── 📁 n8n/                   # ⚡ طبقة الأتمتة وجدولة التشغيل (DataOps & Workflow Automation Layer)
│   ├── depi.json             # ملف سير العمل المصدر بصيغة JSON ويشمل أوامر الـ SSH وبوت تليجرام
│   └── README.md             # دليل استيراد وإعداد الجدولة والتنبيهات
│
├── 📁 docs/                  # 📚 مركز التوثيق والأدلة الشاملة للمشروع
│   ├── README.md             # التوثيق التقني الشامل (باللغة الإنجليزية)
│   ├── README_AR.md          # التوثيق التقني والهندسي الشامل (باللغة العربية)
│   ├── SERVER_UPDATE_GUIDE.md # دليل تحديث ونشر المشروع على السيرفر السحابي
│   └── FUTURE_ENHANCEMENTS_ROADMAP.md # خارطة طريق التطوير وزيادة القيمة
│
├── 📄 README.md              # واجهة التنقل والمقدمة التنفيذية (باللغة الإنجليزية)
└── 📄 README_AR.md           # واجهة التنقل والمقدمة التنفيذية (باللغة العربية)
```

---

## 4. التقنيات المستخدمة | Technology Stack

- **لغة البرمجة الأساسية:** Python 3.11+
- **معالجة وتنظيف البيانات:** Pandas, NumPy
- **فحص جودة البيانات والتحقق:** Pydantic v2
- **قواعد البيانات والتخزين:** PostgreSQL 15 (Alpine), psycopg2-binary, SQLAlchemy
- **الحاويات وإدارة البيئة:** Docker, Docker Compose
- **أتمتة التشغيل والمراقبة:** n8n Workflow Automation
- **الإشعارات والتنبيهات اللحظية:** Telegram Bot API
- **ذكاء الأعمال واللوحات البيانية:** Metabase BI
- **البنية التحتية والسحاب:** Hostinger Linux Cloud VPS (Ubuntu), UFW Firewall

---

## 5. شرح المراحل الهندسية بالتفصيل | Detailed Engineering Stages

### المرحلة الأولى: استخراج البيانات والتحقق من جودتها (Pydantic & Pandas)

- **الهدف:** جلب بيانات الطقس اللحظية لـ 71 مدينة ومحافظة مصرية (القاهرة، الإسكندرية، أسوان، سيوة، سانت كاترين، الغردقة...) من واجهة Open-Meteo API بدون تخطي حدود الطلبات (Rate Limiting) وضمان خلو البيانات من أي تشوه.
- **التنفيذ:**
  - يقوم ملف `extractor.py` بقراءة إحداثيات المدن من ملف `cities.json`.
  - تحويل الـ JSON المستلم إلى جداول Pandas DataFrames مرتبة.
  - تمرير كل سجل عبر نموذج فحص **Pydantic Validation Schema** للتأكد من:
    - أن درجة الحرارة (`temperature_2m`) تقع في النطاق الجوي المنطقي ($-50^\circ\text{C}$ إلى $+60^\circ\text{C}$).
    - أن الرطوبة النسبية (`relative_humidity_2m`) بين $0\%$ و $100\%$.
    - صحة صيغة الطابع الزمني (ISO-8601 UTC).
  - أي قراءة شاذة أو تالفة يتم استبعادها وتسجيلها في الـ Logs فوراً لمنع تلوث قاعدة البيانات.

### المرحلة الثانية: بناء قاعدة البيانات ومنع التكرار (Idempotent Upsert)

- **الهدف:** تخزين البيانات في قاعدة بيانات علائقية قوية مع تطبيق خاصية الـ **Idempotency** (ضمان أن تشغيل البايبلاين 100 مرة متتالية لن ينتج عنه أي سطور مكررة في الداتابيز).
- **التنفيذ:**
  - تشغيل قاعدة بيانات PostgreSQL 15 مع وحدة تخزين دائمة (`postgres_data`).
  - إنشاء جدول `weather_readings` مع قيد فريد مركب: `UNIQUE(city, ingestion_time)`.
  - هندسة منطق الـ Upsert في ملف `loader.py`:
    ```sql
    INSERT INTO weather_readings (city, governorate, latitude, longitude, temperature, humidity, wind_speed, weather_code, ingestion_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (city, ingestion_time)
    DO UPDATE SET
        temperature = EXCLUDED.temperature,
        humidity = EXCLUDED.humidity,
        wind_speed = EXCLUDED.wind_speed,
        weather_code = EXCLUDED.weather_code;
    ```

### المرحلة الثالثة: الـ DevOps والحاويات (Docker & Cloud VPS)

- **الهدف:** القضاء تماماً على مشكلة "الكود شغال عندي ومش شغال عندك" وضمان عمل المشروع في أي بيئة أو سيرفر بضغطة زرار واحدة.
- **التنفيذ:**
  - كتابة ملف `Dockerfile` خفيف ومخصص لتطبيق البايثون.
  - استخدام `docker-compose.yml` لإدارة وتشغيل المنظومة بالكامل (PostgreSQL + ETL Pipeline + Metabase BI)، مع ضبط شبكات الاتصال الداخلية وإعدادات الفحص التلقائي للصحة (`pg_isready`).
  - إعداد جدار الحماية (Firewall) على سيرفر Hostinger لحماية بورتات الداتابيز الداخلية وعرض منافذ الويب بأمان.

### المرحلة الرابعة: أتمتة التشغيل والإنذارات (n8n & Telegram Bot)

- **الهدف:** أتمتة التشغيل اليومي للبايبلاين ومراقبة صحة النظام لحظياً بدون تدخل بشري.
- **التنفيذ:**
  - تصميم مسار أتمتة ذكي في منصة **n8n** السحابية (مرفق في الريبوزيتوري باسم `n8n_workflow.json`).
  - يستخدم مسار n8n نود SSH للاتصال بالسيرفر السحابي وتشغيل حاويات دوكر يومياً الساعة 00:00 UTC.
  - ربط النظام ببوت تليجرام (**`@wether_app_bot`**):
    - **في حالة النجاح (Success Alert):** يرسل رسالة فورية للتيم بتوقيت التشغيل وعدد السجلات التي تم سحبها وحفظها في قاعدة البيانات.
    - **في حالة الفشل (Failure Alert):** يرسل إنذار خطأ فوري مع تفاصيل المشكلة (Logs) لو حدث أي انقطاع في الاتصال أو خطأ في الـ API.

### المرحلة الخامسة: ذكاء الأعمال وصلاحيات الوصول (Metabase & RBAC)

- **الهدف:** توفير لوحات عرض تحليلية متطورة لمتخذي القرار مع تطبيق صارم لمبدأ الصلاحية الأدنى (Principle of Least Privilege).
- **التنفيذ:**
  - تشغيل منصة **Metabase BI** كحاوية مستقلة على المنفذ `3000`.
  - تفعيل خاصية الـ **X-Ray Analytics** لإنشاء مخططات بيانية وتوزيعات الحرارة والرطوبة وسرعة الرياح لمدن مصر تلقائياً.
  - **حكمة البيانات والأمان (RBAC):** لحماية السيرفر ومنع أي مسح أو تعديل بالخطأ من قبل محللي البيانات أو أكواد التقارير، تم إنشاء حساب مستخدم في PostgreSQL مخصص **للقراءة فقط (Read-Only)**:
    ```sql
    CREATE USER team_view WITH PASSWORD 'team_view';
    GRANT CONNECT ON DATABASE project TO team_view;
    GRANT USAGE ON SCHEMA public TO team_view;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO team_view;
    ```

---

## 6. دليل التشغيل السريع | Quick Start Guide

### الخيار الأول: التشغيل الكامل باستخدام Docker Compose (الموصى به)

لتشغيل المنظومة بالكامل (PostgreSQL + Python ETL + Metabase BI) على أي جهاز:

1. **نسخ الريبوزيتوري من GitHub:**

   ```bash
   git clone https://github.com/your-username/depi_project.git
   cd depi_project
   ```

2. **إعداد متغيرات البيئة (Environment Variables):**

   ```bash
   cp .env.example .env
   cp api/.env.example api/.env
   # قم بتعديل ملفات .env ووضع بياناتك الخاصة
   ```

3. **تشغيل الحاويات في الخلفية:**

   ```bash
   docker-compose up -d --build
   ```

4. **التأكد من صحة عمل الحاويات:**
   ```bash
   docker ps
   # يجب أن ترى weather_postgres و weather_metabase و weather-etl تعمل بنجاح
   ```

### الخيار الثاني: التشغيل اليدوي المحلي (Python Virtual Environment)

لتطوير أو تجربة كود البايثون محلياً بدون دوكر:

```bash
cd api
python3 -m venv venv
source venv/bin/activate  # في ويندوز: venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```

---

## 7. دليل وصول فريق الداشبورد والتحليل | BI & Analytics Team Access Guide

لضمان أمان السيرفر بنسبة 100%، **يمنع تماماً** مشاركة باسورد الـ Root أو حساب الـ Superuser مع أعضاء الفريق. بدلاً من ذلك، يتم إعطاؤهم بيانات حساب القراءة فقط (**`team_view`**) أو روابط الويب:

### 📊 لمحللي ذكاء الأعمال (Metabase / PowerBI / Tableau / Excel)

- **الطريقة الأولى: لوحة Metabase التفاعلية على المتصفح (لا تحتاج أي تثبيت)**
  - افتح المتصفح على الرابط: `http://<VPS_PUBLIC_IP>:3000`
  - سجل دخول بالإيميل والباسورد الذي أنشأه مدير النظام في إعدادات Metabase.
  - اضغط **`جديد` ➔ `لوحة معلومات` / `سؤال`** وابدأ رسم المخططات بالماوس (Drag & Drop) بأمان تام.

- **الطريقة الثانية: الاتصال المباشر بقاعدة البيانات (لـ PowerBI أو Excel أو Streamlit)**
  - استخدم بيانات حساب القراءة فقط (RBAC Read-Only Credentials):
    - **Host:** `<VPS_PUBLIC_IP>` (مثلاً `72.62.92.93`)
    - **Port:** `32770`
    - **Database Name:** `project`
    - **Username:** `team_view`
    - **Password:** `team_view`

### 🐍 لمحللي البيانات وأكواد التقارير (Python / Jupyter / Pandas / SQL)

يمكن لمحلل البيانات الاتصال بقاعدة البيانات مباشرة باستخدام حساب `team_view` وسحب البيانات في ثواني وتحويلها إلى Pandas DataFrame لإجراء التحليل الاستكشافي (EDA) أو إعداد تقارير دورية:

```python
import pandas as pd
from sqlalchemy import create_engine

# الاتصال بقاعدة البيانات باستخدام حساب القراءة فقط (team_view)
DATABASE_URI = "postgresql+psycopg2://team_view:team_view@72.62.92.93:32770/project"
engine = create_engine(DATABASE_URI)

# سحب البيانات لاستكشافها وعمل التقارير التحليلية
query = "SELECT city, governorate, temperature, humidity, wind_speed, ingestion_time FROM weather_readings;"
df = pd.read_sql(query, engine)

print(f"✅ تم سحب {len(df)} سجل طقس بنجاح للتحليل الاستكشافي!")
print(df.head())
```

---

## 8. الخطوات المستقبلية | Future Roadmap

1. **تطوير لوحات العرض والخرائط الحرارية (Advanced BI Dashboards & Geo-Mapping):**
   - تصميم لوحات تفاعلية مخصصة في Metabase و PowerBI تحتوي على خرائط حرارية (Heatmaps) لمقارنة محافظات الوجه البحري بالصعيد.
   - تضمين المخططات التفاعلية (`<iframe>`) مباشرة داخل مواقع الويب وتطبيقات التيم.
2. **نظام الإنذارات الجوية المتقدم (Automated Weather Alerts & Thresholds):**
   - تطوير مسار n8n وبوت التليجرام لإرسال تنبيهات تحذيرية مخصصة عندما تتخطى درجات الحرارة أو الرطوبة معدلات خطرة في محافظات معينة.
3. **التكامل والمستمر (CI/CD Pipeline):**
   - إعداد GitHub Actions لتشغيل الفحص التلقائي وأختبارات الـ Pydantic فوراً عند رفع أي تعديلات برمجية على الريبوزيتوري.

---

### 🎓 مشروع تخرج مبادرة رواد مصر الرقمية (DEPI)

**مسار هندسة البيانات (Microsoft Data Engineer Track) | وزارة الاتصالات وتكنولوجيا المعلومات (MCIT)**
_تطبيق عملي متكامل يجمع بين استخراج البيانات، هندسة قواعد البيانات، البنية التحتية السحابية، الأتمتة، وذكاء الأعمال._
