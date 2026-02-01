import requests
import feedparser
from pathlib import Path

FEED_URL = "https://theherndonherald.substack.com/feed"
OUTPUT_FILE = Path("herndon_herald_posts.html")

def fetch_feed(url: str):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.content

def build_html_list(feed_bytes: bytes, max_items: int | None = None) -> str:
    feed = feedparser.parse(feed_bytes)
    entries = feed.entries

    if max_items is not None:
        entries = entries[:max_items]

    lines = []
    lines.append('<ul class="space-y-3 max-h-96 overflow-y-auto">')
    for entry in entries:
        title = entry.get("title", "").replace('"', "&quot;")
        link = entry.get("link", "#")
        line = (
            f'  <li>'
            f'<a href="{link}" target="_blank" '
            f'class="text-slate-700 hover:underline">{title}</a>'
            f'</li>'
        )
        lines.append(line)
    lines.append("</ul>")
    return "\n".join(lines)

def build_full_html(body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>The Herndon Herald Posts</title>
</head>
<body>
{body_html}
</body>
</html>
"""

def main():
    feed_bytes = fetch_feed(FEED_URL)
    ul_html = build_html_list(feed_bytes, max_items=None)  # set a number to limit
    full_html = build_full_html(ul_html)

    OUTPUT_FILE.write_text(full_html, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()
