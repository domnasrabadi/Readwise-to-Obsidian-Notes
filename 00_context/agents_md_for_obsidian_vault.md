This directory is your personal Obsidian vault for tracking, retaining, and sharpening knowledge across books, technical research, workflows, and personal development. 

Folders are organized by life domain and learning stage so you can capture raw highlights, evolve them into structured syntheses, and surface them when needed. At a glance, the vault covers: 
- long-form reading notes 
- in-progress studies 
- AI/agent research 
- productivity systems  
- personal planning.

---

# 1 Book Notes Vault Index

```shell
Book Notes Vault/
├── 01 Books/                     # Long-form book syntheses, finished reading logs, upcoming plan base files
├── 02 In Progress Books/         # Active reading projects, chapter notes, and staging area for summaries
├── 03 Technical Notes/           # Research on AI/agents, technical articles, reference images, and how-to guides
├── 04 Personal/                  # Personal planning, work reflections, health logs, and archival subfolders
├── 05 Paper Notes (readwise)/    # Dated imports of academic paper highlights synced from Readwise
├── 06 Learning System/           # Structured learning workflows, methods, prompts, tools, and backlog pipeline
├── 07 Readwise/                  # Readwise article highlights plus custom prompt libraries
├── 100 ⌛️ Backlog to process/     # Triaged items awaiting organization, flashcards, and reference archives
├── Hotkeys, Mac apps & keyboard shortcuts.md  # Running cheat sheet for productivity tooling
├── Running note list.md                          # Meta index of notes to revisit or expand
└── To buy list.md                                # Purchase tracker for books, gear, and supplies
```

## 1.1 Books

Holds your canonical reading records: Books + Reading Plan.base outlines master scheduling, Finished Books 2025 captures consolidated
takeaways, MindBranches Notes stores mind-map exports, and Upcoming + Reading Plan tracks next selections. Use this area for
finalized book syntheses and planning artifacts.

## 1.2 In Progress Books

Contains active study streams such as Building Apps w AI Agents notebooks, plus chapter-by-chapter notes like The Hundred-Page LLM
Book.md. The archive/ subfolder keeps wrapped-up drafts before they move into the main book library.

## 1.3 Technical Notes

A research hub spanning topical files (e.g., ⭐️ Best Python Packages.md), dedicated directories (10 Agents, Article Notes, Technical
How to), and supporting images/. Subfolders often use icon prefixes to signal priority or status; keep that convention when adding
new material.

## 1.4 Personal

Personal knowledge base split into focus areas: Health, Work, Office Setup, Mac, Monitors, along with evergreen documents like 👌🏼Work plan + moving forward.md. The archive/ folder safeguards deprecated or sensitive records.

## 1.5 Paper Notes (readwise)

Readwise ingests organized by capture date (07-06, 07-12, etc.). Each dated folder holds highlight dumps that you can promote into
long-form notes elsewhere after processing.

## 1.6 Learning System

A numbered framework for continuous improvement: 10 Workflows & Plans, 20 Methods (Meta-Learning), 30 Tools & Integrations, 40
Prompts & Templates, with 50 Backlog (to process) feeding the pipeline and 90 Archive storing retired assets.

## 1.7 Readwise

Stores non-paper Readwise imports. Articles/ houses article highlights, while copilot-custom-prompts/ maintains reusable AI prompt
sets curated from sync jobs.

## 1.8 ⌛️ Backlog to process

Triage center for new material such as LLM Evaluation Collated Notes.md, uv (Astral) — Python env & project management cheat
sheet.md, and ⭐️ Flashcards to Add.md. Use the archive/ folder once items are processed or superseded.

---

# 2 Instructions to Use for Various Tasks 
## 2.1 Flashcard generation 
- Description: Given some text, use the below to create high quality, atomic flashcards.
- Prompt/instructions 

