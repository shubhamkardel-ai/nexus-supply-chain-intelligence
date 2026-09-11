import streamlit as st

st.set_page_config(
    page_title="NEXUS Supply Chain Intelligence",
    page_icon="📦",
    layout="wide",
)

st.title("NEXUS Supply Chain Intelligence")
st.subheader("AI-Powered Supply Chain Decision Platform")

st.divider()

st.header("Demand Forecast")

product_id = st.selectbox(
    "Select Product",
    ["P001", "P002", "P003", "P004", "P005"],
)

forecast_date = st.date_input(
    "Forecast Date",
)

current_inventory = st.number_input(
    "Current Inventory",
    min_value=0,
    value=50,
    step=1,
)

if st.button("Generate Forecast"):
    import requests

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

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Predicted Demand",
                f"{result['predicted_units_sold']:.2f} units",
            )

        with col2:
            st.metric(
                "Forecast Range",
                f"{result['forecast_lower']:.2f} – {result['forecast_upper']:.2f}",
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

        st.subheader("Inventory Decision")

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

            if risk == "HIGH":
                st.error(f"Risk: {risk}")
            elif risk == "MEDIUM":
                st.warning(f"Risk: {risk}")
            else:
                st.success(f"Risk: {risk}")

        st.divider()

        st.subheader("Supply Chain Decision Flow")

        flow_col1, flow_col2, flow_col3, flow_col4 = st.columns(4)

        with flow_col1:
            st.metric(
                "Predicted Demand",
                f"{result['predicted_units_sold']:.2f}",
            )

        with flow_col2:
            st.metric(
                "Safety Stock",
                f"{result['safety_stock']}",
            )

        with flow_col3:
            st.metric(
                "Reorder Point",
                f"{result['reorder_point']}",
            )

        with flow_col4:
            st.metric(
                "Current Inventory",
                f"{result['current_inventory']}",
            )

        st.divider()

        st.subheader("Final Recommendation")

        recommendation = result["inventory_recommendation"]

        if recommendation == "REORDER":
            st.error(
                f"REORDER REQUIRED — Inventory is below the reorder point. "
                f"Recommended reorder quantity: "
                f"{result['recommended_reorder_quantity']} units."
            )
        elif recommendation == "MONITOR":
            st.warning(
                "MONITOR INVENTORY — Stock is close to the expected demand. "
                "Prepare for replenishment if demand increases."
            )
        else:
            st.success(
                "SUFFICIENT INVENTORY — Current stock is sufficient. "
                "No immediate reorder is required."
            )

        st.write(
            f"Inventory Recommendation: **{recommendation}**"
        )

        st.divider()

        st.subheader("Demand Forecast Visualization")

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

    else:
        st.error(
            f"Forecast request failed: {response.text}"
        )

if st.button("View Model Performance"):
    import requests

    response = requests.get(
        "http://127.0.0.1:8000/forecast/report"
    )

    if response.status_code == 200:
        report = response.json()

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

        st.write(
            f"Model: {report['model']}"
        )

    else:
        st.error(
            f"Model performance request failed: {response.text}"
        )