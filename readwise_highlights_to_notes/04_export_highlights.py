#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from typing import List, Optional

from rwhtn.config import DEBUG_OUTPUT_DIR, ensure_dir, try_load_dotenv, write_json
from rwhtn.readwise_api import export_highlights_for_book_id


def main(argv: Optional[List[str]] = None) -> int:
    try_load_dotenv()

    parser = argparse.ArgumentParser(description="Export highlights for a Readwise book_id.")
    parser.add_argument("book_id", type=int)
    parser.add_argument("--token-env", default="READWISE_TOKEN")
    parser.add_argument("--out-dir", default=DEBUG_OUTPUT_DIR)
    args = parser.parse_args(argv)

    token = os.environ.get(args.token_env)
    if not token:
        raise RuntimeError(f"Missing token env var {args.token_env!r}")

    highlights = export_highlights_for_book_id(token=token, book_id=int(args.book_id))
    out_dir = ensure_dir(args.out_dir)
    out_path = os.path.join(out_dir, f"highlights_{args.book_id}.json")
    write_json(out_path, highlights)
    print(f"Wrote {out_path} ({len(highlights)} highlights)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