```markdown fold
You are a flashcard generator with expertise in being given a set of notes or article content, and then producing
high quality flashcards (Questions + Answers) that focus on the main key points from that resource such that 
the user will get the most value from learning the concepts in your flashcard. 

You will be given a text snippet, and you are to return one or more flashcards based on the below instructions. 
Focus on QUALITY not QUANTITY. 

### 1. **Ask a Single, Clear Question per Card**

**Why:** Cards that ask more than one thing overload your brain and are harder to review.  
**How:**

- Each card should ask **exactly one thing**:
    
    - "What is…?"
        
    - "Why does…?"
        
    - "How do…?"
        
- If your idea splits naturally, **make two cards**:
    
    - ❌ _“Name 3 types of attention and explain how each works”_
        
    - ✅ _“Name 3 types of attention mechanisms”_
        
    - ✅ _“How does self-attention work?”_
        

---

### 2. **Keep the Prompt Focused and Unambiguous**

**Why:** Precision improves recall and avoids confusion.  
**How:**

- Use phrasing that makes it clear what’s expected.
    
- Add a little **context** if needed (e.g. “In LLMs…”).
    
- Avoid vague questions like “Gradient descent?”
    
- ✅ _“What does `requires_grad=True` do in PyTorch?”_
    

---

### 3. **Answer Brevity: Stick to 10–50 Words**

**Why:** Short answers are faster to review and easier to remember.  
**How:**

- Get to the point. Use 1–3 sentences max.
    
- If the answer is long, **split** the idea into multiple cards.
    
- ✅ _“ReLU outputs 0 for negative inputs and x for positive inputs.”_
    

---

### 4. **Use Active Recall Prompts**

**Why:** Testing yourself boosts memory better than re-reading.  
**How:**

- Use **question-answer** or **cloze (fill-in-the-blank)** formats.
    
- Include **explanation questions**: "Why…" or "How…"
    
- ✅ _“Why does dropout reduce overfitting?”_
    

---

### 5. **Avoid Trivia, Prioritise High-Yield Concepts**

**Why:** Not all knowledge deserves equal effort.  
**How:**

- **Avoid obscure facts or one-time-use details.**
    
- Prioritise:
    
    - Definitions
        
    - Core formulas
        
    - Key concepts
        
    - Use-cases and reasoning (“why” cards)
        
- ✅ _“What is the difference between L1 and L2 regularization?”_
    

---

### 6. **Use Cloze Deletions for Simple Facts**

**Why:** They’re fast and effective for targeted recall.  
**How:**

- Blank out one or two key terms.
    
- ✅ _“Softmax converts logits into ____ that sum to 1.”_
    

---

### 7. **Write in Your Own Words**

**Why:** Paraphrasing shows you understand.  
**How:**

- Don’t copy the textbook.
    
- Pretend you're explaining it to a smart peer.
    
- ✅ _“Cross-entropy measures how far off predicted probabilities are from the true label.”_
    

---

### 8. **Avoid Yes/No and Overly Simple Questions**

**Why:** These encourage guessing, not deep thinking.  
**How:**

- Reframe yes/no into explanation.
    
- ❌ _“Is ReLU nonlinear?”_
    
- ✅ _“Why is ReLU considered a non-linear activation function?”_
    

---

### 9. **Use Visual Flashcards for Processes & Diagrams**

**Why:** Visual memory strengthens conceptual recall.  
**How:**

- Use diagrams with missing labels.
    
- Add image occlusion cards (if using Anki).
    
- ✅ _“Label the components of a Transformer encoder.”_
    

---

### 10. **Review and Curate Regularly**

**Why:** Deadweight cards waste your time.  
**How:**

- Edit awkward cards.
    
- Delete low-value or trivial ones.
    
- Mark overly complex cards to split.
    
- Add hints if needed for clarity.
    

---

## 📝 Flashcard Templates

|Format|Example|
|---|---|
|Q&A|**Q:** What is the purpose of attention in Transformers? **A:** To weigh the relevance of different input tokens when producing each output token.|
|Cloze|**Q:** The derivative of sigmoid is highest when x = ____.|
|Diagram|_(Image of a neural net)_ → “Label the activation function in each layer.”|
|Why|**Q:** Why does increasing learning rate sometimes cause divergence?|
```


## 2.2 Book Summarisation 
- Description: Given a small, medium or large chunk(s) of text, you should generate clearly structured concise notes as below
- Prompt/Instructions

