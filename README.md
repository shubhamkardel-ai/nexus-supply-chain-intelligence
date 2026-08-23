<div align="center">

📦 NEXUS

Supply Chain Intelligence

AI-powered demand forecasting & inventory decision support

<br>

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=19&duration=2400&pause=700&color=00D4FF&center=true&vCenter=true&width=1000&lines=SUPPLY+CHAIN+INTELLIGENCE+SYSTEM;DEMAND+FORECASTING+ENGINE+ONLINE;INVENTORY+RISK+ANALYSIS+ACTIVE;LEAKAGE-SAFE+FEATURE+ENGINEERING;FASTAPI+SERVICE+READY;TURNING+SALES+DATA+INTO+DECISIONS" />

<br><br>

<img src="https://img.shields.io/badge/SYSTEM-NEXUS-00D4FF?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/FORECASTING-RANDOM%20FOREST-00D4FF?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/API-FASTAPI-00D4FF?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=07111F"/>
<img src="https://img.shields.io/badge/TESTS-18%20PASSED-35D07F?style=for-the-badge&labelColor=07111F"/>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:07111F,30:0B2740,60:006D8F,100:00D4FF&height=140&section=footer" width="100%"/>

</div>

🛰️ SYSTEM BRIEF

NEXUS is a supply-chain intelligence system that combines historical sales data, leakage-safe demand features, machine-learning forecasting, and inventory risk analysis behind a FastAPI service.

It is designed to help supply-chain teams answer four practical questions:

Decision

NEXUS answers

📈 Demand

How much demand should we expect for a product?

⚠️ Risk

Is current inventory high, medium, or low risk?

📦 Reorder

How much inventory should be reordered?

🎯 Confidence

How reliable is the forecast through its prediction range?

🧭 INTELLIGENCE FLOW

flowchart LR
    A["📊 Historical Sales"] --> B["⚙️ Data Loading"]
    B --> C["🧩 Demand Features"]
    C --> D["🌲 Random Forest"]
    D --> E["📈 Demand Prediction"]
    D --> F["📏 Forecast Range"]
    E --> G["📦 Inventory Analysis"]
    F --> G
    G --> H["🚀 FastAPI Response"]

    style A fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style B fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style C fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style D fill:#07111F,stroke:#35D07F,color:#FFFFFF
    style E fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style F fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style G fill:#07111F,stroke:#FFB84D,color:#FFFFFF
    style H fill:#07111F,stroke:#35D07F,color:#FFFFFF

⚙️ CORE CAPABILITIES

📊 Demand Feature Engineering

The feature pipeline creates three groups of demand signals:

Calendar features

day_of_week

day_of_month

month

Business features

revenue_per_unit

units_per_customer

Historical demand features

lag_1

lag_7

rolling_mean_7

rolling_mean_30

Historical features use shifted observations so the current target is not included in its own forecasting features.

📈 Demand Forecasting

The forecasting pipeline:

Loads the sales dataset.

Creates demand features.

Removes rows without the required historical features.

Sorts observations chronologically.

Uses an 80/20 chronological train/test split.

One-hot encodes product_id.

Trains a RandomForestRegressor with 200 trees.

Evaluates the model using MAE and RMSE.

Produces a prediction range from the distribution of individual tree predictions.

📦 Inventory Intelligence

The inventory service evaluates current inventory against predicted demand and returns:

Inventory risk level

Current inventory

Recommended reorder quantity

🌐 FastAPI Service

Method

Endpoint

Purpose

GET

/

Service information

GET

/health

Health check

GET

/inventory/status

Inventory service status

POST

/forecast

Demand forecast + inventory analysis

🧱 ARCHITECTURE

flowchart TB
    A["📊 Historical Sales Data"] --> B["Data Loading Layer"]
    B --> C["Demand Feature Engineering"]

    C --> D["Calendar Features"]
    C --> E["Historical Features"]

    D --> F["Forecast Model"]
    E --> F

    F --> G["🌲 Random Forest"]
    G --> H["Demand Prediction"]
    G --> I["Forecast Range"]

    H --> J["Inventory Analysis"]
    I --> J

    J --> K["FastAPI Response"]

    style A fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style B fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style C fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style D fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style E fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style F fill:#07111F,stroke:#35D07F,color:#FFFFFF
    style G fill:#07111F,stroke:#35D07F,color:#FFFFFF
    style H fill:#00D4FF,stroke:#00D4FF,color:#07111F
    style I fill:#07111F,stroke:#FFB84D,color:#FFFFFF
    style J fill:#07111F,stroke:#FFB84D,color:#FFFFFF
    style K fill:#07111F,stroke:#35D07F,color:#FFFFFF

