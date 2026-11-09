import requests
import streamlit as st
from datetime import date

# ============================================================
# NEXUS SUPPLY CHAIN INTELLIGENCE — DASHBOARD V2
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="NEXUS | Supply Chain Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
       

        .stApp {
            background: #0b0f14;
        }

        .block-container {
            max-width: 1500px;
            padding: 1.6rem 2.2rem 2.5rem 2.2rem;
        }

        [data-testid="stSidebar"] {
            background: #0f141b;
            border-right: 1px solid #202833;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 2rem;
        }

        .brand-mark {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, #2563eb, #06b6d4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .brand-name {
            font-size: 1.05rem;
            font-weight: 750;
            color: #f8fafc;
            letter-spacing: .01em;
        }

        .brand-sub {
            font-size: .7rem;
            color: #64748b;
            margin-top: 2px;
        }

        .hero {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            padding: .4rem 0 1.5rem 0;
            border-bottom: 1px solid #202833;
            margin-bottom: 1.4rem;
        }

        .hero-title {
            font-size: 2.15rem;
            font-weight: 760;
            color: #f8fafc;
            letter-spacing: -.03em;
            margin: 0;
        }

        .hero-subtitle {
            color: #94a3b8;
            font-size: .94rem;
            margin-top: .35rem;
        }

        .status-pill {
            border: 1px solid #245c48;
            background: #0d241d;
            color: #6ee7b7;
            border-radius: 999px;
            padding: .38rem .7rem;
            font-size: .72rem;
            font-weight: 650;
            white-space: nowrap;
        }

        .section-label {
            color: #94a3b8;
            font-size: .72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .12em;
            margin: 1.1rem 0 .65rem 0;
        }

        .kpi-card {
            background: #111820;
            border: 1px solid #202a36;
            border-radius: 12px;
            padding: 1rem 1.05rem;
            min-height: 108px;
        }

        .kpi-label {
            color: #7f8ea3;
            font-size: .72rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            font-weight: 650;
        }

        .kpi-value {
            color: #f8fafc;
            font-size: 1.65rem;
            font-weight: 760;
            margin-top: .35rem;
        }

        .kpi-meta {
            color: #64748b;
            font-size: .72rem;
            margin-top: .2rem;
        }

        .panel {
            background: #111820;
            border: 1px solid #202a36;
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
        }

        .panel-title {
            color: #e2e8f0;
            font-size: .95rem;
            font-weight: 700;
            margin-bottom: .15rem;
        }

        .panel-subtitle {
            color: #64748b;
            font-size: .72rem;
            margin-bottom: .85rem;
        }

        .decision-card {
            border-radius: 12px;
            padding: 1.25rem;
            min-height: 190px;
            border: 1px solid #283241;
            background: #111820;
        }

        .decision-card.high {
            border-color: #7f1d1d;
            background: #1b1114;
        }

        .decision-card.medium {
            border-color: #6b5b12;
            background: #1b1910;
        }

        .decision-card.low {
            border-color: #14532d;
            background: #101b15;
        }

        .decision-kicker {
            color: #7f8ea3;
            font-size: .68rem;
            text-transform: uppercase;
            letter-spacing: .1em;
            font-weight: 700;
        }

        .decision-main {
            color: #f8fafc;
            font-size: 1.5rem;
            font-weight: 780;
            margin-top: .45rem;
        }

        .decision-detail {
            color: #94a3b8;
            font-size: .78rem;
            line-height: 1.5;
            margin-top: .35rem;
        }

        .decision-action {
            margin-top: 1rem;
            color: #e2e8f0;
            font-size: .85rem;
            font-weight: 700;
        }

        .flow-card {
            background: #0f151d;
            border: 1px solid #202a36;
            border-radius: 10px;
            padding: .9rem;
            min-height: 125px;
        }

        .flow-step {
            color: #64748b;
            font-size: .65rem;
            text-transform: uppercase;
            letter-spacing: .1em;
            font-weight: 700;
        }

        .flow-value {
            color: #f8fafc;
            font-size: 1.15rem;
            font-weight: 750;
            margin-top: .45rem;
        }

        .flow-detail {
            color: #7f8ea3;
            font-size: .7rem;
            margin-top: .25rem;
        }

        .metric-note {
            color: #64748b;
            font-size: .72rem;
            margin-top: .55rem;
        }

        .footer {
            border-top: 1px solid #202833;
            margin-top: 2rem;
            padding-top: 1rem;
            color: #475569;
            font-size: .68rem;
            display: flex;
            justify-content: space-between;
        }

        .sidebar-heading {
            color: #94a3b8;
            font-size: .68rem;
            text-transform: uppercase;
            letter-spacing: .11em;
            font-weight: 700;
            margin-bottom: .55rem;
        }

        div[data-testid="stButton"] > button {
            border-radius: 9px;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: transparent;
        }

        .stAlert {
            border-radius: 9px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

def api_get(path: str):
    try:
        response = requests.get(f"{API_BASE_URL}{path}", timeout=20)
        return response
    except requests.RequestException:
        return None


def api_post(path: str, payload: dict):
    try:
        response = requests.post(
            f"{API_BASE_URL}{path}",
            json=payload,
            timeout=60,
        )
        return response
    except requests.RequestException:
        return None

def api_post_json(path: str, payload: dict):
    response = api_post(path, payload)

    if response is None:
        return None

    if response.status_code != 200:
        st.error(f"API Error ({response.status_code}): {response.text}")
        return None

    try:
        return response.json()
    except ValueError:
        st.error("API returned an invalid JSON response.")
        return None

def format_units(value):
    return f"{value:,.2f}"


def risk_class(risk):
    return {
        "HIGH": "high",
        "MEDIUM": "medium",
        "LOW": "low",
    }.get(risk, "medium")


def risk_message(risk):
    return {
        "HIGH": "Immediate inventory attention required.",
        "MEDIUM": "Inventory should be monitored closely.",
        "LOW": "Inventory position is currently healthy.",
    }.get(risk, "Review inventory position.")


# ============================================================
# SIDEBAR — CONTROL CENTER
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">📦</div>
            <div>
                <div class="brand-name">NEXUS</div>
                <div class="brand-sub">SUPPLY CHAIN INTELLIGENCE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-heading">Forecast Controls</div>',
                unsafe_allow_html=True)

    product_id = st.selectbox(
        "Product",
        ["P001", "P002", "P003", "P004", "P005"],
        label_visibility="collapsed",
    )

    forecast_date = st.date_input(
        "Forecast Date",
        value=date.today(),
    )

    current_inventory = st.number_input(
        "Current Inventory",
        min_value=0,
        value=50,
        step=1,
    )

    forecast_horizon = st.slider(
        "Forecast Horizon",
        min_value=7,
        max_value=30,
        value=7,
        step=1,
    )

    generate = st.button(
        "Generate Forecast",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    st.markdown('<div class="sidebar-heading">System</div>',
                unsafe_allow_html=True)

    health_response = api_get("/")

    if health_response is not None and health_response.status_code == 200:
        st.success("API connected")
    else:
        st.error("API unavailable")

    st.caption("Local FastAPI inference service")
    st.caption("Random Forest demand engine")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div>
            <div class="hero-title">Supply Chain Intelligence</div>
            <div class="hero-subtitle">
                AI-powered demand forecasting, inventory risk analysis and replenishment decisions
            </div>
        </div>
        <div class="status-pill">● INTELLIGENCE ENGINE ONLINE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# INITIAL / GENERATED STATE
# ============================================================

if "forecast_result" not in st.session_state:
    st.session_state.forecast_result = None

if "multi_day_forecast_result" not in st.session_state:
    st.session_state.multi_day_forecast_result = None

if generate:
    with st.spinner("Running demand forecast and inventory analysis..."):
        response = api_post(
            "/forecast",
            {
                "product_id": product_id,
                "forecast_date": forecast_date.isoformat(),
                "current_inventory": current_inventory,
            },
        )

        multi_day_response = api_post(
            "/forecast/multi-day",
            {
                "product_id": product_id,
                "start_date": forecast_date.isoformat(),
                "horizon": forecast_horizon,
            },
        )

    if response is not None and response.status_code == 200:
        st.session_state.forecast_result = response.json()
    elif response is None:
        st.error(
            "Unable to connect to the FastAPI backend. "
            "Start the API with your project command and try again."
        )
    else:
        st.error(f"Forecast request failed: {response.text}")

    if multi_day_response is not None and multi_day_response.status_code == 200:
        st.session_state.multi_day_forecast_result = multi_day_response.json()
    elif multi_day_response is not None:
        st.error(
            f"Multi-day forecast request failed: "
            f"{multi_day_response.text}"
        )

    if (
        response is not None
        and response.status_code == 200
        and multi_day_response is not None
        and multi_day_response.status_code == 200
    ):
        st.toast("Forecast generated successfully")


result = st.session_state.forecast_result

# ============================================================
# EMPTY STATE
# ============================================================

if result is None:
    st.markdown(
        '<div class="section-label">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    empty_cards = [
        ("Forecast Demand", "—", "Run a forecast"),
        ("Reorder Point", "—", "Inventory threshold"),
        ("Safety Stock", "—", "Protection buffer"),
        ("Inventory Risk", "—", "Risk classification"),
    ]

    for column, (label, value, meta) in zip(
        [c1, c2, c3, c4],
        empty_cards,
    ):
        with column:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-meta">{meta}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="panel" style="margin-top:1.2rem;">
            <div class="panel-title">Ready for analysis</div>
            <div class="panel-subtitle">
                Select a product, forecast date and current inventory from the control center,
                then generate a supply-chain forecast.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    # ========================================================
    # EXECUTIVE KPI STRIP
    # ========================================================

    st.markdown(
        '<div class="section-label">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    kpis = [
        (
            "Forecast Demand",
            f"{result['predicted_units_sold']:.2f}",
            "units expected",
        ),
        (
            "Reorder Point",
            f"{result['reorder_point']:,}",
            "units threshold",
        ),
        (
            "Safety Stock",
            f"{result['safety_stock']:,}",
            "units buffer",
        ),
        (
            "Inventory Risk",
            result["inventory_risk"],
            risk_message(result["inventory_risk"]),
        ),
    ]

    for column, (label, value, meta) in zip([c1, c2, c3, c4], kpis):
        with column:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-meta">{meta}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # FORECAST + INVENTORY POSITION
    # ========================================================

    left, right = st.columns([1.6, 1])

    with left:
        st.markdown(
            '<div class="section-label">Demand Forecast</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">Forecast range</div>
                <div class="panel-subtitle">
                    {result['product_id']} · {result['forecast_date']} · {result['model']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        forecast_chart_data = {
            "Metric": [
                "Lower Forecast",
                "Predicted Demand",
                "Upper Forecast",
                "Current Inventory",
                "Reorder Point",
            ],
            "Units": [
                result["forecast_lower"],
                result["predicted_units_sold"],
                result["forecast_upper"],
                result["current_inventory"],
                result["reorder_point"],
            ],
        }

        st.bar_chart(
            forecast_chart_data,
            x="Metric",
            y="Units",
            height=320,
        )

        st.caption(
            "Forecast range compared with current inventory and the calculated reorder threshold."
        )

    with right:
        st.markdown(
            '<div class="section-label">Inventory Position</div>',
            unsafe_allow_html=True,
        )

        risk = result["inventory_risk"]
        risk_css = risk_class(risk)

        st.markdown(
            f"""
            <div class="decision-card {risk_css}">
                <div class="decision-kicker">Inventory health</div>
                <div class="decision-main">{risk}</div>
                <div class="decision-detail">
                    Current inventory: <strong>{result['current_inventory']:,} units</strong><br>
                    Reorder point: <strong>{result['reorder_point']:,} units</strong><br>
                    Predicted demand: <strong>{result['predicted_units_sold']:.2f} units</strong>
                </div>
                <div class="decision-action">{risk_message(risk)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # MULTI-DAY DEMAND OUTLOOK
    # ========================================================

    multi_day_result = st.session_state.multi_day_forecast_result

    if multi_day_result is not None:
        st.markdown(
            '<div class="section-label">Demand Outlook</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">Multi-day demand forecast</div>
                <div class="panel-subtitle">
                    {multi_day_result['product_id']} ·
                    {multi_day_result['start_date']} ·
                    {multi_day_result['horizon']} day horizon
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        import pandas as pd

        multi_day_data = pd.DataFrame(
            multi_day_result["forecasts"]
        )

        multi_day_data["forecast_date"] = pd.to_datetime(
            multi_day_data["forecast_date"]
        )

        multi_day_data = multi_day_data.set_index(
            "forecast_date"
        )

        chart_data = multi_day_data[
            [
                "forecast_lower",
                "predicted_units_sold",
                "forecast_upper",
            ]
        ].copy()

        chart_data.columns = [
            "Lower Forecast",
            "Predicted Demand",
            "Upper Forecast",
        ]

        st.line_chart(
            chart_data,
            height=360,
        )

        st.caption(
            "Predicted demand with the model's forecast range across the selected horizon."
        )

        display_data = multi_day_data.reset_index()

        display_data["forecast_date"] = display_data[
            "forecast_date"
        ].dt.strftime("%Y-%m-%d")

        display_data = display_data.rename(
            columns={
                "forecast_date": "Date",
                "predicted_units_sold": "Predicted Demand",
                "forecast_lower": "Lower Forecast",
                "forecast_upper": "Upper Forecast",
            }
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
        )

    # ========================================================
    # BUSINESS DECISION
    # ========================================================

    st.markdown(
        '<div class="section-label">Recommended Action</div>',
        unsafe_allow_html=True,
    )

    decision = result["inventory_recommendation"]
    reorder_qty = result["recommended_reorder_quantity"]

    d1, d2 = st.columns([1, 1.35])

    with d1:
        if decision == "REORDER":
            action_title = f"REORDER {reorder_qty:,} UNITS"
            action_detail = "Current inventory is below the calculated reorder point."
            action_css = "high"
        elif decision == "MONITOR":
            action_title = "MONITOR INVENTORY"
            action_detail = "Inventory is above demand but approaching the monitoring threshold."
            action_css = "medium"
        else:
            action_title = "SUFFICIENT INVENTORY"
            action_detail = "No replenishment action is currently required."
            action_css = "low"

        st.markdown(
            f"""
            <div class="decision-card {action_css}">
                <div class="decision-kicker">Business recommendation</div>
                <div class="decision-main">{action_title}</div>
                <div class="decision-detail">{action_detail}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with d2:
        st.markdown(
            """
            <div class="decision-card">
                <div class="decision-kicker">Decision rationale</div>
                <div class="decision-detail" style="margin-top:.8rem;">
                    NEXUS combines predicted demand, demand variability, lead-time coverage
                    and current inventory to determine the replenishment threshold.
                </div>
                <div class="decision-detail" style="margin-top:.8rem;">
                    The recommendation is generated from the same inventory-planning logic
                    used by the FastAPI service.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # DECISION FLOW
    # ========================================================

    st.markdown(
        '<div class="section-label">Decision Flow</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3, f4 = st.columns(4)

    flow = [
        (
            "01 · FORECAST",
            f"{result['predicted_units_sold']:.2f} units",
            "Expected demand",
        ),
        (
            "02 · BUFFER",
            f"{result['safety_stock']:,} units",
            "Safety stock",
        ),
        (
            "03 · THRESHOLD",
            f"{result['reorder_point']:,} units",
            "Reorder point",
        ),
        (
            "04 · ACTION",
            decision,
            f"{reorder_qty:,} units recommended" if decision == "REORDER"
            else "Supply decision",
        ),
    ]

    for column, (step, value, detail) in zip([f1, f2, f3, f4], flow):
        with column:
            st.markdown(
                f"""
                <div class="flow-card">
                    <div class="flow-step">{step}</div>
                    <div class="flow-value">{value}</div>
                    <div class="flow-detail">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # MODEL PERFORMANCE
    # ========================================================

    st.markdown(
        '<div class="section-label">Model Performance</div>',
        unsafe_allow_html=True,
    )

    performance_response = api_get("/forecast/report")

    if performance_response is not None and performance_response.status_code == 200:
        report = performance_response.json()

        p1, p2, p3, p4 = st.columns(4)

        performance = [
            ("MAE", report["mae"], "lower is better"),
            ("RMSE", report["rmse"], "lower is better"),
            ("MAPE", f"{report['mape']:.2f}%", "forecast error"),
            ("TREES", report["trees"], "Random Forest"),
        ]

        for column, (label, value, meta) in zip([p1, p2, p3, p4], performance):
            with column:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                        <div class="kpi-meta">{meta}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            f"""
            <div class="metric-note">
                Model: {report['model']} · Forecast evaluation metrics from the production API
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Model performance information is currently unavailable.")

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <span>NEXUS Supply Chain Intelligence</span>
        <span>AI-driven demand forecasting · inventory planning · decision support</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# NEXUS DECISION CENTER
# --------------------------------------------------

st.divider()

st.header("NEXUS Decision Center")

st.subheader("1. Disruption Simulation")

col1, col2, col3 = st.columns(3)

with col1:
    disruption_product = st.selectbox(
        "Select Product",
        ["P001", "P002", "P003", "P004", "P005"],
        key="disruption_product",
    )

    disruption_type = st.selectbox(
        "Disruption Type",
        [
            "supplier_unavailable",
            "transport_delay",
            "demand_surge",
            "production_delay",
        ],
        key="disruption_type",
    )

with col2:
    severity_percent = st.slider(
        "Disruption Severity (%)",
        min_value=0,
        max_value=100,
        value=50,
        key="severity_percent",
    )

    duration_days = st.number_input(
        "Duration (Days)",
        min_value=1,
        max_value=365,
        value=7,
        key="duration_days",
    )

with col3:
    base_demand = st.number_input(
        "Base Daily Demand",
        min_value=0.0,
        value=50.0,
        key="base_demand",
    )

    base_lead_time = st.number_input(
        "Base Lead Time (Days)",
        min_value=1,
        value=7,
        key="base_lead_time",
    )

current_inventory_disruption = st.number_input(
    "Current Inventory",
    min_value=0,
    value=100,
    key="current_inventory_disruption",
)

simulate_button = st.button(
    "Simulate Disruption",
    type="primary",
    key="simulate_disruption_button",
)

if simulate_button:

    disruption_payload = {
        "product_id": disruption_product,
        "disruption_type": disruption_type,
        "severity_percent": severity_percent,
        "duration_days": duration_days,
        "base_demand": base_demand,
        "base_lead_time": base_lead_time,
        "current_inventory": current_inventory_disruption,
    }

    with st.spinner("Simulating supply chain disruption..."):

        disruption_result = api_post_json(
            "/disruption/simulate",
            disruption_payload,
        )

    if disruption_result:

        st.session_state["disruption_result"] = disruption_result

        st.success("Disruption simulation completed!")

    else:
        st.error("Disruption simulation failed. Check the API server.")

# Display saved simulation results
if "disruption_result" in st.session_state:

    st.markdown("### Simulation Results")

    simulation = st.session_state["disruption_result"]

    st.metric(
        "Expected Shortage",
        f"{simulation['expected_shortage']} units"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Projected Inventory",
        simulation["projected_inventory"]
    )

    col2.metric(
        "Simulated Demand",
        simulation["simulated_demand"]
    )

    col3.metric(
        "Risk Level",
        simulation["risk_level"]
    )

# --------------------------------------------------
# IMPACT ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("2. Disruption Impact Analysis")

if "disruption_result" in st.session_state:

    disruption_result = st.session_state["disruption_result"]

    analyze_button = st.button(
        "Analyze Disruption Impact",
        type="primary",
        key="analyze_impact_button",
    )

    if analyze_button:

        impact_payload = {
            "product_id": disruption_result["product_id"],
            "disruption_type": disruption_result["disruption_type"],
            "expected_shortage": disruption_result["expected_shortage"],
            "projected_inventory": disruption_result["projected_inventory"],
            "risk_level": disruption_result["risk_level"],
        }

        with st.spinner("Analyzing disruption impact..."):

            impact_result = api_post_json(
                "/impact/analyze",
                impact_payload,
            )

        if impact_result:

            st.session_state["impact_result"] = impact_result

            st.success("Impact analysis completed!")

        else:
            st.error("Impact analysis failed. Check the API server.")

else:
    st.info("Run a disruption simulation first to analyze its impact.")

# Display saved impact analysis results
if "impact_result" in st.session_state:

    st.markdown("### Impact Analysis Results")

    impact = st.session_state["impact_result"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Impact Level", impact["impact_level"])
    col2.metric("Expected Shortage", f"{impact['expected_shortage']} units")
    col3.metric("Projected Inventory", f"{impact['projected_inventory']} units")

    st.info(f"Recommendation: {impact['recommendation']}")

# --------------------------------------------------
# DECISION RECOMMENDATION
# --------------------------------------------------

st.divider()

st.subheader("3. Decision Recommendation")

if "impact_result" in st.session_state:

    impact_result = st.session_state["impact_result"]

    recommend_button = st.button(
        "Generate Decision Recommendation",
        type="primary",
        key="generate_decision_button",
    )

    if recommend_button:

        decision_payload = {
            "product_id": impact_result["product_id"],
            "disruption_type": impact_result["disruption_type"],
            "impact_level": impact_result["impact_level"],
            "expected_shortage": impact_result["expected_shortage"],
            "projected_inventory": impact_result["projected_inventory"],
        }

        with st.spinner("Generating supply chain decision..."):

            decision_result = api_post_json(
                "/decision/recommend",
                decision_payload,
            )

        if decision_result:

            st.session_state["decision_result"] = decision_result

            st.success("Decision recommendation generated!")

        else:
            st.error("Decision recommendation failed. Check the API server.")

else:
    st.info("Complete impact analysis first.")

# Display saved decision recommendation
if "decision_result" in st.session_state:

    st.markdown("### Recommended Supply Chain Action")

    decision = st.session_state["decision_result"]

    col1, col2 = st.columns(2)

    col1.metric(
        "Recommended Action",
        decision["recommended_action"]
    )

    col2.metric(
        "Priority",
        decision["priority"]
    )

    st.info(
        f"Decision Rationale: {decision['rationale']}"
    )

# --------------------------------------------------
# DECISION EXPLANATION
# --------------------------------------------------

st.divider()

st.subheader("4. Why Was This Decision Selected?")

if "decision_result" in st.session_state:

    explain_button = st.button(
        "Explain Recommended Decision",
        type="primary",
        key="explain_decision_button",
    )

    if explain_button:

        decision_result = st.session_state["decision_result"]

        explanation_payload = {
            "product_id": decision_result["product_id"],
            "disruption_type": decision_result["disruption_type"],
            "impact_level": decision_result["impact_level"],
            "expected_shortage": decision_result["expected_shortage"],
            "projected_inventory": decision_result["projected_inventory"],
        }

        with st.spinner("Preparing decision explanation..."):

            explanation_result = api_post_json(
                "/decision/explain",
                explanation_payload,
            )

        if explanation_result:

            st.session_state["explanation_result"] = explanation_result

            st.success("Decision explanation generated!")

        else:
            st.error("Decision explanation failed. Check the API server.")

else:
    st.info("Generate a decision recommendation first.")

# Display saved decision explanation
if "explanation_result" in st.session_state:

    st.markdown("### Decision Explanation")

    explanation = st.session_state["explanation_result"]

    st.info(explanation["decision_summary"])

    st.markdown("#### Key Decision Factors")

    for factor in explanation["key_factors"]:

        st.markdown(f"**{factor['factor']}**")

        st.write(f"Value: {factor['value']}")

        st.caption(factor["effect"])

    st.markdown("#### Alternatives Considered")

    for alternative in explanation["alternatives_considered"]:

        st.markdown(f"**{alternative['action']}**")

        st.write(alternative["reason"])

    st.markdown("#### Supporting Evidence")

    st.json(explanation["supporting_evidence"])

st.markdown(
    """
    Simulate supply chain disruptions, analyze their impact,
    and receive AI-powered operational recommendations.
    """
)


# ==========================================
# SUPPLIER PROCUREMENT OPTIMIZATION
# ==========================================

st.divider()

st.header("Supplier Procurement Optimization")

st.markdown(
    """
    Compare suppliers based on procurement cost, delivery time,
    and reliability to identify the best eligible supplier.
    """
)

st.info(
    "Enter supplier procurement details below. "
    "Cost and capacity values are user-provided inputs."
)

required_quantity = st.number_input(
    "Required Procurement Quantity",
    min_value=1,
    value=100,
    step=10,
)

st.subheader("Supplier Details")

supplier_count = st.number_input(
    "Number of Suppliers",
    min_value=2,
    max_value=10,
    value=3,
    step=1,
)

supplier_inputs = []

for i in range(int(supplier_count)):

    st.markdown(f"### Supplier {i + 1}")

    col1, col2, col3 = st.columns(3)

    with col1:
        supplier_name = st.text_input(
            "Supplier Name",
            value=f"Supplier {i + 1}",
            key=f"supplier_name_{i}",
        )

        supplier_id = st.text_input(
            "Supplier ID",
            value=f"SUP00{i + 1}",
            key=f"supplier_id_{i}",
        )

        country = st.text_input(
            "Country",
            value="India",
            key=f"supplier_country_{i}",
        )

    with col2:
        lead_time = st.number_input(
            "Lead Time (Days)",
            min_value=1,
            value=5,
            key=f"supplier_lead_time_{i}",
        )

        reliability = st.number_input(
            "Reliability Score (0–100)",
            min_value=0.0,
            max_value=100.0,
            value=90.0,
            key=f"supplier_reliability_{i}",
        )

        unit_cost = st.number_input(
            "Unit Cost",
            min_value=0.01,
            value=120.0,
            key=f"supplier_unit_cost_{i}",
        )

    with col3:
        capacity = st.number_input(
            "Available Capacity",
            min_value=1,
            value=500,
            key=f"supplier_capacity_{i}",
        )

        minimum_order = st.number_input(
            "Minimum Order Quantity",
            min_value=1,
            value=50,
            key=f"supplier_moq_{i}",
        )

        email = st.text_input(
            "Contact Email",
            value=f"supplier{i + 1}@example.com",
            key=f"supplier_email_{i}",
        )

    supplier_inputs.append(
        {
            "supplier_id": supplier_id,
            "name": supplier_name,
            "country": country,
            "lead_time_days": int(lead_time),
            "reliability_score": reliability,
            "unit_cost": unit_cost,
            "capacity": int(capacity),
            "minimum_order_quantity": int(minimum_order),
            "contact_email": email,
        }
    )

    st.divider()


if st.button(
    "Optimize Supplier Selection",
    type="primary",
    use_container_width=True,
):

    payload = {
        "required_quantity": int(required_quantity),
        "suppliers": supplier_inputs,
    }

    with st.spinner("Comparing suppliers and optimizing procurement..."):

        result = api_post_json(
            "/suppliers/analytics",
            payload,
        )

    if result:

        st.session_state["supplier_optimization_result"] = result

        st.success("Supplier comparison completed successfully!")

    else:
        st.error(
            "Supplier optimization failed. "
            "Check supplier eligibility and API server."
        )


# Display saved supplier optimization results

if "supplier_optimization_result" in st.session_state:

    result = st.session_state["supplier_optimization_result"]

    recommended = result["recommended_supplier"]

    st.divider()

    st.subheader("Recommended Supplier")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Supplier",
        recommended["supplier_name"],
    )

    col2.metric(
        "Total Procurement Cost",
        f"{recommended['total_cost']:,.2f}",
    )

    col3.metric(
        "Lead Time",
        f"{recommended['lead_time_days']} days",
    )

    st.success(
        f"Recommended supplier: {recommended['supplier_name']}"
    )

    st.subheader("Supplier Rankings")

    rankings = result["supplier_rankings"]

    st.dataframe(
        [
            {
                "Rank": item["rank"],
                "Supplier": item["supplier_name"],
                "Supplier ID": item["supplier_id"],
                "Unit Cost": item["unit_cost"],
                "Total Cost": item["total_cost"],
                "Lead Time (Days)": item["lead_time_days"],
                "Reliability": item["reliability_score"],
                "Optimization Score": item["optimization_score"],
            }
            for item in rankings
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Only eligible suppliers are included in the rankings. "
        "Lower optimization scores indicate better overall performance."
    )


    # Advanced Supplier Analytics

    analytics = result["analytics"]

    st.divider()
    st.header("Advanced Supplier Analytics")

    # 1. Procurement Cost Analysis
    cost_analysis = analytics["cost_analysis"]

    st.subheader("Procurement Cost Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Lowest Cost Supplier",
        cost_analysis["lowest_cost_supplier"]["supplier_name"],
        f"{cost_analysis['lowest_cost_supplier']['total_cost']:,.2f}",
    )

    col2.metric(
        "Highest Cost Supplier",
        cost_analysis["highest_cost_supplier"]["supplier_name"],
        f"{cost_analysis['highest_cost_supplier']['total_cost']:,.2f}",
    )

    col3.metric(
        "Cost Difference",
        f"{cost_analysis['cost_difference']:,.2f}",
    )

    st.dataframe(
        cost_analysis["supplier_costs"],
        use_container_width=True,
        hide_index=True,
    )

    # 2. Supplier Performance Analysis
    performance = analytics["performance_analysis"]

    st.subheader("Supplier Performance Analysis")

    col1, col2 = st.columns(2)

    col1.metric(
        "Fastest Supplier",
        performance["fastest_supplier"]["supplier_name"],
        f"{performance['fastest_supplier']['lead_time_days']} days",
    )

    col2.metric(
        "Most Reliable Supplier",
        performance["most_reliable_supplier"]["supplier_name"],
        f"{performance['most_reliable_supplier']['reliability_score']} reliability",
    )

    # 3. Supplier Eligibility Analysis
    eligibility = analytics["eligibility_analysis"]

    st.subheader("Supplier Eligibility Analysis")

    col1, col2 = st.columns(2)

    col1.metric("Eligible Suppliers", eligibility["eligible_count"])
    col2.metric("Excluded Suppliers", eligibility["excluded_count"])

    st.dataframe(
        [
            {
                "Supplier ID": item["supplier_id"],
                "Supplier": item["supplier_name"],
                "Eligible": "Yes" if item["eligible"] else "No",
                "Reasons": ", ".join(item["reasons"]) or "Eligible",
            }
            for item in eligibility["supplier_details"]
        ],
        use_container_width=True,
        hide_index=True,
    )

    # 4. Recommendation Explanation
    explanation = analytics["recommendation_explanation"]

    st.subheader("Procurement Recommendation Explanation")

    st.info(explanation["summary"])

    st.markdown("**Key Recommendation Reasons**")

    for reason in explanation["reasons"]:
        st.markdown(f"- {reason}")

    st.markdown("**Procurement Trade-offs**")

    for trade_off in explanation["trade_offs"]:
        st.markdown(f"- {trade_off}")
