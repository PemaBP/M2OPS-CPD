
import re
from datetime import UTC
from email.utils import parsedate_to_datetime
from html import unescape

import feedparser


def parse_rss(content: bytes) -> list[dict]:
    feed = feedparser.parse(content)

    if feed.bozo and not feed.entries:
        raise ValueError("Flux RSS invalide")

    articles = []

    for entry in feed.entries:
        title = unescape(entry.get("title", "")).strip()
        link = entry.get("link", "").strip()
        description = entry.get("summary", "")

        excerpt = re.sub(r"<[^>]+>", "", description)
        excerpt = unescape(excerpt).strip()

        published = entry.get("published", "")
        published_at = None

        if published:
            try:
                date = parsedate_to_datetime(published)
                if date.tzinfo is None:
                    date = date.replace(tzinfo=UTC)
                published_at = date.isoformat()
            except (ValueError, TypeError, IndexError):
                pass

        if title and link:
            articles.append({
                "title": title,
                "excerpt": excerpt[:300],
                "link": link,
                "published_at": published_at,
            })

    return articles
