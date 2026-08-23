🧠 NEXUS Supply Chain Intelligence

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:07111F,25:0B2239,50:123B55,75:00A6A6,100:00E5C7&height=270&section=header&text=NEXUS&fontSize=68&fontColor=FFFFFF&fontAlignY=38&desc=AI-POWERED%20SUPPLY%20CHAIN%20INTELLIGENCE&descAlignY=62&descSize=18&animation=fadeIn" width="100%"/>

<br>

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=19&duration=2200&pause=700&color=00E5C7&center=true&vCenter=true&width=1000&lines=FORECAST+%7C+ANALYZE+%7C+OPTIMIZE;DEMAND+INTELLIGENCE+SYSTEM+ONLINE;LEAKAGE-SAFE+FORECASTING+PIPELINE;INVENTORY+RISK+ANALYSIS+ACTIVE;RANDOM+FOREST+FORECASTING+ENGINE;FASTAPI+DECISION+SUPPORT+SERVICE;SUPPLY+CHAIN+INTELLIGENCE+READY"/>

<br><br>

<img src="https://img.shields.io/badge/PROJECT-NEXUS-00E5C7?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/STATUS-COMPLETE-00D084?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/ML-RANDOM%20FOREST-00A6A6?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/API-FASTAPI-00E5C7?style=for-the-badge&labelColor=07111F"/>

</div>

🧠 What is NEXUS?

NEXUS Supply Chain Intelligence is an AI-powered supply chain decision-support system that transforms historical sales data into demand forecasts and inventory insights.

Instead of looking only at historical sales, NEXUS combines:

📊 Demand Intelligence

📦 Inventory Intelligence

Historical Sales

Inventory Risk

Calendar Features

Reorder Recommendations

Lag Features

Current Inventory

Rolling Demand

Demand-Aware Decisions

Machine Learning

Operational Insights

The platform combines:

Historical Sales + Leakage-Safe Features + Machine Learning + Forecast Ranges + Inventory Analysis + FastAPI

into a single supply-chain intelligence application.

✨ The Intelligence Layer

<div align="center">

<table width="100%" cellspacing="0" cellpadding="20">
<tr>
<td align="center">

📊

OBSERVE

Historical product-level sales data.

</td>
<td align="center">

🧠

UNDERSTAND

Build calendar and historical demand features.

</td>
<td align="center">

🔮

FORECAST

Predict future demand with Random Forest.

</td>
<td align="center">

📦

ASSESS

Evaluate inventory risk and reorder needs.

</td>
<td align="center">

🚀

SERVE

Expose decisions through FastAPI.

</td>
</tr>
</table>

</div>

🎯 Project Vision

The goal of NEXUS is simple:

Turn historical demand into actionable supply-chain decisions.

A traditional forecasting workflow may stop at:

Sales Data → Forecast

NEXUS extends the workflow into:

Sales Data → Feature Intelligence → Forecast → Forecast Range → Inventory Risk → Reorder Decision

This makes the system useful as a foundation for AI-assisted supply-chain planning.

🌌 Platform Overview

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=22&duration=2400&pause=700&color=00E5C7&center=true&vCenter=true&width=950&lines=SUPPLY+CHAIN+INTELLIGENCE+CORE;HISTORICAL+DATA+%E2%86%92+DEMAND+FEATURES;DEMAND+FEATURES+%E2%86%92+ML+FORECAST;FORECAST+%E2%86%92+INVENTORY+INTELLIGENCE;INVENTORY+INTELLIGENCE+%E2%86%92+DECISION+SUPPORT"/>

</div>

flowchart LR

    A["📊 Historical Sales"] --> B["🧩 Feature Engineering"]

    B --> C["🧠 Random Forest"]

    C --> D["🔮 Demand Forecast"]

    D --> E["📈 Forecast Range"]

    E --> F["📦 Inventory Analysis"]

    F --> G["⚠️ Risk Level"]

    F --> H["🔁 Reorder Quantity"]

    G --> I["🚀 FastAPI"]

    H --> I

