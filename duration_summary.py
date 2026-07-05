"""Duration summary CLI."""

from __future__ import annotations

import json
import sys


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    data = json.load(open(argv[0], encoding="utf-8")) if argv else []
    print(json.dumps({"count": len(data)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

