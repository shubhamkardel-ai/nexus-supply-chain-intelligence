from datetime import date
from pathlib import Path

from services.decision_explanation_service import explain_decision

from models.disruption import DisruptionScenario
from services.disruption_service import simulate_disruption

from services.impact_analysis_service import analyze_disruption_impact

from services.supplier_service import create_supplier
from services.supply_chain_optimizer import compare_suppliers
from services.supplier_analytics import generate_supplier_analytics


from services.decision_engine import generate_decision

from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel, Field
from services.scenario_service import calculate_scenario

from services.multi_day_forecast import generate_multi_day_forecast

from services.forecast_features import create_forecast_features
from services.forecast_model import (
    prepare_data,
    train_model,
    predict_with_range,
)
from services.forecast_report import generate_forecast_report
from services.inventory_planning import (
    calculate_inventory_plan,
    calculate_product_demand_std_dev,
    calculate_safety_stock,
    calculate_reorder_point,
)

from services.inventory_service import (
    calculate_inventory_risk,
    get_inventory_recommendation,
)


class DisruptionRequest(BaseModel):
    product_id: str = Field(..., min_length=1)
    disruption_type: str = Field(..., min_length=1)
    severity_percent: float = Field(..., ge=0, le=100)
    duration_days: int = Field(..., ge=1)
    base_demand: float = Field(..., ge=0)
    base_lead_time: int = Field(..., ge=1)
    current_inventory: int = Field(..., ge=0)


class DisruptionResponse(BaseModel):
    product_id: str
    disruption_type: str
    duration_days: int
    simulated_demand: float
    simulated_lead_time: int
    projected_inventory: int
    expected_demand: float
    expected_shortage: int
    risk_level: str

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
    inventory_recommendation: str
    current_inventory: int
    recommended_reorder_quantity: int
    safety_stock: int
    reorder_point: int


class BatchForecastItem(BaseModel):
    product_id: str = Field(..., min_length=1)
    current_inventory: int = Field(..., ge=0)


class BatchForecastRequest(BaseModel):
    forecast_date: date
    forecasts: list[BatchForecastItem] = Field(..., min_length=1)


class BatchForecastResponse(BaseModel):
    forecasts: list[ForecastResponse]


class MultiDayForecastRequest(BaseModel):
    product_id: str = Field(..., min_length=1)
    start_date: date
    horizon: int = Field(..., ge=1, le=30)


class MultiDayForecastItem(BaseModel):
    forecast_date: date
    predicted_units_sold: float
    forecast_lower: float
    forecast_upper: float


class MultiDayForecastResponse(BaseModel):
    product_id: str
    start_date: date
    horizon: int
    forecasts: list[MultiDayForecastItem]

class InventoryPlanRequest(BaseModel):
    average_daily_demand: float = Field(..., ge=0)
    demand_std_dev: float = Field(..., ge=0)
    lead_time_days: int = Field(..., ge=1)
    service_level_z: float = Field(1.65, gt=0)


class InventoryPlanResponse(BaseModel):
    average_daily_demand: float
    demand_std_dev: float
    lead_time_days: int
    service_level_z: float
    lead_time_demand: int
    safety_stock: int
    reorder_point: int

class InventoryPlanResponse(BaseModel):
    average_daily_demand: float
    demand_std_dev: float
    lead_time_days: int
    service_level_z: float
    lead_time_demand: int
    safety_stock: int
    reorder_point: int


class ScenarioRequest(BaseModel):
    product_id: str = Field(..., min_length=1)
    base_demand: float = Field(..., ge=0)
    base_lead_time: int = Field(..., ge=1)
    base_reorder_point: int = Field(..., ge=0)
    demand_change_percent: float = 0
    lead_time_change_percent: float = 0

class ScenarioResponse(BaseModel):
    product_id: str
    base_demand: float
    adjusted_demand: float
    base_lead_time: int
    adjusted_lead_time: int
    base_reorder_point: int
    adjusted_reorder_point: int
    demand_change_percent: float
    lead_time_change_percent: float

class ImpactAnalysisRequest(BaseModel):
    product_id: str
    disruption_type: str
    expected_shortage: int = Field(..., ge=0)
    projected_inventory: int = Field(..., ge=0)
    risk_level: str


class ImpactAnalysisResponse(BaseModel):
    product_id: str
    disruption_type: str
    impact_level: str
    expected_shortage: int
    projected_inventory: int
    recommendation: str

class DecisionRequest(BaseModel):
    product_id: str
    disruption_type: str
    impact_level: str
    expected_shortage: int = Field(..., ge=0)
    projected_inventory: int = Field(..., ge=0)


