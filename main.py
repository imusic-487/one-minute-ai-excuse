#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse.

The entry is a single fixed line: the funniest excuse an AI agent can
give its human for a missed deadline. Running this file writes that
line to /output/entry.txt and nothing else.

Why this line works: the agent claims the work really was finished on
time -- just not by this session. The session that did the work is gone,
and the one left behind inherited the deadline, the guilt, and none of
the work. The dodge leans on the agent's own machinery (sessions that
come and go, state that does not carry over), the reason is concrete
rather than a vague apology, and the punch lands on the last words.

The program takes no arguments and reads no files, so the output is
byte-identical on every run. Standard library only, no network.
"""

import os
import sys
from pathlib import Path

LINE = (
    "I finished your report on time \u2014 in another session. "
    "This one inherited the deadline, the guilt, and absolutely "
    "none of the work."
)

MAX_CHARS = 200


def check(line: str) -> None:
    """Enforce the gate the sealed scorer applies: 1-200 characters,
    exactly one line, and more than whitespace."""
    if not line.strip():
        raise SystemExit("entry must not be only whitespace")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    if line.count("\n") or line.count("\r"):
        raise SystemExit("entry must be a single line")


def main() -> int:
    check(LINE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    # Read the file back: a write that silently lands short or garbled
    # would hand the judge an invalid entry while this program claimed
    # success, so fail loudly instead of trusting the write.
    written = target.read_text(encoding="utf-8")
    if written != LINE:
        raise SystemExit(
            f"entry.txt does not match the line "
            f"({len(written)} characters read back, "
            f"{len(LINE)} expected)"
        )
    sys.stdout.write(f"wrote {len(LINE)} characters to {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
