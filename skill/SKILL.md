---
name: excalidraw
description: Create, edit, and export Excalidraw diagrams (flowcharts, architecture diagrams, mind maps, system designs) using the excalidraw-agent-cli CLI tool. Use this skill whenever the user asks to draw, diagram, visualize, chart, or map out anything — flowcharts, system architecture, process flows, network diagrams, org charts, sequence diagrams, mind maps, wireframes, or any other visual diagram. Also trigger when the user says things like "create a diagram", "draw a flowchart", "sketch out the architecture", "visualize this", "make a chart of", "diagram this for me", "show me how X connects to Y", "export to SVG/PNG from excalidraw", or wants to open a .excalidraw file. Even if the user doesn't say "excalidraw" explicitly, trigger this skill for any diagramming request.
---

# Excalidraw CLI Skill

You have access to a fully installed `excalidraw-agent-cli` CLI. Use it to build diagrams that **argue, not just display** — if you removed all text, the structure alone should communicate the concept.

## Environment Setup

```bash
# Locate the CLI — works whether installed via pip or from source
CLI=$(which excalidraw-agent-cli 2>/dev/null || echo "")
if [[ -z "$CLI" ]]; then
  echo "ERROR: excalidraw-agent-cli not found. Install with: pip install excalidraw-agent-cli" >&2
  exit 1
fi

# Add common Node.js locations to PATH so the export backend can find `node`
export PATH="$PATH:/usr/local/bin:/opt/homebrew/bin:$HOME/.nvm/versions/node/$(node --version 2>/dev/null | tr -d v)/bin"
```

Use **absolute paths** for all `--project` and `--output` arguments.

## CRITICAL: Flag Placement

`--project` and `--json` are **global flags** — before the subcommand:

```bash
✅  $CLI --project $PROJECT --json element add rectangle --x 200 --y 150
❌  $CLI element add rectangle --project $PROJECT --x 200 --y 150  # errors
```

Arrow labels **must use `-l`** (short form) to handle spaces:
```bash
✅  $CLI --project $PROJECT --json element connect --from $A --to $B -l "1. Authenticate"
❌  --label "1. Authenticate"  # fails with spaces
```

---

## Color Palette

Always use these **paired fill + stroke** combinations. Never invent colors.

| Layer / Purpose | `--bg` (fill) | `--stroke` | `--fill-style` |
|-----------------|--------------|------------|----------------|
| **Clients** | `#bfdbfe` | `#1e40af` | `solid` |
| **Security / Edge** | `#fed7aa` | `#c2410c` | `solid` |
| **Gateway / Routing** | `#bbf7d0` | `#15803d` | `solid` |
| **Application Services** | `#86efac` | `#15803d` | `solid` |
| **Async / Queue** | `#fef08a` | `#a16207` | `solid` |
| **Data / Storage** | `#ddd6fe` | `#6d28d9` | `solid` |
| **Observability** | `#fecdd3` | `#be123c` | `solid` |
| **Decision diamond** | `#fef3c7` | `#b45309` | `solid` |
| **Error / Reject** | `#fecaca` | `#b91c1c` | `solid` |
| **Success / End** | `#a7f3d0` | `#047857` | `solid` |
| **External / Third-party** | `#fed7aa` | `#c2410c` | `solid` |
| **Legacy / Uncertain** | `#f1f5f9` | `#475569` | `hachure` |

Always pass **both** `--bg` and `--stroke` for colored elements:
```bash
$CLI --project $P --json element add rectangle --x 200 --y 150 -w 180 -h 80 \
  --label "Auth Service" --bg "#86efac" --stroke "#15803d" --fill-style solid
```

---

## Shape Reference

### Available element types

| Type | Key flags | Notes |
|------|-----------|-------|
| `rectangle` | `--label`, `--bg`, `--stroke`, `--fill-style`, `--sw`, `--roughness`, `--opacity`, `--roundness` | `--roundness` for pill corners |
| `ellipse` | same as rectangle minus `--roundness` | Use for actors/users/start nodes |
| `diamond` | same as ellipse | Use for decisions/branches |
| `text` | `-t "text"`, `--fs`, `--ff`, `--color`, `--text-align`, `--opacity` | Content is positional or `-t` |
| `arrow` | `--stroke`, `--sw`, `--stroke-style`, `--roughness`, `--start-arrowhead`, `--end-arrowhead`, `-l` | Standalone or bound via `--from`/`--to` |
| `line` | `--points "x,y x,y ..."`, `--stroke`, `--sw`, `--stroke-style`, `--roughness` | Multi-point polyline; points are relative to `--x`/`--y` |
| `frame` | `-w`, `-h`, `--stroke`, `--name` | Container/grouping; children use `--frame-id $FRAME_ID` (rectangle only) |

