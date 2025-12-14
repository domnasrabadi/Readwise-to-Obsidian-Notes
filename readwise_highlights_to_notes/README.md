## readwise_highlights_to_notes

Tools to export Readwise Reader **Shortlist** items and turn their highlights into structured Markdown notes.

## What This Does (High-Level)

For each selected Readwise Reader document (usually from your Shortlist), the pipeline:

1. Pulls the target document metadata from Readwise Reader (and fetches `html_content` when needed).
2. Resolves the Reader document to a Readwise “book/article” `book_id` (best-effort match by `source_url`, fallback to title).
3. Exports highlights for that `book_id` via the Readwise export API.
4. Sorts highlights into reading order (primarily by numeric `location`).
5. Removes exact duplicates (common for duplicated image highlights).
6. Extracts HTML headings (`<h1..h6>`) from the document’s `html_content`.
7. Renders a Markdown note:
   - YAML frontmatter metadata
   - centered cover image (when present)
   - highlighted headings promoted to Markdown headings
   - other highlights as bullet points
   - image-only highlights as standalone blocks with whitespace around them

### Setup (uv)

From repo root:

- `uv add --project readwise_highlights_to_notes requests python-dotenv rich`
- `cp readwise_highlights_to_notes/.env.example readwise_highlights_to_notes/.env`
- Put your token into `readwise_highlights_to_notes/.env` (or export `READWISE_TOKEN` in your shell)

Note: if `uv add` fails on your machine, you can still run the scripts with system-installed packages as long as `requests` is available (it is on this machine).

## Run (Most Common)

Generate notes for everything in your Shortlist (top-level only):

```bash
uv run --project readwise_highlights_to_notes \
  python readwise_highlights_to_notes/08_make_notes.py \
  --all-shortlist
```

Generate notes for specific items (title substring match; multiple supported):

```bash
uv run --project readwise_highlights_to_notes \
  python readwise_highlights_to_notes/08_make_notes.py \
  "Product Evals in Three Simple Steps" \
  "Designing Machine Learning Systems"
```

Generate notes from a file (one title substring per line):

```bash
uv run --project readwise_highlights_to_notes \
  python readwise_highlights_to_notes/08_make_notes.py \
  --titles-file titles.txt
```

Re-run without overwriting notes that already exist:

```bash
uv run --project readwise_highlights_to_notes \
  python readwise_highlights_to_notes/08_make_notes.py \
  --all-shortlist \
  --skip-existing
```

Save debug intermediates (raw doc JSON, extracted headings, raw+sorted highlights):

```bash
uv run --project readwise_highlights_to_notes \
  python readwise_highlights_to_notes/08_make_notes.py \
  --all-shortlist \
  --debug
```

## Output Locations

- Final notes: `readwise_highlights_to_notes/10_output_notes/`
  - Filename is `slug(title).md` (no `highlights_` prefix).
- Debug intermediates (only with `--debug`): `readwise_highlights_to_notes/09_shortlist_outputs/<slug>/`
- Cache: `readwise_highlights_to_notes/11_cache/` (e.g., cached `books.json`)

## CLI Options (`08_make_notes.py`)

### Selection

- `--all-shortlist`
  - Generate notes for every top-level document currently in your Shortlist.
- `titles ...` (positional arguments)
  - One or more title *substrings* to match against Shortlist titles.
  - If a substring matches multiple docs, the run will report an ambiguity and skip that query.
- `--titles-file titles.txt`
  - Read title substrings from a file (one per line) and process them as if provided positionally.

### Scope / safety

- `--skip-existing`
  - If the note file already exists in `10_output_notes/`, do not overwrite it.
- `--limit N`
  - Process at most `N` selected documents (useful with `--all-shortlist` while iterating).
- `--include-children`
  - Include child documents (`parent_id` set). Default behavior is “top-level only”.

### Debugging

- `--debug`
  - Write intermediates to `09_shortlist_outputs/<slug>/`:
    - `reader_doc.json` (Reader doc with `html_content`)
    - `headings.json` (extracted headings + `html_stream`)
    - `highlights_raw.json` (raw highlights from export API)
    - `highlights_sorted.json` (sorted + deduped highlights)

### Authentication

- `--token-env NAME`
  - Env var name that holds your Readwise token (default: `READWISE_TOKEN`).
  - The scripts will load `readwise_highlights_to_notes/.env` if present (and also `readwise/.env` as a migration convenience).

## Other Step Scripts (Optional / Power-User)

These are thin CLIs useful for inspecting pipeline stages:

- `01_pull_from_shortlist.py`: pull shortlist + write snapshot files (MD/JSON) to a directory you choose
- `02_fetch_reader_doc.py`: fetch a single Reader doc by id and write JSON
- `03_resolve_doc_to_book_id.py`: resolve (`source_url`, `title`) → `book_id`
- `04_export_highlights.py`: export highlights for a `book_id` to JSON
- `05_sort_and_dedupe.py`: sort + dedupe a highlights JSON file
- `06_extract_headings.py`: extract headings (and build `html_stream`) from a saved Reader doc JSON
- `07_render_note.py`: render a note from prepared JSON inputs

Most of the time, you only need `08_make_notes.py`.
