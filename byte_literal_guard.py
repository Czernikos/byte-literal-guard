#!/usr/bin/env python3
"""Reject direct non-ASCII characters inside Python byte-string literals."""
from __future__ import annotations

import argparse
import io
import re
import sys
import tokenize
from pathlib import Path
from typing import Iterable


PREFIX = re.compile(r"(?i)^([rubf]*)")
SKIP_PARTS = {".git", ".venv", "__pycache__"}


def python_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if not path.exists():
            raise FileNotFoundError("input path does not exist: {}".format(path))
        if path.is_file():
            if path.suffix == ".py":
                yield path
            continue
        for candidate in path.rglob("*.py"):
            if not SKIP_PARTS.intersection(candidate.parts):
                yield candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    arguments = parser.parse_args()
    failures = []
    checked = 0
    for path in python_files(arguments.paths):
        checked += 1
        with tokenize.open(path) as stream:
            source = stream.read()
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type != tokenize.STRING:
                continue
            prefix = PREFIX.match(token.string).group(1).casefold()
            if "b" in prefix and any(ord(character) > 127 for character in token.string):
                failures.append("{}:{}".format(path, token.start[0]))
    if failures:
        raise SystemExit("non-ascii-byte-literal:" + ",".join(failures))
    if checked == 0:
        raise ValueError("no Python files selected")
    print("byte-literal-guard: PASS ({} Python files)".format(checked))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, UnicodeError, SyntaxError, tokenize.TokenError, ValueError) as exc:
        print("byte-literal-guard: ERROR: {}".format(exc), file=sys.stderr)
        raise SystemExit(2)
