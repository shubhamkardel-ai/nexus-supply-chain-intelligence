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
            risk = result["inventory_risk"]

            if risk == "HIGH":
                st.error(f"Inventory Risk: {risk}")
            elif risk == "MEDIUM":
                st.warning(f"Inventory Risk: {risk}")
            else:
                st.success(f"Inventory Risk: {risk}")

        with col4:
            st.metric(
                "Reorder Quantity",
                f"{result['recommended_reorder_quantity']} units",
            )

        st.divider()

        st.write(
            "Inventory Recommendation:",
            result["inventory_recommendation"],
        )

        st.divider()

        st.subheader("Decision Summary")

        if result["inventory_risk"] == "HIGH":
            st.error(
                f"Inventory is below predicted demand. "
                f"Reorder approximately "
                f"{result['recommended_reorder_quantity']} units."
            )
        elif result["inventory_risk"] == "MEDIUM":
            st.warning(
                "Inventory is close to predicted demand. "
                "Monitor stock levels and prepare for replenishment."
            )
        else:
            st.success(
                "Inventory is sufficient to cover predicted demand. "
                "No immediate reorder is required."
            )

    else:
        st.error(
            f"Forecast request failed: {response.text}"
        )


st.divider()

st.header("Model Performance")

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