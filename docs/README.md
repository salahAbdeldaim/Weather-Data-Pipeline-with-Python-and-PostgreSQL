# 🌤️ Egypt Weather Data Engineering & BI Platform 🇪🇬

### Production-Grade End-to-End Data Pipeline, DevOps Infrastructure & Business Intelligence

**🎓 Graduation Project — Digital Egypt Pioneers Initiative (DEPI)**
\*Ministry of Communications and Information Technology (MCIT), Egypt — **Microsoft Data Engineer Track\***

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED.svg?logo=docker&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Workflow_Automation-EA4B71.svg?logo=n8n&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-BI_Dashboard-509EE3.svg?logo=metabase&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Alert_Bot-2CA5E0.svg?logo=telegram&logoColor=white)

---

## 📑 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Team Structure & Roles](#2-team-structure--roles)
3. [System Architecture & Data Flow](#3-system-architecture--data-flow)
4. [Technology Stack](#4-technology-stack)
5. [Detailed Engineering Stages](#5-detailed-engineering-stages)
   - [Stage 1: Extraction & Strict Validation (Pydantic & Pandas)](#stage-1-extraction--strict-validation-pydantic--pandas)
   - [Stage 2: Database Architecture & Idempotent Upsert](#stage-2-database-architecture--idempotent-upsert)
   - [Stage 3: Cloud DevOps & Containerization (Docker)](#stage-3-cloud-devops--containerization-docker)
   - [Stage 4: DataOps Orchestration & Telegram Alerting (n8n)](#stage-4-dataops-orchestration--telegram-alerting-n8n)
   - [Stage 5: Business Intelligence & RBAC Data Governance](#stage-5-business-intelligence--rbac-data-governance)
6. [Quick Start Guide](#6-quick-start-guide)
7. [BI & Analytics Team Access Guide](#7-bi--analytics-team-access-guide)
8. [Future Roadmap](#8-future-roadmap)

---

## 1. Executive Summary

The **Egypt Weather Data Engineering & BI Platform** is an end-to-end, automated, production-grade data ecosystem developed as a capstone graduation project for the **Digital Egypt Pioneers Initiative (DEPI)** under the **Ministry of Communications and Information Technology (MCIT)** in the **Microsoft Data Engineer** track.

Designed to extract, validate, store, orchestrate, and visualize real-time atmospheric telemetry across **71 Egyptian cities and governorates**, the platform eliminates manual intervention by running autonomously on a Cloud VPS. Built with modern **DataOps** and **DevOps** industry standards, it guarantees high data purity through strict schema validation, prevents duplicate records via idempotent database transactions, provides real-time team alerting via Telegram, and implements strict **Role-Based Access Control (RBAC)** to securely empower Business Intelligence (BI) developers and Data Analysts.

---

## 2. Team Structure & Roles

This project collaboratively simulates a professional enterprise data engineering team, covering five core specialized domains within the Microsoft Data Engineer track:

| Role                                             | Responsibility & Deliverables                                                                                                                                                   | Primary Technologies                          |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------- |
| 🐍 **1. Data Extraction & Quality Engineer**     | Built the API ingestion engine for 71 Egyptian cities (`cities.json`). Designed strict data quality guardrails and type checking to reject corrupted telemetry before storage.  | Python, Pandas, Pydantic, Requests            |
| 🐘 **2. Database Architect & Load Engineer**     | Designed the relational PostgreSQL database schema (`weather_readings`). Implemented idempotent transactional loading (`ON CONFLICT DO UPDATE`) to prevent duplicate rows.      | PostgreSQL, SQL, psycopg2, SQLAlchemy         |
| 🐳 **3. DevOps & Cloud Infrastructure Engineer** | Containerized the entire stack using Docker & Docker Compose. Deployed and configured the Linux Cloud VPS (Hostinger), network bridges, and firewall security rules.            | Docker, Docker Compose, Linux, UFW/Firewall   |
| ⚡ **4. DataOps & Automation Engineer**          | Built autonomous daily cron orchestration using cloud n8n via SSH. Developed a Telegram Bot (`@wether_app_bot`) for instant team notifications on success or pipeline failures. | n8n Workflow, Telegram Bot API, SSH/Bash      |
| 📊 **5. BI Developer & Data Governance Lead**    | Deployed Metabase BI platform, configured interactive X-Ray visualizations, and established RBAC security by provisioning Read-Only database roles (`team_view`).               | Metabase BI, PostgreSQL RBAC, Data Governance |

---

## 3. System Architecture & Data Flow

The platform operates as a multi-layered pipeline ensuring data isolation, fault tolerance, and security:

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

### 3.1 Repository & Folder Structure (`Clean Modular Architecture`)

To ensure clean separation of concerns across our multi-role engineering team (Data Extraction, Database Architecture, DevOps/Docker, and BI), the project structure is organized into dedicated domain folders:

```text
depi_project/
├── 📁 api/                   # 🐍 Python ETL Extraction Layer (Open-Meteo API & Pydantic Validation)
│   ├── main.py               # Main pipeline execution entrypoint
│   ├── extractor.py          # API fetching and Pandas data transformation
│   ├── loader.py             # Idempotent PostgreSQL loading engine (Upsert logic)
│   ├── cities.json           # Egyptian cities coordinate catalog (71 cities)
│   └── Dockerfile            # Python container build recipe
│
├── 📁 database/              # 🐘 Database Architecture & SQL Layer
│   ├── schema.sql            # PostgreSQL DDL table definitions, constraints, and indexes
│   ├── queries.sql           # Verification & analytical SQL queries for local/team testing
│   └── README.md             # Connection guide (how to connect via DBeaver, VS Code, Azure Data Studio)
│
├── 📁 docker/                # 🐳 DevOps & Containerization Layer
│   ├── docker-compose.yml    # Modular Docker Compose configuration
│   ├── start_services.bat    # One-click batch script to launch all Docker containers (Windows)
│   ├── stop_services.bat     # One-click batch script to safely stop all containers
│   ├── run_pipeline_now.bat  # Instant ETL trigger script for live demos & testing
│   └── README.md             # Docker management and container networking documentation
│
├── 📁 n8n/                   # ⚡ DataOps & Workflow Automation Layer
│   ├── depi.json             # n8n exported workflow with SSH triggers & Telegram alerts
│   └── README.md             # Guide on importing & configuring n8n automation
│
├── 📁 docs/                  # 📚 Project Documentation & Guides
│   ├── README.md             # Comprehensive English technical documentation
│   ├── README_AR.md          # Comprehensive Arabic technical documentation
│   ├── SERVER_UPDATE_GUIDE.md # Production cloud VPS deployment & update procedures
│   └── FUTURE_ENHANCEMENTS_ROADMAP.md # Future roadmap and architecture enhancements
│
├── 📄 README.md              # Root Navigation Landing Page (English)
└── 📄 README_AR.md           # Root Navigation Landing Page (Arabic)
```

---

## 4. Technology Stack

- **Core Programming:** Python 3.11+
- **Data Manipulation & Cleaning:** Pandas, NumPy
- **Data Quality & Schema Validation:** Pydantic v2
- **Database & Storage:** PostgreSQL 15 (Alpine), psycopg2-binary, SQLAlchemy
- **Containerization & Orchestration:** Docker, Docker Compose
- **Workflow Automation:** n8n (Node-based workflow automation)
- **Alerting & Notifications:** Telegram Bot API
- **Business Intelligence & Analytics:** Metabase BI
- **Cloud Infrastructure:** Hostinger Linux Cloud VPS (Ubuntu), UFW Firewall

---

## 5. Detailed Engineering Stages

### Stage 1: Extraction & Strict Validation (Pydantic & Pandas)

- **Objective:** Extract live atmospheric telemetry for 71 Egyptian cities/governorates (e.g., Cairo, Alexandria, Aswan, Siwa, Saint Catherine, Hurghada) from the Open-Meteo API without exceeding rate limits or accepting corrupt payloads.
- **Implementation:**
  - `extractor.py` reads city coordinates from `cities.json`.
  - Converts JSON responses into structured Pandas DataFrames.
  - Passes each record through a **Pydantic Validation Schema** ensuring:
    - Temperature (`temperature_2m`) is strictly within realistic atmospheric limits ($-50^\circ\text{C}$ to $+60^\circ\text{C}$).
    - Relative humidity (`relative_humidity_2m`) is between $0\%$ and $100\%$.
    - Timestamps are properly parsed into ISO-8601 UTC format.
  - Any record violating these guardrails is automatically logged and rejected, preventing database poisoning.

### Stage 2: Database Architecture & Idempotent Upsert

- **Objective:** Store telemetry in a robust relational database while ensuring **Idempotency** (running the pipeline 100 times produces the exact same clean database state without duplicate rows).
- **Implementation:**
  - Deployed PostgreSQL 15 with persistent volume storage (`postgres_data`).
  - Created table `weather_readings` with a composite unique constraint: `UNIQUE(city, ingestion_time)`.
  - Implemented transactional PostgreSQL Upsert logic in `loader.py`:
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

### Stage 3: Cloud DevOps & Containerization (Docker)

- **Objective:** Eliminate "it works on my machine" issues and ensure seamless deployment across any developer laptop or cloud server.
- **Implementation:**
  - Built a custom lightweight `Dockerfile` for the Python ETL application.
  - Orchestrated the entire multi-container ecosystem via `docker-compose.yml`, defining network bridges, container health checks (`pg_isready`), and automatic restart policies (`restart: always`).
  - Configured Hostinger Cloud VPS firewall rules to protect internal database ports while exposing web interfaces securely.

### Stage 4: DataOps Orchestration & Telegram Alerting (n8n)

- **Objective:** Automate daily pipeline execution and establish real-time observability for the engineering team.
- **Implementation:**
  - Designed an autonomous workflow in **n8n** (`n8n_workflow.json`).
  - Uses an SSH Node to connect to the cloud server and execute the Dockerized ETL pipeline daily at 00:00 UTC.
  - Integrated a **Telegram Alerting Bot** (`@wether_app_bot`):
    - **Success Notification:** Transmits exact execution timestamps and the count of inserted/updated records.
    - **Failure Notification:** Instantly triggers an error alert with stderr stack traces if API timeouts or database connection drops occur.

### Stage 5: Business Intelligence & RBAC Data Governance

- **Objective:** Provide visual analytics to stakeholders while strictly adhering to the **Principle of Least Privilege (RBAC)**.
- **Implementation:**
  - Deployed **Metabase BI** as an isolated container on port `3000`.
  - Configured automatic **X-Ray analytics** to generate distribution charts for temperature, wind speeds, and regional humidity comparisons across Egypt.
  - **Data Governance & Security:** To protect the server and prevent accidental schema modification or data deletions by analysts or reporting scripts, provisioned a dedicated **Read-Only Database Role**:
    ```sql
    CREATE USER team_view WITH PASSWORD 'team_view';
    GRANT CONNECT ON DATABASE project TO team_view;
    GRANT USAGE ON SCHEMA public TO team_view;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO team_view;
    ```

---

## 6. Quick Start Guide

### Option A: Complete Docker Compose Deployment (Recommended)

To launch the entire platform (PostgreSQL + Python ETL + Metabase BI) on any machine:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/depi_project.git
   cd depi_project
   ```

2. **Configure Environment Variables:**

   ```bash
   cp .env.example .env
   cp api/.env.example api/.env
   # Edit .env files with your desired credentials
   ```

3. **Launch the Stack:**

   ```bash
   docker-compose up -d --build
   ```

4. **Verify Container Health:**
   ```bash
   docker ps
   # You should see weather_postgres, weather_metabase, and weather-etl running
   ```

### Option B: Local Manual Execution (Python Virtual Environment)

If developing or testing Python ETL scripts locally without Docker:

```bash
cd api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```

---

## 7. BI & Analytics Team Access Guide

To ensure absolute server security, **NEVER** share root SSH credentials or superuser database passwords with team members. Instead, provide them with the dedicated **Read-Only credentials** or Web UI links:

### 📊 For BI Developers & Data Analysts (Metabase Web UI / PowerBI / Tableau / Excel)

- **Option 1: Metabase Interactive Web Dashboard (No Setup Required)**
  - Open Browser: `http://<VPS_PUBLIC_IP>:3000`
  - Login with the web account credentials created by the Admin in Metabase Settings.
  - Click **`New` ➔ `Dashboard` / `Question`** to build drag-and-drop charts safely.

- **Option 2: Direct Database Connection (For PowerBI / Tableau / Excel / Streamlit)**
  - Use the following **Read-Only RBAC Credentials**:
    - **Host:** `<VPS_PUBLIC_IP>` (e.g., `72.62.92.93`)
    - **Port:** `32770`
    - **Database Name:** `project`
    - **Username:** `team_view`
    - **Password:** `team_view`

### 🐍 For Python Data Analysts & Reporting Scripts (Jupyter / Pandas / SQL)

Data analysts can connect directly to PostgreSQL using the `team_view` read-only role to load clean atmospheric telemetry into Pandas DataFrames for exploratory data analysis (EDA) or automated reporting:

```python
import pandas as pd
from sqlalchemy import create_engine

# Connect using Read-Only RBAC Role (team_view)
DATABASE_URI = "postgresql+psycopg2://team_view:team_view@72.62.92.93:32770/project"
engine = create_engine(DATABASE_URI)

# Fetch atmospheric telemetry for data exploration & analysis
query = "SELECT city, governorate, temperature, humidity, wind_speed, ingestion_time FROM weather_readings;"
df = pd.read_sql(query, engine)

print(f"✅ Successfully loaded {len(df)} atmospheric telemetry records for Data Analysis!")
print(df.head())
```

---

## 8. Future Roadmap

1. **Advanced BI Dashboards & Geo-Mapping:**
   - Design custom interactive Metabase dashboards with geo-heatmaps comparing coastal vs. upper Egypt governorates.
   - Embed interactive `<iframe>` charts directly into public-facing team web applications or presentations.
2. **Automated Weather Alerts & Thresholds:**
   - Enhance the n8n orchestration workflow and Telegram bot to trigger specialized warning alerts whenever extreme heatwaves or abnormal humidity thresholds are exceeded in specific governorates.
3. **CI/CD & Automated Testing:**
   - Integrate GitHub Actions to automatically execute Pydantic unit tests, schema validation checks, and Python code linting whenever pull requests are submitted.

---

### 🎓 Digital Egypt Pioneers Initiative (DEPI) — Graduation Project

**Microsoft Data Engineer Track | Ministry of Communications and Information Technology (MCIT), Egypt**
_Demonstrating production-grade mastery across Data Extraction, Database Architecture, Cloud DevOps, Orchestration, and Business Intelligence._
