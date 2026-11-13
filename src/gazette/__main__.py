
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import requests

from gazette.rss import parse_rss


def main():
    url = os.getenv("RSS_URL")

    if not url:
        raise RuntimeError("La variable RSS_URL est obligatoire")

    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "M2OPS-CPD/0.1"}
    )
    response.raise_for_status()

    articles = parse_rss(response.content)

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_file = output_dir / f"articles-{timestamp}.json"

    output_file.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"{len(articles)} articles enregistrés : {output_file}")


if __name__ == "__main__":
    main()
