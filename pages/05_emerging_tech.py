import streamlit as st

from utils.charts import bar
from utils.data_loader import emerging_capacity, emerging_signals
from utils.metrics import format_quantity
from utils.ui import render_sources, show_table

st.title("05 · Emerging technologies")
st.write("Capacity and workload outlook copied from public industry reports.")

capacity = emerging_capacity()
signals = emerging_signals()


def reading(key: str) -> str:
    row = signals.loc[signals["key"] == key].iloc[0]
    return format_quantity(float(row["value"]), str(row["unit"]))


capacity_2030 = int(capacity.loc[capacity["year"] == "2030", "capacity_gw"].iloc[0])

outlook, growth, ai_share = st.columns(3)
outlook.metric("2030 global capacity", f"{capacity_2030} GW")
growth.metric("Growth rate", reading("cagr"))
ai_share.metric("AI share by 2030", reading("ai_share"))

figure = bar(
    capacity,
    x="year",
    y="capacity_gw",
    title="Global data center capacity outlook",
    value_title="Global capacity (GW)",
)
st.plotly_chart(figure, use_container_width=True)

st.subheader("Signals")
st.caption(
    "These figures do not share a unit, so they stay in a table instead of one bar chart."
)
display = signals.copy()
display["reading"] = [
    format_quantity(value, unit)
    for value, unit in zip(display["value"], display["unit"], strict=True)
]
show_table(display, {"label": "Signal", "reading": "Reading"})

st.subheader("Reading the figures")
st.write(
    "1. AI is shifting data center design toward higher power density and energy-aware infrastructure."
)
st.write(
    "2. Capacity growth is accelerating, and grid constraints make energy innovation a competitive advantage."
)
st.write(
    "3. Efficiency still matters at this scale: the 2024 industry average PUE is 1.56, "
    "so overhead energy remains a design constraint."
)
render_sources("emerging")
