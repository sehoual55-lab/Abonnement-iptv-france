#!/usr/bin/env python3
"""Swap the placeholder domain for the real one across the whole site.

Usage:  python3 _sources/set_domain.py exemple.fr

Prints a replacement count per file per pattern, so a silent miss is visible.
"""
import sys, pathlib

PLACEHOLDER = "votre-domaine.fr"
ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTS = {".html", ".xml", ".txt", ".webmanifest"}

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: set_domain.py <nouveau-domaine.fr>")
    new = sys.argv[1].strip().replace("https://", "").replace("http://", "").rstrip("/")

    total = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTS:
            continue
        if "_sources" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        n = text.count(PLACEHOLDER)
        rel = path.relative_to(ROOT)
        print(f"{rel}: {PLACEHOLDER!r} -> {new!r} : {n} replacement(s)")
        if n:
            path.write_text(text.replace(PLACEHOLDER, new), encoding="utf-8")
            total += n

    print(f"\nTotal: {total} replacement(s) across the site.")
    if total == 0:
        print("WARNING: nothing replaced — the placeholder may already be gone.")

if __name__ == "__main__":
    main()
