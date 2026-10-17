import pandas as pd
import streamlit as st

from utils.charts import bar
from utils.data_loader import energy_reference, lookup
from utils.metrics import interpret_pue, power_usage_effectiveness
from utils.ui import render_sources, show_table

st.title("02 · Energy")
st.write(
    "Power Usage Effectiveness for a facility, compared with the published industry average."
)

reference = energy_reference()
benchmark = float(lookup(reference, "industry_pue_2024"))

st.latex(
    r"PUE = \frac{\text{total facility energy}}{\text{IT equipment energy}}"
)
st.caption(
    "Both inputs have to cover the same period. The unit cancels, which is why PUE is a ratio. "
    "The defaults below reproduce the 2024 industry average."
)

it_column, facility_column = st.columns(2)
with it_column:
    it_load = st.number_input(
        "IT equipment energy (kWh)",
        min_value=1.0,
        value=1000.0,
        step=10.0,
        format="%.1f",
    )
with facility_column:
    total_facility = st.number_input(
        "Total facility energy (kWh)",
        min_value=1.0,
        value=1560.0,
        step=10.0,
        format="%.1f",
    )

pue = power_usage_effectiveness(total_facility, it_load)

average, calculated = st.columns(2)
average.metric(
    "Industry average PUE, 2024",
    f"{benchmark:.2f}",
    help="Uptime Institute Global Data Center Survey 2024.",
)
calculated.metric("Calculated PUE", f"{pue:.2f}")

message = interpret_pue(pue, benchmark)
if pue < 1:
    st.error(message)
else:
    st.info(message)

comparison = pd.DataFrame(
    {
        "scenario": ["Industry average, 2024", "This calculation"],
        "pue": [benchmark, pue],
    }
)
figure = bar(
    comparison,
    x="scenario",
    y="pue",
    title="Calculated PUE against the 2024 industry average",
    color="scenario",
    value_title="PUE",
)
st.plotly_chart(figure, use_container_width=True)

st.subheader("Reference")
show_table(reference, {"label": "Metric", "value": "Value"})
render_sources("energy")
