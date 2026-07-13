#!/usr/bin/env python3
"""Repository quality checks for awesome-leetcode-patterns.

Enforces the three invariants this repo is built on:

  1. No em dashes or en dashes anywhere in the Markdown (house style).
  2. Every relative .md link resolves to a file that exists.
  3. Every fenced ```python block compiles (syntax only, not executed).

Run locally with `python3 scripts/check.py`. Exits non-zero on any failure, so
it doubles as the CI gate. No third-party dependencies: compile() parses without
importing, so blocks that import sortedcontainers still pass.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EM_EN = ("—", "–")            # em dash, en dash
LINK_RE = re.compile(r"(?<!\!)\]\((?!https?://)([^)#]+\.md)(?:#[^)]*)?\)")
IMG_RE = re.compile(r"!\[[^\]]*\]\((?!https?://)([^)#]+)(?:#[^)]*)?\)")
PY_RE = re.compile(r"```python\n(.*?)```", re.S)


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def rel(path):
    return os.path.relpath(path, ROOT)


def check_dashes(failures):
    for path in md_files():
        text = open(path, encoding="utf-8").read()
        for lineno, line in enumerate(text.splitlines(), 1):
            for ch in EM_EN:
                if ch in line:
                    name = "em dash" if ch == "—" else "en dash"
                    failures.append(f"{rel(path)}:{lineno}: contains an {name}")


def check_links(failures):
    for path in md_files():
        base = os.path.dirname(path)
        text = open(path, encoding="utf-8").read()
        for m in LINK_RE.finditer(text):
            target = os.path.normpath(os.path.join(base, m.group(1)))
            if not os.path.isfile(target):
                failures.append(f"{rel(path)}: broken link -> {m.group(1)}")


def check_images(failures):
    for path in md_files():
        base = os.path.dirname(path)
        text = open(path, encoding="utf-8").read()
        for m in IMG_RE.finditer(text):
            target = os.path.normpath(os.path.join(base, m.group(1)))
            if not os.path.isfile(target):
                failures.append(f"{rel(path)}: broken image -> {m.group(1)}")


def check_python(failures):
    for path in md_files():
        text = open(path, encoding="utf-8").read()
        for m in PY_RE.finditer(text):
            code = m.group(1)
            try:
                compile(code, rel(path), "exec")
            except SyntaxError as e:
                failures.append(f"{rel(path)}: python block does not compile "
                                f"(line {e.lineno}: {e.msg})")


def main():
    failures = []
    check_dashes(failures)
    check_links(failures)
    check_images(failures)
    check_python(failures)

    if failures:
        print(f"FAIL: {len(failures)} issue(s) found\n")
        for f in failures:
            print("  " + f)
        return 1

    n_md = sum(1 for _ in md_files())
    print(f"OK: {n_md} markdown files pass (no em/en dashes, links resolve, "
          f"python compiles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
