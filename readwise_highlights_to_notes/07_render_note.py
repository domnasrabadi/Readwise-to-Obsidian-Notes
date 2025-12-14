#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List, Optional, Tuple

from rwhtn.render import render_markdown_note


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Render a Markdown note from metadata + highlights + headings.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-url", default="")
    parser.add_argument("--cover-image-url", default="")
    parser.add_argument("--frontmatter-json", required=True)
    parser.add_argument("--highlights-json", required=True)
    parser.add_argument("--headings-json", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    with open(args.frontmatter_json, "r", encoding="utf-8") as f:
        frontmatter = json.load(f)
    with open(args.highlights_json, "r", encoding="utf-8") as f:
        highlights = json.load(f)
    with open(args.headings_json, "r", encoding="utf-8") as f:
        headings_payload = json.load(f)

    headings = headings_payload.get("headings") if isinstance(headings_payload, dict) else []
    if not isinstance(headings, list):
        headings = []

    render_markdown_note(
        path=args.out,
        title=args.title,
        source_url=args.source_url,
        cover_image_url=args.cover_image_url,
        frontmatter=frontmatter if isinstance(frontmatter, dict) else {},
        highlights=highlights if isinstance(highlights, list) else [],
        headings=[(int(lvl), str(txt)) for (lvl, txt) in headings if isinstance(lvl, (int, str))],
    )
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
