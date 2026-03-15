# Mermaid-Parity Diagram Skill — Design Spec

**Date:** 2026-03-15
**Status:** Approved for implementation
**Project:** excalidraw-agent-cli

---

## Problem Statement

The excalidraw-agent-cli skill can generate high-quality diagrams but Claude must compute layout coordinates, choose colors, and structure each diagram type from first principles on every invocation. This produces inconsistent quality — diagrams look different each time, common mistakes recur (unreadable text on dark backgrounds, title overlap, bidirectional arrows), and Claude spends significant tokens on geometry rather than content.

Mermaid provides a proven taxonomy of diagram types that covers the same conceptual space. The goal is a recipe-based system: one reference file per diagram type that gives Claude a pre-solved layout template, correct style defaults, and known pitfalls — so each invocation starts from a reliable baseline rather than from scratch.

**Primary use cases:**
- Claude Code documenting a codebase: reads files → generates architecture diagram → embeds in markdown doc
- Claude writing a blog post or technical report: generates illustrative diagrams inline as it writes
- User explicitly requesting a diagram: Claude picks the right type, generates, embeds

**Out of scope (v1):** XY charts, Sankey diagrams, timeline diagrams — these require arc/area primitives not available in the CLI. Auto-layout (Mermaid computes node positions; excalidraw-agent-cli requires explicit coordinates) is a known gap addressed by the layout templates.

**Deferred to v2 — CLI `convert` subcommand:**
`excalidraw-agent-cli convert --input diagram.mmd --output diagram.excalidraw`
Converts Mermaid syntax directly to Excalidraw without Claude. Works in CI/CD, scripts, and other AI agents. Layout algorithm: recipe-based coordinate mapping — each diagram type's canonical coordinate grid (from the v1 recipe files) is used as the layout engine, avoiding a Dagre port. When Claude receives Mermaid input in v2+, it calls `convert` rather than generating bash from scratch. The v1 recipe format must be designed to be compatible with this future converter (coordinate grids as explicit variables, type-keyed layout templates).

---

## Prerequisites and Environment

- **CLI:** `/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin/excalidraw-agent-cli`
- **PATH required:** `PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"`
- **Node.js:** `/Users/bhushan/.nvm/versions/node/v22.9.0/bin/node` — required for SVG/PNG export
- **Color palette:** `skill/references/color-palette.md` — already exists; recipes must use only colors defined there
- **Layout rules:** `skill/references/layout-rules.md` — already exists; recipes must comply with all rules, especially Rule 21 (≥60px title clearance) and Rule 22 (label contrast)
- **SVG support:** CLI supports `export svg` natively — no conversion step required
- **Output formats:** PNG (`export png`), SVG (`export svg`), raw JSON (`export json` → `.excalidraw`)

---

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Approach | Workflow command built on recipe docs | Low friction; Claude handles the whole pipeline; recipes are reusable reference, not runtime code |
| Content sourcing | Claude reads codebase → presents summary → user confirms before generating | Autonomous but verified; avoids hallucinated structure |
| Diagram type selection | Claude silently picks best type using rubric, mentions it, offers to change | Fast default with easy escape hatch; no interruption for obvious cases |
| Output location | Same directory as the doc being written, or `docs/diagrams/` if that directory already exists in the project | Predictable; co-located with docs by default |
| Output location fallback | If no doc context and no `docs/diagrams/` directory: save to project root or current directory | Explicit fallback removes ambiguity |
| Output format | PNG default; SVG for web projects; `.excalidraw` when user says "I want to edit it" | PNG works everywhere for docs/blogs |
| Quality gate | Self-inspection loop: Claude reads PNG, fixes issues, max 3 iterations, then delivers with warning if still imperfect | 3 iterations balances quality vs token cost; most layout issues are fixed in 1–2 passes |
| Self-inspection limit behavior | After 3 iterations: deliver the best version, note any remaining issues to the user | Never silently deliver a broken diagram; always surface known issues |
| Large diagrams | Cap at 20 nodes for v1; if content exceeds this, Claude splits into multiple diagrams and notes the split | Prevents illegible crowding; sets a clear implementable bound |
| CLI error handling | On non-zero exit: log the error, retry once with a minimal script (only `project new` + `element add` + `export` — no `--label`, no `--sw`, no `--roughness`, no `--fill-style`), surface to user if still failing | Fail loudly, not silently; minimal script isolates whether the issue is a flag or a core problem |

---

## Architecture

### New files