### Fill styles

All shapes support `--fill-style`:

| Value | Visual | Best for |
|-------|--------|---------|
| `solid` | Flat color fill | Active/confirmed components |
| `hachure` | Diagonal lines | Legacy, uncertain, or in-progress |
| `cross-hatch` | Grid lines | Reference or background zones |
| `zigzag` | Zigzag lines | Sketchy/draft look |
| `dots` | Dot pattern | Optional or low-priority |

### Roughness levels

`--roughness 0` = clean vector, `--roughness 1` = normal (default), `--roughness 2` = hand-drawn sketch.
Mix smooth and rough to signal "live vs future/planned".

### Opacity

`--opacity 0-100` works on all shapes and text. Use semi-transparent rectangles (opacity 15-30) as zone/swimlane backgrounds layered behind real nodes.

### Text element syntax

```bash
# Text does NOT use --label — use positional arg or -t:
$CLI --project $P --json element add text --x 400 --y 120 --fs 20 --ff 1 --color "#1e293b" -t "Section Title"
# Fonts: --ff 1 = Virgil (handwritten), --ff 2 = Helvetica, --ff 3 = Cascadia (monospace)
```

---

## Arrow & Connection Reference

### `element connect` — bind arrow between two shapes (recommended)

```bash
$CLI --project $P --json element connect \
  --from $A --to $B \
  -l "label text" \
  --stroke "#3b82f6" \
  --sw 2 \
  --stroke-style dashed \
  --roughness 0 \
  --start-arrowhead arrow \
  --end-arrowhead triangle
```

**All flags:**

| Flag | Values | Default |
|------|--------|---------|
| `--from`, `--to` | element IDs | required |
| `-l` | any string | none |
| `--stroke` | hex color | `#1e1e1e` |
| `--sw` | int | `2` |
| `--stroke-style` | `solid`, `dashed`, `dotted` | `solid` |
| `--roughness` | `0`-`2` | `1` |
| `--start-arrowhead` | `arrow`, `triangle`, `dot`, `bar`, `circle`, or omit | none |
| `--end-arrowhead` | `arrow`, `triangle`, `dot`, `bar`, `circle`, `None` | `arrow` |

Use `--start-arrowhead arrow --end-arrowhead arrow` for bidirectional arrows via `element connect`.

### `element add arrow` — freestanding arrow (for legends/annotations)

```bash
$CLI --project $P --json element add arrow \
  --x 200 --y 300 --ex 400 --ey 300 \
  --stroke "#dc2626" --sw 3 --stroke-style dashed --roughness 2 \
  --start-arrowhead arrow --end-arrowhead triangle \
  -l "bidirectional"
```

Additional flags over `connect`: `--x/--y/--ex/--ey` coordinates for precise positioning.

### Arrowhead types

| Value | Shape |
|-------|-------|
| `arrow` | Classic open arrowhead (default) |
| `triangle` | Filled solid triangle |
| `dot` | Circle endpoint |
| `bar` | Perpendicular bar (terminus) |
| `None` | No arrowhead (plain line) |

Use `--start-arrowhead` + `--end-arrowhead` together for bidirectional arrows.

### Arrow color conventions (use consistently)

| Relationship type | Color |
|------------------|-------|
| Normal request/call | `#1e1e1e` (default) |
| Async / event | `#a16207` (yellow-brown) |
| Error path | `#dc2626` (red) |
| Auth / security | `#c2410c` (orange) |
| Data read/write | `#6d28d9` (purple) |
| External call | `#0891b2` (cyan) |
| Observability / logs | `#be123c` (pink) |

### Line element for swimlanes/dividers

```bash
# Horizontal divider
$CLI --project $P --json element add line \
  --x 200 --y 500 --points "0,0 900,0" \
  --stroke "#e2e8f0" --sw 1 --stroke-style dashed

# Zigzag annotation path
$CLI --project $P --json element add line \
  --x 300 --y 400 --points "0,0 50,40 100,0 150,40 200,0" \
  --stroke "#be123c" --sw 2 --roughness 2
```

Points are **relative** to `--x`/`--y`.

---

## Layout Rules — Mandatory Before Planning

