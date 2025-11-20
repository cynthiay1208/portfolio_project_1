# Sales Reporting Data Pipeline — Architecture Blueprint (Phase 2.1)

## 1. Naming Standards

### 1.1 Python File Naming

All Python scripts follow snake_case and follow the format:

verb_noun.py

Examples:

ingest_dn.py

clean_bo.py

merge_all.py

load_fact_tables.py

file_utils.py

config_reader.py

This improves readability and makes imports consistent.

### 1.2 SQL Table Naming

SQL tables follow lowercase snake_case and use:

dim_ prefix for dimensions

fact_ prefix for facts

Tables used in this project:

dim_product

dim_customer

dim_date

fact_dn

fact_bo

fact_psi

fact_soh

fact_forecast

This aligns with star-schema best practices for Power BI.

## 2. Folder Structure Standards

This project follows a layered data pipeline architecture:

Bronze Layer — Raw Data
data_raw/

Stores raw Excel files exactly as received (no changes).

Silver Layer — Cleaned Data
data_clean/

Stores cleaned, validated, standardized datasets produced by Python transformations.

Gold Layer — Database
db/

Stores the SQLite database (sales_reporting.db) used for Power BI.

Source Code
src/
    ingestion/
    transformations/
    load/
    utils/

ingestion → reading raw files

transformations → cleaning & merging

load → loading into SQL

utils → reusable helper functions

Configuration Files
config/
    connections.yaml
    table_schema.yaml
    mappings/

paths, schema, and cleaning rules live here

makes the whole pipeline configurable

Documentation
docs/

Architecture diagrams, planning notes, flowcharts.

Notebooks
notebooks/

Exploratory Python work before moving into production code.

SQL Scripts
sql/

Manual SQL queries, DDL scripts, fact/dim logic.

Tests
tests/

Unit tests for pipeline components (added later).

## 3. Architecture Diagram (ASCII)

Below is a high-level overview of the data pipeline using a simple text-based ASCII diagram:

                ┌────────────────────────────────────────────┐
                │              DATA SOURCES                  │
                └────────────────────────────────────────────┘
   Daily DN (Excel)
   Daily BO (Excel)
   PSI (Excel)
   SOH (Excel)
   Forecast Consensus (Excel)
   Master Data (Excel)

                           │
                           ▼
          ┌─────────────────────────────────────────────┐
          │           Python Ingestion Layer            │
          └─────────────────────────────────────────────┘
    /src/ingestion/
       - ingest_dn.py
       - ingest_bo.py
       - ingest_psi.py
       - ingest_soh.py
       - ingest_forecast.py
       - ingest_masterdata.py

                           │
                           ▼
          ┌─────────────────────────────────────────────┐
          │       Local Data Lake (Bronze Layer)        │
          └─────────────────────────────────────────────┘
    /data_raw/

                           │
                           ▼
          ┌─────────────────────────────────────────────┐
          │        Transformation Layer (Silver)        │
          └─────────────────────────────────────────────┘
    /data_clean/
    /src/transformations/

                           │
                           ▼
          ┌─────────────────────────────────────────────┐
          │             SQL Database (Gold)             │
          └─────────────────────────────────────────────┘
    /db/sales_reporting.db

                           │
                           ▼
          ┌─────────────────────────────────────────────┐
          │           Power BI Consumption              │
          └─────────────────────────────────────────────┘

## 4. Architecture Diagram (Mermaid)

flowchart TD

    subgraph Sources[Data Sources]
        DN[Daily DN (Excel)]
        BO[Daily BO (Excel)]
        PSI[PSI (Excel)]
        SOH[SOH (Excel)]
        FC[Forecast Consensus (Excel)]
        MD[Master Data (Excel)]
    end

    subgraph Ingestion[Python Ingestion Layer (/src/ingestion)]
        IDN[ingest_dn.py]
        IBO[ingest_bo.py]
        IPSI[ingest_psi.py]
        ISOH[ingest_soh.py]
        IFC[ingest_forecast.py]
        IMD[ingest_masterdata.py]
    end

    subgraph RawData[Bronze Layer (/data_raw)]
    end

    subgraph Transform[Silver Layer (/data_clean + /src/transformations)]
    end

    subgraph SQLDB[Gold Layer (/db)]
        DB[(SQLite Database)]
    end

    subgraph PowerBI[Power BI Consumption]
    end

    Sources --> Ingestion
    Ingestion --> RawData
    RawData --> Transform
    Transform --> SQLDB
    SQLDB --> PowerBI

## 5. Database ERD (ASCII)

                      ┌──────────────────────┐
                      │     dim_product      │
                      ├──────────────────────┤
                      │ product_id (PK)      │
                      │ model                │
                      │ category             │
                      │ segment              │
                      │ size                 │
                      │ brand                │
                      │ status               │
                      └───────────┬──────────┘
                                  │
                                  │
                                  │ FK
                                  │
        ┌─────────────────────────▼─────────────────────────┐
        │                      fact_dn                      │
        ├───────────────────────────────────────────────────┤
        │ dn_id (PK)                                       │
        │ product_id (FK)                                  │
        │ customer_id (FK)                                 │
        │ order_date (FK)                                  │
        │ allocated_qty                                     │
        └──────────────┬───────────────┬────────────────────┘
                       │               │
                       │               │
                       │               │
                       │               │
           ┌───────────▼──────┐   ┌────▼──────────────┐
           │   dim_customer   │   │     dim_date       │
           ├──────────────────┤   ├────────────────────┤
           │ customer_id (PK) │   │ date (PK)          │
           │ customer_name    │   │ year               │
           │ channel          │   │ month              │
           │ region           │   │ week               │
           └──────────────────┘   │ weekday            │
                                  │ month_year         │
                                  └────────────────────┘


