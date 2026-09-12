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
        header {visibility: hidden;}

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

    if response is not None and response.status_code == 200:
        st.session_state.forecast_result = response.json()
        st.toast("Forecast generated successfully")
    elif response is None:
        st.error(
            "Unable to connect to the FastAPI backend. "
            "Start the API with your project command and try again."
        )
    else:
        st.error(f"Forecast request failed: {response.text}")


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
