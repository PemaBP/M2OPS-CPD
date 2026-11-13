
from pathlib import Path

from gazette.rss import parse_rss


def test_parse_rss():
    fixture = Path("tests/fixtures/sample.xml").read_bytes()
    articles = parse_rss(fixture)

    assert len(articles) == 1
    assert articles[0]["title"] == "Actualité en Bretagne"
    assert articles[0]["link"] == "https://example.org/article-1"
    assert articles[0]["excerpt"] == "Un exemple de résumé."
    assert articles[0]["published_at"] == "2026-11-13T06:00:00+00:00"


def test_invalid_rss():
    try:
        parse_rss(b"<rss><broken>")
    except ValueError:
        return

    raise AssertionError("Le flux invalide aurait dû être rejeté")
