from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests import exceptions as req_exc


READER_LIST_URL = "https://readwise.io/api/v3/list/"


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
            raise RuntimeError(f"Reader API request failed: {e}") from e
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


def fetch_reader_documents(
    *,
    token: str,
    location: Optional[str] = None,
    updated_after: Optional[str] = None,
    category: Optional[str] = None,
    tags: Tuple[str, ...] = (),
    with_html_content: bool = False,
    top_level_only: bool = False,
    page_limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    next_page_cursor: Optional[str] = None
    page_count = 0

    while True:
        if page_limit is not None and page_count >= page_limit:
            break
        page_count += 1

        params: Dict[str, Any] = {}
        if next_page_cursor:
            params["pageCursor"] = next_page_cursor
        if location:
            params["location"] = location
        if updated_after:
            params["updatedAfter"] = updated_after
        if category:
            params["category"] = category
        if tags:
            params["tag"] = list(tags)
        if with_html_content:
            params["withHtmlContent"] = "true"

        payload = _get_json(url=READER_LIST_URL, token=token, params=params)
        page_items = payload.get("results", [])
        if not isinstance(page_items, list):
            raise RuntimeError(f"Unexpected payload shape: {type(page_items)}")

        if top_level_only:
            page_items = [d for d in page_items if d.get("parent_id") in (None, "")]

        results.extend([d for d in page_items if isinstance(d, dict)])
        next_page_cursor = payload.get("nextPageCursor")
        if not next_page_cursor:
            break

    return results


def fetch_reader_document(
    *,
    token: str,
    document_id: str,
    with_html_content: bool = False,
) -> Dict[str, Any]:
    payload = _get_json(
        url=READER_LIST_URL,
        token=token,
        params={"id": document_id, "withHtmlContent": "true" if with_html_content else "false"},
    )
    results = payload.get("results") or []
    if not results or not isinstance(results, list):
        return {}
    first = results[0]
    return first if isinstance(first, dict) else {}
