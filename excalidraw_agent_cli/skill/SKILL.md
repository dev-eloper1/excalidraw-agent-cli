---
name: excalidraw
description: Create, edit, and export Excalidraw diagrams (flowcharts, architecture diagrams, mind maps, system designs) using the excalidraw-agent-cli tool. Use this skill whenever the user asks to draw, diagram, visualize, chart, or map out anything — flowcharts, system architecture, process flows, network diagrams, org charts, sequence diagrams, mind maps, wireframes, entity relationships, data flows, or any other visual diagram. Also trigger when the user says things like "create a diagram", "draw a flowchart", "sketch out the architecture", "visualize this", "make a chart of", "diagram this for me", "show me how X connects to Y", or wants to export to SVG/PNG from excalidraw. Even if the user doesn't say "excalidraw" explicitly, trigger this skill for any diagramming request.
---

# Excalidraw Agent CLI Skill

Generate diagrams that **argue visually**, not just display information. A diagram is a visual argument that shows relationships, causality, and flow that words alone cannot express. **The shape should BE the meaning.**

## Reference files in this skill

Read these as needed — they are the ground truth for specifics:

| File | When to read |
|------|-------------|
| `references/color-palette.md` | **Before every diagram** — all hex values live here |
| `references/cli-reference.md` | CLI syntax, flags, bash helper patterns |
| `references/patterns.md` | Visual pattern library with CLI examples |
| `references/layout-rules.md` | Layout rules + coordinate templates |
| `references/diagram-type-rubric.md` | **Type selection** — which diagram type to use when |
| `references/diagram-recipes/<type>.md` | **Before generating** — layout template, color defaults, pitfalls per type |

Available recipes: `flowchart.md`, `sequence.md`, `mindmap.md`, `class-diagram.md`, `state-diagram.md`, `er-diagram.md`, `gantt.md`, `architecture.md`

---

---

## Diagram Generation Workflow

Use this workflow when generating a diagram as part of documentation, a report, or a blog post — or when the user asks for a diagram without specifying exact elements.

### 1. Type selection
Read `references/diagram-type-rubric.md`. Pick the best type silently.
Say: *"I'll generate a [type] diagram for this."* — user can redirect before you proceed.

### 2. Content sourcing

**Codebase task** (documenting a repo, explaining a system):
- **Parallelize file reads** — identify all relevant source files first, then read them all in a single turn using multiple parallel Read tool calls (entry points, services, config, etc.). For large repos (>5 files), spawn parallel **Haiku sub-agents** per service/module — each reads its files and returns a node+relationship summary.
- Present a brief bullet summary: *"Here's what I found: [nodes + relationships]"*
- Wait for user confirmation before generating (max 3 rounds; proceed after 3 or if user says "go ahead")

**Multiple diagrams in one request** (e.g., "give me a flowchart and a sequence diagram"):
- Generate all diagrams in parallel using sub-agents — each diagram is fully independent

**Conceptual task** (blog post, report, explanation):
- Derive structure from the user's message and any open documents
- No confirmation needed — proceed directly

### 3. Read the recipe
**Parallelize with Step 2** — read `references/diagram-recipes/<type>.md` AND `references/color-palette.md` in the same turn as your source file reads. Do not compute coordinates from scratch.

### 4. Generate and export
Run the bash script. Export using:
```bash
$CLI -p "$P" export png -o <name>.png --overwrite   # default
$CLI -p "$P" export svg -o <name>.svg --overwrite   # for web projects
$CLI -p "$P" export json -o <name>.excalidraw --overwrite  # when user wants to edit
```
Format choice: PNG for markdown/docs/blogs; SVG if web project; `.excalidraw` if user says "I want to edit it".

Output file naming: `<kebab-case-subject>-<type>.<ext>` — e.g., `auth-flow-sequence.png`

### 5. Self-inspection loop (max 3 iterations)
Read the PNG with the Read tool. Check all 7 items:
- [ ] All nodes labeled and readable
- [ ] No label text overlapping node borders or other nodes
- [ ] All expected connections present
- [ ] Arrow directions correct (no unintended bidirectional arrows)
- [ ] Title has ≥60px clearance from first element (Rule 21)
- [ ] Dark-background nodes use light stroke `#e2e8f0` (Rule 22)
- [ ] Color coding consistent with the recipe defaults

If any item fails: fix script, regenerate, re-inspect. After 3 iterations: deliver best version and list remaining issues.

### 6. Output location and embed
Save to: same directory as the doc being written → or `docs/diagrams/` if it exists → or current directory.