```
skill/
  references/
    diagram-recipes/               ← NEW: one recipe per diagram type
      flowchart.md
      sequence.md
      mindmap.md
      class-diagram.md
      state-diagram.md
      er-diagram.md
      gantt.md
      architecture.md
    diagram-type-rubric.md         ← NEW: type selection logic + tie-breaking
  SKILL.md                         ← UPDATED: diagram workflow section added
templates/                         ← NEW: runnable .sh example per type
  flowchart-example.sh
  sequence-example.sh
  mindmap-example.sh
  class-diagram-example.sh
  state-diagram-example.sh
  er-diagram-example.sh
  gantt-example.sh
  architecture-example.sh
docs/superpowers/specs/
  2026-03-15-mermaid-parity-design.md   ← this file
```

### SKILL.md changes required

Add a new section **"Diagram Generation Workflow"** after the existing element reference section, containing:
1. The trigger signals (when to auto-generate a diagram vs wait for explicit request)
2. A pointer to `diagram-type-rubric.md` with instruction to read it for type selection
3. The step-by-step workflow (see Workflow section below)
4. The output format decision table
5. The self-inspection checklist (what to look for when reading the PNG)
6. The markdown embed format template

No existing SKILL.md sections should be removed — this is additive only.

### Recipe file format

Each recipe in `skill/references/diagram-recipes/` must use this exact structure:

```markdown
# <Type> Diagram Recipe

## When to use
<3-6 bullet points: context signals that indicate this type. Include keywords
the user typically says and describe the shape of the problem, not just keywords.>

## Layout template
<A comment-annotated bash snippet showing the canonical coordinate system for
this type. Use placeholder labels like "NodeA", "NodeB". Show exact x/y values
and spacing constants. Include zone backgrounds if applicable.
Format: valid bash using the CLI — this template runs as-is with placeholder labels.

Reference canvas: 1200×800px (all recipes use this as the coordinate space).
Coordinate origin: top-left (0,0). All x/y values are absolute pixel positions.
Spacing constants must be explicitly listed as shell variables at the top of
the template (e.g., ROW_H=100, COL_W=200) so the template is readable and
the spacing rationale is clear. Coordinate choices must comply with
layout-rules.md — particularly Rule 21 (≥60px below title baseline before
first element) and all zone/spacing rules defined there.>

## Color and style defaults
<A table mapping node roles to --bg/--stroke/--fill-style from color-palette.md.
Include arrow color choices. Include font size and --ff values.>

## Common pitfalls
<3-5 bullet points: type-specific mistakes and the fix for each.>

## Worked example
<A complete self-contained bash script that generates a realistic, well-styled
diagram for a concrete scenario. The script must run successfully with the CLI.>
```

### Diagram type rubric format

`skill/references/diagram-type-rubric.md` must contain:

1. A decision table (context signal → diagram type) covering all 8 types
2. A tie-breaking rule: when two types could work, prefer the one that is structurally simpler (fewer node types, fewer arrow styles)
3. A fallback: if no type matches clearly, default to Flowchart and mention the assumption
4. An ambiguity handling note: ask the user when the request contains explicit type keywords conflicting with the content (e.g., "draw a sequence diagram of our database schema")

---

## End-to-End Workflow

### Trigger conditions

Claude initiates diagram generation when:
- User explicitly asks: "create a diagram", "draw a flowchart", "diagram this", "visualize as diagram", "generate a <type>"
- Claude is writing documentation and encounters a section that benefits from a visual (architecture, flow, sequence)
- User asks to "document the codebase" or "explain how X works" — Claude judges whether a diagram would reduce the explanation length

### Step-by-step workflow

