#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List, Optional

from rwhtn.config import write_json
from rwhtn.transform import dedupe_exact_highlights_in_place_order, sort_highlights_in_read_order


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Sort and dedupe exported highlights JSON.")
    parser.add_argument("in_json")
    parser.add_argument("out_json")
    parser.add_argument("--html-stream-json", default=None, help="Optional JSON file containing {'html_stream': ...}.")
    args = parser.parse_args(argv)

    with open(args.in_json, "r", encoding="utf-8") as f:
        highlights = json.load(f)
    if not isinstance(highlights, list):
        raise RuntimeError("Expected a JSON list of highlights.")

    html_stream = ""
    if args.html_stream_json:
        with open(args.html_stream_json, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if isinstance(payload, dict) and isinstance(payload.get("html_stream"), str):
            html_stream = payload["html_stream"]

    highlights = sort_highlights_in_read_order(highlights, html_stream)
    highlights = dedupe_exact_highlights_in_place_order(highlights)
    write_json(args.out_json, highlights)
    print(f"Wrote {args.out_json} ({len(highlights)} highlights)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