```markdown fold
<task>
Reformat and structure the text below which are highlights from a book I am reading. 
Your job is to output a well formatted (in markdown), structured and concise version of the notes/highlights provided to you.

You ARE NOT to just summarise the content since these are manually curated snippets of utmost importance from the resource in question. 
</task>

<instructions>

**You MUST do the following:**
- use bullet points and nested bullet points to explain related ideas 
    - nested bullet points should be indented by 4 spaces exactly, never 2 spaces
    - you can indent multiple levels based on how many related ideas/snippets are presented that relate to past snippets 
- when defining or introducing a new concept, start the bullet point with the concept name then "=" and a definition 
    - e.g. "loss function = mathematical function that ..."
- don't need fullstops after each sentence 
- don't capitalisation unless it is to represent a noun e.g. name of a paper, place or person
    - but YOU MUST capitalise acronyms or nouns if found in the source 
        - e.g. "AnchorBench provides a comprehensive...." - you would output "AnchorBench" not "anchorbench"

**If appropriate, you SHOULD do the following also:**
- fix words and grammar e.g. hyphens between words 
- if there is any repetitive ideas or text, briefly summarise the main points
- for nested bullet points that cover questions or considerations, and are phrased like a question, include ? after each
- use inline or block math equations with mathjax/latex for when you see a math equation
    - i.e. you would encapsulate the math formula/equation with either a single "$" for inline math, or a double "$$" for a math block
</instructions>


<example>
Please see the example of a typical input and ideal output below. You also have a longer example stored within you knowledge - it is the example_input_output.md file. 

Input: We present a practical evaluation framework which outlines how to proactively curate representative datasets, select meaningful evaluation metrics, and employ meaningful evaluation methodologies that integrate well with practical development and deployment of LLM-reliant systems that must adhere to real-world requirements and meet user- facing needs.

The evaluation design process is organized around three funda- mental pillars: 1. Datasets: Curating representative and high- quality data tailored to the evaluation goals.

2. Metrics: Selecting appropriate quantitative and qualitative measures to assess perfor- mance against specified objectives.

3. Methodology: Designing the overall evalu- ation approach, including specific strategies to handle challenges like non-determinism, prompt sensitivity, and hallucination mea- surement.

2 Evaluation Dataset Formulation

While the importance of evaluation is clear – enabling iterative progress, building user trust, ensuring consistency, and improving efficiency – practitioners often select from a plethora of

Datasets are composed of prompts and optionally associated ground truth responses,

To create a robust and reliable evaluation dataset, five core principles, the 5 D’s, should be followed.

1. Defined Scope that aligns with specific tasks the model is meant to perform. The dataset should further be 2. Demonstrative of Production Us- age, mimicking the inputs and scenarios expected from actual users. The dataset should be 3. Di- verse, capturing the variety of the problem space to avoid a narrow or biased evaluation. To ensure the integrity of the results, the dataset must be 4. Decontaminated, meaning it is distinct from any data used during model training to prevent mis- leadingly high performance metrics. Finally, the dataset should be 5. Dynamic, treated as a living body of work that evolves as the real-world appli- cation changes.

2.1.2 Human-Annotated Golden Datasets

Human annotation is preferable for tasks requir- ing specialized knowledge not found in founda- tion models, as it can reveal subtleties in what con- stitutes a high-quality response (e.g., correctness, usefulness, completeness).

However, this pro- cess is often difficult, costly, and time-consuming, risking low-quality or biased annotations due to the need for deep domain expertise and team co- ordination.

Common collection workflows in- clude leveraging in-house Subject Matter Experts (SMEs), outsourcing to third parties, employing user data and feedback, or gathering prompts through User Experience Research (UXR) sur- veys. These methods require clear instructions to ensure data quality, and practitioners should be aware that user data may have privacy con- straints and that feedback tends to be biased to- ward negative experiences.


Output:
- practical evaluation framework = guides the creation of evaluations for llm-reliant systems
- 3 pillars of evaluation design
	- datasets = curate representative, high-quality data aligned with evaluation goals
	- metrics = choose quantitative + qualitative measures tied to objectives
	- methodology = design procedures that address non-determinism, prompt sensitivity, hallucination measurement
- evaluation dataset formulation
	- datasets consist of prompts + optional ground-truth responses
	- robust evaluation enables iterative improvement, trust, consistency and efficiency
	- five core principles (5 D's) for dataset creation
		- defined scope = aligns with specific model tasks
		- demonstrative of production usage = mirrors real user scenarios
		- diverse = covers the breadth of the problem space
		- decontaminated = kept separate from training data to avoid inflated scores
		- dynamic = updated and version-controlled as applications evolve
	- human-annotated golden datasets = preferred for specialised knowledge tasks
		- captures subtleties like correctness, usefulness, completeness
		- challenges include cost, time, and risk of biased or low-quality labels
		- collection workflows = main ways teams gather evaluation data
			- in-house subject-matter experts (SMEs) label or create prompts
			- third-party vendors handle annotation when internal capacity is limited
			- user-generated data + feedback harvested from live products
			- UX-research surveys solicit fresh prompts directly from target users
		- workflow considerations
			- give annotators clear task instructions to secure data quality
			- respect privacy constraints when reusing user data
			- account for negativity bias since user feedback often skews toward problem reports
</example>

<input_highlights>
```


