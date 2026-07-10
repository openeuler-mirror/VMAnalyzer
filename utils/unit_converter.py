#!/usr/bin/env python3
"""Unit converter for length, weight, and temperature."""
from typing import Dict

LENGTH_FACTORS = {
    "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
    "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344
}

WEIGHT_FACTORS = {
    "mg": 0.001, "g": 1.0, "kg": 1000.0, "t": 1_000_000.0,
    "oz": 28.3495, "lb": 453.592
}

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in LENGTH_FACTORS or to_unit not in LENGTH_FACTORS:
        raise ValueError("Unknown length unit")
    meters = value * LENGTH_FACTORS[from_unit]
    return meters / LENGTH_FACTORS[to_unit]

def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in WEIGHT_FACTORS or to_unit not in WEIGHT_FACTORS:
        raise ValueError("Unknown weight unit")
    grams = value * WEIGHT_FACTORS[from_unit]
    return grams / WEIGHT_FACTORS[to_unit]

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    units = {"C", "F", "K"}
    if from_unit not in units or to_unit not in units:
        raise ValueError("Unknown temperature unit")
    if from_unit == to_unit:
        return value
    celsius = value
    if from_unit == "F":
        celsius = (value - 32) * 5/9
    elif from_unit == "K":
        celsius = value - 273.15
    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius * 9/5 + 32
    else:
        return celsius + 273.15

def convert_data_size(value: float, from_unit: str, to_unit: str) -> float:
    sizes = ["B", "KB", "MB", "GB", "TB", "PB"]
    from_idx = sizes.index(from_unit)
    to_idx = sizes.index(to_unit)
    return value * (1024 ** (from_idx - to_idx))
