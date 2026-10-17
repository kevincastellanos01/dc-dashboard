"""Layout helpers shared by every page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.data_loader import sources_for

_STYLE = """
<style>
    .stApp {
        background: linear-gradient(180deg, #0b1020 0%, #111827 100%);
        color: #f3f4f6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #f9fafb;
    }
</style>
"""


def apply_page_style() -> None:
    """Apply the dashboard chrome. Call it after ``st.set_page_config``."""
    st.markdown(_STYLE, unsafe_allow_html=True)
    st.sidebar.caption("YucaCore · Querétaro and Mérida")


def show_table(frame: pd.DataFrame, columns: dict[str, str]) -> None:
    """Render a dataframe with display names and no index."""
    display = frame.loc[:, list(columns)].rename(columns=columns)
    st.dataframe(display, hide_index=True, use_container_width=True)


def render_sources(page: str) -> None:
    """Print the citations stored for one page."""
    rows = sources_for(page).loc[:, ["publisher", "title", "url"]]
    items = "\n".join(
        f"- {row.publisher}, **{row.title}**  \n  {row.url}"
        for row in rows.itertuples(index=False)
    )
    st.markdown("### Sources")
    st.markdown(items)
