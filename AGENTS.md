# AGENTS.md

This repository is a personal knowledge management (PKM) workflow project focused on
turning Readwise Reader highlights into structured, Obsidian-ready Markdown notes with
minimal manual cleanup.

## End goal

- Preserve document structure (headings, sections, images) when exporting highlights
- Produce clean Markdown notes that align with the Obsidian vault conventions
- Keep the pipeline modular, readable, and easy to extend
- Optionally add LLM-based enhancements later (tags, summaries, formatting variants)

## Top-level layout

- `readwise_highlights_to_notes/`
  - Main Python pipeline and CLI scripts
  - Generates the final notes into `readwise_highlights_to_notes/10_output_notes/`
- `00_context/`
  - Context and instructions for the Obsidian vault layout and formatting
- `00_plan_and_progress/`
  - Project planning notes and options documents
- `99_archive/`
  - Historical or archived material
- `README.md`
  - High-level project context, goals, workflow, and constraints
- `TODO.md`
  - Next steps and possible improvements

## Pipeline overview (readwise_highlights_to_notes)

The pipeline turns Readwise Reader documents (often from the Shortlist) into
structured Markdown notes:

1. Fetch Reader document metadata and HTML content
2. Resolve the Reader document to a Readwise book/article `book_id`
3. Export highlights for that `book_id`
4. Sort highlights into reading order
5. Remove exact duplicates
6. Extract headings from HTML content
7. Render Markdown with frontmatter, headings, bullets, and images

### Key entry points

- `readwise_highlights_to_notes/08_make_notes.py`
  - Primary CLI to generate notes
- `readwise_highlights_to_notes/rwhtn/orchestrate.py`
  - Main orchestration logic
- `readwise_highlights_to_notes/rwhtn/transform.py`
  - Highlight sorting, deduping, heading extraction
- `readwise_highlights_to_notes/rwhtn/render.py`
  - Markdown rendering logic

### Output and debug locations

- Final notes: `readwise_highlights_to_notes/10_output_notes/`
- Debug intermediates: `readwise_highlights_to_notes/09_shortlist_outputs/<slug>/`
- Cache: `readwise_highlights_to_notes/11_cache/`

## Obsidian vault conventions

Details live in `00_context/agents_md_for_obsidian_vault.md`, which defines:

- Vault structure and folder purposes
- Formatting and indentation rules for notes
- Flashcard creation guidance and templates

## Known pain points (context)

- Readwise exports can lose structural context, increasing manual cleanup time
- Some highlights can have missing or zero `location` values, which can affect
  ordering for specific documents

## Future enhancements (from TODO)

- LLM tag suggestions based on note content
- Summarization depth options (brief, moderate, detailed)
- Formatting style variants for notes

