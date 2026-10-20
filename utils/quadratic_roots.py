"""Quadratic root solving with explicit discriminant handling."""
import cmath
import logging

LOG = logging.getLogger(__name__)


def real_roots(a, b, c):
    """Return the real roots of a*x^2 + b*x + c, or an empty tuple."""
    if a == 0:
        raise ValueError('a must be non-zero for a quadratic')
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return ()
    if discriminant == 0:
        return (-b / (2 * a),)
    root = discriminant ** 0.5
    return ((-b - root) / (2 * a), (-b + root) / (2 * a))


def complex_roots(a, b, c):
    """Return both roots of a*x^2 + b*x + c on the complex plane."""
    if a == 0:
        raise ValueError('a must be non-zero for a quadratic')
    discriminant = cmath.sqrt(b * b - 4 * a * c)
    return ((-b - discriminant) / (2 * a), (-b + discriminant) / (2 * a))


def vertex(a, b, c):
    """Return the (x, y) turning point of the parabola."""
    if a == 0:
        raise ValueError('a must be non-zero for a quadratic')
    x = -b / (2 * a)
    return x, a * x * x + b * x + c


__all__ = ['real_roots', 'complex_roots', 'vertex']
