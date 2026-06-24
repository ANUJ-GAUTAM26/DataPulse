# DataPulse

DataPulse is an end-to-end YouTube Analytics Data Engineering project that extracts trending video data from multiple countries using the YouTube Data API, processes it through ETL pipelines, and stores it in PostgreSQL for analytics and reporting.

The project demonstrates modern Data Engineering concepts including API ingestion, data transformation, dimensional modeling, database loading, workflow automation, and cloud integration.

---

## Project Objectives

- Extract trending YouTube videos from multiple regions
- Collect channel-level metadata
- Build Bronze and Silver data layers
- Store analytics-ready data in PostgreSQL
- Create reusable ETL pipelines
- Automate workflows using Airflow
- Containerize services with Docker
- Build dashboards using Power BI
- Deploy cloud storage using AWS S3

---

## Architecture

YouTube API
    ↓
Raw JSON (Bronze Layer)
    ↓
Transformation Layer
    ↓
Processed CSV (Silver Layer)
    ↓
PostgreSQL Data Warehouse
    ↓
Power BI Dashboard

---

## Tech Stack

### Programming

- Python

### Data Processing

- Pandas

### Database

- PostgreSQL
- Psycopg2

### APIs

- YouTube Data API v3

### Workflow Orchestration

- Apache Airflow (Upcoming)

### Containerization

- Docker (Upcoming)

### Cloud

- AWS S3 (Upcoming)

### Visualization

- Power BI (Upcoming)

---

## Project Structure

```text
DataPulse/
│
├── extractor/
│   ├── youtube_client.py
│   ├── fetch_videos.py
│   ├── fetch_channels.py
│   ├── transform_raw.py
│   └── transform_channels.py
│
├── loader/
│   ├── db_connection.py
│   ├── load_data.py
│   └── test_connection.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── tests/
│
├── requirements.txt
├── .env
├── README.md
└── .gitignore
```

---

## Data Model

### Dimension Table

#### dim_channel

| Column | Description |
|----------|------------|
| channel_id | Unique channel identifier |
| channel_title | Channel name |
| country | Channel country |
| subscriber_count | Total subscribers |
| video_count | Total uploaded videos |
| total_view_count | Total channel views |

---

### Fact Table

#### fact_video_metrics

| Column | Description |
|----------|------------|
| video_id | Unique video identifier |
| title | Video title |
| channel_id | Channel reference |
| category_id | Video category |
| published_at | Publish timestamp |
| view_count | Total views |
| like_count | Total likes |
| comment_count | Total comments |
| extraction_date | ETL extraction date |

---

## ETL Workflow

### Extract

- Fetch trending videos from multiple regions
- Fetch corresponding channel information

### Transform

- Clean missing values
- Convert numeric fields
- Remove duplicates
- Standardize schema

### Load

- Load channel data into dimension table
- Load video metrics into fact table
- Maintain relational integrity

---

## Dataset Statistics

Current Dataset:

- 500 Raw Video Records
- 349 Unique Channels
- Multi-country Coverage
- Trending Video Analytics

---

## Sample SQL Analysis

### Top 10 Videos by Views

```sql
SELECT
    title,
    view_count
FROM fact_video_metrics
ORDER BY view_count DESC
LIMIT 10;
```

### Top Channels by Subscribers

```sql
SELECT
    channel_title,
    subscriber_count
FROM dim_channel
ORDER BY subscriber_count DESC
LIMIT 10;
```

---

## Future Enhancements

- Docker Containerization
- Apache Airflow DAGs
- AWS S3 Data Lake
- dbt Transformations
- Power BI Dashboards
- CI/CD Pipeline
- Data Quality Testing

---

## Author

Anuj Gautam

Aspiring Data Engineer focused on building production-style data pipelines and analytics solutions.
