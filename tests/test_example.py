"""Contract tests for the Docker Compose example."""

from html.parser import HTMLParser
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]


class PageContractParser(HTMLParser):
    """Collect the small HTML contract without browser dependencies."""

    def __init__(self) -> None:
        super().__init__()
        self.lang: str | None = None
        self.charset: str | None = None
        self.current_tag: str | None = None
        self.title: list[str] = []
        self.heading: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "html":
            self.lang = attributes.get("lang")
        elif tag == "meta" and "charset" in attributes:
            self.charset = attributes["charset"]
        self.current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        if self.current_tag == tag:
            self.current_tag = None

    def handle_data(self, data: str) -> None:
        if self.current_tag == "title":
            self.title.append(data)
        elif self.current_tag == "h1":
            self.heading.append(data)


def test_compose_file_matches_the_reviewed_contract() -> None:
    expected = dedent(
        """\
        name: xnova-compose-demo
        services:
          web:
            image: nginx:stable-alpine@sha256:0e52bd054126cdc040b1276c0af347aeb02a41b9cfe305d6094767ac30e97949
            ports:
              - "127.0.0.1:8080:80"
            volumes:
              - ./site:/usr/share/nginx/html:ro
        """
    )

    assert (ROOT / "compose.yaml").read_text(encoding="utf-8") == expected


def test_index_page_matches_the_http_contract() -> None:
    parser = PageContractParser()
    parser.feed((ROOT / "site" / "index.html").read_text(encoding="utf-8"))

    assert parser.lang == "ru"
    assert parser.charset == "utf-8"
    assert "".join(parser.title).strip() == "Compose demo"
    assert "".join(parser.heading).strip() == "Compose работает"
