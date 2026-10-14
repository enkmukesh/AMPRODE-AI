import pandas as pd
import plotly.express as px
import streamlit as st

from src.energy_optimizer import estimate_energy_plan

st.set_page_config(page_title="AMPRODE-AI | Energy Optimizer", page_icon="⚡", layout="wide")

st.title("⚡ AMPRODE-AI")
st.subheader("Smart energy planning for factories and commercial facilities")
st.caption(
    "Interactive prototype • Uses simplified estimates, not live meter readings or guaranteed savings."
)

with st.sidebar:
    st.header("Scenario settings")
    demand = st.number_input("Daily electricity demand (kWh)", min_value=0.0, value=1200.0, step=50.0)
    solar = st.number_input("Solar energy available per day (kWh)", min_value=0.0, value=450.0, step=25.0)
    tariff = st.number_input("Grid electricity tariff (₹/kWh)", min_value=0.0, value=8.0, step=0.5)
    st.divider()
    st.subheader("Battery assumptions")
    battery_capacity = st.number_input("Battery capacity (kWh)", min_value=0.0, value=300.0, step=25.0)
    battery_charge = st.number_input("Energy currently stored (kWh)", min_value=0.0, value=240.0, step=20.0)
    battery_discharge_limit = st.number_input("Maximum battery delivery per day (kWh)", min_value=0.0, value=200.0, step=20.0)
    efficiency = st.slider("Battery discharge efficiency", min_value=0.50, max_value=1.00, value=0.90, step=0.05)

plan = estimate_energy_plan(
    demand_kwh=demand,
    solar_available_kwh=solar,
    grid_tariff_per_kwh=tariff,
    battery_capacity_kwh=battery_capacity,
    battery_charge_kwh=battery_charge,
    battery_discharge_limit_kwh=battery_discharge_limit,
    battery_efficiency=efficiency,
)

monthly_days = 30
monthly_baseline = plan.baseline_cost * monthly_days
monthly_optimized = plan.optimized_cost * monthly_days
monthly_savings = plan.estimated_savings * monthly_days

col1, col2, col3, col4 = st.columns(4)
col1.metric("Estimated daily grid cost", f"₹{plan.optimized_cost:,.0f}")
col2.metric("Estimated daily savings", f"₹{plan.estimated_savings:,.0f}")
col3.metric("Estimated monthly savings", f"₹{monthly_savings:,.0f}")
col4.metric("Savings vs. grid-only baseline", f"{plan.savings_percent:.1f}%")

st.markdown("### Daily energy plan")
energy_df = pd.DataFrame({
    "Energy source": ["Solar", "Battery", "Grid"],
    "Energy supplied (kWh)": [plan.solar_used_kwh, plan.battery_used_kwh, plan.grid_used_kwh],
})
chart_col, summary_col = st.columns([1.4, 1])
with chart_col:
    fig = px.bar(
        energy_df,
        x="Energy source",
        y="Energy supplied (kWh)",
        title="Estimated energy supplied by source",
        text_auto=".1f",
    )
    fig.update_layout(yaxis_title="kWh", xaxis_title="", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with summary_col:
    st.markdown("#### Energy breakdown")
    st.write(f"**Demand:** {plan.demand_kwh:,.1f} kWh/day")
    st.write(f"**Solar used:** {plan.solar_used_kwh:,.1f} kWh/day")
    st.write(f"**Battery delivered:** {plan.battery_used_kwh:,.1f} kWh/day")
    st.write(f"**Grid required:** {plan.grid_used_kwh:,.1f} kWh/day")
    st.info(
        "This version assumes solar is used first, then the battery, then grid electricity. "
        "Battery charging costs and time-of-use tariffs are not modeled yet."
    )

st.markdown("### Cost comparison")
cost_df = pd.DataFrame({
    "Scenario": ["Grid-only baseline", "Solar + battery estimate"],
    "Daily cost (₹)": [plan.baseline_cost, plan.optimized_cost],
    "Monthly estimate (₹)": [monthly_baseline, monthly_optimized],
})
st.dataframe(cost_df, hide_index=True, use_container_width=True)

st.caption(
    "Monthly figures multiply the selected daily scenario by 30 days. Actual savings depend on site load, "
    "solar availability, battery losses, charging source, tariffs, and operating constraints."
)