Return this markdown embed snippet:
```
![<Type> diagram showing <brief description>](<relative-path-to-file>)
```
Path is relative to the document, not the project root. If file already exists, append `-2`, `-3`.

### Output format by context

| Context | Format |
|---|---|
| Markdown doc, README, blog post | PNG |
| Web project (HTML/CSS/JS present) | SVG |
| User says "I want to edit it" | `.excalidraw` |
| User specifies a format | User's choice |

---

## Environment Setup

```bash
CLI=$(which excalidraw-agent-cli 2>/dev/null || echo "")
if [[ -z "$CLI" ]]; then
  echo "ERROR: excalidraw-agent-cli not found. Install: pip install excalidraw-agent-cli" >&2
  exit 1
fi
export PATH="$PATH:/usr/local/bin:/opt/homebrew/bin"
```

Use **absolute paths** for all `--project` and `--output` arguments.

---

## Core Philosophy

### Diagrams Should ARGUE, Not DISPLAY

**The Isomorphism Test**: Remove all text. Does the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram — actual formats, real event names, how things actually connect — or does it just label boxes?

### Container Discipline

Not every piece of text needs a shape around it. Default to free-floating text. Add containers only when:
- Arrows need to connect to the element
- The shape itself carries meaning (decision diamond, start ellipse, etc.)
- Visual grouping with a background zone is needed

**Target**: fewer than 30% of text elements inside containers. Use font size and color for hierarchy.

### Bad vs Good

| Bad (Displaying) | Good (Arguing) |
|-----------------|----------------|
| 5 equal boxes with generic labels | Each concept shaped to mirror its behavior |
| Uniform card grid | Structure matches conceptual structure |
| "API" → "Database" → "Client" | Real service names + actual request/response formats |
| Same container style everywhere | Distinct visual vocabulary per concept type |
| Arrows all look the same | Color-coded arrows encoding relationship type |

---

## Step 0: Depth Assessment (Do This First)

**Simple / Conceptual** — abstract shapes, clean labels. Use for mental models, overviews, philosophical points.

**Comprehensive / Technical** — concrete examples, real data, code snippets. Use for real systems, architectures, tutorials, anything educational.

**If comprehensive**: research the actual specs before drawing. Look up real event names, API formats, method signatures. Generic placeholders ("Event 1", "Service A") make diagrams useless.

---

## Step 1: Map Concepts to Visual Patterns

For each major concept, choose the pattern that mirrors its behavior. Full CLI examples in `references/patterns.md`.

| If the concept... | Use this pattern |
|------------------|-----------------|
| Spawns multiple outputs | Fan-out (radial arrows from center) |
| Combines inputs into one | Convergence (arrows merging to a point) |
| Has levels / hierarchy | Tree (lines + free-floating text) |
| Is a sequence of steps | Timeline (line + dot markers + labels) |
| Loops or improves continuously | Cycle (arrows returning to start) |
| Groups related components | Swim lanes (zone backgrounds) |
| Transforms input to output | Assembly line (before → process → after) |
| Has many typed subtypes | Hub-and-spoke (center + spokes) |
| Compares two options | Side-by-side (parallel columns) |

**Variety rule**: Each major concept must use a different visual pattern. No uniform grids of identical boxes.

---

## Step 2: Evidence Artifacts (Technical Diagrams)

Evidence artifacts make technical diagrams accurate and educational. Required whenever you diagram a real system.

| Artifact type | When to use | How to build with CLI |
|--------------|-------------|----------------------|
| Code snippet | APIs, integrations, how-to | Dark rect (`--bg "#1e293b"`) + monospace text elements |
| Data / JSON payload | Message formats, schemas | Dark rect + green text (`--color "#22c55e"`) |
| Event sequence | Protocols, lifecycles | Timeline with real event names |
| Real API / method names | SDK usage, endpoints | Use actual names in labels — never "doSomething()" |

---

## Step 3: Multi-Zoom Architecture (Comprehensive Diagrams)

Build at three levels simultaneously:

**Level 1 — Summary strip**: A simplified overview at the top/bottom showing the full flow. Example: `User → Auth → Core API → DB`

**Level 2 — Section boundaries**: Labelled, colored zone backgrounds grouping related components into visual "rooms".

**Level 3 — Detail inside sections**: Evidence artifacts, code snippets, real data. This is where educational value lives.

---

## Step 4: Plan Before Writing Commands

**Do not write a single CLI command until you have completed both sub-steps.**

### 4a — Color plan (write as bash comments)

