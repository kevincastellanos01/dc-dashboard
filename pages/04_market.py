import streamlit as st

from utils.charts import bar
from utils.data_loader import lookup, market_focus, market_latam, market_mexico
from utils.ui import render_sources, show_table

st.title("04 · Market intelligence")
st.write(
    "A frozen snapshot of public figures for Mexico and the broader Latin American market."
)

mexico = market_mexico()
latam = market_latam()
focus = market_focus()

total = int(mexico["data_centers"].sum())
queretaro = int(mexico.loc[mexico["location"] == "Querétaro", "data_centers"].iloc[0])
vacancy = float(lookup(latam, "vacancy_rate", "percent"))

facilities, queretaro_metric, vacancy_metric = st.columns(3)
facilities.metric("Mexico data centers", total)
queretaro_metric.metric("Querétaro data centers", queretaro)
vacancy_metric.metric("LATAM vacancy rate", f"{vacancy:.0f}%")

cities = bar(
    mexico,
    x="location",
    y="data_centers",
    title="Mexico data center directory snapshot",
    value_title="Facilities",
)
st.plotly_chart(cities, use_container_width=True)
st.caption(
    "Facility counts are a snapshot saved in this repository. "
    "Cloudscene's live directory can move after this snapshot."
)

regional = bar(
    latam,
    x="label",
    y="percent",
    title="LATAM market indicators, 2025",
    horizontal=True,
    value_title="Percent",
)
regional.update_traces(texttemplate="%{x:.0f}%", textposition="outside", cliponaxis=False)
regional.update_layout(margin={"r": 72})
st.plotly_chart(regional, use_container_width=True)

st.subheader("Core demand countries in Latin America")
show_table(focus, {"country_group": "Country group", "countries": "Countries"})

export = mexico.rename(columns={"location": "Location", "data_centers": "Data Centers"})
st.download_button(
    label="Download Mexico market data as CSV",
    data=export.to_csv(index=False).encode("utf-8"),
    file_name="mexico_market_data.csv",
    mime="text/csv",
)
render_sources("market")