## 6. Database ERD (Mermaid)

erDiagram

    dim_product {
        int product_id PK
        string model
        string category
        string segment
        string size
        string brand
        string status
    }

    dim_customer {
        int customer_id PK
        string customer_name
        string channel
        string region
    }

    dim_date {
        date date PK
        int year
        int month
        int week
        string month_year
        string weekday
    }

    fact_dn {
        int dn_id PK
        int product_id FK
        int customer_id FK
        date order_date FK
        int allocated_qty
    }

    fact_bo {
        int bo_id PK
        int product_id FK
        int customer_id FK
        date snapshot_date FK
        int backorder_qty
    }

    fact_psi {
        int psi_id PK
        int product_id FK
        date snapshot_date FK
        int opening_stock
    }

    fact_soh {
        int soh_id PK
        int product_id FK
        date snapshot_date FK
        int stock_on_hand
    }

    fact_forecast {
        int forecast_id PK
        int product_id FK
        string forecast_month
        int forecast_qty
    }

    %% Relationships
    fact_dn }o--|| dim_product : "product_id"
    fact_dn }o--|| dim_customer : "customer_id"
    fact_dn }o--|| dim_date : "order_date"

    fact_bo }o--|| dim_product : "product_id"
    fact_bo }o--|| dim_customer : "customer_id"
    fact_bo }o--|| dim_date : "snapshot_date"

    fact_psi }o--|| dim_product : "product_id"
    fact_psi }o--|| dim_date : "snapshot_date"

    fact_soh }o--|| dim_product : "product_id"
    fact_soh }o--|| dim_date : "snapshot_date"

    fact_forecast }o--|| dim_product : "product_id"

## 7. Data Dictionary (Template)

Below is the initial data dictionary template for all fact and dimension tables.

This will be updated during Phase 3 after data profiling and SQL modeling.

---

### 📘 dim_product

| Column       | Type    | Example     | Description                     |
|--------------|---------|-------------|---------------------------------|
| product_id   | int PK  | 101         | Unique product identifier       |
| model        | string  | "55A7G"     | Model name                      |
| category     | string  | "TV"        | Product category                |
| segment      | string  | "ULED"      | Marketing segment               |
| size         | string  | "55"        | Panel size                      |
| brand        | string  | "Hisense"   | Brand                           |
| status       | string  | "Active"    | Product status                  |

---

### 📘 dim_customer

| Column        | Type    | Example            | Description                  |
|---------------|---------|--------------------|------------------------------|
| customer_id   | int PK  | 2001               | Unique customer identifier   |
| customer_name | string  | "Harvey Norman"    | Name of retailer             |
| channel       | string  | "Retail"           | Channel type                 |
| region        | string  | "AU/NZ"            | Market region                |

---

### 📘 dim_date

| Column      | Type   | Example      | Description                    |
|-------------|--------|--------------|--------------------------------|
| date        | date PK| 2024-07-15   | Actual calendar date           |
| year        | int    | 2024         | Calendar year                  |
| month       | int    | 7            | Calendar month                 |
| week        | int    | 29           | Calendar week                  |
| weekday     | string | "Monday"     | Day of week                    |
| month_year  | string | "Jul-2024"   | Month label                    |

---

### 📗 fact_dn (Daily Allocated Orders)

| Column        | Type      | Example       | Description                           |
|---------------|-----------|---------------|---------------------------------------|
| dn_id         | int PK    | 1             | Unique DN record identifier           |
| product_id    | int FK    | 101           | Product reference                     |
| customer_id   | int FK    | 2001          | Customer reference                    |
| order_date    | date FK   | 2024-07-14    | Order date                            |
| allocated_qty | int       | 120           | Allocated quantity                    |

---

### 📗 fact_bo (Backorders)

| Column        | Type      | Example       | Description                            |
|---------------|-----------|----------------|----------------------------------------|
| bo_id         | int PK    | 1             | Unique BO record identifier            |
| product_id    | int FK    | 101           | Product reference                      |
| customer_id   | int FK    | 2001          | Customer reference                     |
| snapshot_date | date FK   | 2024-07-14     | Snapshot date                          |
| backorder_qty | int       | 35            | Backorder quantity                     |

---

### 📗 fact_psi (Opening Stock / PSI)

| Column        | Type      | Example       | Description                            |
|---------------|-----------|----------------|----------------------------------------|
| psi_id        | int PK    | 1             | Unique PSI record identifier           |
| product_id    | int FK    | 101           | Product reference                      |
| snapshot_date | date FK   | 2024-07-01     | Stock as of date                       |
| opening_stock | int       | 800            | Opening stock quantity                 |

---

### 📗 fact_soh (Stock on Hand)

| Column        | Type      | Example       | Description                            |
|---------------|-----------|----------------|----------------------------------------|
| soh_id        | int PK    | 1             | Unique SOH record identifier           |
| product_id    | int FK    | 101           | Product reference                      |
| snapshot_date | date FK   | 2024-07-14     | Snapshot date                          |
| stock_on_hand | int       | 750            | Stock on hand quantity                 |

---

### 📗 fact_forecast (KAM Forecast)

| Column         | Type    | Example      | Description                          |
|----------------|---------|--------------|--------------------------------------|
| forecast_id    | int PK  | 1            | Unique forecast entry                |
| product_id     | int FK  | 101          | Product reference                    |
| forecast_month | string  | "2024-08"     | Forecast month                       |
| forecast_qty   | int     | 220          | Forecasted quantity                  |

---

*(Note: This dictionary will be updated after data cleaning and actual schema implementation.)*
