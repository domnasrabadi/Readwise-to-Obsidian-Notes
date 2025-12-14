#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Any, Dict, List, Optional

from rwhtn.config import DEBUG_OUTPUT_DIR, coerce_bool, ensure_dir, iso_now, try_load_dotenv, write_json
from rwhtn.reader_api import fetch_reader_documents


def summarize(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_location: Dict[str, int] = {}
    by_category: Dict[str, int] = {}
    top_level = 0
    child = 0
    with_html = 0

    for d in documents:
        location = d.get("location") or ""
        category = d.get("category") or ""
        by_location[location] = by_location.get(location, 0) + 1
        by_category[category] = by_category.get(category, 0) + 1
        if d.get("parent_id") in (None, ""):
            top_level += 1
        else:
            child += 1
        if isinstance(d.get("html_content"), str) and d["html_content"].strip():
            with_html += 1

    return {
        "count": len(documents),
        "top_level": top_level,
        "children": child,
        "with_html_content": with_html,
        "by_location": dict(sorted(by_location.items(), key=lambda kv: (-kv[1], kv[0]))),
        "by_category": dict(sorted(by_category.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


def write_markdown(path: str, documents: List[Dict[str, Any]], meta: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Reader shortlist snapshot\n\n")
        f.write(f"- Queried at: `{meta.get('queried_at','')}`\n")
        f.write(f"- Summary: `{meta.get('summary',{})}`\n\n")

        f.write("| # | title | category | source_url | updated_at | id |\n")
        f.write("|---:|---|---|---|---|---|\n")
        for idx, d in enumerate(documents, start=1):
            title = (d.get("title") or "").replace("\n", " ").strip()
            category = (d.get("category") or "").strip()
            source_url = (d.get("source_url") or "").strip()
            updated_at = (d.get("updated_at") or "").strip()
            doc_id = (d.get("id") or "").strip()
            f.write(f"| {idx} | {title} | {category} | {source_url} | {updated_at} | {doc_id} |\n")


def main(argv: Optional[List[str]] = None) -> int:
    try_load_dotenv()

    parser = argparse.ArgumentParser(description="Pull Readwise Reader shortlist and write snapshot files.")
    parser.add_argument("--token-env", default="READWISE_TOKEN")
    parser.add_argument("--location", default="shortlist")
    parser.add_argument("--with-html", type=coerce_bool, default=False)
    parser.add_argument("--top-level-only", type=coerce_bool, default=True)
    parser.add_argument("--page-limit", type=int, default=None)
    parser.add_argument("--out-dir", default=DEBUG_OUTPUT_DIR)
    args = parser.parse_args(argv)

    import os

    token = os.environ.get(args.token_env)
    if not token:
        raise RuntimeError(f"Missing token env var {args.token_env!r}")

    out_dir = ensure_dir(args.out_dir)
    docs = fetch_reader_documents(
        token=token,
        location=args.location,
        with_html_content=bool(args.with_html),
        top_level_only=bool(args.top_level_only),
        page_limit=args.page_limit,
    )

    meta = {"queried_at": iso_now(), "summary": summarize(docs)}
    write_json(f"{out_dir}/shortlist_snapshot.json", {"meta": meta, "documents": docs})
    write_markdown(f"{out_dir}/shortlist_snapshot.md", docs, meta)
    print(f"Wrote shortlist snapshot to {out_dir}/shortlist_snapshot.* ({len(docs)} docs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
