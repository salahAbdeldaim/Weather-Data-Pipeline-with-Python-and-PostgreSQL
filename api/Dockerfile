# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for psycopg2 and database connections
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Ensure Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Default command to run the ETL pipeline
CMD ["python", "main.py"]
