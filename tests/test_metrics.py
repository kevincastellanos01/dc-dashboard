import pytest

from utils.metrics import format_quantity, interpret_pue, power_usage_effectiveness


def test_pue_is_total_facility_over_it_load():
    assert power_usage_effectiveness(1560, 1000) == pytest.approx(1.56)
    assert power_usage_effectiveness(2000, 1000) == pytest.approx(2.0)


def test_pue_rejects_non_positive_energy():
    with pytest.raises(ValueError):
        power_usage_effectiveness(100, 0)
    with pytest.raises(ValueError):
        power_usage_effectiveness(0, 100)


def test_interpret_pue_bands():
    assert "not physically plausible" in interpret_pue(0.8).lower()
    assert "1.20" in interpret_pue(1.2)
    assert "at or below" in interpret_pue(1.56).lower()
    assert "above" in interpret_pue(1.57).lower()


def test_format_quantity_keeps_the_unit_attached():
    assert format_quantity(14, "%") == "14%"
    assert format_quantity(100, "GW") == "100 GW"
    assert format_quantity(1.56, "ratio") == "1.56"
    with pytest.raises(ValueError):
        format_quantity(1, "kWh")
