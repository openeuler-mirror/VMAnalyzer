"""Z score based anomaly screening.

Subtracting the rolling mean and dividing by the rolling standard deviation
turns metrics expressed in different units into a comparable anomaly score.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def rolling_zscore(values, window=10):
    """Return the z score of every sample against its trailing window."""
    clean = [float(v) for v in values or [] if v is not None]
    scores = []
    for index, value in enumerate(clean):
        chunk = clean[max(0, index - window + 1):index + 1]
        if len(chunk) < 2:
            scores.append(0.0)
            continue
        deviation = statistics.pstdev(chunk)
        if deviation == 0:
            scores.append(0.0)
            continue
        scores.append(round((value - statistics.fmean(chunk)) / deviation, 3))
    return scores


def is_anomalous(score, threshold=3.0):
    """Report whether the absolute score crosses the anomaly threshold."""
    return abs(float(score)) >= threshold


def flag_positions(scores, threshold=3.0):
    """Return the sample indices whose score crosses the threshold."""
    return [index for index, score in enumerate(scores) if is_anomalous(score, threshold)]


__all__ = ['rolling_zscore', 'is_anomalous', 'flag_positions']