```
1. TYPE SELECTION
   Read diagram-type-rubric.md
   Select best type → say "I'll generate a [type] diagram for this."
   → User can redirect before step 2

2. CONTENT SOURCING
   [codebase task]
     Read relevant source files (entry points, service files, config)
     Extract: components, their relationships, data flow direction
     Present summary as a bullet list: "Here's what I found: ..."
     Wait for user confirmation → if user rejects: re-read or ask what to change
     → "Explicitly skips" means: user says "just go ahead", "looks fine", "skip",
       "proceed anyway", or gives no substantive objection (e.g., just "ok")
     → Loop until user confirms or explicitly skips (max 3 rounds; after 3 rounds
       without confirmation, proceed with best current understanding and note it)
     → In automated/non-interactive contexts (e.g., running as part of a demo script):
       skip the confirmation step entirely — proceed directly to generation

   [conceptual task]
     Derive structure from: user's message text, current document being written
     (if Claude is actively editing a file), open files listed in context
     No confirmation needed unless structure is non-obvious (e.g., inferred from
     vague input like "diagram our system")

3. GENERATION
   Read diagram-recipes/<type>.md
   Adapt layout template to actual content (fill in node labels, connections)
   If node count > 20: split into multiple diagrams, note the split to user.
     Splitting heuristic by type:
     - Architecture: split by layer (client/gateway/service/data each become their own diagram)
     - Flowchart: split at subprocess boundaries (each major subprocess becomes its own diagram)
     - Sequence: split at natural phases (e.g., auth phase vs. main request phase)
     - Other types: split by natural grouping in the source content (e.g., domain, module)
   Generate bash script
   Run script via CLI with full PATH set
   On non-zero exit: retry once with simplified script; surface error to user if still failing

4. EXPORT
   Export to output file using appropriate format:
     PNG: excalidraw-agent-cli export png --project <file> --output <name>.png --overwrite
     SVG: excalidraw-agent-cli export svg --project <file> --output <name>.svg --overwrite
     .excalidraw: excalidraw-agent-cli export json --project <file> --output <name>.excalidraw --overwrite
   Output file naming: <kebab-case-subject>-<type>.<ext>
     e.g., auth-flow-sequence.png, order-service-arch.svg

5. SELF-INSPECTION LOOP (max 3 iterations)
   Read the PNG using the Read tool (visual inspection).
   Capability check: the Read tool renders images visually when used with PNG/SVG files
   in Claude Code. If visual rendering is unavailable (e.g., plain text output instead
   of an image), fall back to script review — but acknowledge that only 3 of the 7
   checklist items can be verified analytically from the bash script:
     ✓ Arrow directions (check --start-arrowhead/--end-arrowhead flags)
     ✓ Title clearance (check y-coordinates: title baseline + 60px ≤ first element y)
     ✓ Dark background stroke (check --bg and --stroke color pairs)
   The remaining 4 items (label overlap, connection presence, color consistency, overall
   layout) require visual inspection and cannot be verified without rendering. In script-
   review fallback mode: deliver the diagram and note to the user that visual inspection
   was not possible.
   Check each item on the inspection checklist:
     □ All nodes labeled and readable
     □ No label text overlapping node borders or other nodes
     □ All expected connections present
     □ Arrow directions correct (no unintended bidirectional arrows)
     □ Title has ≥60px clearance from first element (Rule 21)
     □ Dark-background nodes use light stroke (Rule 22)
     □ Color coding consistent with diagram type recipe
   If any item fails: fix the script, regenerate, re-inspect
   After 3 iterations: deliver best version, list any known remaining issues

6. OUTPUT LOCATION
   Priority order (first match wins):
   1. If actively writing a specific document: same directory as that document
   2. Else if docs/diagrams/ exists in the project root: use docs/diagrams/
   3. Else: current working directory
   Create the output directory if it doesn't exist: `mkdir -p <output-dir>` in bash scripts;
   `os.makedirs(output_dir, exist_ok=True)` in Python contexts

7. EMBED
   Return this exact markdown snippet:
     ![<Alt text describing what the diagram shows>](<relative-path-to-file>)
   Alt text format: "<Type> diagram showing <brief description>"
   Path: relative to the document file, not the project root
```

### Output format decision table

| Context | Format |
|---|---|
| Writing markdown doc, README, blog post | PNG |
| Web project with HTML/CSS/JS files present | SVG |
| User says "I want to edit it" / "make it editable" | `.excalidraw` |
| User explicitly names a format | User's choice |
| No doc context (standalone request) | PNG |

---

## Diagram Types in Scope (v1)

| Type | Mermaid equivalent | Key parity note |
|---|---|---|
| Flowchart | `graph TD/LR` | Full parity — rectangles, diamonds, arrows, labels |
| Sequence | `sequenceDiagram` | Use explicit `add arrow` with coords, never `element connect` for same-row participants |
| Mindmap | `mindmap` | Radial layout; root node must use `--stroke "#e2e8f0"` on dark background |
| Class diagram | `classDiagram` | Compartments via multi-line labels; inheritance with open-triangle arrowhead |
| State diagram | `stateDiagram-v2` | Rounded rectangles for states; start/end markers as ellipses |
| ER diagram | `erDiagram` | Rectangles with attribute text blocks; crow's foot notation via arrow labels |
| Gantt chart | `gantt` | Horizontal bar rectangles; time axis as evenly-spaced text labels |
| Architecture | `architecture-beta` / C4 | Zone backgrounds first, then nodes; semantic color coding mandatory |

---

## Quality Bar

Every diagram must satisfy all three levels before delivery:

### Level 1: Structural correctness
- All nodes requested or derived from content are present
- All connections exist with correct directionality
- All labels match the source content (no placeholder text)
- Comparison method: Claude cross-checks the generated bash script against the confirmed content summary (not by parsing the PNG)

