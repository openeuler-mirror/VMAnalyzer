"""Convert temperature readings between Celsius, Fahrenheit and Kelvin.

Hardware sensors expose temperatures in mixed units depending on the
vendor.  Normalising to Celsius before threshold checks prevents false
overheating alerts from a Fahrenheit reading.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def to_celsius(value: float, unit: str = "C") -> float:
    """Convert a temperature reading into Celsius."""
    key = unit.strip().upper()
    if key == "C":
        return float(value)
    if key == "F":
        return (float(value) - 32.0) * 5.0 / 9.0
    if key == "K":
        return float(value) - 273.15
    raise ValueError("unsupported temperature unit {!r}".format(unit))


def from_celsius(value: float, unit: str = "C") -> float:
    """Convert a Celsius value into the requested unit."""
    key = unit.strip().upper()
    if key == "C":
        return float(value)
    if key == "F":
        return float(value) * 9.0 / 5.0 + 32.0
    if key == "K":
        return float(value) + 273.15
    raise ValueError("unsupported temperature unit {!r}".format(unit))


def hottest(readings: Dict[str, float], unit: str = "C") -> Dict[str, object]:
    """Return the hottest sensor name and its Celsius value."""
    if not readings:
        return {"sensor": "", "celsius": 0.0}
    converted = {name: to_celsius(value, unit) for name, value in readings.items()}
    name = max(converted, key=lambda key: converted[key])
    LOG.debug("hottest sensor %s at %.1fC", name, converted[name])
    return {"sensor": name, "celsius": round(converted[name], 2)}


__all__ = ["to_celsius", "from_celsius", "hottest"]
