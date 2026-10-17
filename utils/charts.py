"""Plotly charts that share one visual system across pages."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.45)",
        font={"color": "#e5e7eb", "family": "Source Sans Pro, sans-serif"},
        title={"font": {"size": 16, "color": "#f9fafb"}},
        colorway=["#38bdf8", "#34d399", "#fbbf24", "#fb7185", "#a78bfa"],
        xaxis={
            "gridcolor": "#1f2937",
            "linecolor": "#374151",
            "zerolinecolor": "#1f2937",
        },
        yaxis={
            "gridcolor": "#1f2937",
            "linecolor": "#374151",
            "zerolinecolor": "#1f2937",
        },
        margin={"l": 48, "r": 24, "t": 64, "b": 48},
        bargap=0.35,
    )
)

pio.templates["yucacore"] = _TEMPLATE
pio.templates.default = "yucacore"


def bar(
    frame: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    *,
    color: str | None = None,
    horizontal: bool = False,
    value_title: str | None = None,
) -> go.Figure:
    """Bar chart that keeps the row order of ``frame``."""
    labels = frame[x].astype(str).tolist()
    if horizontal:
        figure = px.bar(
            frame,
            x=y,
            y=x,
            orientation="h",
            title=title,
            color=color,
            template="yucacore",
        )
        figure.update_yaxes(
            type="category",
            categoryorder="array",
            categoryarray=list(reversed(labels)),
            title="",
        )
        if value_title:
            figure.update_xaxes(title=value_title)
    else:
        figure = px.bar(
            frame,
            x=x,
            y=y,
            title=title,
            color=color,
            template="yucacore",
        )
        figure.update_xaxes(
            type="category",
            categoryorder="array",
            categoryarray=labels,
            title="",
        )
        if value_title:
            figure.update_yaxes(title=value_title)

    figure.update_traces(marker_line_width=0)
    figure.update_xaxes(automargin=True)
    figure.update_yaxes(automargin=True)
    if color:
        figure.update_layout(showlegend=False)
    return figure
