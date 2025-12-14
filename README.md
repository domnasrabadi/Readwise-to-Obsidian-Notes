# Personal Knowledge Management Context

## Problem Statement
- Build a repeatable, high-signal workflow for capturing, distilling, and retaining insights across data science, AI, psychology, finance, communication, soft skills, productivity, and similar domains.
- Ensure material can be prioritized, structured, and converted into long-term learning assets (notes + flashcards) with minimal friction.

## Content Sources & Intake
- Heavy use of Readwise Reader (RR) to import EPUB/PDF technical books (O'Reilly, Manning, AI Engineering, Hands-On ML, etc.), research papers, and diverse web content (articles, blogs, tweets, practical tips such as ClaudeCode or flashcard techniques).
- Personal library is extensive; can provide catalog if needed for future automation or recommendations.
- RR enables categorization, tagging, and annotation (highlights, inline notes, tags) at read time.

## Tagging & Progress Tracking
- Tag system in RR reflects both topical categories and workflow status (examples: `highlights_finished`, `notes_began`, `notes_finished`, `flashcards_todo`, `flashcards_done`).
- Tags primarily act as personal reminders of reading/note state rather than metadata that must survive downstream automation.

## Reading, Annotation, and Distillation
1. Prioritize what to read next based on interest + importance tags.
2. Read inside RR, highlight/annotate aggressively to capture raw signal.
3. Export highlights manually or via Obsidian sync.
4. Refine exports into polished Markdown notes inside Obsidian using preferred structure: headings/subheadings, bullet hierarchies, code blocks, inline + block math, emphasis/highlights, embedded images/diagrams.
5. For standout resources (books, research papers, exceptional articles) perform progressive distillation passes to condense into even higher-signal artifacts.

## Pain Points & Opportunities
- Highlight exports arrive as flat, line-delimited text with no trace of original structure (TOC, callouts, section context), so manual cleanup to reach a workable outline consumes the most time.
- Need to preserve highlight context (chapter/section/heading) to produce high-quality, distilled notes on the first pass.
- After the initial draft, additional refinement/cleanup is common, further extending cycle time.
- Reading backlog exceeds available time; prioritization relies on tags + gut feel but still feels difficult.

## Metadata Fidelity Requirements
- RR workflow tags mainly communicate personal status (in-progress, note started, note finished, flashcard to-do/done) and do not need long-term preservation.
- Future tooling should focus on richer structural context (chapters, headings, callouts, embedded assets) rather than faithfully mirroring RR tag sets.

## Obsidian Vault Structure
- Vault layout described in `agents_md_for_obsidian_vault.md`:
  - `01 Books/` and `02 In Progress Books/` store finalized syntheses and active chapter work respectively.
  - `03 Technical Notes/`, `04 Personal/`, `05 Paper Notes (readwise)/`, and `07 Readwise/` separate technical research, personal material, paper imports, and article highlights.
  - `06 Learning System/` captures workflows, prompts, and tools; `100 ⌛️ Backlog to process/` holds triaged items awaiting processing.
- Subfolder icon prefixes communicate priority/status; archives exist inside most areas for completed artifacts.
- Supporting docs (e.g., `Hotkeys, Mac apps & keyboard shortcuts.md`, `Running note list.md`) act as meta indexes and productivity aids.

## Templates & Formatting Conventions
- Flashcard creation instructions emphasize atomic Q/A pairs, clarity, and progressive elaboration (see Section 2.1 of `agents_md_for_obsidian_vault.md`).
- Note-formatting guidance (Section 2.3) defines bullet-first structure, indentation depth, casing rules, punctuation, math formatting, and consistent rhythm (title → concepts → examples).
- Future tooling should allow selecting a preferred template (or skipping to live-edit) when transforming highlights so the user can decide how prescriptive the structure is per note.
- These templates should be mirrored by any automation so generated notes slot directly into the vault without reformatting.

## Flashcard Workflow & Cadence
- RemNote holds the master flashcard deck; new cards are drafted after polishing a note.
- Target throughput: ~10 cards per day because of limited review time.
- Selection criteria favor foundational, technical content tied to work (classification metrics, LLM engineering practices, algorithm mechanics, etc.).

## Scale & Prioritization
- Typical intake: 1–5 books/month and 5–20 articles/month, with an existing backlog inside Readwise Reader.
- After triaging, each item gets a priority tag and only 2–5 items are actively pushed forward at once.
- The bottleneck is transforming highlights into structured notes fast enough to keep pace with intake.

## Flashcard Creation (Optional)
- When deeper mastery is desired, revisit the finished note and extract key concepts into flashcards stored in RemNote.
- Follow personal flashcard templates/instructions to maximize spaced-repetition effectiveness.

## Asset Handling
- Notes embed local assets via Obsidian wiki links (e.g., `![[image-file.png]]`) and rely on CSS snippets (`| center | 600`) for alignment/sizing.
- Automation must preserve these references and optionally apply consistent sizing/centering directives when importing figures, screenshots, or diagrams so visual context is not lost.

_This document is a living brief; we will refine it as more details emerge._
