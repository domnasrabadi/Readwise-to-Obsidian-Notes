from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

from rwhtn.config import iso_now
from rwhtn.transform import is_image_only_highlight, norm, norm_heading, strip_heading_prefix


def _yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _yaml_line(key: str, value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        if not value.strip():
            return None
        return f"{key}: {_yaml_quote(value)}"
    if isinstance(value, bool):
        return f"{key}: {'true' if value else 'false'}"
    if isinstance(value, (int, float)):
        return f"{key}: {value}"
    return f"{key}: {_yaml_quote(json.dumps(value, ensure_ascii=False))}"


def render_markdown_note(
    *,
    path: str,
    title: str,
    source_url: str,
    cover_image_url: str,
    frontmatter: Dict[str, Any],
    highlights: List[Dict[str, Any]],
    headings: List[Tuple[int, str]],
) -> None:
    ordered_headings = [(lvl, txt, norm_heading(txt)) for (lvl, txt) in headings]

    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        for k in sorted(frontmatter.keys()):
            line = _yaml_line(k, frontmatter.get(k))
            if line:
                f.write(line + "\n")
        f.write("---\n\n")

        f.write(f"# {title}\n\n")

        if cover_image_url:
            f.write('<div align="center">\n')
            f.write(f'  <img src="{cover_image_url}" width="220" />\n')
            f.write("</div>\n\n")

        if source_url:
            f.write(f"Source: {source_url}\n\n")

        f.write(f"Exported at: `{iso_now()}`\n\n")

        heading_index = 0
        for h in highlights:
            text = h.get("text") or ""
            if not isinstance(text, str):
                continue
            text = " ".join(text.split())
            if not text:
                continue
            text_norm = norm_heading(text)

            matched: Optional[Tuple[int, str]] = None
            if ordered_headings:
                for j in range(heading_index, len(ordered_headings)):
                    lvl, heading_text, heading_norm = ordered_headings[j]
                    if heading_norm == text_norm:
                        matched = (lvl, heading_text)
                        heading_index = j + 1
                        break
                if matched is None:
                    for lvl, heading_text, heading_norm in ordered_headings:
                        if heading_norm == text_norm:
                            matched = (lvl, heading_text)
                            break

            if matched:
                html_level, heading_text = matched
                if html_level == 1 and norm(heading_text) == norm(title):
                    continue
                md_level = min(6, html_level + 1)
                f.write(f"\n{'#' * md_level} {strip_heading_prefix(heading_text)}\n\n")
                continue

            if is_image_only_highlight(text):
                f.write(f"\n{text}\n\n")
            else:
                f.write(f"- {text}\n")