class DecisionResponse(BaseModel):
    product_id: str
    disruption_type: str
    impact_level: str
    expected_shortage: int
    projected_inventory: int
    recommended_action: str
    priority: str
    rationale: str

class SupplierInput(BaseModel):
    supplier_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    lead_time_days: int = Field(..., ge=1)
    reliability_score: float = Field(..., ge=0, le=100)
    unit_cost: float = Field(..., gt=0)
    capacity: int = Field(..., ge=1)
    minimum_order_quantity: int = Field(..., ge=1)
    contact_email: str | None = None


class SupplierComparisonRequest(BaseModel):
    required_quantity: int = Field(..., ge=1)
    suppliers: list[SupplierInput] = Field(..., min_length=1)

file_path = Path("data/sales.csv")

DEFAULT_LEAD_TIME_DAYS = 7

X_train, X_test, y_train, y_test = prepare_data(file_path)

model, preprocessor = train_model(
    X_train,
    y_train,
)


# --------------------------------------------------
# Shared forecast logic
# --------------------------------------------------

def generate_forecast(
    product_id: str,
    forecast_date: date,
    current_inventory: int,
) -> dict:

    features = create_forecast_features(
        file_path=file_path,
        product_id=product_id,
        forecast_date=forecast_date.isoformat(),
    )

    encoded_data = preprocessor.transform(features)

    prediction, lower_bound, upper_bound = predict_with_range(
        model,
        encoded_data,
    )

    demand_std_dev = calculate_product_demand_std_dev(
        file_path=file_path,
        product_id=product_id,
    )

    safety_stock = calculate_safety_stock(
        demand_std_dev=demand_std_dev,
        lead_time_days=DEFAULT_LEAD_TIME_DAYS,
    )

    reorder_point = calculate_reorder_point(
        average_daily_demand=prediction,
        lead_time_days=DEFAULT_LEAD_TIME_DAYS,
        safety_stock=safety_stock,
    )

    inventory_analysis = calculate_inventory_risk(
        product_id=product_id,
        current_inventory=current_inventory,
        predicted_demand=prediction,
        reorder_point=reorder_point,
    )

    inventory_recommendation = get_inventory_recommendation(
        current_inventory=current_inventory,
        predicted_demand=prediction,
        reorder_point=reorder_point,
    )

    return {
        "product_id": product_id,
        "forecast_date": forecast_date,
        "predicted_units_sold": round(float(prediction), 2),
        "forecast_lower": round(float(lower_bound), 2),
        "forecast_upper": round(float(upper_bound), 2),
        "forecast_type": "demand_forecast",
        "model": "Random Forest",
        "inventory_risk": inventory_analysis.inventory_risk,
        "inventory_recommendation": inventory_recommendation,
        "current_inventory": inventory_analysis.current_inventory,
        "recommended_reorder_quantity": (
            inventory_analysis.recommended_reorder_quantity
        ),
        "safety_stock": safety_stock,
        "reorder_point": reorder_point,
    }


# --------------------------------------------------
# Basic endpoints
# --------------------------------------------------

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

@app.post(
    "/inventory/plan",
    response_model=InventoryPlanResponse,
)
def inventory_plan(
    request: InventoryPlanRequest,
):
    return calculate_inventory_plan(
        average_daily_demand=request.average_daily_demand,
        demand_std_dev=request.demand_std_dev,
        lead_time_days=request.lead_time_days,
        service_level_z=request.service_level_z,
    )


@app.post(
    "/scenario",
    response_model=ScenarioResponse,
)
def scenario_analysis(
    request: ScenarioRequest,
):
    return calculate_scenario(
        product_id=request.product_id,
        base_demand=request.base_demand,
        base_lead_time=request.base_lead_time,
        base_reorder_point=request.base_reorder_point,
        demand_change_percent=request.demand_change_percent,
        lead_time_change_percent=request.lead_time_change_percent,
    )


@app.get("/forecast/report")
def forecast_report():
    return generate_forecast_report(file_path)


# --------------------------------------------------
# Single forecast
# --------------------------------------------------

@app.post("/forecast", response_model=ForecastResponse)
def forecast(request: ForecastRequest):

    return generate_forecast(
        product_id=request.product_id,
        forecast_date=request.forecast_date,
        current_inventory=request.current_inventory,
    )


# --------------------------------------------------
# Batch forecast
# --------------------------------------------------