### Level 2: Visual polish
- Consistent semantic color coding per node role (as defined in recipe)
- No labels overlapping each other or overflowing node borders
- Title has ≥60px clearance (Rule 21)
- All text readable: minimum 13px font, correct contrast (Rule 22)
- "Readable at normal doc size" = legible when rendered at 800px wide (standard GitHub markdown width)
- "Blog-post quality" = a technical reader would not feel the need to re-draw it; used as a qualitative anchor for the moderator, not a pixel measurement

### Level 3: Self-inspection gate
- Claude reads the exported PNG and checks the 7-item inspection checklist (see workflow step 5)
- Fixes and regenerates until checklist passes or iteration limit reached
- Delivers with explicit issue list if limit reached

---

## Test Framework

### Overview

8 test scenarios, one per diagram type. Each scenario runs two agents in parallel plus one moderator.

### Agent invocation

All agents are spawned as sub-agents via Claude Code's `Agent` tool (subagent_type: general-purpose). Each sub-agent receives its full task description as a prompt and operates independently with no shared state. Agent A and Agent B for each scenario are spawned in the same parent turn (parallel execution). The moderator for each scenario is spawned after both A and B complete.

### Per-scenario agents

**Agent A (Mermaid):** Given the test prompt, generate the correct Mermaid syntax. Output: a `.md` file containing the Mermaid code block and a brief structural inventory (list of nodes and connections as plain text — this is the comparison reference).