### Rule 1: Start at x ≥ 200, y ≥ 150

SVG viewBox is computed from element bounds. Elements at x < 150 clip at the left edge.
```
❌ x=50, x=60, x=80   (clips)
✅ x=200 minimum
```

### Rule 2: Use these canonical spacings

| Direction | Element size | Gap | Step |
|-----------|-------------|-----|------|
| Vertical rows | h=80 | 120px | **200px** (y+200 per row) |
| Horizontal cols | w=180 | 80px | **260px** (x+260 per col) |

For wider elements (w=200): x step = **280px**

### Rule 3: Prefer horizontal layouts for 4+ layer architectures

Vertical stacking of 6+ layers makes diagrams 1000px+ tall. Use left-to-right flow instead:
```
Clients → Edge → Gateway → Services → Data
```
Keep total Y span under 600px. Use X span freely.

### Rule 4: Center hub nodes over their targets

When one node fans out to N children, center the hub horizontally:
```
center_x = (leftmost_child_center + rightmost_child_center) / 2
hub_x    = center_x - hub_width / 2
```
This ensures arrows fan out cleanly without crossing.

### Rule 5: Never draw long diagonal return arrows

Loop-backs spanning the full diagram look like slashes. Instead:
- **Omit** response arrows when they're implied
- Place return targets **adjacent**, not across the diagram
- Use a text label annotation instead of a drawn arrow for long paths

### Rule 6: Keep labels ≤ 25 characters

Longer labels overflow boxes. Abbreviate ruthlessly:
```
❌ "Identity Provider (SSO / SAML / OIDC)"  →  ✅ "Identity Provider"
❌ "Core API (REST/GraphQL)"                 →  ✅ "Core API"
❌ "Message Queue (Kafka)"                   →  ✅ "Kafka / MQ"
```
If the full name is needed, add a standalone `text` element below as a caption.

### Rule 7: Every node must have at least one connection

Before exporting, walk every node: does it have ≥1 arrow in or out? Floating nodes with no connections look abandoned. Observability nodes must connect to the services they observe.

### Rule 8: Place decision diamonds immediately after their trigger

A JWT validation diamond belongs right after the gateway, not at the bottom. The diamond's position should mirror its logical place in the flow.

### Rule 9: Limit arrows into any single target to ~3

When 5+ arrows converge on one node, they overlap and create an X-pattern through the box. If a node would receive more than 3 arrows, restructure: add an intermediate aggregator node, or reroute some connections.

### Rule 10: Box width must fit its label (auto-enforced, still plan ahead)

The CLI auto-expands width to fit the label, but layout calculations should still account for it:
```
min_width = max(120, len(label) * 9.6 + 32)
# "excalidraw_backend" (18 chars) → max(120, 18*9.6+32) = 205px
```
If a node's auto-expanded width would push it into the next column, increase the column step or shorten the label.

### Rule 11: Zone boundary clearance — 30px minimum

A node's **right edge** (`x + width`) must be **at least 30px away** from the start `x` of the adjacent zone. Verify:
```
node.right_edge = node.x + node.width
assert node.right_edge ≤ next_zone.x - 30
```
When placing nodes in the rightmost position of a zone, use:
```
node.x = zone.x + zone.width - node.width - 30
```
If a label auto-expands the box and causes a violation, either widen the zone or shorten the label.

### Rule 12: Swim lane cross-connectors — no long diagonals

When an arrow must cross from one swim lane (row) to another far-away lane, **never** draw a direct diagonal. Instead:
- Route via a short vertical drop to a relay node, or
- Use a `line` element with waypoints (`--points "0,0 0,dy dx,dy dx,0"`)
- Or simply **omit** the cross-lane arrow and describe the relationship with a label

Long diagonals that span 2+ swim lanes create visual noise and obscure the flow direction.

### Rule 13: Terminal/output nodes belong at the END of their lane

Output or result nodes (SVG file, PNG file, report, response) must be placed at the **far-right end** of their row, not above it, not outside the lane:
```
❌ output_node.y = lane.y - 80   (floats above the lane)
✅ output_node.x = lane.x + lane.width - node.width - 20
   output_node.y = lane.y + (lane.height - node.height) / 2
```
If a lane ends with an output, it should be the rightmost element in that row.

### Rule 14: Minimum font sizes — never below 12px

| Text purpose | Minimum `--fs` |
|-------------|---------------|
| Annotation / caption | `12` |
| Section header / label | `14` |
| Main section titles | `16–20` |
| Never use | `< 12` (illegible at typical SVG zoom) |

