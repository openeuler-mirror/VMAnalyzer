"""Ordinary least squares line fitting for paired samples."""
from dataclasses import dataclass


@dataclass
class LineFit:
    """Slope and intercept of a fitted straight line."""

    slope: float
    intercept: float

    def predict(self, x):
        """Return the fitted y value at x."""
        return self.slope * x + self.intercept

    def residual_sum(self, xs, ys):
        """Return the sum of squared residuals for the samples."""
        return sum((self.predict(float(x)) - float(y)) ** 2
                   for x, y in zip(xs or [], ys or []))


def fit_line(xs, ys):
    """Return the least squares line fitted to paired samples."""
    pairs = [(float(x), float(y)) for x, y in zip(xs or [], ys or [])]
    if len(pairs) < 2:
        return LineFit(0.0, pairs[0][1] if pairs else 0.0)
    count = len(pairs)
    mean_x = sum(x for x, _ in pairs) / count
    mean_y = sum(y for _, y in pairs) / count
    var_x = sum((x - mean_x) ** 2 for x, _ in pairs)
    if var_x == 0:
        return LineFit(0.0, mean_y)
    cov = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    slope = cov / var_x
    return LineFit(slope, mean_y - slope * mean_x)


__all__ = ['LineFit', 'fit_line']
