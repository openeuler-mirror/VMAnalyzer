#!/usr/bin/env python3
"""Color space conversion between RGB, HSL, and HEX."""
from typing import Tuple

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0, 0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60, s * 100, l * 100

def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    h, s, l = h/360, s/100, l/100
    if s == 0:
        v = int(l * 255)
        return v, v, v
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    def hue_to_rgb(t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p
    return tuple(round(hue_to_rgb(t) * 255) for t in [h+1/3, h, h-1/3])

def lighten(hex_color: str, amount: float) -> str:
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(r, g, b)
    l = min(100, l + amount)
    return rgb_to_hex(*hsl_to_rgb(h, s, l))

def darken(hex_color: str, amount: float) -> str:
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(r, g, b)
    l = max(0, l - amount)
    return rgb_to_hex(*hsl_to_rgb(h, s, l))
