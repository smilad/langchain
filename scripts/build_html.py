"""Render every repo .md to a readable .html next to it.

Run: uv run --with markdown python scripts/build_html.py
"""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"superpowers", ".venv", ".git", "node_modules", ".pytest_cache"}

CSS = """
:root{--bg:#fff;--fg:#1f2328;--mut:#59636e;--bd:#d1d9e0;--code:#f6f8fa;--a:#0969da}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--mut:#9198a1;--bd:#3d444d;--code:#161b22;--a:#4493f8}}
body{background:var(--bg);color:var(--fg);font:17px/1.7 -apple-system,system-ui,sans-serif;margin:0}
main{max-width:50rem;margin:0 auto;padding:1.5rem 1rem 4rem}
h1{font-size:2rem;border-bottom:1px solid var(--bd);padding-bottom:.3em}
h2{margin-top:2rem;border-bottom:1px solid var(--bd);padding-bottom:.2em}
a{color:var(--a)}
code{background:var(--code);padding:.15em .35em;border-radius:4px;font-size:.88em}
pre{background:var(--code);padding:1rem;border-radius:8px;overflow-x:auto}
pre code{padding:0;background:none}
table{border-collapse:collapse;display:block;overflow-x:auto}
th,td{border:1px solid var(--bd);padding:.4rem .7rem;text-align:left}
th{background:var(--code)}
blockquote{margin-left:0;padding-left:1rem;border-left:4px solid var(--bd);color:var(--mut)}
nav{font-size:.9rem;color:var(--mut);margin-bottom:1rem}
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{css}</style></head>
<body><main><nav><a href="{home}">Lesson index</a>{prev}{next}</nav>{body}</main></body></html>
"""

# ./x.md, ../x.md#frag -> .html (external URLs untouched)
LINK = re.compile(r'(href="(?!\w+:|#)[^"]*?)\.md((?:#[^"]*)?")')


def slug(value: str, sep: str) -> str:
    """GitHub-style heading ids so #fragment links match the .md rendering."""
    value = re.sub(r"[^\w\- ]", "", value.lower()).strip()
    return value.replace(" ", sep)


def main() -> None:
    n = 0
    order = sorted(
        p for p in (ROOT / "lessons").glob("[0-9][0-9]_*/[0-9][0-9].md")
    )
    pos = {p: i for i, p in enumerate(order)}
    for md in ROOT.rglob("*.md"):
        if SKIP & set(md.relative_to(ROOT).parts):
            continue
        text = md.read_text(encoding="utf-8")
        body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "toc"], extension_configs={"toc": {"slugify": slug}})
        body = LINK.sub(r"\1.html\2", body)
        m = re.search(r"^#\s+(.+)$", text, re.M)
        home = Path(
            __import__("os").path.relpath(ROOT / "lessons" / "README.html", md.parent)
        ).as_posix()
        prev = nxt = ""
        if md in pos:
            rel = lambda q: __import__("os").path.relpath(q.with_suffix(".html"), md.parent)
            i = pos[md]
            if i > 0:
                prev = f' · <a href="{rel(order[i - 1])}">&larr; Previous</a>'
            if i < len(order) - 1:
                nxt = f' · <a href="{rel(order[i + 1])}">Next &rarr;</a>'
        md.with_suffix(".html").write_text(
            PAGE.format(title=m.group(1) if m else md.stem, css=CSS, home=home, prev=prev, next=nxt, body=body),
            encoding="utf-8",
        )
        n += 1
    print(f"wrote {n} html files")


if __name__ == "__main__":
    main()
