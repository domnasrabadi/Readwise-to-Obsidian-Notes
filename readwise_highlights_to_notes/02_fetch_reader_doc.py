#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from typing import List, Optional

from rwhtn.config import DEBUG_OUTPUT_DIR, coerce_bool, ensure_dir, try_load_dotenv, write_json
from rwhtn.reader_api import fetch_reader_document


def main(argv: Optional[List[str]] = None) -> int:
    try_load_dotenv()

    parser = argparse.ArgumentParser(description="Fetch one Reader document by id (optionally with html_content).")
    parser.add_argument("document_id")
    parser.add_argument("--token-env", default="READWISE_TOKEN")
    parser.add_argument("--with-html", type=coerce_bool, default=True)
    parser.add_argument("--out-dir", default=DEBUG_OUTPUT_DIR)
    args = parser.parse_args(argv)

    token = os.environ.get(args.token_env)
    if not token:
        raise RuntimeError(f"Missing token env var {args.token_env!r}")

    doc = fetch_reader_document(token=token, document_id=args.document_id, with_html_content=bool(args.with_html))
    out_dir = ensure_dir(args.out_dir)
    out_path = os.path.join(out_dir, f"reader_doc_{args.document_id}.json")
    write_json(out_path, doc)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
