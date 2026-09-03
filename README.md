# NEXUS Supply Chain Intelligence

AI-powered demand forecasting and inventory intelligence system designed to transform historical sales data into actionable supply chain decisions.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas)](https://pandas.pydata.org/)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikit-learn)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-28%20Passing-success)](#testing)
[![Model](https://img.shields.io/badge/Model-Random%20Forest-orange)](#machine-learning)

---

## Overview

**NEXUS Supply Chain Intelligence** is an end-to-end machine learning system for demand forecasting and inventory decision support.

The system combines:

- Historical sales analysis
- Leakage-safe feature engineering
- Machine learning demand forecasting
- Forecast uncertainty estimation
- Inventory risk analysis
- Reorder recommendations
- REST API integration
- Automated testing

The goal is to move from **raw sales data → predictive intelligence → operational decision**.

---

## System Architecture

```text
                    ┌──────────────────────┐
                    │     Sales Dataset    │
                    │      sales.csv       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Data Loading      │
                    │      Pandas          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Feature Engineering  │
                    │                      │
                    │ • Calendar Features  │
                    │ • Lag Features       │
                    │ • Rolling Features   │
                    │ • Historical Signals │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Random Forest Model  │
                    │   200 Estimators     │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │        Forecast Engine           │
              │                                 │
              │ • Predicted Demand              │
              │ • Lower Forecast Bound          │
              │ • Upper Forecast Bound          │
              └───────────────┬─────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │ Inventory Intelligence│
                    │                      │
                    │ • Risk Classification │
                    │ • Reorder Quantity    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      REST API        │
                    └──────────────────────┘