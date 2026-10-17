"""Read the snapshot tables in ``data/``."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_SCHEMAS: dict[str, tuple[str, ...]] = {
    "operations_benchmarks.csv": ("key", "label", "value"),
    "operations_incidents.csv": ("category", "incidents"),
    "operations_mac.csv": ("request_id", "type", "status", "owner"),
    "energy_reference.csv": ("key", "label", "value"),
    "security_checklist.csv": ("control", "status"),
    "security_layers.csv": ("layer", "primary_control", "risk_level"),
    "market_mexico.csv": ("location", "data_centers"),
    "market_latam.csv": ("key", "label", "percent"),
    "market_focus.csv": ("country_group", "countries"),
    "emerging_capacity.csv": ("year", "capacity_gw"),
    "emerging_signals.csv": ("key", "label", "value", "unit"),
    "sources.csv": ("page", "publisher", "title", "url"),
}


def _read(filename: str) -> pd.DataFrame:
    frame = pd.read_csv(DATA_DIR / filename)
    expected = _SCHEMAS[filename]
    missing = [column for column in expected if column not in frame.columns]
    if missing:
        raise ValueError(f"{filename} is missing columns: {missing}")
    if frame.empty:
        raise ValueError(f"{filename} has no rows")
    return frame


def lookup(frame: pd.DataFrame, key: str, column: str = "value"):
    """Return one cell from a table that has a ``key`` column."""
    if "key" not in frame.columns:
        raise KeyError("frame has no key column")
    matches = frame.loc[frame["key"] == key, column]
    if matches.empty:
        raise KeyError(key)
    return matches.iloc[0]


def operations_benchmarks() -> pd.DataFrame:
    return _read("operations_benchmarks.csv")


def operations_incidents() -> pd.DataFrame:
    return _read("operations_incidents.csv")


def operations_mac() -> pd.DataFrame:
    return _read("operations_mac.csv")


def energy_reference() -> pd.DataFrame:
    return _read("energy_reference.csv")


def security_checklist() -> pd.DataFrame:
    return _read("security_checklist.csv")


def security_layers() -> pd.DataFrame:
    return _read("security_layers.csv")


def market_mexico() -> pd.DataFrame:
    return _read("market_mexico.csv")


def market_latam() -> pd.DataFrame:
    return _read("market_latam.csv")


def market_focus() -> pd.DataFrame:
    return _read("market_focus.csv")


def emerging_capacity() -> pd.DataFrame:
    frame = _read("emerging_capacity.csv")
    frame["year"] = frame["year"].astype(str)
    return frame


def emerging_signals() -> pd.DataFrame:
    return _read("emerging_signals.csv")


def citations() -> pd.DataFrame:
    return _read("sources.csv")


def sources_for(page: str) -> pd.DataFrame:
    frame = citations()
    rows = frame.loc[frame["page"] == page]
    if rows.empty:
        raise KeyError(page)
    return rows.reset_index(drop=True)
