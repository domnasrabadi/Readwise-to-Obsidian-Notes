from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from rwhtn.config import (
    FINAL_NOTES_DIR,
    debug_paths_for_slug,
    ensure_dir,
    format_dd_mmm_yyyy,
    iso_now,
    slugify,
    write_json,
)
from rwhtn.reader_api import fetch_reader_document, fetch_reader_documents
from rwhtn.readwise_api import book_by_id, export_highlights_for_book_id, fetch_all_books, resolve_book_id_for_source_url
from rwhtn.render import render_markdown_note
from rwhtn.transform import build_html_stream, dedupe_exact_highlights_in_place_order, extract_headings_from_html, sort_highlights_in_read_order


@dataclass(frozen=True)
class TargetDoc:
    reader_doc_id: str
    title: str
    source_url: str


def find_shortlist_docs_by_queries(shortlist: List[Dict[str, Any]], queries: List[str]) -> Tuple[List[TargetDoc], List[str]]:
    targets: List[TargetDoc] = []
    errors: List[str] = []

    for query in queries:
        q = (query or "").strip().lower()
        if not q:
            continue
        matches: List[TargetDoc] = []
        for d in shortlist:
            title = (d.get("title") or "").strip()
            if not title or q not in title.lower():
                continue
            matches.append(
                TargetDoc(
                    reader_doc_id=(d.get("id") or "").strip(),
                    title=title,
                    source_url=(d.get("source_url") or "").strip(),
                )
            )

        if not matches:
            errors.append(f"No Shortlist matches for title containing: {query!r}")
            continue
        if len(matches) > 1:
            lines = [f"Ambiguous title query {query!r}; matches:"]
            for m in matches:
                lines.append(f"- {m.title} | {m.source_url} | id={m.reader_doc_id}")
            errors.append("\n".join(lines))
            continue

        targets.append(matches[0])

    return targets, errors


def load_title_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def frontmatter_for(
    *,
    reader_doc: Dict[str, Any],
    book: Optional[Dict[str, Any]],
    book_id: int,
    highlights_count: int,
    cover_image_url: str,
) -> Dict[str, Any]:
    title = (reader_doc.get("title") or "").strip()
    author = (reader_doc.get("author") or "").strip()
    category = (reader_doc.get("category") or "").strip()
    site_name = (reader_doc.get("site_name") or "").strip()
    source_url = (reader_doc.get("source_url") or "").strip()
    reader_url = (reader_doc.get("url") or "").strip()

    shortlist_added = format_dd_mmm_yyyy((reader_doc.get("last_moved_at") or "").strip())
    published_date = (reader_doc.get("published_date") or "").strip()

    return {
        "author": author or ((book or {}).get("author") or "").strip(),
        "category": category or ((book or {}).get("category") or "").strip(),
        "highlights_count": highlights_count,
        "published_date": published_date or ((book or {}).get("published_date") or ""),
        "shortlist_added": shortlist_added,
        "title": title or ((book or {}).get("title") or ""),
    }


def make_note_for_doc(
    *,
    token: str,
    target: TargetDoc,
    books: List[Dict[str, Any]],
    debug: bool,
    skip_existing: bool,
) -> Tuple[Optional[str], Optional[str]]:
    reader_doc = fetch_reader_document(token=token, document_id=target.reader_doc_id, with_html_content=True)
    if not reader_doc:
        return None, f"Failed to fetch reader doc: {target.reader_doc_id}"

    book_id = resolve_book_id_for_source_url(books, target.source_url, target.title)
    if book_id is None:
        return None, (
            "Could not resolve a Readwise book/article id for this Shortlist item "
            f"(title={target.title!r}, source_url={target.source_url!r})."
        )

    raw_highlights = export_highlights_for_book_id(token=token, book_id=book_id)

    html = reader_doc.get("html_content") or ""
    html = html if isinstance(html, str) else ""
    headings = extract_headings_from_html(html)
    html_stream = build_html_stream(html)

    highlights = sort_highlights_in_read_order(raw_highlights, html_stream)
    highlights = dedupe_exact_highlights_in_place_order(highlights)

    cover_image_url = (reader_doc.get("image_url") or "").strip()
    book = book_by_id(books, book_id)
    if not cover_image_url and book:
        cover_image_url = (book.get("cover_image_url") or "").strip()

    out_dir = ensure_dir(FINAL_NOTES_DIR)
    slug = slugify(target.title)
    out_path = os.path.join(out_dir, f"{slug}.md")

    if skip_existing and os.path.exists(out_path):
        return out_path, None

    if debug:
        dp = debug_paths_for_slug(slug)
        write_json(dp.reader_doc_json, reader_doc)
        write_json(dp.headings_json, {"headings": headings, "html_stream": html_stream})
        write_json(dp.highlights_raw_json, raw_highlights)
        write_json(dp.highlights_sorted_json, highlights)

    frontmatter = frontmatter_for(
        reader_doc=reader_doc,
        book=book,
        book_id=book_id,
        highlights_count=len(highlights),
        cover_image_url=cover_image_url,
    )

    render_markdown_note(
        path=out_path,
        title=target.title,
        source_url=target.source_url,
        cover_image_url=cover_image_url,
        frontmatter=frontmatter,
        highlights=highlights,
        headings=headings,
    )

    return out_path, None


def load_shortlist_and_books(*, token: str, top_level_only: bool) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    shortlist = fetch_reader_documents(
        token=token,
        location="shortlist",
        with_html_content=False,
        top_level_only=top_level_only,
    )
    books = fetch_all_books(token=token, use_cache=True)
    return shortlist, books
