import requests
import streamlit as st


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="NEXUS Supply Chain Intelligence",
    page_icon="📦",
    layout="wide",
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .nexus-title {
            font-size: 2.6rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .nexus-subtitle {
            font-size: 1.15rem;
            margin-bottom: 0.2rem;
        }

        .nexus-caption {
            color: #6b7280;
            font-size: 0.95rem;
        }

        .section-title {
            font-size: 1.45rem;
            font-weight: 650;
            margin-top: 1rem;
            margin-bottom: 0.8rem;
        }

        .decision-box {
            padding: 1rem;
            border-radius: 0.7rem;
            border: 1px solid rgba(128,128,128,0.25);
            margin-top: 0.5rem;
        }

        .decision-label {
            font-size: 0.8rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .decision-value {
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }

        div[data-testid="stMetric"] {
            padding: 0.5rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="nexus-title">NEXUS Supply Chain Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="nexus-subtitle">AI-Powered Supply Chain Decision Platform</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="nexus-caption">'
    "Demand forecasting • Inventory risk analysis • Reorder planning"
    "</div>",
    unsafe_allow_html=True,
)

st.divider()


# --------------------------------------------------
# DEMAND FORECAST
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Demand Forecast</div>',
    unsafe_allow_html=True,
)


input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    product_id = st.selectbox(
        "Select Product",
        ["P001", "P002", "P003", "P004", "P005"],
    )

with input_col2:
    forecast_date = st.date_input(
        "Forecast Date",
    )

with input_col3:
    current_inventory = st.number_input(
        "Current Inventory",
        min_value=0,
        value=50,
        step=1,
    )


if st.button(
    "Generate Forecast",
    type="primary",
    use_container_width=True,
):

    with st.spinner("Generating demand forecast..."):

        response = requests.post(
            "http://127.0.0.1:8000/forecast",
            json={
                "product_id": product_id,
                "forecast_date": forecast_date.isoformat(),
                "current_inventory": current_inventory,
            },
        )


    if response.status_code == 200:

        result = response.json()

        st.success("Forecast generated successfully.")


        # --------------------------------------------------
        # FORECAST SUMMARY
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Forecast Summary</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Predicted Demand",
                f"{result['predicted_units_sold']:.2f} units",
            )

        with col2:
            st.metric(
                "Forecast Range",
                f"{result['forecast_lower']:.2f} – "
                f"{result['forecast_upper']:.2f}",
            )

        with col3:
            st.metric(
                "Safety Stock",
                f"{result['safety_stock']} units",
            )

        with col4:
            st.metric(
                "Reorder Point",
                f"{result['reorder_point']} units",
            )


        st.divider()


        # --------------------------------------------------
        # INVENTORY DECISION
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Inventory Decision</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Current Inventory",
                f"{result['current_inventory']} units",
            )

        with col2:
            st.metric(
                "Predicted Demand",
                f"{result['predicted_units_sold']:.2f} units",
            )

        with col3:
            st.metric(
                "Reorder Quantity",
                f"{result['recommended_reorder_quantity']} units",
            )

        with col4:
            risk = result["inventory_risk"]

            st.metric(
                "Inventory Risk",
                risk,
            )

        # Risk message
        risk = result["inventory_risk"]

        if risk == "HIGH":
            st.error("High inventory risk — immediate attention required.")

        elif risk == "MEDIUM":
            st.warning("Medium inventory risk — inventory should be monitored.")

        else:
            st.success("Low inventory risk — inventory level is healthy.")


        # Business decision
        decision = result["inventory_recommendation"]

        if decision == "REORDER":

            st.error(
                f"Business Decision: REORDER "
                f"{result['recommended_reorder_quantity']} units"
            )

        elif decision == "MONITOR":

            st.warning(
                "Business Decision: MONITOR inventory"
            )

        else:

            st.success(
                "Business Decision: SUFFICIENT inventory"
            )


        st.divider()


        # --------------------------------------------------
        # DECISION FLOW
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Supply Chain Decision Flow</div>',
            unsafe_allow_html=True,
        )

        flow_col1, flow_col2, flow_col3 = st.columns(3)

        with flow_col1:

            st.info(
                f"### 1. Demand Forecast\n\n"
                f"Expected demand\n\n"
                f"**{result['predicted_units_sold']:.2f} units**"
            )

        with flow_col2:

            st.warning(
                f"### 2. Inventory Planning\n\n"
                f"Reorder point\n\n"
                f"**{result['reorder_point']} units**"
            )

        with flow_col3:

            if decision == "REORDER":

                st.error(
                    f"### 3. Action Required\n\n"
                    f"**REORDER**\n\n"
                    f"{result['recommended_reorder_quantity']} units"
                )

            elif decision == "MONITOR":

                st.warning(
                    "### 3. Action Required\n\n"
                    "**MONITOR**\n\n"
                    "Inventory level"
                )

            else:

                st.success(
                    "### 3. Action Required\n\n"
                    "**SUFFICIENT**\n\n"
                    "No reorder required"
                )


        st.caption(
            "Forecast demand → calculate inventory threshold → recommend supply action"
        )


        st.divider()


        # --------------------------------------------------
        # FORECAST VISUALIZATION
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Demand Forecast Visualization</div>',
            unsafe_allow_html=True,
        )

        forecast_chart_data = {
            "Metric": [
                "Forecast Lower",
                "Predicted Demand",
                "Forecast Upper",
            ],
            "Units": [
                result["forecast_lower"],
                result["predicted_units_sold"],
                result["forecast_upper"],
            ],
        }

        st.bar_chart(
            forecast_chart_data,
            x="Metric",
            y="Units",
        )


        st.divider()


        # --------------------------------------------------
        # MODEL PERFORMANCE
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Model Performance</div>',
            unsafe_allow_html=True,
        )

        performance_response = requests.get(
            "http://127.0.0.1:8000/forecast/report"
        )

        if performance_response.status_code == 200:

            report = performance_response.json()

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "MAE",
                    report["mae"],
                )

            with col2:
                st.metric(
                    "RMSE",
                    report["rmse"],
                )

            with col3:
                st.metric(
                    "MAPE",
                    f"{report['mape']:.2f}%",
                )

            with col4:
                st.metric(
                    "Trees",
                    report["trees"],
                )

            st.caption(
                f"Model: {report['model']} • "
                f"{report['trees']} decision trees"
            )

        else:

            st.warning(
                "Model performance information is currently unavailable."
            )


    else:

        st.error(
            f"Forecast request failed: {response.text}"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "NEXUS Supply Chain Intelligence • "
    "AI-driven demand forecasting and inventory decision support"
)