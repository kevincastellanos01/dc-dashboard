import streamlit as st

from utils.data_loader import security_checklist, security_layers
from utils.ui import show_table

st.title("03 · Security")
st.write(
    "Fictional checklist for the YucaCore case. Control names follow common "
    "data-center practice and the vocabulary of ISO/IEC 27001 and ANSI/TIA-942. "
    "This page is not an audit or a certification."
)

checklist = security_checklist()
layers = security_layers()

implemented, in_progress = st.columns(2)
implemented.metric(
    "Implemented controls",
    int((checklist["status"] == "Implemented").sum()),
)
in_progress.metric(
    "Controls in progress",
    int((checklist["status"] == "In Progress").sum()),
)

st.subheader("Reference checklist")
show_table(checklist, {"control": "Control", "status": "Status"})

st.subheader("Physical security controls")
show_table(
    layers,
    {
        "layer": "Layer",
        "primary_control": "Primary control",
        "risk_level": "Risk level",
    },
)
