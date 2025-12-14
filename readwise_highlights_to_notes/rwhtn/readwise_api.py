from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional

import requests
from requests import exceptions as req_exc

from rwhtn.config import CACHE_DIR, ensure_dir, write_json


READWISE_BOOKS_URL = "https://readwise.io/api/v2/books/"
READWISE_EXPORT_URL = "https://readwise.io/api/v2/export/"


def _sleep_backoff(attempt: int, retry_after_seconds: Optional[int]) -> None:
    if retry_after_seconds is not None and retry_after_seconds > 0:
        time.sleep(retry_after_seconds)
        return
    time.sleep(min(30, 1.5**attempt))


def _get_json(
    *,
    url: str,
    token: str,
    params: Dict[str, Any],
    timeout: int = 60,
    max_retries: int = 10,
) -> Dict[str, Any]:
    attempt = 0
    while True:
        try:
            resp = requests.get(url, params=params, headers={"Authorization": f"Token {token}"}, timeout=timeout)
        except req_exc.RequestException as e:
            raise RuntimeError(f"Readwise API request failed: {e}") from e
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            retry_after_seconds = int(retry_after) if retry_after and retry_after.isdigit() else None
            attempt += 1
            if attempt > max_retries:
                raise RuntimeError("Hit rate limit repeatedly (429); aborting.")
            _sleep_backoff(attempt, retry_after_seconds)
            continue
        resp.raise_for_status()
        payload = resp.json()
        return payload if isinstance(payload, dict) else {"results": payload}


def _books_cache_path() -> str:
    ensure_dir(CACHE_DIR)
    return os.path.join(CACHE_DIR, "books.json")


def _books_cache_is_fresh(path: str, max_age_seconds: int) -> bool:
    try:
        st = os.stat(path)
        return (time.time() - st.st_mtime) <= max_age_seconds
    except Exception:
        return False


def fetch_all_books(
    *,
    token: str,
    max_pages: int = 200,
    use_cache: bool = True,
    cache_max_age_seconds: int = 24 * 60 * 60,
) -> List[Dict[str, Any]]:
    cache_path = _books_cache_path()
    if use_cache and _books_cache_is_fresh(cache_path, cache_max_age_seconds):
        try:
            import json

            with open(cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if isinstance(cached, dict) and isinstance(cached.get("results"), list):
                return [b for b in cached["results"] if isinstance(b, dict)]
        except Exception:
            pass

    results: List[Dict[str, Any]] = []
    page = 1
    while page <= max_pages:
        payload = _get_json(url=READWISE_BOOKS_URL, token=token, params={"page": page})
        page_results = payload.get("results") or []
        if not isinstance(page_results, list) or not page_results:
            break
        results.extend([b for b in page_results if isinstance(b, dict)])
        if not payload.get("next"):
            break
        page += 1

    if use_cache:
        write_json(cache_path, {"fetched_at": time.time(), "results": results})

    return results


def resolve_book_id_for_source_url(books: List[Dict[str, Any]], source_url: str, title: str) -> Optional[int]:
    source_url_norm = (source_url or "").strip()
    title_norm = (title or "").strip().lower()

    for b in books:
        if (b.get("source_url") or "").strip() == source_url_norm and source_url_norm:
            try:
                return int(b["id"])
            except Exception:
                return None

    for b in books:
        if (b.get("title") or "").strip().lower() == title_norm and title_norm:
            try:
                return int(b["id"])
            except Exception:
                return None

    return None


def book_by_id(books: List[Dict[str, Any]], book_id: int) -> Optional[Dict[str, Any]]:
    for b in books:
        try:
            if int(b.get("id")) == int(book_id):
                return b
        except Exception:
            continue
    return None


def export_highlights_for_book_id(*, token: str, book_id: int) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    next_page_cursor: Optional[str] = None
    while True:
        params: Dict[str, Any] = {"ids": str(book_id)}
        if next_page_cursor:
            params["pageCursor"] = next_page_cursor
        payload = _get_json(url=READWISE_EXPORT_URL, token=token, params=params)
        results.extend(payload.get("results", []) if isinstance(payload.get("results"), list) else [])
        next_page_cursor = payload.get("nextPageCursor")
        if not next_page_cursor:
            break

    if not results:
        return []
    first = results[0] if isinstance(results[0], dict) else {}
    highlights = first.get("highlights") or []
    return highlights if isinstance(highlights, list) else []
