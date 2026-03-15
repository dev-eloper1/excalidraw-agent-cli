# Mermaid-Parity Implementation Plan

**Spec:** `2026-03-15-mermaid-parity-design.md`
**Date:** 2026-03-15

---

## Phase 0: Foundation (do first, everything depends on this)

### 0.1 — Create recipe directory structure
```
mkdir -p skill/references/diagram-recipes
mkdir -p excalidraw_agent_cli/skill/references/diagram-recipes
mkdir -p templates
```

### 0.2 — Verify CLI capabilities
Run these checks before writing any recipe:
```bash
export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"
CLI=/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin/excalidraw-agent-cli
$CLI backend check --json          # confirm Node.js/PNG/SVG export works
$CLI export svg --help             # confirm SVG export flag syntax
$CLI export json --help            # confirm .excalidraw export flag syntax
```
Document any flag differences from assumptions in the spec.

### 0.3 — Create diagram-type-rubric.md
File: `skill/references/diagram-type-rubric.md`

Must contain (per spec):
- Decision table: context signal → diagram type (all 8 types)
- Tie-breaking rule: prefer structurally simpler type
- Fallback: default to Flowchart, note the assumption
- Conflict rule: ask user only when explicit type keyword is structurally incompatible with content
- Default behavior: silently pick, mention choice, offer to change

---

## Phase 1: Recipe Files (8 files, can be written in parallel)

Each file: `skill/references/diagram-recipes/<type>.md`
Format: 5 mandatory sections (When to use / Layout template / Color defaults / Common pitfalls / Worked example)
Canvas: 1200×800px, origin top-left, spacing as named shell variables
Colors: only from `skill/references/color-palette.md`
Rules: must comply with layout-rules.md Rules 21 and 22

### 1.1 — flowchart.md
Layout: top-to-bottom (TD) default, left-to-right (LR) when >5 nodes in a chain
Key pitfall: diamond decision nodes need explicit `-w 60 -h 60` to avoid misshapen diamonds
Color defaults: process=Application Services green, decision=Decision Diamond amber, start=Start/Trigger blue, end=End/Success green

### 1.2 — sequence.md
Layout: participants as columns, messages as horizontal arrows descending vertically
Key pitfall: NEVER use `element connect` for same-row participants — always use explicit `add arrow` coords
Spacing: participant columns 200px apart, message rows 60px apart, first message at y=120
Color defaults: actor boxes=Neutral/Base, arrows=black for sync, amber for async, red for error

### 1.3 — mindmap.md
Layout: radial — root center at (600, 400), branches at 8 compass points, leaves 180px beyond branches
Key pitfall: root node on dark background MUST use `--stroke "#e2e8f0"` (light stroke = readable white text)
Key pitfall: left-side annotations must be at x<150 to avoid overlapping nodes at x=220+

### 1.4 — class-diagram.md
Layout: grid — classes as tall rectangles (w=180, h varies by field count), inheritance arrows upward
Key pitfall: multi-line labels use `\n` — test that CLI renders them as separate lines
Color defaults: class boxes=Data/Storage purple, interface=lighter variant, abstract=hachure fill

### 1.5 — state-diagram.md
Layout: left-to-right flow for linear states, radial for state machines with many transitions
Key pitfall: start state = filled ellipse (small, dark), end state = double-border ellipse (use two concentric ellipses)
Color defaults: active state=Application Services green, error state=Error/Reject red, initial/final=Start/Trigger blue

### 1.6 — er-diagram.md
Layout: entities as rectangles in a grid, relationship arrows between them, attribute text blocks below entity names
Key pitfall: crow's foot notation — use arrow labels ("1", "N", "0..1") not arrowhead types since CLI arrowheads are limited
Color defaults: entity=Data/Storage purple, weak entity=hachure fill

### 1.7 — gantt.md
Layout: horizontal — time axis as evenly-spaced text labels at top (y=80), task bars as colored rectangles below
Spacing: each task row 50px tall, 10px gap between rows, time columns 150px wide
Key pitfall: bar widths must be calculated from duration × column_width — document the formula in the template
Color defaults: task bars by phase (design=blue, dev=green, test=amber, launch=teal)

### 1.8 — architecture.md
Layout: layered horizontal bands — client (top), gateway, services, data (bottom)
Key pitfall: zone backgrounds MUST be drawn before nodes (z-order), zone opacity 30-35%
Key pitfall: title at y=12, zones start at y=90+ (Rule 21 clearance)
Color defaults: per color-palette.md semantic mapping (Clients/blue, Gateway/green, Services/green, Data/purple, Async/yellow)

---

## Phase 2: Template Scripts (8 files, parallel with Phase 1)

