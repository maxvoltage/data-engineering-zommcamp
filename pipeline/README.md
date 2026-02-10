# NYC Taxi Data Pipeline (DE Zoomcamp Module 1)

This project explores a containerized data ingestion pipeline for the NYC Taxi dataset, part of the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp).

## 🚀 Quick Start

### 1. Prerequisites
- [Docker](https://www.docker.com/) & Docker Compose
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### 2. Environment Setup
Create your local environment file:
```bash
cp .env.example .env
```
*Note: Default credentials are set to `root/root` and `admin@admin.com/root`.*

### 3. Spin up the Infrastructure
Start PostgreSQL and PgAdmin:
```bash
docker-compose up -d
```

## 📥 Data Ingestion

### Option A: Local Execution (Recommended for Debugging)
Run the scripts directly using `uv` (will automatically load `.env` variables):
```bash
# Ingest Trip Data
uv run --env-file .env python ingest_data.py

# Ingest Zone Data
uv run --env-file .env python ingest_zones.py
```

### Option B: Docker Execution
Build and run the ingestion logic inside a container:
```bash
# 1. Build the image
docker build -t taxi_ingest:latest .

# 2. Run Trip Ingestion (Default Entrypoint)
docker run -it --rm --network=pipeline_default taxi_ingest:latest --pg-host=pgdatabase

# 3. Run Zone Ingestion (Override Entrypoint)
docker run -it --rm --network=pipeline_default \
  --entrypoint uv taxi_ingest:latest \
  run python ingest_zones.py --pg-host=pgdatabase
```

## 📊 Exploration
- **PgAdmin:** [http://localhost:8085](http://localhost:8085)
- **PostgreSQL:** `localhost:5432` (Database: `ny_taxi`)

## 🛠 Project Structure
- `ingest_data.py`: Main pipeline for Yellow Taxi trip data (chunked ingestion).
- `ingest_zones.py`: Helper script for Taxi Zone lookup data.
- `Dockerfile`: Multi-stage build for the ingestion environment.
- `docker-compose.yaml`: Orchestration for Postgres & PgAdmin.
- `notebook.ipynb`: Exploratory data analysis.