🧠 MODEL & DATA DESIGN

Forecasting Model

NEXUS currently uses:

Model: RandomForestRegressor

Trees: 200

Split: chronological 80/20 train/test

Metrics: MAE and RMSE

Categorical handling: one-hot encoded product_id

Dataset

The current generated dataset contains:

Property

Value

Rows

7,300

Products

20

Frequency

Daily

Date range

Jan 1, 2025 → Dec 31, 2025

Base columns:

product_id
sale_date
units_sold
revenue
customer_count

🛡️ DATA LEAKAGE PROTECTION

Forecasting systems are highly sensitive to target leakage.

NEXUS protects the forecasting pipeline by ensuring historical demand features are built only from previous observations:

Feature

Meaning

lag_1

Previous observation

lag_7

Observation seven periods earlier

rolling_mean_7

Previous seven observations

rolling_mean_30

Previous thirty observations

The rolling calculations use a shift before calculating the rolling mean.

The project also uses a chronological train/test split, rather than randomly mixing historical and future observations.

📐 CURRENT PERFORMANCE

Current local evaluation:

Training samples : 5360
Testing samples  : 1340

MAE              : approximately 4.6
RMSE             : approximately 6.3

Example model run:

Demand Forecasting Model
------------------------
Training samples: 5360
Testing samples: 1340
MAE: 4.64
RMSE: 6.34

These metrics are based on the current generated dataset and can change when the dataset or feature pipeline changes.

🗂️ PROJECT STRUCTURE

nexus-supply-chain-intelligence/
│
├── app/
│   ├── __init__.py
│   └── forecast_api.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sales.csv
│
├── models/
│   ├── __init__.py
│   ├── inventory.py
│   ├── sales.py
│   └── supplier.py
│
├── services/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── demand_analysis.py
│   ├── demand_features.py
│   ├── forecast_model.py
│   ├── generate_dataset.py
│   ├── inventory_service.py
│   └── sales_service.py
│
├── tests/
│   ├── __init__.py
│   ├── test_demand_features.py
│   ├── test_forecast_api.py
│   ├── test_forecast_model.py
│   └── test_inventory_service.py
│
├── main.py
├── requirements.txt
└── README.md

🧰 TECHNOLOGY STACK

<div align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,pandas,sklearn,git,github,pytest" />

<br><br>

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Uvicorn-Server-499848?style=for-the-badge"/>

</div>

🚀 QUICK START

1. Clone

git clone https://github.com/shubhamkardel-ai/nexus-supply-chain-intelligence.git
cd nexus-supply-chain-intelligence

2. Create the virtual environment

Windows PowerShell

python -m venv .venv311
.\.venv311\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

📊 GENERATE THE DATASET

If the dataset needs to be regenerated:

python -m services.generate_dataset

Expected output:

Dataset generated successfully!
Rows: 7300
Products: 20
Date range: 2025-01-01 → 2025-12-31

🌲 RUN THE FORECASTING MODEL

python -m services.forecast_model

Expected output:

Demand Forecasting Model
------------------------
Training samples: 5360
Testing samples: 1340
MAE: 4.64
RMSE: 6.34

🌐 RUN THE API

uvicorn app.forecast_api:app --reload

Local service:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

🧪 TEST THE SYSTEM

Run the complete test suite:

pytest -v

Current result:

18 passed, 1 warning

Coverage includes:

Demand feature creation

Lag feature correctness

Historical-only rolling features

Forecast data preparation

Model training

Prediction range generation

API endpoints

API validation

Inventory risk classification

Reorder quantity logic

Known warning

The suite currently reports a Starlette deprecation warning related to the httpx integration used by the FastAPI test client.

The warning does not currently cause test failures:

18 passed, 1 warning

This should be addressed during dependency maintenance.

🔌 API EXAMPLE

POST /forecast

Example request:

{
  "product_id": "P001",
  "day_of_week": 2,
  "day_of_month": 15,
  "month": 8,
  "revenue_per_unit": 400,
  "units_per_customer": 1.2,
  "lag_1": 30,
  "lag_7": 28,
  "rolling_mean_7": 29.5,
  "rolling_mean_30": 30.1,
  "current_inventory": 100
}

Example response:

{
  "product_id": "P001",
  "predicted_units_sold": 30.12,
  "forecast_lower": 25.4,
  "forecast_upper": 35.1,
  "forecast_type": "demand_forecast",
  "model": "Random Forest",
  "inventory_risk": "low",
  "current_inventory": 100,
  "recommended_reorder_quantity": 0
}

