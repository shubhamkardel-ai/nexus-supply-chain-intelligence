from datetime import date
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.forecast_features import create_forecast_features
from services.forecast_model import (
    prepare_data,
    train_model,
    predict_with_range,
)
from services.forecast_report import generate_forecast_report
from services.inventory_service import calculate_inventory_risk


app = FastAPI(
    title="NEXUS Supply Chain Intelligence",
    description="AI-powered demand forecasting API",
    version="1.0.0",
)


class ForecastRequest(BaseModel):
    product_id: str = Field(..., min_length=1)
    forecast_date: date
    current_inventory: int = Field(..., ge=0)


class ForecastResponse(BaseModel):
    product_id: str
    forecast_date: date
    predicted_units_sold: float
    forecast_lower: float
    forecast_upper: float
    forecast_type: str
    model: str
    inventory_risk: str
    current_inventory: int
    recommended_reorder_quantity: int


# Train the model when the API starts
file_path = Path("data/sales.csv")

X_train, X_test, y_train, y_test = prepare_data(file_path)

model, preprocessor = train_model(
    X_train,
    y_train,
)


@app.get("/")
def root():
    return {
        "project": "NEXUS Supply Chain Intelligence",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/inventory/status")
def inventory_status():
    return {
        "service": "inventory_management",
        "status": "active",
    }

@app.get("/forecast/report")
def forecast_report():
    return generate_forecast_report(file_path)


@app.post("/forecast", response_model=ForecastResponse)
def forecast(request: ForecastRequest):
    features = create_forecast_features(
        file_path=file_path,
        product_id=request.product_id,
        forecast_date=request.forecast_date.isoformat(),
    )

    encoded_data = preprocessor.transform(features)

    prediction, lower_bound, upper_bound = predict_with_range(
        model,
        encoded_data,
    )

    inventory_analysis = calculate_inventory_risk(
        product_id=request.product_id,
        current_inventory=request.current_inventory,
        predicted_demand=prediction,
    )

    return {
        "product_id": request.product_id,
        "forecast_date": request.forecast_date,
        "predicted_units_sold": round(float(prediction), 2),
        "forecast_lower": round(float(lower_bound), 2),
        "forecast_upper": round(float(upper_bound), 2),
        "forecast_type": "demand_forecast",
        "model": "Random Forest",
        "inventory_risk": inventory_analysis.inventory_risk,
        "current_inventory": inventory_analysis.current_inventory,
        "recommended_reorder_quantity": inventory_analysis.recommended_reorder_quantity,
    }
class BatchForecastItem(BaseModel):
    product_id: str = Field(..., min_length=1)
    current_inventory: int = Field(..., ge=0)


class BatchForecastRequest(BaseModel):
    forecast_date: date
    forecasts: list[BatchForecastItem] = Field(..., min_length=1)


class BatchForecastResponse(BaseModel):
    forecasts: list[ForecastResponse]


@app.post("/forecast/batch", response_model=BatchForecastResponse)
def batch_forecast(request: BatchForecastRequest):
    results = []

    for item in request.forecasts:
        features = create_forecast_features(
            file_path=file_path,
            product_id=item.product_id,
            forecast_date=request.forecast_date.isoformat(),
        )

        encoded_data = preprocessor.transform(features)

        prediction, lower_bound, upper_bound = predict_with_range(
            model,
            encoded_data,
        )

        inventory_analysis = calculate_inventory_risk(
            product_id=item.product_id,
            current_inventory=item.current_inventory,
            predicted_demand=prediction,
        )

        results.append(
            {
                "product_id": item.product_id,
                "forecast_date": request.forecast_date,
                "predicted_units_sold": round(float(prediction), 2),
                "forecast_lower": round(float(lower_bound), 2),
                "forecast_upper": round(float(upper_bound), 2),
                "forecast_type": "demand_forecast",
                "model": "Random Forest",
                "inventory_risk": inventory_analysis.inventory_risk,
                "current_inventory": inventory_analysis.current_inventory,
                "recommended_reorder_quantity": inventory_analysis.recommended_reorder_quantity,
            }
        )

    return {"forecasts": results}