Map every node to its semantic color pair from `references/color-palette.md` before building. Color discipline degrades as element count rises — plan it once upfront:

```bash
# COLOR PLAN
# Web App, Mobile App  → bg "#bfdbfe"  stroke "#1e40af"   (Clients/Users)
# API Gateway          → bg "#bbf7d0"  stroke "#15803d"   (Gateway)
# Auth Service         → bg "#fed7aa"  stroke "#c2410c"   (Security/Edge)
# Payment Service      → bg "#86efac"  stroke "#15803d"   (App Service)
# Postgres             → bg "#ddd6fe"  stroke "#6d28d9"   (Data/Storage)
# Redis                → bg "#fef08a"  stroke "#92400e"   (Async/Queue — use #92400e NOT #a16207)
```

At the nodes checkpoint, verify each node's actual color matches this plan.

### 4b — Coordinates + arrows

1. List every node and connection in a table
2. **Structured layout**: choose a template from `references/layout-rules.md`
   **Freeform layout**: pick a gravity center (the most-connected node), place it at canvas center, then place other nodes by relationship distance — directly connected = 200–300px away, indirectly connected = 400–500px away. Use cluster background rectangles (not full-width zones) to show groupings.
3. Assign `x`, `y`, `w`, `h` to every node; verify `min_width = max(120, len(label)*9.6+32)`
4. Trace every arrow — identify stagger values for fan-out sources and shared-target entries
5. Arrows default to `--start-arrowhead none --end-arrowhead arrow` — never omit `--start-arrowhead none`

---

## Step 5: Build the Diagram

Full command reference in `references/cli-reference.md`. Critical rules:

1. Add zone backgrounds **first** (they appear behind nodes)
2. Capture every element ID you'll connect: `ID=$(add ... | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")`
3. Use the bash array `conn()` helper — never inline `${:+--flag value}` expansion with hex colors (breaks Click)
4. Read `references/color-palette.md` — every `--bg` and `--stroke` must come from there

---

## Step 6: Render and Validate (Mandatory)

You cannot judge a diagram from CLI commands alone. Export and view it.

```bash
$CLI -p "$P" export png -o /tmp/diagram.png --overwrite
# Then use the Read tool to view the PNG
```

### The loop

1. Export PNG → read it with Read tool
2. **Vision check** — does the structure match the concept you planned? Eye flow correct? Hierarchy clear?
3. **Defect check** — look for:
   - Text truncated or overflowing boxes
   - Nodes bleeding into adjacent zone backgrounds (Rule 11)
   - Long diagonal arrows crossing swim lanes (Rule 12)
   - Output nodes above their lane instead of at the far right (Rule 13)
   - Font sizes below 12px (Rule 14)
   - All arrows looking identical (Rule 15)
   - **Color audit**: each node's fill matches the color plan from Step 4a — wrong colors (e.g. Postgres orange instead of purple) mean a `--bg` value was copied from the wrong node
   - **Arrow direction audit**: any arrow showing arrowheads at both ends has a missing `--start-arrowhead none`
4. Fix coordinates, labels, connections → re-export → re-view
5. Repeat until both checks pass. Typically 2–3 iterations.

---

## Quality Checklist

### Philosophy
- [ ] Isomorphism test passes — structure alone communicates the concept
- [ ] No uniform card grids — each major concept uses a different visual pattern
- [ ] < 30% of text elements inside containers

### Depth & Evidence
- [ ] Real terminology used — no "API", "Service", "Data" placeholders
- [ ] Evidence artifacts present for technical diagrams
- [ ] Multi-zoom structure: summary strip + zone labels + detail

### Layout
- [ ] All nodes: x ≥ 200, y ≥ 150
- [ ] All labels: `max(120, len(label)*9.6+32)` width applied
- [ ] Zone clearance: node right edge ≥ 30px from adjacent zone start
- [ ] No cross-lane long diagonals
- [ ] Terminal nodes are rightmost in their lane
- [ ] All `--fs` values ≥ 12
- [ ] Arrow styles differentiate: spokes (dotted gray), cross-connections (colored dashed), primary flow (solid black)

### Connections
- [ ] Every relationship has an arrow
- [ ] Arrow colors from `references/color-palette.md` arrow conventions
- [ ] No node receives more than 3 inbound arrows
- [ ] Bidirectional: `--start-arrowhead arrow --end-arrowhead arrow`

### After Render
- [ ] No text overflow or truncation
- [ ] No zone boundary violations
- [ ] Arrows land on the correct elements
- [ ] All text legible at export size
- [ ] Composition balanced — no voids, no overcrowded regions
