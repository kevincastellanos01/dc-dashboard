import streamlit as st

from utils.charts import bar
from utils.data_loader import (
    lookup,
    operations_benchmarks,
    operations_incidents,
    operations_mac,
)
from utils.ui import render_sources, show_table

st.title("01 · Operations")
st.write(
    "A fictional operating log for YucaCore, read next to published outage benchmarks."
)

benchmarks = operations_benchmarks()
incidents = operations_incidents()
mac = operations_mac()

outages_100k, outages_1m, cause = st.columns(3)
outages_100k.metric(
    "Industry: outages > $100k",
    lookup(benchmarks, "outages_over_100k"),
    help="Share of outages in the cited Uptime Institute analysis.",
)
outages_1m.metric(
    "Industry: outages > $1M",
    lookup(benchmarks, "outages_over_1m"),
    help="Share of outages in the cited Uptime Institute analysis.",
)
cause.metric("Top serious-outage cause", lookup(benchmarks, "leading_cause"))

figure = bar(
    incidents,
    x="category",
    y="incidents",
    title="Incident log by category",
    value_title="Incidents",
)
st.plotly_chart(figure, use_container_width=True)
st.caption("Fictional case log. These counts are not an industry distribution.")

st.subheader("Move, add, and change log")
st.caption("Fictional requests for the YucaCore case.")
show_table(
    mac,
    {
        "request_id": "Request ID",
        "type": "Type",
        "status": "Status",
        "owner": "Owner",
    },
)

st.subheader("Industry benchmarks")
show_table(benchmarks, {"label": "Metric", "value": "Value"})
render_sources("operations")
