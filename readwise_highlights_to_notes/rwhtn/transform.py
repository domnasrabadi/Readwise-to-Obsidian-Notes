from __future__ import annotations

import os
import re
import urllib.parse
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

from rwhtn.config import compact_whitespace


def strip_markdown(text: str) -> str:
    text = text or ""
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)  # images
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # links
    text = text.replace("`", "")
    text = text.replace("**", "").replace("*", "").replace("__", "").replace("_", "")
    return compact_whitespace(text)


def image_basename_from_markdown_image(markdown_image: str) -> Optional[str]:
    match = re.search(r"!\[[^\]]*\]\(([^)]+)\)", markdown_image or "")
    if not match:
        return None
    url = match.group(1)

    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    inner = query.get("url", [None])[0]
    url_for_name = urllib.parse.unquote(inner) if inner else url
    try:
        path = urllib.parse.urlparse(url_for_name).path
        base = os.path.basename(path)
        return base or None
    except Exception:
        return None


def is_image_only_highlight(text: str) -> bool:
    return bool(re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", (text or "").strip()))


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._level: Optional[int] = None
        self._buf: List[str] = []
        self.headings: List[Tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._level = int(tag[1])
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if self._level is None:
            return
        if tag != f"h{self._level}":
            return
        text = compact_whitespace("".join(self._buf))
        if text:
            self.headings.append((self._level, text))
        self._level = None
        self._buf = []

    def handle_data(self, data: str) -> None:
        if self._level is not None:
            self._buf.append(data)


class HtmlStreamParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag != "img":
            return
        attr_map = {k: v for k, v in attrs}
        src = attr_map.get("src") or attr_map.get("data-src")
        if not src:
            return

        base = ""
        try:
            parsed = urllib.parse.urlparse(src)
            query = urllib.parse.parse_qs(parsed.query)
            inner = query.get("url", [None])[0]
            if inner:
                inner = urllib.parse.unquote(inner)
                base = os.path.basename(urllib.parse.urlparse(inner).path)
            if not base:
                base = os.path.basename(parsed.path)
        except Exception:
            base = ""

        if base:
            self.parts.append(f" [IMG:{base}] ")

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)


def extract_headings_from_html(html: str) -> List[Tuple[int, str]]:
    if not html or not isinstance(html, str):
        return []
    parser = HeadingParser()
    parser.feed(html)
    return parser.headings


def build_html_stream(html: str) -> str:
    if not html or not isinstance(html, str):
        return ""
    parser = HtmlStreamParser()
    parser.feed(html)
    return compact_whitespace(" ".join(parser.parts))


def norm(value: str) -> str:
    return compact_whitespace(value).strip().lower()


def norm_heading(value: str) -> str:
    value = compact_whitespace(value).strip()
    value = re.sub(r"^\(?\s*\d+(?:\.\d+)*\s*\)?\s+", "", value)
    value = re.sub(
        r"^\(?\s*[ivxlcdm]+(?:\.[ivxlcdm]+)*\s*\)?\s+",
        "",
        value,
        flags=re.IGNORECASE,
    )
    return value.strip().lower()


def strip_heading_prefix(value: str) -> str:
    value = compact_whitespace(value).strip()
    stripped = re.sub(r"^\(?\s*\d+(?:\.\d+)*\s*\)?\s+", "", value)
    stripped = re.sub(
        r"^\(?\s*[ivxlcdm]+(?:\.[ivxlcdm]+)*\s*\)?\s+",
        "",
        stripped,
        flags=re.IGNORECASE,
    )
    return stripped.strip() or value


def sort_highlights_in_read_order(highlights: List[Dict[str, Any]], html_stream: str) -> List[Dict[str, Any]]:
    location_type = None
    for h in highlights:
        if h.get("location_type"):
            location_type = h.get("location_type")
            break

    def effective_offset(h: Dict[str, Any]) -> int:
        try:
            loc_i = int(h.get("location"))
        except Exception:
            loc_i = 10**18

        if loc_i not in (0, 10**18):
            return loc_i

        if location_type == "offset" and html_stream:
            text = h.get("text") or ""
            if isinstance(text, str) and "![](" in text:
                base = image_basename_from_markdown_image(text)
                if base:
                    pos = html_stream.find(f"[IMG:{base}]")
                    if pos >= 0:
                        return pos
        return loc_i

    def key(h: Dict[str, Any]) -> Tuple[int, str]:
        highlighted_at = h.get("highlighted_at") or ""
        return (effective_offset(h), highlighted_at if isinstance(highlighted_at, str) else "")

    return sorted(highlights, key=key)


def dedupe_exact_highlights_in_place_order(highlights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen: set[Tuple[Any, ...]] = set()
    deduped: List[Dict[str, Any]] = []
    for h in highlights:
        key = (h.get("text"), h.get("location_type"), h.get("location"), h.get("end_location"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(h)
    return deduped

