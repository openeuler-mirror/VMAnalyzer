"""VM health summary CLI."""

from __future__ import annotations

import json
import sys


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    items = json.load(open(argv[0], encoding="utf-8")) if argv else []
    scores = [float(item.get("health_score", 0.0)) for item in items]
    avg = sum(scores) / len(scores) if scores else 0.0
    print(json.dumps({"count": len(scores), "avg_health_score": avg}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

