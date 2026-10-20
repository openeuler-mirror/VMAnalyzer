"""Chi-square statistic for a 2x2 contingency table."""
import logging

LOG = logging.getLogger(__name__)


def expected(table):
    """Return the expected counts under independence for a 2x2 table."""
    (a, b), (c, d) = table
    row1, row2 = a + b, c + d
    col1, col2 = a + c, b + d
    total = row1 + row2
    if total == 0:
        return ((0.0, 0.0), (0.0, 0.0))
    return (
        (row1 * col1 / total, row1 * col2 / total),
        (row2 * col1 / total, row2 * col2 / total),
    )


def chi_square(table):
    """Return the chi-square statistic of a 2x2 contingency table."""
    (a, b), (c, d) = table
    expected_cells = expected(table)
    observed = ((a, b), (c, d))
    total = 0.0
    for row in range(2):
        for col in range(2):
            exp = expected_cells[row][col]
            if exp > 0:
                total += (observed[row][col] - exp) ** 2 / exp
    return total


def cramers_v(table):
    """Return Cramer's V effect size derived from the chi-square value."""
    (a, b), (c, d) = table
    total = a + b + c + d
    if total == 0:
        return 0.0
    return (chi_square(table) / total) ** 0.5


__all__ = ['expected', 'chi_square', 'cramers_v']