🔬 Core Features

📊 01 — Demand Feature Engineering

The feature pipeline creates calendar, business, and historical demand features.

Calendar Features

day_of_week

day_of_month

month

Business Features

revenue_per_unit

units_per_customer

Historical Demand Features

lag_1

lag_7

rolling_mean_7

rolling_mean_30

Historical features use shifted observations so the current target is not included in its own forecasting features.

🔮 02 — Demand Forecasting

The forecasting pipeline:

Loads the sales dataset.

Creates demand features.

Removes rows without required historical features.

Sorts observations chronologically.

Uses an 80/20 chronological train/test split.

One-hot encodes product_id.

Trains a RandomForestRegressor with 200 trees.

Evaluates using MAE and RMSE.

Produces a prediction range from individual tree predictions.

Forecasting Flow

flowchart TD

    A["📊 Sales Dataset"] --> B["🧩 Feature Engineering"]
    B --> C["🧹 Remove Invalid Historical Rows"]
    C --> D["📅 Chronological Sorting"]
    D --> E["✂️ 80/20 Time Split"]
    E --> F["🏷️ One-Hot Product Encoding"]
    F --> G["🌲 Random Forest"]
    G --> H["🔮 Demand Prediction"]
    G --> I["📈 Tree Prediction Distribution"]
    I --> J["Forecast Range"]

📦 03 — Inventory Intelligence

The inventory service evaluates current inventory against predicted demand.

It returns:

⚠️ Inventory risk level

📦 Current inventory

🔁 Recommended reorder quantity

Decision Flow

flowchart LR

    A["🔮 Predicted Demand"] --> C["📦 Inventory Analysis"]
    B["📦 Current Inventory"] --> C

    C --> D["⚠️ Risk Classification"]
    C --> E["🔁 Reorder Recommendation"]

    D --> F["🚀 API Response"]
    E --> F

🧬 System Architecture

flowchart TD

    A["📊 Historical Sales Data"] --> B["📥 Data Loading Layer"]

    B --> C["🧩 Demand Feature Engineering"]

    C --> D["📅 Calendar Features"]
    C --> E["📈 Historical Demand Features"]
    C --> F["💼 Business Features"]

    D --> G["🧠 Forecast Model"]
    E --> G
    F --> G

    G --> H["🌲 Random Forest"]

    H --> I["🔮 Demand Prediction"]
    H --> J["📈 Forecast Range"]

    I --> K["📦 Inventory Analysis"]
    J --> K

    K --> L["⚠️ Inventory Risk"]
    K --> M["🔁 Reorder Quantity"]

    L --> N["🚀 FastAPI"]
    M --> N

🔄 End-to-End Intelligence Pipeline

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=17&duration=1800&pause=500&color=00D084&center=true&vCenter=true&width=1000&lines=%5B01%5D+LOAD+SALES+DATA;%5B02%5D+BUILD+HISTORICAL+FEATURES;%5B03%5D+PROTECT+AGAINST+TARGET+LEAKAGE;%5B04%5D+TRAIN+RANDOM+FOREST;%5B05%5D+GENERATE+DEMAND+FORECAST;%5B06%5D+ESTIMATE+FORECAST+RANGE;%5B07%5D+ANALYZE+INVENTORY;%5B08%5D+RETURN+DECISION+SUPPORT"/>

</div>

🛡️ Leakage-Safe Forecasting

Forecasting systems are especially sensitive to target leakage.

NEXUS avoids using the current day's demand when constructing historical demand features.

Feature

Historical Information Used

lag_1

Previous observation

lag_7

Observation seven periods earlier

rolling_mean_7

Previous seven observations

rolling_mean_30

Previous thirty observations

The rolling calculations use a shift before calculating the rolling mean.

The model also uses a chronological train/test split rather than randomly mixing historical and future observations.

