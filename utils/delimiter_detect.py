"""Guess the field delimiter used by a block of delimited text."""
import logging

__all__ = ["detect_delimiter", "score_delimiters", "CANDIDATES"]

LOG = logging.getLogger(__name__)
CANDIDATES = (",", "\t", ";", "|", " ")


def score_delimiters(lines, candidates=CANDIDATES):
    """Return a mapping of candidate delimiter to consistency score."""
    scores = {}
    for delim in candidates:
        counts = [line.count(delim) for line in lines if line.strip()]
        if not counts or min(counts) == 0:
            continue
        scores[delim] = len(counts) / (1 + max(counts) - min(counts))
    return scores


def detect_delimiter(lines, candidates=CANDIDATES):
    """Return the most consistent delimiter, defaulting to a comma."""
    scores = score_delimiters(lines, candidates)
    if not scores:
        LOG.debug("no delimiter candidate produced a usable score")
        return ","
    return max(scores, key=scores.get)
