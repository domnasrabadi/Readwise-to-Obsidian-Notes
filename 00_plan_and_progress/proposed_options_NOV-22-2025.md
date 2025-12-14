# Proposed PKM Automation Options (22 Nov)

## Summary Ranking (Impact vs Effort)
| Rank | Option | Impact | Build Effort | Why it’s placed here |
| --- | --- | --- | --- | --- |
| 1 | 7. RR → Obsidian Auto-Outline | High | Low | Fastest lift, directly fixes missing structure in exports and drops notes into the vault templates. |
| 2 | 4. Obsidian-Only Automation (Templater/Dataview) | Medium-High | Low | Lives where you work; minimal setup; good structure gains without extra apps. |
| 3 | 8. Guided Note Builder (Light UI) | High | Medium | Keeps human control, trims cleanup time; moderate UI lift. |
| 4 | 10. Flashcard-First Pipeline | Medium | Medium | Accelerates mastery pipeline; some parsing/RemNote sync needed. |
| 5 | 11. Backlog Triage Dashboard | Medium | Medium | Improves prioritization/WIP; mostly orchestration UI. |
| 6 | 1. Custom CLI + Obsidian Plugin | Medium | Medium-High | More code than #7 for similar outcomes due to plugin layer. |
| 7 | 5. Shortcut/Alfred Workflow + LLM API | Medium | Medium | Quick to operate but adds API costs/latency; relies on good prompting. |
| 8 | 9. Live “Distill As You Read” | High | Medium-High | Great context preservation; RR integration/UI makes it heavier. |
| 9 | 6. Embedded EPUB Reader + Live Note Pane | Medium | Medium-High | Strong for EPUBs; limited coverage and UI maintenance. |
| 10 | 2. Desktop Electron App | Medium-High | High | Best UX but heavy build/packaging overhead. |
| 11 | 3. Web Service + Browser Dashboard | Medium | High | Always-on ops/auth costs for modest incremental benefit over local tools. |

## 1. Custom CLI + Obsidian Plugin
- **How it works:** local CLI ingests Readwise exports, reconstructs outline context, applies chosen note template, and emits structured Markdown plus flashcard suggestions; companion Obsidian plugin provides sidebar tweaks/status updates.
- **Interaction:** run terminal command (`process-highlights <file>`), then fine-tune via Obsidian panel; prompts allow per-note template selection.
- **Feasibility:** moderate engineering (Python parser + TypeScript plugin); no external dependencies beyond Readwise export files.
- **Cost:** none (local tooling).
- **Tradeoffs:** fast to prototype; limited GUI polish; still requires manual export steps and terminal familiarity.

## 2. Desktop Electron App
- **How it works:** drag-and-drop highlights into Electron UI; app parses context, previews structured note, lets you rearrange sections, select template, embed assets, and push outputs to Obsidian/RemNote.
- **Interaction:** GUI workflow with live preview, toggles for template choice, inline editing before finalizing.
- **Feasibility:** higher effort (frontend + backend parsing logic, packaging); still entirely local.
- **Cost:** none for runtime, but larger build/maintenance investment.
- **Tradeoffs:** best UX and lowest friction, yet heavier codebase, packaging across OS versions, and more upkeep.

## 3. Web Service + Browser Dashboard
- **How it works:** backend (FastAPI/Next.js) receives highlights via Readwise API/webhook, enriches structure (optionally with LLM), stores drafts; browser dashboard lets you review, edit, choose template, and sync to Obsidian/RemNote via APIs.
- **Interaction:** log into dashboard, manage queue of pending notes, approve and push with one click.
- **Feasibility:** high complexity (hosting, auth, storage, syncing); requires ongoing ops.
- **Cost:** hosting + any LLM usage; consider privacy/security controls.
- **Tradeoffs:** accessible anywhere, supports continuous automation, but introduces recurring costs and data-handling concerns.

## 4. Obsidian-Only Automation (Templater/Dataview Scripts)
- **How it works:** leverage existing Obsidian plugins/scripts to ingest Readwise sync files, run JavaScript transformations to apply templates, and prompt user inside Obsidian to finalize notes/flashcards.
- **Interaction:** trigger commands via palette or hotkeys; dialogs appear inside Obsidian for template selection and edits.
- **Feasibility:** low-to-moderate effort, limited to Obsidian scripting APIs.
- **Cost:** none.
- **Tradeoffs:** stays in current tool, minimal setup, but constrained by plugin capabilities and harder to integrate advanced parsing/AI.