Why this matters

flowchart LR

    A["Historical Observations"] --> B["Shift"]
    B --> C["Rolling Features"]
    C --> D["Current Target"]

    E["Current Target"] -.->|"Not used as input"| C

This helps preserve the temporal structure required for realistic forecasting evaluation.

🧩 Modular Project Architecture

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

🧠 Module Intelligence Map

Module

Responsibility

data_loader.py

Load sales data

demand_analysis.py

Analyze demand patterns

demand_features.py

Build forecasting features

forecast_model.py

Train and evaluate the forecasting model

generate_dataset.py

Generate the current sales dataset

inventory_service.py

Inventory risk and reorder analysis

sales_service.py

Sales-related service logic

forecast_api.py

FastAPI forecasting service

models/

Application data models

tests/

Automated unit and API tests

🏗️ Engineering Design

NEXUS separates the major responsibilities of the system into dedicated layers.

flowchart TD

    A["🚀 API Layer"] --> B["⚙️ Service Layer"]

    B --> C["📊 Data Layer"]
    B --> D["🧩 Feature Layer"]
    B --> E["🧠 Forecast Layer"]
    B --> F["📦 Inventory Layer"]

    C --> D
    D --> E
    E --> F

    F --> G["📤 Decision Support Response"]

This separation provides:

Cleaner responsibilities

Easier testing

Reusable forecasting components

Better maintainability

Clear API boundaries

Easier future productionization

🌲 Forecasting Engine

The current model is:

RandomForestRegressor(n_estimators=200)

The model receives:

Calendar features

Business features

Historical demand features

One-hot encoded product_id

and predicts:

Expected units sold

Forecast Range

The system also derives a prediction range from the distribution of individual Random Forest tree predictions.

flowchart LR

    A["Input Features"] --> B["🌲 Tree 1"]
    A --> C["🌲 Tree 2"]
    A --> D["🌲 ..."]
    A --> E["🌲 Tree 200"]

    B --> F["Prediction Distribution"]
    C --> F
    D --> F
    E --> F

    F --> G["🔮 Forecast"]
    F --> H["📈 Forecast Range"]

📊 Model Performance

Current local evaluation on the generated dataset:

Metric

Current Result

Training samples

5,360

Testing samples

1,340

MAE

Approximately 4.6

RMSE

Approximately 6.3

These metrics are based on the current generated dataset and can change when the dataset or feature pipeline changes.

<div align="center">

<img src="https://img.shields.io/badge/TRAIN-5360%20SAMPLES-00E5C7?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/TEST-1340%20SAMPLES-00A6A6?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/MAE-%7E4.6-00D084?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/RMSE-%7E6.3-00D084?style=for-the-badge&labelColor=07111F"/>

</div>

📦 Dataset

The current generated dataset contains:

Property

Value

Rows

7,300

Products

20

Frequency

Daily

Start

January 1, 2025

End

December 31, 2025

Base Columns

product_id
sale_date
units_sold
revenue
customer_count

🌐 FastAPI Intelligence Layer

NEXUS exposes its forecasting and inventory capabilities through FastAPI.

Endpoints

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

🚀 API Request

POST /forecast

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

Response Structure

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

🧪 Testing

Run the complete test suite:

pytest -v

Current test result:

18 passed, 1 warning

Test Coverage

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

⚠️ Known Warning

The test suite currently reports a Starlette deprecation warning related to the httpx integration used by the FastAPI test client.

The warning does not currently cause test failures:

18 passed, 1 warning

This should be addressed during dependency maintenance.

🛠️ Technology Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,sklearn,pandas,numpy,pytest,git,github"/>

<br><br>

