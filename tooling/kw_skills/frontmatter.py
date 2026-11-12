"""Minimal, strict SKILL.md frontmatter parser (no PyYAML dependency).

Supports: `key: value` scalars (optionally quoted) and one level of nested
mapping (used for `metadata:`). Anything else is reported as an error rather
than silently misread.
"""
from __future__ import annotations

import re

_KEY = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse(text: str) -> tuple[dict, str, list[str]]:
    """Return (frontmatter, body, errors)."""
    errors: list[str] = []
    text = text.lstrip("﻿").replace("\r\n", "\n")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text, ["file must start with a '---' frontmatter line"]
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text, ["frontmatter is not closed with '---'"]
    fm: dict = {}
    current: str | None = None
    for n, raw in enumerate(lines[1:end], start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[0] in " \t"
        if indented:
            m = _KEY.match(raw.strip())
            if current is None or not isinstance(fm.get(current), dict) or not m:
                errors.append(f"line {n}: unsupported indented construct")
                continue
            fm[current][m.group(1)] = _unquote(m.group(2))
            continue
        m = _KEY.match(raw)
        if not m:
            errors.append(f"line {n}: not a 'key: value' pair")
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ("|", ">", "|-", ">-") or val.startswith(("[", "{")):
            errors.append(f"line {n}: block scalars/flow collections are not supported; use a plain string")
            continue
        if key in fm:
            errors.append(f"line {n}: duplicate key '{key}'")
        if val == "":
            fm[key] = {}
            current = key
        else:
            fm[key] = _unquote(val)
            current = None
    return fm, "\n".join(lines[end + 1 :]), errors