Actual forecast values depend on the trained model and input data.

🔄 DEVELOPMENT WORKFLOW

flowchart LR
    A["Implement"] --> B["Run Tests"]
    B --> C["Inspect Results"]
    C --> D["Fix / Improve"]
    D --> B
    B --> E["Git Add"]
    E --> F["Git Commit"]
    F --> G["Git Push"]

    style A fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style B fill:#07111F,stroke:#35D07F,color:#FFFFFF
    style C fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style D fill:#07111F,stroke:#FFB84D,color:#FFFFFF
    style E fill:#07111F,stroke:#00D4FF,color:#FFFFFF
    style F fill:#07111F,stroke:#35D07F,color:#FFFFFF
    style G fill:#07111F,stroke:#35D07F,color:#FFFFFF

Git checkpoints are used after meaningful completed stages so the repository remains recoverable and progress is traceable.

✅ CURRENT STATUS

<div align="center">

SYSTEM

STATUS

📊 Sales dataset generation

🟢 Complete

📥 Data loading

🟢 Complete

📈 Demand analysis

🟢 Complete

🛡️ Leakage-safe feature engineering

🟢 Complete

🌲 Random Forest forecasting

🟢 Complete

📏 Forecast prediction range

🟢 Complete

📦 Inventory risk analysis

🟢 Complete

🔄 Reorder quantity recommendation

🟢 Complete

🌐 FastAPI forecasting service

🟢 Complete

✅ API validation

🟢 Complete

🧪 Automated unit/API tests

🟢 Complete

🐙 GitHub repository & checkpoints

🟢 Complete

<br>

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=17&duration=1800&pause=500&color=35D07F&center=true&vCenter=true&width=850&lines=CORE+PIPELINE+OPERATIONAL;FORECASTING+ENGINE+READY;INVENTORY+INTELLIGENCE+READY;API+SERVICE+READY;TEST+SUITE+PASSING" />

</div>

🔭 NEXT DEVELOPMENT OPPORTUNITIES

The current implementation is complete for its present scope. Potential future improvements include:

Model persistence instead of training on API startup

Configurable forecast horizons

Feature importance reporting

Historical forecast-vs-actual visualization

Supplier lead-time modeling

Safety-stock calculations

Automated retraining workflow

Structured API error handling

Docker support

CI/CD with GitHub Actions

Production monitoring and model performance tracking

🧪 TESTING & ENGINEERING QUALITY

NEXUS was developed around a checkpoint-based, test-first workflow.

The current tests validate both the intelligence layer and API layer, including feature correctness, forecasting preparation, model training, prediction ranges, endpoint behavior, validation, inventory classification, and reorder logic.

TEST SUITE
    │
    ├── Feature Engineering
    ├── Forecast Model
    ├── Prediction Range
    ├── API Endpoints
    ├── API Validation
    └── Inventory Logic

            ↓

      18 PASSED

🌐 REPOSITORY

<div align="center">

<a href="https://github.com/shubhamkardel-ai/nexus-supply-chain-intelligence">
<img src="https://img.shields.io/badge/GitHub-NEXUS%20Repository-181717?style=for-the-badge&logo=github&logoColor=white"/>
</a>

</div>

👨‍💻 AUTHOR

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=21&duration=2200&pause=700&color=00D4FF&center=true&vCenter=true&width=850&lines=SHUBHAM+KARDEL;AI%2FML+ENGINEER;PYTHON+DEVELOPER;INTELLIGENT+SYSTEMS+BUILDER" />

<br><br>

<a href="https://github.com/shubhamkardel-ai">
<img src="https://img.shields.io/badge/GitHub-shubhamkardel--ai-181717?style=for-the-badge&logo=github&logoColor=white"/>
</a>

<a href="https://www.linkedin.com/in/shubham-kardel-303356312/">
<img src="https://img.shields.io/badge/LinkedIn-Shubham%20Kardel-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>

<br><br>

Building practical AI systems, one engineering problem at a time.

</div>

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=17&duration=2400&pause=700&color=00D4FF&center=true&vCenter=true&width=900&lines=DATA+%E2%86%92+INTELLIGENCE+%E2%86%92+DECISION;FORECAST+%E2%86%92+RISK+%E2%86%92+ACTION;NEXUS+SUPPLY+CHAIN+INTELLIGENCE;SYSTEM+READY" />

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00D4FF,35:006D8F,65:0B2740,100:07111F&height=130&section=footer" width="100%"/>

</div>