<img src="https://img.shields.io/badge/Python-3.11-00E5C7?style=for-the-badge&logo=python&logoColor=white&labelColor=07111F"/>
<img src="https://img.shields.io/badge/FastAPI-API-00A6A6?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=07111F"/>
<img src="https://img.shields.io/badge/Scikit--Learn-ML-00E5C7?style=for-the-badge&logo=scikit-learn&logoColor=white&labelColor=07111F"/>
<img src="https://img.shields.io/badge/Pandas-DATA-00A6A6?style=for-the-badge&logo=pandas&logoColor=white&labelColor=07111F"/>
<img src="https://img.shields.io/badge/NumPy-COMPUTING-00E5C7?style=for-the-badge&logo=numpy&logoColor=white&labelColor=07111F"/>
<img src="https://img.shields.io/badge/Pytest-TESTING-00D084?style=for-the-badge&logo=pytest&logoColor=white&labelColor=07111F"/>
<img src="https://img.shields.io/badge/Uvicorn-SERVER-00A6A6?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/Git-GITHUB-00E5C7?style=for-the-badge&logo=git&logoColor=white&labelColor=07111F"/>

</div>

⚙️ Installation

01 — Clone

git clone https://github.com/shubhamkardel-ai/nexus-supply-chain-intelligence.git
cd nexus-supply-chain-intelligence

02 — Virtual Environment

Windows PowerShell

python -m venv .venv311
.\.venv311\Scripts\Activate.ps1

Install Dependencies

pip install -r requirements.txt

🗃️ Generate the Dataset

If the dataset needs to be regenerated:

python -m services.generate_dataset

Expected output:

Dataset generated successfully!
Rows: 7300
Products: 20
Date range: 2025-01-01 → 2025-12-31

🔮 Run the Forecasting Model

python -m services.forecast_model

Example output:

Demand Forecasting Model
------------------------
Training samples: 5360
Testing samples: 1340
MAE: 4.64
RMSE: 6.34

🚀 Run the API

Start FastAPI:

uvicorn app.forecast_api:app --reload

Local service:

http://127.0.0.1:8000

Interactive documentation:

http://127.0.0.1:8000/docs

🧪 Development Workflow

NEXUS follows a test-first, checkpoint-based development workflow.

flowchart LR

    A["💻 Implement"] --> B["🧪 Run Tests"]
    B --> C["🔍 Inspect"]
    C --> D["🛠️ Fix / Improve"]
    D --> E["🧪 Test Again"]
    E --> F["📦 Commit"]
    F --> G["🚀 Push"]
    G --> A

Git checkpoints are created after meaningful completed stages so the repository remains recoverable and progress stays traceable.

📈 Current System Status

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=17&duration=1700&pause=450&color=00D084&center=true&vCenter=true&width=1000&lines=%5BOK%5D+DATASET+GENERATION;%5BOK%5D+DATA+LOADING;%5BOK%5D+DEMAND+ANALYSIS;%5BOK%5D+FEATURE+ENGINEERING;%5BOK%5D+LEAKAGE+PROTECTION;%5BOK%5D+RANDOM+FOREST+FORECASTING;%5BOK%5D+FORECAST+RANGE;%5BOK%5D+INVENTORY+ANALYSIS;%5BOK%5D+FASTAPI+SERVICE;%5BOK%5D+AUTOMATED+TESTING;%5BOK%5D+GITHUB+CHECKPOINTS"/>

<br><br>

<img src="https://img.shields.io/badge/DATA-ONLINE-00D084?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/ML-ONLINE-00E5C7?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/API-ONLINE-00A6A6?style=for-the-badge&labelColor=07111F"/>
<img src="https://img.shields.io/badge/TESTS-18%20PASSED-00D084?style=for-the-badge&labelColor=07111F"/>

</div>

🔮 Future Evolution

The current implementation is a completed portfolio-stage system. Future development opportunities include:

🟣 Forecasting Intelligence

Model persistence instead of training on API startup

Configurable forecast horizons

Feature importance reporting

Historical forecast-vs-actual visualization

🔵 Supply Chain Intelligence

Supplier lead-time modeling

Safety-stock calculations

