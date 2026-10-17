import streamlit as st

st.title("YucaCore DC Ops Dashboard")
st.write(
    "Operating picture for a fictional colocation and hybrid-cloud provider "
    "in Mexico. Process data in this app is a case study. The benchmarks "
    "next to it are cited public figures."
)

site, edge, model = st.columns(3)
site.metric("Primary site", "Querétaro")
edge.metric("Edge site", "Mérida")
model.metric("Service model", "Colocation + hybrid cloud")

st.markdown("### Sections")
sections = [
    (
        "pages/01_operations.py",
        "Operations",
        "🛠️",
        "Fictional incident and MAC log beside Uptime Institute outage benchmarks.",
    ),
    (
        "pages/02_energy.py",
        "Energy",
        "⚡",
        "PUE calculator measured against the 2024 industry average.",
    ),
    (
        "pages/03_security.py",
        "Security",
        "🔒",
        "Fictional physical-security checklist using standard control vocabulary.",
    ),
    (
        "pages/04_market.py",
        "Market intelligence",
        "📈",
        "Snapshot of Mexico facility counts and LATAM market indicators.",
    ),
    (
        "pages/05_emerging_tech.py",
        "Emerging technologies",
        "🛰️",
        "Global capacity and AI-workload outlook from public reports.",
    ),
]

left, right = st.columns(2)
for index, (path, label, icon, blurb) in enumerate(sections):
    column = left if index % 2 == 0 else right
    with column:
        st.page_link(path, label=label, icon=icon)
        st.caption(blurb)

st.markdown("### What is simulated, and what is cited")
st.markdown(
    """
| Section | Case study | Published evidence |
| --- | --- | --- |
| Operations | Incident and MAC log | Uptime Institute outage shares |
| Energy | Energy inputs in the calculator | Green Grid definition and the 2024 average PUE |
| Security | Control checklist | Vocabulary of ISO/IEC 27001 and ANSI/TIA-942 |
| Market | Frozen directory snapshot | Cloudscene counts and JLL indicators |
| Emerging technologies | No simulated series | JLL capacity outlook and the 2024 PUE survey |
"""
)

st.caption(
    "Run it locally with Streamlit. The cited figures and the case-study tables live in data/."
)
