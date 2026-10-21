"""Build QEMU guest agent ``guest-exec`` request payloads safely.

Agent commands are passed through JSON, so quoting bugs break the guest
call.  This builder escapes arguments and always returns the exact JSON
string expected by ``virsh qemu-agent-command``.
"""

import json
import logging
from typing import Iterable, List, Optional

LOG = logging.getLogger(__name__)


def build_exec(command: str, arguments: Optional[Iterable[str]] = None,
               capture_output: bool = True) -> str:
    """Return a guest-exec payload JSON string for *command*."""
    argv: List[str] = [command] + [str(value) for value in (arguments or [])]
    payload = {
        "execute": "guest-exec",
        "arguments": {
            "path": argv[0],
            "arg": argv[1:],
            "capture-output": bool(capture_output),
        },
    }
    encoded = json.dumps(payload, separators=(",", ":"))
    LOG.debug("built guest-exec payload for %s with %d argument(s)",
              command, len(argv) - 1)
    return encoded


def shell_exec(script: str, shell: str = "/bin/sh") -> str:
    """Wrap a shell snippet into a guest-exec payload."""
    return build_exec(shell, ["-c", script])


def unwrap_pid(response: str) -> Optional[int]:
    """Extract the pid from a guest-exec response payload."""
    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        LOG.warning("guest-exec response is not valid JSON")
        return None
    pid = parsed.get("return", {}).get("pid")
    return int(pid) if isinstance(pid, int) else None


__all__ = ["build_exec", "shell_exec", "unwrap_pid"]
