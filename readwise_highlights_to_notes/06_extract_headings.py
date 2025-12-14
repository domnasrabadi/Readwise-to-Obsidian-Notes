#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import List, Optional

from rwhtn.config import write_json
from rwhtn.transform import build_html_stream, extract_headings_from_html


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Extract headings from a Reader document JSON (with html_content).")
    parser.add_argument("reader_doc_json")
    parser.add_argument("out_json")
    args = parser.parse_args(argv)

    with open(args.reader_doc_json, "r", encoding="utf-8") as f:
        doc = json.load(f)
    if not isinstance(doc, dict):
        raise RuntimeError("Expected a Reader document JSON object.")

    html = doc.get("html_content") or ""
    headings = extract_headings_from_html(html if isinstance(html, str) else "")
    html_stream = build_html_stream(html if isinstance(html, str) else "")
    write_json(args.out_json, {"headings": headings, "html_stream": html_stream})
    print(f"Wrote {args.out_json} ({len(headings)} headings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
