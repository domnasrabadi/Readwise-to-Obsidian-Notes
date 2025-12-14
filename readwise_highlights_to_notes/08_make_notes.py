#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from typing import List, Optional

from rwhtn.config import coerce_bool, try_load_dotenv
from rwhtn.orchestrate import find_shortlist_docs_by_queries, load_shortlist_and_books, load_title_file, make_note_for_doc, TargetDoc


def _get_printer():
    try:
        from rich.console import Console  # type: ignore
        from rich.markup import escape  # type: ignore

        console = Console()

        def _print_ok(title: str, rest: str) -> None:
            console.print(f"[green][OK][/green] [blue]{escape(title)}[/blue]{escape(rest)}")

        def _print_fail(title: str, rest: str) -> None:
            console.print(f"[red][FAIL][/red] [blue]{escape(title)}[/blue]{escape(rest)}")

        def _print_err(message: str) -> None:
            console.print(f"[red]{escape(message)}[/red]", highlight=False)

        def _print_plain(message: str) -> None:
            console.print(escape(message), highlight=False)

        return _print_ok, _print_fail, _print_err, _print_plain
    except Exception:
        def _print_ok(title: str, rest: str) -> None:
            print(f"[OK] {title}{rest}")

        def _print_fail(title: str, rest: str) -> None:
            print(f"[FAIL] {title}{rest}", file=os.sys.stderr)

        def _print_err(message: str) -> None:
            print(message, file=os.sys.stderr)

        def _print_plain(message: str) -> None:
            print(message)

        return _print_ok, _print_fail, _print_err, _print_plain


def main(argv: Optional[List[str]] = None) -> int:
    try_load_dotenv()
    print_ok, print_fail, print_err, print_plain = _get_printer()

    parser = argparse.ArgumentParser(description="Generate structured Markdown notes from Readwise Reader shortlist.")
    parser.add_argument("titles", nargs="*", help="One or more title substrings to match in shortlist.")
    parser.add_argument("--titles-file", default=None, help="File containing one title substring per line.")
    parser.add_argument("--all-shortlist", action="store_true", help="Generate notes for every top-level item in Shortlist.")
    parser.add_argument("--debug", action="store_true", help="Write intermediates to 09_shortlist_outputs/ (per-doc).")
    parser.add_argument("--skip-existing", action="store_true", help="Skip writing notes that already exist in 10_output_notes/.")
    parser.add_argument(
        "--include-children",
        action="store_true",
        help="Include child documents (parent_id set). Default is top-level only.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Limit number of docs processed (useful with --all-shortlist).")
    parser.add_argument("--token-env", default="READWISE_TOKEN")
    args = parser.parse_args(argv)

    token = os.environ.get(args.token_env)
    if not token:
        raise RuntimeError(f"Missing token env var {args.token_env!r}")

    try:
        shortlist, books = load_shortlist_and_books(token=token, top_level_only=(not args.include_children))
    except RuntimeError as e:
        print_err(str(e))
        return 1

    targets: List[TargetDoc] = []
    errors: List[str] = []

    if args.all_shortlist:
        for d in shortlist:
            title = (d.get("title") or "").strip()
            if not title:
                continue
            targets.append(
                TargetDoc(
                    reader_doc_id=(d.get("id") or "").strip(),
                    title=title,
                    source_url=(d.get("source_url") or "").strip(),
                )
            )
    else:
        title_queries: List[str] = list(args.titles or [])
        if args.titles_file:
            title_queries.extend(load_title_file(args.titles_file))
        targets, errors = find_shortlist_docs_by_queries(shortlist, title_queries)

    if args.limit is not None:
        targets = targets[: max(0, int(args.limit))]

    if not targets:
        for e in errors:
            print_err(e)
        print_err("No documents selected.")
        return 1

    ok = 0
    failed = 0
    for t in targets:
        out_path, err = make_note_for_doc(
            token=token,
            target=t,
            books=books,
            debug=args.debug,
            skip_existing=args.skip_existing,
        )
        if err:
            failed += 1
            print_fail(t.title, f": {err}")
            continue
        ok += 1
        print_ok(t.title, f" -> {out_path}")

    for e in errors:
        print_err(e)

    print_plain(f"Done. ok={ok}, failed={failed}, total={len(targets)}")
    return 0 if failed == 0 and not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
