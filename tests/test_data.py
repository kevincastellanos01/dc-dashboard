import pytest

from utils.data_loader import (
    citations,
    emerging_capacity,
    emerging_signals,
    energy_reference,
    lookup,
    market_latam,
    market_mexico,
    operations_benchmarks,
    operations_incidents,
    operations_mac,
    security_checklist,
    sources_for,
)
from utils.metrics import power_usage_effectiveness


def test_mexico_snapshot_totals_173_facilities():
    mexico = market_mexico()
    assert int(mexico["data_centers"].sum()) == 173
    queretaro = mexico.loc[mexico["location"] == "Querétaro", "data_centers"].iloc[0]
    assert int(queretaro) == 28


def test_latam_indicators_match_the_cited_snapshot():
    latam = market_latam()
    assert float(lookup(latam, "inventory_growth", "percent")) == pytest.approx(20)
    assert float(lookup(latam, "vacancy_rate", "percent")) == pytest.approx(9)
    assert float(lookup(latam, "precommitted", "percent")) == pytest.approx(42)


def test_published_pue_matches_the_calculator_example():
    published = float(lookup(energy_reference(), "industry_pue_2024"))
    assert published == pytest.approx(1.56)
    assert power_usage_effectiveness(1560, 1000) == pytest.approx(published)


def test_capacity_outlook_endpoints():
    capacity = emerging_capacity().set_index("year")["capacity_gw"]
    assert int(capacity["2025"]) == 103
    assert int(capacity["2030"]) == 200


def test_case_study_tables_keep_their_rows():
    assert len(operations_incidents()) == 4
    assert int(operations_incidents()["incidents"].sum()) == 7
    assert len(operations_mac()) == 4
    status = security_checklist()["status"].value_counts().to_dict()
    assert status == {"Implemented": 5, "In Progress": 2}


def test_outage_benchmarks_are_present():
    benchmarks = operations_benchmarks()
    assert lookup(benchmarks, "outages_over_100k") == "54%"
    assert lookup(benchmarks, "outages_over_1m") == "20%"
    assert lookup(benchmarks, "leading_cause") == "Power issues"


def test_emerging_signals_keep_their_units():
    units = emerging_signals().set_index("key")["unit"].to_dict()
    assert units["cagr"] == "%"
    assert units["added_capacity"] == "GW"
    assert units["ai_share"] == "%"
    assert units["industry_pue_2024"] == "ratio"


def test_every_analytical_page_cites_https_sources():
    frame = citations()
    assert set(frame["page"]) == {"operations", "energy", "market", "emerging"}
    assert frame["url"].str.startswith("https://").all()
    assert frame["title"].str.len().gt(0).all()
    assert frame["publisher"].str.len().gt(0).all()
    assert len(sources_for("energy")) >= 1


def test_lookup_missing_key_raises():
    with pytest.raises(KeyError):
        lookup(operations_benchmarks(), "missing")