Each file: `templates/<type>-example.sh`
Requirements: exit code 0, produces non-empty PNG, passes 7-item inspection checklist
Each script must:
- Set PATH at top: `export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"`
- Use `CLI=/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin/excalidraw-agent-cli`
- Create project in `/tmp/` (e.g., `$CLI project new --name flowchart-example --json`)
- Export PNG to `examples/<type>-template-preview.png`
- Use a realistic scenario (not "NodeA → NodeB" placeholders)

Use the same test prompts from the spec's test framework as the scenario for each template:

| Script | Scenario |
|---|---|
| `flowchart-example.sh` | User signup flow |
| `sequence-example.sh` | Auth flow (browser → gateway → auth service → DB) |
| `mindmap-example.sh` | React concepts |
| `class-diagram-example.sh` | Blog system (Post, Comment, User) |
| `state-diagram-example.sh` | Order lifecycle states |
| `er-diagram-example.sh` | Blog tables (users, posts, comments, tags) |
| `gantt-example.sh` | 6-week feature launch |
| `architecture-example.sh` | Microservices (API GW, Auth, Order, Inventory, Notif, Postgres, Redis) |

---

## Phase 3: SKILL.md Update

Add section **"Diagram Generation Workflow"** to `skill/SKILL.md` (additive — no deletions).

Section content (in order):
1. Trigger conditions (3 bullet points from spec)
2. `→ Read diagram-type-rubric.md for type selection`
3. The 7-step workflow (condensed from spec — keep it scannable, not a wall of text)
4. Output format decision table (4-row table)
5. Self-inspection checklist (7-item checkbox list)
6. Markdown embed format: `![<Type> diagram showing <description>](<relative-path>)`
7. Output location priority (3 rules)
8. Pointer: `For detailed layout patterns, read skill/references/diagram-recipes/<type>.md`

Keep the section under 80 lines — it's a workflow guide, not a spec. The recipes hold the detail.

After updating `skill/SKILL.md`:
- Sync to `excalidraw_agent_cli/skill/SKILL.md`
- Sync to `~/.claude/skills/excalidraw/SKILL.md`

---

## Phase 4: Test Suite

### 4.1 — Run template scripts (smoke test)
Run all 8 template scripts. For each:
- Confirm exit code 0
- Confirm PNG exists and is non-empty
- Read PNG with Read tool — confirm 7-item checklist passes
- Fix recipe/script if any item fails, re-run

### 4.2 — Dual-agent validation (8 scenarios)
For each of the 8 diagram types, spawn in parallel:

**Agent A prompt template:**
```
Generate the correct Mermaid syntax for this prompt: "<test prompt>"
Save the .md file to /tmp/mermaid-test/<type>/mermaid-output.md
Include a structural inventory at the end in this format:
Nodes: [node1, node2, ...]
Connections: [node1→node2: "label", ...]
```

**Agent B prompt template:**
```
Using the excalidraw skill at ~/.claude/skills/excalidraw/, generate a diagram for:
"<test prompt>"
Save the PNG to /tmp/mermaid-test/<type>/excalidraw-output.png
Save the bash script used to /tmp/mermaid-test/<type>/script.sh
Include a structural inventory at the end in this format:
Nodes: [node1, node2, ...]
Connections: [node1→node2: "label", ...]
```

After both complete, spawn moderator:

**Moderator prompt template:**
```
You are evaluating diagram quality. Score the following on two axes.

Test prompt: "<test prompt>"

Agent A structural inventory (Mermaid):
<paste inventory>

Agent B structural inventory (Excalidraw):
<paste inventory>

Agent B PNG: /tmp/mermaid-test/<type>/excalidraw-output.png (read it visually)

STRUCTURAL SCORE (0-100, binary checklist, 20pts each):
[ ] All nodes in A's inventory present in B's inventory
[ ] All connections in A's inventory present in B's inventory
[ ] Connection directions match
[ ] All labels non-empty and semantically match (paraphrases OK)
[ ] No spurious connections in B not in A

VISUAL SCORE (0-100, binary checklist, 20pts each):
[ ] All text legible (no overlap, no overflow)
[ ] Color coding semantically consistent within the diagram
[ ] No layout artifacts (floating labels, misaligned zones, arrows missing nodes)
[ ] Title clearly separated from diagram content
[ ] Would be acceptable in a technical blog post

Report: structural score, visual score, which items failed, root cause.
Pass bar: structural ≥ 80, visual ≥ 80.
```

### 4.3 — Self-inspection verification (sequence diagram)
The sequence diagram test must show evidence the loop ran. In the test run, verify that the bash script log contains at least one regeneration cycle (compare v1 script vs final script — they should differ if the loop fired). If no loop fired (diagram was perfect on first try), intentionally introduce a known sequence diagram bug (`element connect` instead of `add arrow`), confirm the loop catches it, then restore the correct version.

### 4.4 — Failure remediation loop
For any moderator failure:
1. Read the failed checklist items
2. Open the recipe file for that type
3. Add/fix the relevant pitfall or template coordinate
4. Re-run only that type's test
5. After all types pass: re-run all 8 (regression check)

