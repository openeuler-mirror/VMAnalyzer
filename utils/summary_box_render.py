"""Draw a simple ASCII box around a short summary block.

Status output pasted into tickets reads better inside a bordered box.  The
renderer measures every line so multi-byte width drift does not break the
right border.
"""

import logging
from typing import Iterable, List

LOG = logging.getLogger(__name__)


def render_box(lines: Iterable[str], title: str = "", width: int = 0) -> List[str]:
    """Return boxed lines with an optional title on the top border."""
    content = [str(line) for line in lines]
    inner = max([width] + [len(line) for line in content] + [len(title) + 2])
    rendered: List[str] = []
    if title:
        rendered.append("+" + title.center(inner + 2, "-") + "+")
    else:
        rendered.append("+" + "-" * (inner + 2) + "+")
    for line in content:
        rendered.append("| " + line.ljust(inner) + " |")
    rendered.append("+" + "-" * (inner + 2) + "+")
    LOG.debug("rendered summary box with %d content line(s)", len(content))
    return rendered


def render_key_values(pairs: Iterable[tuple], title: str = "") -> List[str]:
    """Render a key/value summary inside a box."""
    lines = ["{}: {}".format(key, value) for key, value in pairs]
    return render_box(lines, title)


__all__ = ["render_box", "render_key_values"]
