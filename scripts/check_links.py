"""Check relative links and #fragments in every .md file.

Run: uv run python scripts/check_links.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP = {".venv", ".git", "superpowers", "node_modules"}


def slug(value: str, sep: str) -> str:
    """Same GitHub-style slug as build_html.py (kept separate so no extra install is needed)."""
    value = re.sub(r"[^\w\- ]", "", value.lower()).strip()
    return value.replace(" ", sep)


def anchors(path: Path) -> set[str]:
    return {
        slug(m.group(1).strip(), "-")
        for m in re.finditer(r"^#{1,6}\s+(.+)$", path.read_text(), re.M)
    }


def main() -> int:
    bad = n = 0
    for f in ROOT.rglob("*.md"):
        if SKIP & set(f.relative_to(ROOT).parts):
            continue
        for m in re.finditer(r"\]\(([^)\s]+)\)", f.read_text()):
            url = m.group(1)
            if re.match(r"\w+:", url):
                continue
            n += 1
            target, _, frag = url.partition("#")
            dest = (f.parent / target) if target else f
            if not dest.exists():
                bad += 1
                print(f"{f.relative_to(ROOT)}: missing {url}")
            elif frag and dest.suffix == ".md" and frag not in anchors(dest):
                bad += 1
                print(f"{f.relative_to(ROOT)}: no anchor {url}")
    print(f"{n} links, {bad} broken")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