@app.post(
    "/forecast/batch",
    response_model=BatchForecastResponse,
)
def batch_forecast(request: BatchForecastRequest):

    results = []

    for item in request.forecasts:

        result = generate_forecast(
            product_id=item.product_id,
            forecast_date=request.forecast_date,
            current_inventory=item.current_inventory,
        )

        results.append(result)

    return {
        "forecasts": results,
    }

@app.post(
    "/forecast/multi-day",
    response_model=MultiDayForecastResponse,
)
def multi_day_forecast(
    request: MultiDayForecastRequest,
):
    forecasts = generate_multi_day_forecast(
        file_path=file_path,
        product_id=request.product_id,
        start_date=request.start_date,
        horizon=request.horizon,
        model=model,
        preprocessor=preprocessor,
    )

    return {
        "product_id": request.product_id,
        "start_date": request.start_date,
        "horizon": request.horizon,
        "forecasts": forecasts,
    }

@app.post(
    "/disruption/simulate",
    response_model=DisruptionResponse,
)
def disruption_simulation(
    request: DisruptionRequest,
):
    scenario = DisruptionScenario(
        product_id=request.product_id,
        disruption_type=request.disruption_type,
        severity_percent=request.severity_percent,
        duration_days=request.duration_days,
    )

    return simulate_disruption(
        scenario=scenario,
        base_demand=request.base_demand,
        base_lead_time=request.base_lead_time,
        current_inventory=request.current_inventory,
    )

@app.post(
    "/impact/analyze",
    response_model=ImpactAnalysisResponse,
)
def impact_analysis(request: ImpactAnalysisRequest):
    simulation_result = {
        "product_id": request.product_id,
        "disruption_type": request.disruption_type,
        "expected_shortage": request.expected_shortage,
        "projected_inventory": request.projected_inventory,
        "risk_level": request.risk_level,
    }

    return analyze_disruption_impact(simulation_result)

@app.post(
    "/decision/recommend",
    response_model=DecisionResponse,
)
def decision_recommendation(request: DecisionRequest):
    impact_result = {
        "product_id": request.product_id,
        "disruption_type": request.disruption_type,
        "impact_level": request.impact_level,
        "expected_shortage": request.expected_shortage,
        "projected_inventory": request.projected_inventory,
    }

    return generate_decision(impact_result)

@app.post("/decision/explain")
def decision_explanation(request: DecisionRequest):

    # Prepare impact information
    impact_result = {
        "product_id": request.product_id,
        "disruption_type": request.disruption_type,
        "impact_level": request.impact_level,
        "expected_shortage": request.expected_shortage,
        "projected_inventory": request.projected_inventory,
    }

    # Generate the decision
    decision_result = generate_decision(impact_result)

    # Explain why the decision was selected
    explanation = explain_decision(
        impact_result,
        decision_result
    )

    return explanation


@app.post("/suppliers/compare")
def supplier_comparison(
    request: SupplierComparisonRequest,
):
    suppliers = []

    for item in request.suppliers:
        supplier = create_supplier(
            supplier_id=item.supplier_id,
            name=item.name,
            country=item.country,
            lead_time_days=item.lead_time_days,
            reliability_score=item.reliability_score,
            unit_cost=item.unit_cost,
            capacity=item.capacity,
            minimum_order_quantity=item.minimum_order_quantity,
            contact_email=item.contact_email,
        )

        suppliers.append(supplier)

    try:
        rankings = compare_suppliers(
            suppliers=suppliers,
            required_quantity=request.required_quantity,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "required_quantity": request.required_quantity,
        "recommended_supplier": rankings[0],
        "supplier_rankings": rankings,
    }


@app.post("/suppliers/analytics")
def supplier_analytics(
    request: SupplierComparisonRequest,
):
    suppliers = []

    for item in request.suppliers:
        supplier = create_supplier(
            supplier_id=item.supplier_id,
            name=item.name,
            country=item.country,
            lead_time_days=item.lead_time_days,
            reliability_score=item.reliability_score,
            unit_cost=item.unit_cost,
            capacity=item.capacity,
            minimum_order_quantity=item.minimum_order_quantity,
            contact_email=item.contact_email,
        )

        suppliers.append(supplier)

    rankings = compare_suppliers(
        suppliers=suppliers,
        required_quantity=request.required_quantity,
    )

    analytics = generate_supplier_analytics(
        suppliers=suppliers,
        required_quantity=request.required_quantity,
        supplier_rankings=rankings,
    )

    return {
        "required_quantity": request.required_quantity,
        "recommended_supplier": rankings[0],
        "supplier_rankings": rankings,
        "analytics": analytics,
    }
