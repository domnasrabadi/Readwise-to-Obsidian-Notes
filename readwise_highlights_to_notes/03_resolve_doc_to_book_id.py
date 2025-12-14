#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from typing import List, Optional

from rwhtn.config import try_load_dotenv
from rwhtn.readwise_api import fetch_all_books, resolve_book_id_for_source_url


def main(argv: Optional[List[str]] = None) -> int:
    try_load_dotenv()

    parser = argparse.ArgumentParser(description="Resolve a Reader document (source_url/title) to a Readwise book_id.")
    parser.add_argument("--token-env", default="READWISE_TOKEN")
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args(argv)

    token = os.environ.get(args.token_env)
    if not token:
        raise RuntimeError(f"Missing token env var {args.token_env!r}")

    books = fetch_all_books(token=token)
    book_id = resolve_book_id_for_source_url(books, args.source_url, args.title)
    if book_id is None:
        print("No match.")
        return 1
    print(book_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