More advanced reorder policies

Broader inventory optimization

🟢 Production Engineering

Docker support

CI/CD with GitHub Actions

Structured API error handling

Automated retraining workflow

Production monitoring

Model performance tracking

These are future development opportunities, not claims about the current implementation.

🌐 Future Architecture

flowchart TD

    A["🏢 Supply Chain User"] --> B["🌐 API / Application"]

    B --> C["📊 Data Layer"]

    C --> D["🧩 Feature Intelligence"]

    D --> E["🧠 Forecasting Models"]

    E --> F["📈 Forecast Monitoring"]

    F --> G["📦 Inventory Optimization"]

    G --> H["🔁 Replenishment Intelligence"]

    H --> I["📊 Decision Dashboard"]

    I --> J["📡 Production Monitoring"]

🧠 Engineering Lessons

Building NEXUS provided practical experience across several AI engineering areas.

<div align="center">

<table width="100%" cellspacing="0" cellpadding="20">
<tr>
<td align="center">

🐍 PYTHON

Modular application development and service architecture.

</td>
<td align="center">

📊 DATA

Historical demand analysis and feature engineering.

</td>
<td align="center">

🧠 MACHINE LEARNING

Random Forest regression and model evaluation.

</td>
</tr>
<tr>
<td align="center">

🛡️ DATA LEAKAGE

Temporal feature construction and chronological evaluation.

</td>
<td align="center">

📦 INVENTORY

Risk classification and reorder decision logic.

</td>
<td align="center">

🚀 API ENGINEERING

FastAPI service design and validation.

</td>
</tr>
</table>

</div>

📌 Completed Capabilities

✓ Sales Dataset Generation
✓ Data Loading
✓ Demand Analysis
✓ Leakage-Safe Feature Engineering
✓ Random Forest Demand Forecasting
✓ Forecast Prediction Range
✓ Inventory Risk Analysis
✓ Reorder Quantity Recommendation
✓ FastAPI Forecasting Service
✓ API Validation
✓ Automated Unit/API Tests
✓ GitHub Repository
✓ Checkpoint-Based Development

🤝 Contributing

Contributions, ideas, improvements and suggestions are welcome.

git checkout -b feature/your-feature

git add .

git commit -m "feat: add your feature"

git push origin feature/your-feature

Then open a Pull Request.

📜 License

This project is currently a personal / portfolio project.

Add a formal open-source license before distributing it as an open-source package.

👨‍💻 Author

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=25&duration=2400&pause=700&color=00E5C7&center=true&vCenter=true&width=900&lines=SHUBHAM+KARDEL;AI%2FML+ENGINEER;PYTHON+DEVELOPER;INTELLIGENT+SYSTEMS+BUILDER"/>

<br><br>

<a href="https://github.com/shubhamkardel-ai">
<img src="https://img.shields.io/badge/GitHub-shubhamkardel--ai-181717?style=for-the-badge&logo=github&logoColor=white"/>
</a>

<br><br>

🚀 Building intelligent systems — one project at a time.

</div>

🌟 NEXUS

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=21&duration=2300&pause=700&color=00E5C7&center=true&vCenter=true&width=1000&lines=OBSERVE+%7C+FORECAST+%7C+ANALYZE+%7C+DECIDE;TURNING+DEMAND+DATA+INTO+SUPPLY+CHAIN+INTELLIGENCE;FROM+HISTORICAL+SALES+TO+ACTIONABLE+DECISIONS;NEXUS+SUPPLY+CHAIN+INTELLIGENCE+ONLINE"/>

<br><br>

Forecast demand.
Understand inventory risk.
Recommend replenishment.
Build better supply-chain decisions.

<br><br>

⭐ If you find NEXUS useful, consider giving the repository a star. ⭐

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00E5C7,25:00A6A6,50:123B55,75:0B2239,100:07111F&height=170&section=footer&animation=fadeIn" width="100%"/>

</div>
