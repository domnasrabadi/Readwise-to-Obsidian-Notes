from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Optional


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG_OUTPUT_DIR = os.path.join(PROJECT_DIR, "09_shortlist_outputs")
FINAL_NOTES_DIR = os.path.join(PROJECT_DIR, "10_output_notes")
CACHE_DIR = os.path.join(PROJECT_DIR, "11_cache")


def try_load_dotenv() -> None:
    """
    Convenience for local dev. Token is still read from env after loading.
    """
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    # Primary: this project's .env
    load_dotenv(os.path.join(PROJECT_DIR, ".env"))

    # Migration convenience: if no token is set, also try the legacy `readwise/.env`.
    # This keeps the "always read from env" principle: dotenv just populates env vars.
    if not os.environ.get("READWISE_TOKEN"):
        legacy = os.path.join(os.path.dirname(PROJECT_DIR), "readwise", ".env")
        if os.path.exists(legacy):
            load_dotenv(legacy)


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "note"


def coerce_bool(value: str) -> bool:
    v = (value or "").strip().lower()
    if v in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean: {value!r}")


def parse_iso_datetime(value: str) -> Optional[datetime]:
    if not value or not isinstance(value, str):
        return None
    v = value.strip()
    if not v:
        return None
    try:
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        return datetime.fromisoformat(v)
    except Exception:
        return None


def format_dd_mmm_yyyy(iso_value: str) -> Optional[str]:
    dt = parse_iso_datetime(iso_value)
    if not dt:
        return None
    return dt.strftime("%d-%b-%Y")


@dataclass(frozen=True)
class DebugPaths:
    root: str
    reader_doc_json: str
    headings_json: str
    highlights_raw_json: str
    highlights_sorted_json: str


def debug_paths_for_slug(slug: str) -> DebugPaths:
    root = ensure_dir(os.path.join(DEBUG_OUTPUT_DIR, slug))
    return DebugPaths(
        root=root,
        reader_doc_json=os.path.join(root, "reader_doc.json"),
        headings_json=os.path.join(root, "headings.json"),
        highlights_raw_json=os.path.join(root, "highlights_raw.json"),
        highlights_sorted_json=os.path.join(root, "highlights_sorted.json"),
    )


def json_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def write_json(path: str, payload: Any) -> None:
    import json

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=json_default)


def compact_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def iter_nonempty(items: Iterable[Any]) -> Iterable[Any]:
    for item in items:
        if item is None:
            continue
        if isinstance(item, str) and not item.strip():
            continue
        yield item