## 5. Shortcut/Alfred Workflow + LLM API
- **How it works:** macOS Shortcut or Alfred workflow grabs latest export, calls local script that hits an LLM (e.g., OpenAI/Claude) to restructure highlights per template, then writes Markdown into Obsidian and drafts flashcards.
- **Interaction:** single hotkey to kick off automation; prompts allow quick adjustments; outputs show up directly in target folders.
- **Feasibility:** moderate (automation scripting + API integration); dependent on reliable prompts and network access.
- **Cost:** recurring LLM API charges; potential privacy considerations.
- **Tradeoffs:** very fast to operate and leverages powerful structuring, but tied to third-party APIs and their costs/latency.

## 6. Embedded EPUB Reader + Live Note Pane (Reader3 Fork)
- **How it works:** build on [`karpathy/reader3`](https://github.com/karpathy/reader3) to render EPUBs locally; main pane shows book, side pane is a Markdown editor. Selecting text/images inserts them directly into the note with pre-set formatting options (bullets, numbered lists, image centering/sizing).
- **Interaction:** drop EPUB into app, read in browser/desktop GUI, highlight spans, and watch note build in real time; optionally edit/format on the fly and export straight to Obsidian.
- **Feasibility:** moderate—core EPUB rendering/highlighting already exists; need to extend note-pane features and Obsidian export integration.
- **Cost:** none (local, open source).
- **Tradeoffs:** eliminates export cleanup by combining reading + note drafting; limited to material viewable in the app and requires UI maintenance, but keeps data local and tightly aligned with your workflow.

## 7. RR → Obsidian Auto-Outline
- **How it works:** our own local parser (not an existing plugin) ingests RR exports (or API pulls), reconstructs TOC/section context, applies your preferred note template, and writes structured Markdown into the right vault folder; optional flashcard suggestions generated alongside. Obsidian glue is minimal (e.g., command/hotkey to run the script).
- **Interaction:** run a single command (`process-highlights <source> --template <name>`) and review the drafted note in Obsidian; can offer a prompt to pick a template per run.
- **Feasibility:** low-to-moderate—pure local parsing plus template mapping; extend later with LLM assist if needed.
- **Cost:** none.
- **Tradeoffs:** fastest lift and keeps current flow; quality depends on how well we infer structure from exports and reliably map headings.

## 8. Guided Note Builder (Light UI)
- **How it works:** small CLI or desktop UI loads RR highlights for one source, shows TOC + highlights grouped by section, and lets you drag/drop or checkbox items into note sections before exporting to Obsidian.
- **Interaction:** open the source in the UI, select a template, arrange highlights, tweak inline, then click export; minimal typing.
- **Feasibility:** moderate—needs lightweight UI plus the same parser as above; fully local.
- **Cost:** none.
- **Tradeoffs:** reduces cleanup while keeping you in control; slightly more build effort than a pure CLI but less than full Electron-grade polish.

## 9. Live “Distill As You Read”
- **How it works:** floating pane alongside RR that lets you tag highlights in real time into note sections/flashcard buckets (chapter, concept, example, Q/A). Syncs directly to the vault with the chosen template.
- **Interaction:** while reading, select text → assign to section/card type; a live preview note updates and saves to Obsidian.
- **Feasibility:** moderate-to-high—needs RR API/pseudo-API hooks or clipboard intercepts plus a responsive UI.
- **Cost:** none if fully local; potential cost if LLMs assist with structuring.
- **Tradeoffs:** minimizes post-read cleanup and preserves context perfectly; depends on RR integration stability and introduces another always-on UI.

## 10. Flashcard-First Pipeline
- **How it works:** script takes highlights, proposes atomic Q/A per your flashcard templates, and generates a companion note. You accept/edit cards; accepted cards update the note and RemNote deck.
- **Interaction:** run a command to generate draft cards + note; review in a small UI or CLI prompt; push approved items to RemNote and the vault.
- **Feasibility:** moderate—needs parsing plus card heuristics/LLM assist; RemNote sync required.
- **Cost:** none if heuristic; API/LLM costs if using models.
- **Tradeoffs:** accelerates mastery-focused items; risk of overproduction or noisy cards without good filtering and review UX.

## 11. Backlog Triage Dashboard
- **How it works:** lightweight web/Obsidian view that pulls RR items + tags, shows priority/status (`highlights_finished`, `notes_began`, etc.), and offers one-click actions that launch a chosen pipeline (auto-outline, guided builder, card-first).
- **Interaction:** open the dashboard, pick 2–5 active items, click “process” to start the selected workflow; see state badges update after completion.
- **Feasibility:** moderate—needs RR list/API ingestion and glue to trigger local scripts; mostly UI + orchestration.
- **Cost:** none if local; hosting costs if remote.
- **Tradeoffs:** improves prioritization and WIP limits; adds another interface layer and some maintenance overhead.