## 2.3 Formatting text 
- Description: if the user asks to format their notes, use the below instructions
- Prompt/Instruction

```markdown fold
# structure & indentation

- organise as compact bullets with up to three levels
    
    - section header line (either unbulleted or a top-level `-` bullet)
        
    - sub-bullets with `-`
        
    - deeper detail with tabs/indent before `-`
        
- keep each bullet to one terse line where possible
    
- use micro-subheadings inside a section like `where it fits:`, `when to choose which:`, `outcome:` followed by a short clause
    

# capitalisation

- start bullets in lowercase
    
- capitalise only proper nouns, acronyms, and named patterns (e.g. `PBFT`, `NMR`, `TMR`, `Primary–backup`, `Leader election`, `Byzantine fault tolerance`)
    
- keep variable symbols upper-case when conventional (`$N$`, `$K$`, `$F$`)
    

# punctuation & symbols

- no trailing full stops/periods on bullets
    
- use colons for definitions or lead-ins: `agent redundancy: more agents than strictly needed`
    
- use parentheses for quick clarifiers `(planner a vs planner b)`, `(crash/omission)`
    
- use the right-arrow `→` for causal or “drives/therefore” relationships
    
- use slashes for concise alternatives `w/o`, `hot / warm / cold`
    
- use plus signs for “and/with” emphasis in short phrases `keep system coordinated + state consistent`
    
- use en dashes for compound terms or ranges `Primary–backup`, not hyphen if you can type it
    
- quote “terms of art” with straight quotes when first introduced: `"truth"`
    
- prefer `e.g.` and `i.e.` (with dots); keep it tight (no comma needed after)
    

# typography & maths

- examples or desiderata in brief italics with asterisks: `*service stays up despite X failures*`
    
- inline maths with LaTeX where helpful: `$N$`, `$K$`, `$\ge Y$`
    
- write percentages with a space before `%` to match the sample: `$\ge Y$ %`
    
- keep lists numeric only when it adds meaning; otherwise stick to bullets
    

# wording & tone

- concise, telegraphic, engineer-y fragments (not full sentences)
    
- prefer concrete nouns and verbs: `start $N$ workers and accept if $K$ agree`
    
- include quick “reason” or “where it fits” bullets to anchor why/when
    

# consistency rules

- repeat section patterns in this order when relevant:
    
    - what can go wrong / design targets / kinds of redundancy / adjudication / coordination-state
        
- inside technique sections, keep a rhythm:
    
    - name → one-line what it is
        
    - one-line how it works
        
    - one-line why/when to use
        

# template you can copy

---
section title (topic)
    - single-line idea → short consequence
    - concept: brief definition
    - reason: why this matters
        - example: one concrete illustration
        - note: constraint or edge case
    - where it fits: the role this plays

next section (topic)
    - technique a
        - what: one-liner
        - how: one-liner
        - outcome: one-liner
    - technique b
        - …
---

# quick do/don’t

- do keep bullets short, parallel, and skimmable
    
- do use symbols (→, +, /) to compress wording
    
- don’t add periods at the end of bullets
    
- don’t over-explain; one line per idea
    
- don’t capitalise the start of bullets unless it’s a proper noun or named pattern
    

follow these and your future notes will match the exact look-and-feel of the sample.
```






