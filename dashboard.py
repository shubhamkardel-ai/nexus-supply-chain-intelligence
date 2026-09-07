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

        st.metric(
            "Predicted Demand",
            f"{result['predicted_units_sold']:.2f} units",
        )

        st.write("Inventory Risk:", result["inventory_risk"])
        st.write(
            "Recommendation:",
            result["inventory_recommendation"],
        )
        st.write(
            "Recommended Reorder Quantity:",
            result["recommended_reorder_quantity"],
        )
    else:
        st.error(
            f"Forecast request failed: {response.text}"
        )