### Rule 15: Hub-and-spoke vs cross-connection — always differentiate

When a hub fans out to N type nodes (spokes), use a visually distinct style from cross-connection arrows:

| Arrow purpose | Recommended style |
|--------------|------------------|
| Hub → spoke (type fan-out) | `--stroke "#94a3b8" --stroke-style dotted --sw 1` (thin gray dotted) |
| Cross-connection (A ↔ B) | `--stroke "#3b82f6" --stroke-style dashed --sw 2` (colored dashed) |
| Primary call flow | `--stroke "#1e1e1e" --stroke-style solid --sw 2` (default black) |

Never use red dashed arrows as the dominant pattern — reserve red for error paths only.

---

## Canonical Layout Templates

### Template A — Horizontal Architecture (4+ layers)

```
y=200:  [Client A]    [Client B]    [Client C]
         x=200         x=460         x=720    (step 260, w=180)

y=400:  [Edge A]      [Edge B]      [Edge C]
         x=200         x=460         x=720

y=600:  [──────────── API Gateway (wide) ────────────]
         x=200, w=720  (spans all columns)

y=800:  [Svc A]   [Svc B]   [Svc C]   [Svc D]
         x=200     x=415     x=630     x=845  (step 215, w=180)

y=1000: [DB]     [Cache]   [Search]  [Storage]
         x=200    x=415     x=630     x=845
```

GW center_x = 200 + 720/2 = 560  ✓ (centered over 4 services spanning 200–1025)

### Template B — Vertical Flowchart (≤ 6 steps)

```
y=200:  [Start]         x=350, w=200 (ellipse)
y=400:  [Step 1]        x=350, w=200
y=600:  [Decision?]     x=325, w=250 (diamond, h=120)
y=750:  [Yes]  x=600    [No]  x=100  (branch left/right)
y=950:  [End]           x=350, w=200
```

### Template C — Horizontal Auth / Sequence Flow

```
Row 1 (y=200, h=80):
  [User]    → [API Gateway] → [Auth Service] → [Identity Provider]
   x=200       x=430            x=660            x=900
   w=160,ellipse  w=180            w=180            w=180

Row 2 (y=400, h=80):
              [JWT Valid?]     [User Store]     [Session Cache]
               x=400,diamond    x=660            x=900
               w=230, h=110     w=180            w=180

Row 3 (y=580, h=80):
              [401 Unauth]     [Resource API]
               x=400            x=660
               w=180            w=180
```

---

## Core Workflow

### 1. Create project
```bash
rm -f /tmp/my-diagram.excalidraw
$CLI --json project new --name "my-diagram" --output /tmp/my-diagram.excalidraw
PROJECT=/tmp/my-diagram.excalidraw
```

### 2. Add elements (capture IDs)
```bash
# Helper pattern
add() { $CLI --project "$PROJECT" --json element add "$@" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])"; }

NODE=$(add rectangle --x 200 --y 150 -w 180 -h 80 \
  --label "My Service" --bg "#86efac" --stroke "#15803d" --fill-style solid)
```

### 3. Connect (with styled arrows)

**Use bash arrays** — do NOT use inline `${:+--flag value}` expansion because Click sees hex colors as part of the flag name:

```bash
conn() {
  local from="$1" to="$2" label="$3" color="$4" style="$5" head="$6"
  local args=("--from" "$from" "--to" "$to")
  [[ -n "$label" ]] && args+=("-l" "$label")
  [[ -n "$color" ]] && args+=("--stroke" "$color")
  [[ -n "$style" ]] && args+=("--stroke-style" "$style")
  [[ -n "$head"  ]] && args+=("--end-arrowhead" "$head")
  $CLI --project "$PROJECT" --json element connect "${args[@]}" > /dev/null
}

conn "$A" "$B"                              # default black solid arrow
conn "$A" "$B" "1. Login"                  # labeled
conn "$A" "$B" "async" "#a16207" "dashed"  # colored dashed
conn "$A" "$B" "" "#6d28d9" "dotted" "triangle"  # purple dotted triangle
```

Or for full control (bidirectional, etc.):
```bash
$CLI --project "$PROJECT" --json element connect \
  --from "$A" --to "$B" -l "payload" \
  --stroke "#6d28d9" --sw 3 --stroke-style dotted --roughness 0 \
  --start-arrowhead arrow --end-arrowhead triangle
```