**Agent B (Excalidraw skill):** Given the same test prompt, use the excalidraw skill (at `~/.claude/skills/excalidraw/`) to generate the diagram. Output: the PNG file, the bash script used, and a brief structural inventory (same format as Agent A's inventory — list of nodes and connections).

**Both agents output a structural inventory in this format:**
```
Nodes: [NodeA, NodeB, NodeC, ...]
Connections: [NodeA→NodeB: "label", NodeB→NodeC: "label", ...]
```
This allows the moderator to compare structure textually without parsing pixels.

### Moderator scoring

The moderator agent receives: the test prompt, Agent A's structural inventory, Agent B's structural inventory, and Agent B's PNG exported at default CLI scale (no `--scale` flag — the CLI default produces a PNG at approximately 1x pixel density suitable for screen review).

**Structural correctness score (0–100):**
Scored as a binary checklist — each item is all-or-nothing (pass or fail, no partial credit).
Each item is worth 20 points (5 items × 20 = 100):
- [ ] All nodes in Agent A's inventory are present in Agent B's inventory
- [ ] All connections in Agent A's inventory are present in Agent B's inventory
- [ ] Connection directions match (A→B ≠ B→A)
- [ ] All labels are non-empty and semantically match (paraphrases acceptable; exact wording not required)
- [ ] No extra spurious connections in Agent B that don't exist in Agent A

Pass bar: ≥ 80 (at most 1 item can fail; 4/5 = 80, which is the minimum passing score)

**Visual quality score (0–100):**
Moderator reads the PNG and scores these items (equal weight):
- [ ] All text is legible (no overlap, no overflow, size ≥ 13px visually)
- [ ] Color coding is semantically consistent within the diagram
- [ ] No layout artifacts (misaligned zones, arrows not reaching nodes, floating labels)
- [ ] Title is clearly separated from diagram content
- [ ] Overall impression: would this be acceptable in a technical blog post?

Pass bar: ≥ 80 (at most 1 item can fail)

### Failure remediation

On any failure:
1. Moderator identifies which specific checklist items failed
2. That failure is mapped back to the recipe file for that diagram type
3. The recipe is updated to address the root cause
4. The test for that type is re-run
5. Regression: re-run all 8 tests after any recipe change to catch cross-type regressions
6. Regression runs are triggered manually during development; no CI automation required for v1

### Test prompts and expected structural inventories

| Type | Test prompt | Expected nodes (minimum) |
|---|---|---|
| Flowchart | "Document the user signup flow: form submit → validate email → check existing account → create account → send welcome email → success" | Form Submit, Validate Email, Existing Account? (diamond), Create Account, Send Welcome Email, Success |
| Sequence | "Show the auth flow: browser sends credentials to API gateway, gateway calls auth service, auth service validates against DB, returns JWT, gateway forwards to browser" | Browser, API Gateway, Auth Service, Database — 5 sequential messages |
| Mindmap | "Map the key concepts of React: components, state, props, hooks, context, lifecycle, rendering" | React (root), 7 leaf nodes |
| Class diagram | "Model a blog system: Post has title/body/author, Comment belongs to Post, User has many Posts and Comments" | Post, Comment, User — with field labels and relationship arrows |
| State diagram | "Document order states: placed → payment pending → paid → fulfillment → shipped → delivered; can cancel from placed or paid; can refund from delivered" | 6 state nodes, 2 cancel transitions, 1 refund transition |
| ER diagram | "Model the tables: users, posts, comments, tags, post_tags — show relationships and key fields" | 5 entity nodes, 4+ relationship arrows |
| Gantt | "Plan a 6-week feature launch: week 1-2 design, week 2-3 backend, week 3-5 frontend, week 4-5 testing, week 6 launch" | 5 task bars, time axis 6 units |
| Architecture | "Document the microservices: API Gateway, Auth Service, Order Service, Inventory Service, Notification Service, shared Postgres and Redis" | 7 nodes (5 services + 2 data stores), zone backgrounds for service and data layers |

### Self-inspection verification

The Sequence diagram test is the designated scenario for verifying the self-inspection loop works. Sequence diagrams using `element connect` between same-row participants produce bidirectional arrows — a known issue. The recipe must use explicit `add arrow` coords; if Claude mistakenly uses `element connect`, the inspection loop must catch and fix it. A passing test suite must show evidence that the loop ran at least once on this scenario.

---

## Success Criteria

The implementation is complete when all of the following are true:

1. All 8 recipe files exist in `skill/references/diagram-recipes/` with all 5 required sections populated
2. `diagram-type-rubric.md` covers all 8 types, includes tie-breaking logic, fallback, and ambiguity handling
3. `skill/SKILL.md` has a new "Diagram Generation Workflow" section (additive — no existing sections removed)
4. `templates/` contains 8 runnable bash scripts named `<type>-example.sh`. A template script is "correct" when: (a) it exits with code 0, (b) it produces a non-empty PNG file, and (c) a human reviewer (or Claude via visual Read tool inspection) confirms the PNG passes the 7-item self-inspection checklist. The verification method is visual review — automated checking is not required for v1
5. All 8 diagram types pass dual-agent moderator validation: structural score ≥ 80, visual score ≥ 80
6. Output format is configurable and all three formats (PNG, SVG, `.excalidraw`) are tested and working
7. The self-inspection loop is verified to have caught and fixed at least one issue in the sequence diagram test scenario
8. Two end-to-end demos are documented in `examples/`:
   - `examples/codebase-docs-demo/` — Claude documents the excalidraw-agent-cli repo itself
     (specifically: the `skill/` directory structure and how the skill reads/uses reference files),
     generates an architecture diagram, and embeds it in a `examples/codebase-docs-demo/README.md`
   - `examples/blog-post-demo/` — Claude writes a 3-paragraph technical explanation of
     "how the excalidraw CLI skill works" and inserts a flowchart diagram inline
   A demo passes if: (a) the diagram file is present, (b) the markdown embed path resolves
   to a valid image when opened from the demo README's directory, (c) the diagram's
   structural inventory (written by Claude inline in the README) matches the visible content
9. No existing examples in `examples/` are broken by the changes. Existing example scripts live in `examples/` as `.sh` files: `flowchart.sh`, `arch.sh`, `auth-sequence.sh`, `mindmap.sh`, `cicd.sh`, `data-pipeline.sh`, `microservices.sh`. Regression check: re-run each script and confirm the exported PNG is non-empty and visually correct (human spot-check)
10. `color-palette.md` and `layout-rules.md` are not modified — recipes must work within existing constraints

---

## File Naming Conventions

| File type | Convention | Example |
|---|---|---|
| Recipe files | `<type>.md` (kebab-case) | `class-diagram.md` |
| Template scripts | `<type>-example.sh` | `class-diagram-example.sh` |
| Generated diagram files | `<kebab-case-subject>-<type>.<ext>` | `auth-flow-sequence.png` |
| Project files (temp) | `<kebab-case-subject>.excalidraw` | `auth-flow.excalidraw` |

Output file names must not collide. "Same session" means a single continuous Claude Code conversation. If the target file name already exists on disk at generation time (regardless of how it was created), append `-2`, `-3`, etc. before writing.

### Rubric vs. silent-pick reconciliation

The default behavior is: Claude silently picks the best type and mentions the choice. The exception documented in the rubric ("ask the user when type keywords conflict with content") applies only when the user's explicit type keyword and the content are structurally incompatible (e.g., "draw a sequence diagram of our database schema" — a sequence diagram requires time-ordered interactions, which a schema does not have). In all other cases of ambiguity, use the tie-breaking rule (pick the structurally simpler type) and proceed silently.
