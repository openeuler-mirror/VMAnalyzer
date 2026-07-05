"""VM risk summary CLI."""

from __future__ import annotations

import json
import sys
from collections import Counter


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    items = json.load(open(argv[0], encoding="utf-8")) if argv else []
    tags = []
    for item in items:
        tags.extend(item.get("risk_tags", []))
    print(json.dumps(dict(Counter(tags)), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