### 4. Add zone backgrounds (optional, for swimlanes/groups)
```bash
# Semi-transparent background rectangle behind a cluster of nodes
$CLI --project "$PROJECT" --json element add rectangle \
  --x 180 --y 180 -w 600 -h 300 \
  --bg "#dbeafe" --stroke "#93c5fd" --fill-style solid --opacity 20
```
Add background zones **before** the nodes that sit on top of them, so they appear behind.

### 5. Add section labels
```bash
# Section header (Virgil handwritten font)
$CLI --project "$PROJECT" --json element add text \
  --x 200 --y 165 --fs 14 --ff 2 --color "#6b7280" -t "CLIENT LAYER"
```

### 6. Export
```bash
$CLI --project $PROJECT export svg --output /tmp/diagram.svg --overwrite
$CLI --project $PROJECT export png --output /tmp/diagram.png --overwrite
```

---

## Advanced Patterns

### Zone backgrounds (swimlanes)
Place a large semi-transparent rectangle first, then add nodes on top:
```bash
ZONE=$(add rectangle --x 190 --y 780 -w 840 -h 130 \
  --bg "#fef9c3" --stroke "#fbbf24" --fill-style solid --opacity 20 --sw 1)
# Then add nodes inside the zone's bounds
```

### Mixed roughness for status
```bash
# Live/stable: roughness 0
add rectangle ... --roughness 0 --fill-style solid
# Planned/future: roughness 2 + hachure
add rectangle ... --roughness 2 --fill-style hachure
```

### Colored arrow conventions in a single diagram
Use arrow color to encode relationship type so readers can scan the diagram by color:
- Black solid = synchronous call
- Yellow dashed = async event
- Red dashed = error/failure path
- Purple dotted = data read/write
- Cyan solid = external API call

### Polyline paths for complex flows
```bash
# Route a line around obstacles
$CLI --project "$PROJECT" --json element add line \
  --x 400 --y 300 --points "0,0 0,100 200,100 200,0" \
  --stroke "#6d28d9" --sw 2 --stroke-style dashed
```

---

## Pre-Build Checklist

Before writing a single command:

- [ ] Chose layout orientation (horizontal for 4+ layers, vertical for ≤6 sequential steps)
- [ ] Calculated coordinates for all nodes on paper — checked no node at x < 200
- [ ] Computed hub center_x = (leftmost_child_center + rightmost_child_center) / 2
- [ ] Counted inbound arrows per node — no node receives more than 3
- [ ] All labels ≤ 25 chars; computed min_width for each: `max(120, len(label)*9.6+32)`
- [ ] Every node has ≥1 connection planned
- [ ] Colors assigned from palette table above
- [ ] Arrow colors chosen to encode relationship types
- [ ] Verified each node's right edge (x + width) is ≥30px away from adjacent zone start
- [ ] Terminal/output nodes placed at far-right end of their lane row
- [ ] Cross-lane arrows replaced with relay nodes or waypoint lines
- [ ] All text font sizes ≥12px
- [ ] Hub spokes use dotted gray; cross-connections use colored dashed

## Post-Build Checklist

After exporting, inspect the output and verify:

- [ ] No elements clipped at left or right edge
- [ ] No arrows crossing through boxes
- [ ] No orphaned nodes
- [ ] No label overflow (node right edge not bleeding into adjacent zone)
- [ ] Decision diamonds are in the right logical position
- [ ] Observability / monitoring nodes are connected
- [ ] Return arrows are short or omitted
- [ ] No font sizes below 12px
- [ ] Output/terminal nodes are rightmost in their lane
- [ ] Arrow styles differentiate spoke vs cross-connection vs primary flow

---

## Mutating Elements

```bash
$CLI --project $PROJECT --json element update --id $ID --x 200 --y 200 --label "New"
$CLI --project $PROJECT --json element move   --id $ID --dx 50 --dy 0
$CLI --project $PROJECT --json element delete --id $ID
$CLI --project $PROJECT --json element list
$CLI --project $PROJECT session undo
$CLI --project $PROJECT --json session status
$CLI --json backend check
```

## Step-by-Step Approach

1. **Enumerate** all nodes and relationships explicitly in a table before touching the CLI
2. **Choose template** (A, B, or C above) and assign coordinates to every node
3. **Run pre-build checklist** — fix any issues before coding
4. **Create project**, add zone backgrounds first (if any), then shapes (collect IDs), then connect
5. **Export**, inspect output, run post-build checklist
6. **Fix and re-export** if any checklist item fails — iterate until clean
