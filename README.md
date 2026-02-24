![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![dbt](https://img.shields.io/badge/dbt-Analytics-orange)
![Snowflake](https://img.shields.io/badge/Warehouse-Snowflake-blue)
![Airflow](https://img.shields.io/badge/Orchestration-Airflow-red)
![Kafka](https://img.shields.io/badge/Streaming-Kafka-black)
![Docker](https://img.shields.io/badge/Container-Docker-blue)

---

# 📈 Real-Time Stock Analytics Platform

## 🚀 Project Overview
This project implements an end-to-end real-time data engineering platform built using Modern Data Stack principles.

The pipeline captures live stock market data, streams events in real time, orchestrates ingestion workflows, transforms datasets using analytics engineering practices, and delivers analytics-ready insights for visualization. The goal was to simulate a production-grade data platform rather than a standalone ETL script.

---

## 🧱 Architecture

Stock Market API  
↓  
Kafka Streaming Layer  
↓  
MinIO Data Lake (Bronze Layer)  
↓  
Airflow Orchestration  
↓  
Snowflake Cloud Warehouse  
↓  
dbt Transformations (Bronze → Silver → Gold)  
↓  
Power BI Dashboard  

---

## ⚡ Tech Stack
| Layer | Technology | Purpose |
|------|------------|---------|
| Streaming | Apache Kafka | Real-time ingestion |
| Storage | MinIO | S3-compatible data lake |
| Orchestration | Apache Airflow | Workflow automation |
| Warehouse | Snowflake | Analytical storage |
| Transformation | dbt | Data modeling |
| Processing | Python | API & ingestion |
| Infrastructure | Docker | Containerized services |
| Visualization | Power BI | Analytics dashboards |

---

## 🔄 Pipeline Workflow

### 1️⃣ Live Data Producer
- Python producer fetches stock data from Finnhub API.
- Streams JSON events into Kafka topics.

### 2️⃣ Streaming Ingestion
- Kafka consumer captures events.
- Stores raw data into MinIO object storage.

### 3️⃣ Orchestration Layer
Airflow DAG automates:
- Detection of new files
- Loading data into Snowflake
- Scheduled execution every minute

### 4️⃣ Data Warehouse Modeling
Snowflake organizes data using Medallion Architecture:
- Bronze → Raw ingestion
- Silver → Cleaned datasets
- Gold → Business analytics tables

### 5️⃣ Analytics Engineering (dbt)
dbt handles:
- Data normalization
- KPI modeling
- Aggregations
- Analytical views

### 6️⃣ Visualization
Power BI connects to Snowflake Gold models using DirectQuery.

Dashboards include:
- Candlestick charts
- KPI metrics
- Market trend visualization
- Performance analytics

---

## 📂 Repository Structure

real-time-stocks-modern-data-stack/
├── producer/        # Kafka producer
├── consumer/        # Kafka → MinIO ingestion
├── dags/            # Airflow pipelines
├── dbt_stocks/      # dbt models
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## 🧠 Engineering Concepts Demonstrated
- Real-time streaming pipelines
- Data Lake + Warehouse integration
- Workflow orchestration
- Medallion architecture
- ELT pipelines
- Analytics engineering
- Containerized infrastructure
- Cloud warehouse analytics

---

## 📊 Sample Dashboard

<img width="1164" height="656" alt="image" src="https://github.com/user-attachments/assets/1e5ff150-f71c-466f-b45b-f0f6320c3315" />

##  Future Improvements
- CI/CD pipeline
- Terraform Infrastructure as Code
- Cloud deployment (AWS/Azure)
- Data quality monitoring
- Streaming analytics with Spark

##  Author
Sirisha  
Data Engineering | Analytics Engineering | Modern Data Stack