### 4.5 — Output format test
For one diagram type (architecture), verify all three export formats work:
```bash
excalidraw-agent-cli export png  --project /tmp/test.excalidraw --output /tmp/test.png --overwrite
excalidraw-agent-cli export svg  --project /tmp/test.excalidraw --output /tmp/test.svg --overwrite
excalidraw-agent-cli export json --project /tmp/test.excalidraw --output /tmp/test-export.excalidraw --overwrite
```
Confirm: PNG opens as image, SVG is valid XML with viewBox, `.excalidraw` is valid JSON.

---

## Phase 5: End-to-End Demos

### 5.1 — Codebase docs demo
Location: `examples/codebase-docs-demo/`

Task: document the excalidraw-agent-cli repo's `skill/` directory structure.
- Claude reads `skill/SKILL.md`, `skill/references/` file list
- Generates an architecture diagram showing: SKILL.md → reads → [color-palette.md, layout-rules.md, patterns.md, diagram-type-rubric.md, diagram-recipes/]
- Saves PNG to `examples/codebase-docs-demo/skill-architecture.png`
- Writes `examples/codebase-docs-demo/README.md` with:
  - Brief description of the skill system
  - Embedded diagram: `![Architecture diagram showing the excalidraw skill file structure](skill-architecture.png)`
  - Structural inventory (nodes + connections listed)

Pass criteria: PNG present, embed path resolves, inventory matches visible diagram.

### 5.2 — Blog post demo
Location: `examples/blog-post-demo/`

Task: write a 3-paragraph technical explanation of "how the excalidraw CLI skill works" with an inline flowchart.
- Claude writes `examples/blog-post-demo/README.md` with 3 paragraphs
- Generates a flowchart: user request → type selection → content sourcing → generation → self-inspection → embed
- Embeds diagram inline in the markdown
- Saves PNG to `examples/blog-post-demo/skill-workflow.png`

Pass criteria: PNG present, embed path resolves, diagram matches the workflow described in the text.

---

## Phase 6: Sync and Cleanup

### 6.1 — Sync all skill files
The skill lives in three locations. After all changes, sync:
```bash
# From project root
cp -r skill/references/diagram-recipes/ excalidraw_agent_cli/skill/references/
cp skill/references/diagram-type-rubric.md excalidraw_agent_cli/skill/references/
cp skill/SKILL.md excalidraw_agent_cli/skill/SKILL.md

cp -r skill/references/diagram-recipes/ ~/.claude/skills/excalidraw/references/
cp skill/references/diagram-type-rubric.md ~/.claude/skills/excalidraw/references/
cp skill/SKILL.md ~/.claude/skills/excalidraw/SKILL.md
```

### 6.2 — Regression check
Re-run all 7 existing example scripts:
```bash
for script in examples/flowchart.sh examples/arch.sh examples/auth-sequence.sh \
              examples/mindmap.sh examples/cicd.sh examples/data-pipeline.sh \
              examples/microservices.sh; do
  bash "$script" && echo "✓ $script" || echo "✗ $script FAILED"
done
```
Visually inspect each PNG output.

### 6.3 — Commit
Stage: `skill/`, `excalidraw_agent_cli/skill/`, `templates/`, `examples/`
Commit message: `Add mermaid-parity recipe system: 8 diagram type recipes, templates, and test results`

---

## Parallel execution guide

Phases 1 and 2 can run fully in parallel (recipes and template scripts are independent).
Phase 3 (SKILL.md update) should start after Phase 1 is complete (needs recipe file paths to reference).
Phase 4 (testing) starts after Phases 1, 2, and 3 are complete.
Phases 5 and 6 run after Phase 4 passes.

Suggested batching for parallel sub-agents:

**Batch A (parallel):** recipes 1.1–1.4 + template scripts for those types
**Batch B (parallel):** recipes 1.5–1.8 + template scripts for those types
**Batch C (sequential):** Phase 3 (SKILL.md) → Phase 4 (tests) → Phase 5 (demos) → Phase 6 (sync)

---

## Success checklist

- [ ] 8 recipe files in `skill/references/diagram-recipes/`
- [ ] `diagram-type-rubric.md` with decision table, tie-breaking, fallback, conflict rule
- [ ] `skill/SKILL.md` updated with Diagram Generation Workflow section
- [ ] 8 template scripts in `templates/`, all exit 0 and produce valid PNGs
- [ ] All 8 types pass dual-agent moderator (structural ≥ 80, visual ≥ 80)
- [ ] Sequence diagram test shows self-inspection loop evidence
- [ ] PNG, SVG, `.excalidraw` export formats all verified working
- [ ] Codebase docs demo in `examples/codebase-docs-demo/`
- [ ] Blog post demo in `examples/blog-post-demo/`
- [ ] All 7 existing example scripts still produce valid PNGs
- [ ] Skill synced to all 3 locations
