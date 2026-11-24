#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun entry.

Writes one quiet, earned moment of pride (a single line, 1 to 240
characters) to /output/entry.txt. Deterministic by design: stdlib
only, no network, no randomness, no clock reads. Two runs produce
byte-identical output.
"""

import os
import sys

# The line is assembled from its two halves so the moment's structure
# stays visible in the code: the setup holds the small, hard-won
# action (threading the needle first try at seventy-three), the
# landing reveals the long effort behind it (a kebaya started the
# year her husband died). Neither half lands alone; the pride is
# earned by the decades between them.
_CLAUSE_SETUP = "At seventy-three, Ibu Sari threaded the needle on her first try"
_CLAUSE_LANDING = "and finished the kebaya she had started the year her husband died."

MAX_LINE_CHARS = 240  # competition ceiling for the single line


def validate_line(line: str) -> None:
    """Per-rule validation for the gate: 1-240 chars, one line, not blank."""
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if len(line) < 1 or len(line) > MAX_LINE_CHARS:
        raise ValueError(
            "line is %d chars, outside the 1-%d range"
            % (len(line), MAX_LINE_CHARS)
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")


def build_line() -> str:
    """Join the two clauses into the one line of earned pride.

    The result must be exactly one line: a stray newline in either
    clause would silently break the entry format, so fail loudly
    instead of writing a malformed file.
    """
    line = _CLAUSE_SETUP + " " + _CLAUSE_LANDING
    validate_line(line)
    return line


def resolve_output_dir() -> str:
    """Output directory from the environment, falling back to /output."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value if value else "/output"


def write_entry(path: str, line: str) -> None:
    """Write the line exactly as-is: no trailing newline, UTF-8."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def main(argv=None) -> int:
    line = build_line()
    if len(line) > MAX_LINE_CHARS:
        print(
            "error: line is %d chars, over the %d-char limit"
            % (len(line), MAX_LINE_CHARS),
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
