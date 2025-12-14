# Refactor Plan (Dec 15, 2025) — `readwise_highlights_to_notes/`

This document captures the refactor/restructure plan for the Readwise “Shortlist → structured notes” tooling we built in `readwise/` on Dec 13, 2025.

## Goals

- Create a clean, modular, easy-to-extend pipeline that turns Readwise Reader **Shortlist** items into structured Markdown notes.
- Keep the “reading order” accurate across doc types (article / pdf / epub) by primarily trusting Readwise highlight `location`.
- Promote *highlighted headings* into real Markdown headings (H2/H3/…).
- Include the document cover image at the top when available.
- Support:
  - generating notes for **multiple titles** in one command
  - generating notes for **every item in Shortlist**
  - saving intermediary artifacts only when `--debug` is set
- Adopt `uv` for environment + dependency management.

## New Project Location

All new code and outputs live under a new folder at repo root:

- `readwise_highlights_to_notes/`

We will keep the existing `readwise/` folder as the “reference implementation” until parity is confirmed.

## Directory Layout (Proposed)

```
readwise_highlights_to_notes/
  pyproject.toml
  README.md
  .env              # local only (gitignored); READWISE_TOKEN is read from env
  .env.example      # template committed
  .gitignore

  rwhtn/
    config.py
    reader_api.py
    readwise_api.py
    transform.py
    render.py
    orchestrate.py

  01_pull_from_shortlist.py
  02_fetch_reader_doc.py
  03_resolve_doc_to_book_id.py
  04_export_highlights.py
  05_sort_and_dedupe.py
  06_extract_headings.py
  07_render_note.py
  08_make_notes.py            # main orchestrator

  09_shortlist_outputs/       # debug-only intermediates
  10_output_notes/            # final notes always written here
  11_cache/                   # optional cached books + resolution maps
```

### Output naming rules

- Final notes: `readwise_highlights_to_notes/10_output_notes/<slug>.md`
- No redundant `highlights_` prefix (e.g., `product_evals_in_three_simple_steps.md`)

### Debug/intermediary artifacts

Only written when `--debug` is set.

Suggested per-document structure:

```
readwise_highlights_to_notes/09_shortlist_outputs/<slug>/
  reader_doc.json
  headings.json
  highlights_raw.json
  highlights_sorted.json
```

## `uv` Usage

We will manage the project dependencies with `uv`:

- Initialize the project: `uv init readwise_highlights_to_notes --app --vcs none`
- Add dependencies (expected): `uv add requests python-dotenv rich`
- Run scripts via uv:
  - `uv run --project readwise_highlights_to_notes python readwise_highlights_to_notes/08_make_notes.py "Designing Machine Learning Systems"`
  - `uv run --project readwise_highlights_to_notes python readwise_highlights_to_notes/08_make_notes.py --all-shortlist --debug`

## Pipeline Steps (Modular Responsibilities)

We’ll split work into I/O-only API clients, pure transforms, and thin CLIs.

### Shared modules (imported by step scripts)

Implementation note: Python can’t import modules whose filenames start with digits, so the reusable code lives in the `rwhtn/` package and the numbered scripts are thin CLIs.

- `rwhtn/config.py`
  - reads `READWISE_TOKEN` from environment (required)
  - loads local `.env` (optional convenience) via `python-dotenv`
  - slugify, time formatting helpers, path helpers, debug flags

- `rwhtn/reader_api.py` (Readwise Reader API)
  - `GET https://readwise.io/api/v3/list/`:
    - shortlist listing (paged by `nextPageCursor`)
    - fetch single document by `id` with optional `withHtmlContent=true`

- `rwhtn/readwise_api.py` (Readwise “classic” API)
  - `GET https://readwise.io/api/v2/books/` (paged list)
  - `GET https://readwise.io/api/v2/export/?ids=<book_id>` (highlights export)
  - optional: caching books list in `11_cache/books.json`

- `rwhtn/transform.py`
  - ordering:
    - trust numeric `location` whenever non-zero
    - for `location == 0` image highlights (common in some web sources), optionally fall back to HTML-image-position heuristic
  - dedupe exact duplicates (not “same text elsewhere”): drop later highlights keyed by `(text, location_type, location, end_location)`
  - parse headings from Reader `html_content` (`<h1..h6>`)
  - heading matching normalization (strip PDF-style numeric prefixes, normalize whitespace/case)

- `rwhtn/render.py`
  - render Markdown note with:
    - YAML frontmatter (see below)
    - centered cover image block (if present)
    - “Source” line
    - highlights rendered in reading order:
      - promoted headings become real markdown headings (title remains `#`)
      - image-only highlights rendered as standalone blocks (no bullets) with whitespace above/below

### Step scripts (thin CLIs)

- `01_pull_from_shortlist.py`
  - snapshot shortlist (and, optionally, include `html_content`)
  - writes snapshots only in `--debug` mode

- `08_make_notes.py` (main)
  - Accepts:
    - multiple title substrings as args
    - `--titles-file`
    - `--all-shortlist`
  - For each selected doc:
    1) fetch Reader doc (with html) to obtain `html_content`, `image_url`, metadata
    2) resolve Reader doc → Readwise `book_id` (prefer exact `source_url`, fallback to title match)
    3) export highlights
    4) sort + dedupe
    5) extract headings from HTML, promote matching highlighted headings
    6) render to `10_output_notes/<slug>.md`
  - `--debug` controls writing intermediates to `09_shortlist_outputs/`

## Note Frontmatter (YAML)

Each note should start with YAML frontmatter to make Obsidian indexing/search easier.

Recommended fields (initial):
- `title`
- `author` (prefer Reader author)
- `category` (article/pdf/epub/…)
- `site_name` (when present)
- `source_url`
- `reader_doc_id`
- `readwise_book_id`
- `shortlist_added` (from Reader `last_moved_at`, formatted `DD-MMM-YYYY`; no time)
- `exported_at` (script run time, ISO8601)
- `highlights_count`
- `cover_image_url` (when present)

## Compatibility / Parity Checks

After refactor:
- Regenerate known notes and confirm:
  - heading promotion still works
  - images are ordered correctly and rendered as non-bulleted blocks
  - epub ordering respects earlier chapters
  - duplicate image highlights are removed

## Open Follow-ups (Not part of refactor)

- Optional “assign highlights to nearest heading even if heading itself wasn’t highlighted”
- Better Reader doc → Readwise book id resolution (persistent cache; stronger matching)
- Batch “all shortlist” reporting summary (success/fail counts, ambiguous matches, etc.)
