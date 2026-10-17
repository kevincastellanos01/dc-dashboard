"""Metric definitions used by the dashboard and the tests."""

from __future__ import annotations


def power_usage_effectiveness(total_facility_kwh: float, it_equipment_kwh: float) -> float:
    """Return total facility energy divided by IT equipment energy.

    Both inputs have to cover the same period. The unit cancels, so the
    result is a ratio. The Green Grid definition is the one used here.
    """
    if total_facility_kwh <= 0 or it_equipment_kwh <= 0:
        raise ValueError("Energy inputs must be greater than zero.")
    return float(total_facility_kwh) / float(it_equipment_kwh)


def interpret_pue(pue: float, industry_average: float = 1.56) -> str:
    """Describe a PUE against the published industry average."""
    if pue < 1:
        return (
            "A result below 1.0 is not physically plausible. "
            "Total facility energy includes IT equipment energy."
        )
    if pue <= 1.2:
        return "This result is in the range associated with highly efficient facilities (PUE ≤ 1.20)."
    if pue <= industry_average:
        return f"This result is at or below the industry average of {industry_average:.2f}."
    return f"This result is above the industry average of {industry_average:.2f}."


def format_quantity(value: float, unit: str) -> str:
    """Format a published figure with its unit."""
    numeric = float(value)
    if unit == "%":
        return f"{numeric:g}%"
    if unit == "GW":
        return f"{numeric:g} GW"
    if unit == "ratio":
        return f"{numeric:.2f}"
    raise ValueError(f"Unsupported unit: {unit}")
