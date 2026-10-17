import streamlit as st

from utils.ui import apply_page_style

st.set_page_config(
    page_title="YucaCore DC Ops Dashboard",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/kevin080106/dc-dashboard/issues",
        "About": (
            "Operations dashboard for YucaCore, a fictional colocation and "
            "hybrid-cloud operator in Mexico. Benchmarks are cited public figures."
        ),
    },
)
apply_page_style()

overview = st.Page(
    "pages/00_overview.py",
    title="Overview",
    icon="🖥️",
    default=True,
)
operations = st.Page("pages/01_operations.py", title="Operations", icon="🛠️")
energy = st.Page("pages/02_energy.py", title="Energy", icon="⚡")
security = st.Page("pages/03_security.py", title="Security", icon="🔒")
market = st.Page("pages/04_market.py", title="Market intelligence", icon="📈")
emerging = st.Page(
    "pages/05_emerging_tech.py",
    title="Emerging technologies",
    icon="🛰️",
)

st.navigation(
    [overview, operations, energy, security, market, emerging],
    expanded=True,
).run()
