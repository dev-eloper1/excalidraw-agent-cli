# Layout Rules

20 rules for building readable, well-proportioned diagrams. Every diagram must satisfy all 20 before export.

---

## Rules 1–5: Coordinate Foundations

### Rule 1 — Canvas Origin Margin

Every element must start at `x ≥ 200, y ≥ 150`. Content placed below this threshold gets cropped or hidden in Excalidraw's default viewport.

```
❌  add rectangle --x 50 --y 50 ...
✅  add rectangle --x 200 --y 200 ...
```

### Rule 2 — Node Spacing (Minimum Gap)

Horizontal gap between adjacent nodes: **≥ 40px**.
Vertical gap between rows: **≥ 30px**.

```
# Two nodes side by side, each 180px wide:
Node A at x=200, Node B at x=200+180+40 = x=420  ✅
Node B at x=200+180+10 = x=390                    ❌ (10px gap too tight)
```

### Rule 3 — Label Width Formula

Never hard-code a width without checking it fits the label:

```
min_width = max(120, len(label) * 9.6 + 32)
```

Examples:
| Label | len | Formula | Use |
|-------|-----|---------|-----|
| `"DB"` | 2 | max(120, 51) | **120** |
| `"Auth Service"` | 12 | max(120, 147) | **147** → round up to **160** |
| `"Notification Svc"` | 16 | max(120, 186) | **186** → round up to **195** |
| `"PostgreSQL Read Replica"` | 23 | max(120, 253) | **253** → round up to **260** |

Always round up to the nearest 10px for clean numbers.

### Rule 4 — Row Height Standards

| Node type | Height |
|-----------|--------|
| Standard service / component | `72` |
| Wide gateway spanning columns | `72` |
| Decision diamond | `90–100` |
| Start / End ellipse | `70` |
| Zone background | `≥ node_height + 30` (15px padding top + bottom) |

### Rule 5 — Inter-Zone Horizontal Gap

Leave **≥ 80px** between the right edge of one zone and the left edge of the next zone's first node. This prevents arrows from crossing zone boundaries at tight angles.

```
Zone A: x=185, w=600  → right edge at x=785
Zone B first node: x ≥ 785 + 80 = x=865   ✅
```

---

## Rules 6–9: Zone Backgrounds

### Rule 6 — Draw Zone Backgrounds Before Nodes

Zone backgrounds (semi-transparent rectangles) must be drawn **before** the nodes inside them. Excalidraw renders elements in insertion order — backgrounds drawn after nodes will cover them.

```bash
# ✅ Correct order:
add rectangle --x 185 --y 155 -w 820 -h 140 --bg "#dbeafe" ... > /dev/null  # zone bg
add rectangle --x 205 --y 195 -w 160 -h 72 --label "Web App" ...             # node
```

### Rule 7 — Zone Padding

Nodes must sit at least **15px inside** the zone background on all sides:

```
zone_x = first_node_x - 20
zone_y = first_node_y - 40   (extra space for zone label)
zone_w = (last_node_right_edge) - zone_x + 20
zone_h = node_height + 60    (40px top for label, 20px bottom)
```

### Rule 8 — Zone Labels

Place zone label text **above** the first row of nodes, at `y = zone_top + 8`.

```bash
add text --x 195 --y 163 --fs 14 --ff 2 --color "#1e40af" -t "CLIENTS" > /dev/null
#                                                  ↑ zone_top=155, label at 155+8=163
```

Zone label colors by type:
| Zone | `--color` |
|------|-----------|
| Client / Users | `#1e40af` |
| Services / API | `#15803d` |
| Data / Storage | `#6d28d9` |
| Async / Queue | `#a16207` |
| Security / Edge | `#c2410c` |
| Observability | `#be123c` |

### Rule 9 — Zone Width Covers All Children

The zone background width must extend to cover the rightmost node's right edge plus 20px:

```
zone_w = (rightmost_node_x + rightmost_node_w) - zone_x + 20
```

If you add nodes after setting the zone, recalculate and use `element update` to resize the zone.

---

## Rules 10–15: Readability and Visual Hierarchy

### Rule 10 — Auto-Width Applied Before Every `add`

Check Rule 3 before every node. The CLI auto-applies the formula when `--w` is omitted — but if you specify `--w`, you are responsible for the label fitting.

**When to omit `--w`**: Small diagrams with short labels.
**When to specify `--w`**: Anytime the label is longer than 10 characters or the node must align with others.

### Rule 11 — Zone Boundary Clearance (30px minimum)

A node's right edge must be ≥ 30px away from the x-coordinate of the adjacent zone's left border.

```
Node right edge = node_x + node_w
Next zone start = zone_b_x

Required: node_x + node_w ≤ zone_b_x - 30
```

If a node bleeds into the next zone visually (even if coordinates are correct), increase the gap between zones.

### Rule 12 — No Long Cross-Lane Diagonals

An arrow that spans more than one full zone width and travels diagonally makes the diagram unreadable. When you need to connect elements across swim lanes:

1. **Preferred**: Route through a shared element in a middle lane (e.g., API Gateway)
2. **Fallback**: Use a short horizontal segment within one lane, then a vertical drop to the target lane — implement as two arrows through an invisible waypoint, or just accept the auto-routing
3. **Forbidden**: A single arrow from top-left to bottom-right spanning 3+ zones

### Rule 13 — Terminal Nodes Are Rightmost in Their Lane

The "result", "output", or "end" node in a flow should be the rightmost element in its horizontal band. This mirrors reading direction — the eye travels left to right through the process and ends at the result.

```
❌  [Raw] → [Transform] → [DB]  [Output at x=200 — same column as input!]
✅  [Raw] → [Transform] → [DB]  → [Clean Data at x=800 — rightmost]
```

For vertical flowcharts, the terminal node is at the **bottom**.

### Rule 14 — Minimum Font Size: 12px

All text elements must use `--fs 12` or larger:
- Zone labels: `--fs 14`
- Node labels (inside shapes): rendered by Excalidraw — controlled by shape size, not `--fs`
- Free-floating annotations: `--fs 12` minimum, `--fs 13–14` preferred
- Evidence artifact code: `--fs 12` minimum

```bash
❌  add text --x 200 --y 300 --fs 10 ...
✅  add text --x 200 --y 300 --fs 12 ...
```

### Rule 15 — Arrow Styles Must Differentiate

Never let all arrows look identical. Apply this style vocabulary:

| Relationship | Style | Color |
|--------------|-------|-------|
| Hub → spoke (type fan-out) | `--stroke-style dotted --sw 1` | `#94a3b8` (slate gray) |
| Cross-connections (lateral) | `--stroke-style dashed --sw 2` | semantic color |
| Primary request flow | `--stroke-style solid --sw 2` | `#1e1e1e` (black) |
| Async / event | `--stroke-style dashed --sw 2` | `#a16207` (amber) |
| Error / failure | `--stroke-style dashed --sw 2` | `#dc2626` (red) |
| Data read/write | `--stroke-style solid --sw 2` | `#6d28d9` (purple) |
| Feedback loop | `--stroke-style dashed --sw 2` | `#be123c` (rose) |

### Rule 16 — Sequence Diagrams: Use Explicit Arrow Coordinates

NEVER use `element connect -l "label"` for sequence diagram step arrows. The label renders ON the arrow line and is unreadable. Instead:
1. Draw arrows with `add arrow --x start_x --y step_y --ex end_x --ey step_y` (perfectly horizontal, explicit coords)
2. Add the label as a separate `add text` element placed **20px above** the arrow midpoint

```bash
# Participant center x values:
# P1_CX = p1_x + p1_w/2
# P2_CX = p2_x + p2_w/2
# Step row y = 300 + (step_num * 100)  ← 100px per step
# Label x = (P1_CX + P2_CX) / 2 - estimated_label_width/2
# Label y = step_y - 20

# Step 1: P1 → P2
add arrow --x "$P1_CX" --y 300 --ex "$P2_CX" --ey 300 \
  --stroke "#c2410c" --sw 2 --stroke-style solid \
  --end-arrowhead arrow --start-arrowhead none > /dev/null
add text --x 380 --y 280 --fs 13 --ff 2 --color "#1e293b" -t "1. POST /auth/login" > /dev/null

# Response (right-to-left, dashed):
add arrow --x "$P2_CX" --y 400 --ex "$P1_CX" --ey 400 \
  --stroke "#15803d" --sw 2 --stroke-style dashed \
  --end-arrowhead arrow --start-arrowhead none > /dev/null
add text --x 380 --y 380 --fs 13 --ff 2 --color "#6b7280" -t "2. 200 OK + token" > /dev/null
```

Vertical spacing: **100px per step** minimum. Participants at y=200, lifelines from y=278, first step at y=340.

### Rule 17 — Decision Branch Spacing

For flowcharts with left/right branches from a diamond:
- The entire diagram must be wide enough that the left branch node stays at x ≥ 200
- Required minimum layout:
  - Left branch: x=200, w=160 → right edge=360
  - Diamond: x ≥ 420 (gap of 60px from left branch right edge)
  - Diamond w=240 → right edge = 660
  - Right branch: x ≥ 720 (gap of 60px from diamond right edge)

```
[ERR x=200]  60px gap  [Diamond x=420, w=240]  60px gap  [OK x=720]
                        center_x = 540
[vertical column centered over diamond: x=440, w=200]
```

If the diamond must be centered: shift the whole diagram so left branch x ≥ 200.

### Rule 18 — Mind Map Layout: Left-to-Right Tree

Mind maps must use a **left-to-right tree**, not a radial hub-and-spoke. Hub-and-spoke produces visual clutter and poor hierarchy. Tree structure:

```
Root (ellipse, x=200)  →  Branch nodes (x=500)  →  Sub-labels (x=800, free text)
```

- Root: large ellipse at x=200, vertically centered over all branches
- Branch nodes: spaced 130px vertically at x=500
- Sub-labels: free-floating text at x=800, no boxes needed
- Connections: use `--end-arrowhead none` (plain lines, not arrows) or dotted gray lines

```bash
# 5 branches, total height = 5*130 = 650px
# Center root vertically: root_y = (top_branch_y + bottom_branch_y) / 2 - root_h/2
# top_branch_y=160, bottom_branch_y=680 → root_y = (160+680)/2 - 40 = 380
ROOT=$(add ellipse --x 200 --y 380 -w 200 -h 80 --label "Root" --bg "#1e293b" --stroke "#e2e8f0" --fill-style solid --roughness 0 --sw 2)  # light stroke = readable label (Rule 22)

B1=$(add rectangle --x 500 --y 160 -w 200 -h 65 --label "Branch 1" ...)
B2=$(add rectangle --x 500 --y 290 -w 200 -h 65 --label "Branch 2" ...)
# ... etc

# Plain line connections (no arrowhead = tree aesthetic)
$CLI --project "$P" --json element connect --from "$ROOT" --to "$B1" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid --end-arrowhead none > /dev/null

# Sub-labels as free text beside branch nodes
add text --x 715 --y 148 --fs 12 --ff 1 --color "#1e40af" -t "sub-item 1" > /dev/null
add text --x 715 --y 166 --fs 12 --ff 1 --color "#1e40af" -t "sub-item 2" > /dev/null
```

### Rule 19 — Multi-Layer Architecture: Use Zone Grouping

For diagrams with 4+ components in a fan-out (microservices, etc.), group services into **labeled zone columns**:
- Column 1 (Edge/Ingress): CDN, Load Balancer, API Gateway
- Column 2 (Services): individual microservices
- Column 3 (Data/External): databases, queues, external APIs

Each column gets a zone background. Vertical spacing between services: 110px. Arrow routes go horizontally between columns, never diagonally across 2+ columns.

### Rule 20 — No Double Arrows Between Adjacent Nodes

When two nodes are at the same y-coordinate, `element connect` may produce doubled or curved arrows due to Excalidraw's auto-routing. Prevention:
- Ensure ≥ 60px horizontal gap between adjacent same-row nodes
- For same-row connections, use `add arrow` with explicit coordinates instead of `element connect`
- Never connect two nodes that share both a y-coordinate AND are within 40px of each other

### Rule 21 — Title Spacing: 60px Minimum Below Title Baseline

The title text and the first diagram element (zone background, node, or annotation) must have **≥ 60px vertical clearance**. Closer than this and they visually collide or overlap.

```
Title at y=15, font-size=22 → baseline ≈ y=37
First element must start at y ≥ 37 + 60 = y=97
```

Recommended safe baseline:
- Title: `--y 15 --fs 20`  (baseline ≈ y=35)
- First zone or node: `--y 100` minimum

For diagrams with a ∩ fail path or legend just below the title, place the extra element between title and main content — but still give the title at least 15px of breathing room before the next element.

### Rule 22 — Label Contrast: Always Match Text Color to Background

In Excalidraw, `--stroke` sets **both** the border color and the label text color inside shapes. There is no separate label-color flag.

**Fail modes:**
- `--bg "#1e293b" --stroke "#334155"` → unreadable dark-on-dark ❌
- `--bg "#fef08a" --stroke "#a16207"` → muddy amber-on-yellow ❌

**Fix:**
- Dark backgrounds (`#1e293b`, `#0f172a`, `#334155`, any bg with lightness < 40%): use `--stroke "#e2e8f0"` (near-white label + light border)
- Pale yellow bg (`#fef08a`): use `--stroke "#92400e"` (dark brown — high contrast)
- Pale pink bg (`#fecdd3`): use `--stroke "#9f1239"` (dark rose)
- When in doubt: aim for ≥ 4.5:1 contrast ratio between `--stroke` and `--bg`

```bash
# ✅ Dark hub node — readable white-ish label text
ROOT=$(add ellipse --x 200 --y 380 -w 200 -h 80 \
  --label "Root" --bg "#1e293b" --stroke "#e2e8f0" --fill-style solid)

# ❌ WRONG — label invisible on dark bg
ROOT=$(add ellipse --x 200 --y 380 -w 200 -h 80 \
  --label "Root" --bg "#1e293b" --stroke "#334155" --fill-style solid)
```

---

## Canonical Layout Templates

Choose the template that matches your diagram type, then substitute your actual values.

---

### Template A — Horizontal Architecture (Swim Lanes)

Best for: 3-layer system architectures (clients → services → data), API flows, microservice maps.

```
Canvas: 1200px wide × 600px tall

Zone 1 (Clients):   x=185, y=155, w=970, h=140
Zone 2 (Services):  x=185, y=315, w=970, h=140
Zone 3 (Data):      x=185, y=475, w=970, h=140

Zone labels at y = zone_top + 8
Node rows:
  Row 1: y=195, h=72
  Row 2: y=355, h=72
  Row 3: y=515, h=72

Node columns (3-column example):
  Col 1: x=205
  Col 2: x=415   (205 + 160 + 50)
  Col 3: x=625   (415 + 160 + 50)
  Col 4: x=835   (625 + 160 + 50) — optional 4th column
```

```bash
#!/usr/bin/env bash
set -e
CLI=$(which excalidraw-agent-cli)
P=/tmp/arch.excalidraw

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local from="$1" to="$2" label="$3" color="$4" style="$5"
  local args=("--from" "$from" "--to" "$to")
  [[ -n "$label" ]] && args+=("-l" "$label")
  [[ -n "$color" ]] && args+=("--stroke" "$color")
  [[ -n "$style" ]] && args+=("--stroke-style" "$style")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "arch" --output "$P" > /dev/null

# Zone backgrounds (before nodes)
add rectangle --x 185 --y 155 -w 970 -h 140 --bg "#dbeafe" --stroke "#93c5fd" --fill-style solid --opacity 15 --sw 1 > /dev/null
add rectangle --x 185 --y 315 -w 970 -h 140 --bg "#dcfce7" --stroke "#86efac" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 185 --y 475 -w 970 -h 140 --bg "#ede9fe" --stroke "#c4b5fd" --fill-style solid --opacity 20 --sw 1 > /dev/null

# Zone labels
add text --x 195 --y 163 --fs 14 --ff 2 --color "#1e40af" -t "CLIENTS"  > /dev/null
add text --x 195 --y 323 --fs 14 --ff 2 --color "#15803d" -t "SERVICES" > /dev/null
add text --x 195 --y 483 --fs 14 --ff 2 --color "#6d28d9" -t "DATA"     > /dev/null

# Row 1 — Clients
WEB=$(    add rectangle --x 205 --y 195 -w 160 -h 72 --label "Web App"    --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid)
MOBILE=$( add rectangle --x 415 --y 195 -w 160 -h 72 --label "Mobile App" --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid)

# Row 2 — Services
GW=$(add rectangle --x 205 --y 355 -w 580 -h 72 --label "API Gateway" --bg "#86efac" --stroke "#15803d" --fill-style solid)

# Row 3 — Data
DB=$(    add rectangle --x 205 --y 515 -w 160 -h 72 --label "PostgreSQL" --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid)
CACHE=$( add rectangle --x 415 --y 515 -w 160 -h 72 --label "Redis"      --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid)

conn "$WEB"    "$GW" "" "#1e40af"
conn "$MOBILE" "$GW" "" "#1e40af"
conn "$GW"     "$DB"    "" "#6d28d9"
conn "$GW"     "$CACHE" "" "#6d28d9"
```

---

### Template B — Vertical Flowchart

Best for: decision trees, request lifecycles, user journeys, step-by-step processes.

```
Canvas: 600px wide × 800px tall

Center x = 400
Node widths: diamonds=240, rectangles=200, ellipses=180

Node column:  x = center_x - node_w/2
Row spacing:  120px between rows (node_h=72, gap=48)

Rows:
  Row 1 (Start):    y=180
  Row 2 (Step):     y=300
  Row 3 (Decision): y=420
  Row 4a (Branch):  y=540, x = center_x + 160   (right branch)
  Row 4b (Branch):  y=540, x = center_x - 240   (left branch, wider)
  Row 5 (End):      y=660
```

```bash
START=$(  add ellipse   --x 310 --y 180 -w 180 -h 70 --label "Start"    --bg "#a7f3d0" --stroke "#047857")
STEP1=$(  add rectangle --x 300 --y 300 -w 200 -h 72 --label "Validate" --bg "#bfdbfe" --stroke "#1e40af")
DECIDE=$( add diamond   --x 280 --y 420 -w 240 -h 90 --label "Valid?"   --bg "#fef3c7" --stroke "#b45309")
OK=$(     add rectangle --x 480 --y 540 -w 160 -h 72 --label "Process"  --bg "#86efac" --stroke "#15803d")
ERR=$(    add rectangle --x 120 --y 540 -w 160 -h 72 --label "Reject"   --bg "#fecaca" --stroke "#b91c1c")
END=$(    add ellipse   --x 310 --y 660 -w 180 -h 70 --label "End"      --bg "#a7f3d0" --stroke "#047857")

conn "$START"  "$STEP1"
conn "$STEP1"  "$DECIDE"
conn "$DECIDE" "$OK"  "yes" "#15803d"
conn "$DECIDE" "$ERR" "no"  "#b91c1c"
conn "$OK"     "$END"
conn "$ERR"    "$END"
```

---

### Template C — Sequence / Protocol

Best for: auth flows, API request/response, event sequences, messaging protocols.

```
Participants across top (columns), time flows downward

Column spacing: 200px
Participant row: y=180, h=70
Timeline spine: from y=280 downward, one per participant

Sequence steps: every 110px down from y=300
```

```bash
# Participants
USER=$(   add rectangle --x 200 --y 180 -w 160 -h 70 --label "User"    --bg "#bfdbfe" --stroke "#1e40af")
GW=$(     add rectangle --x 440 --y 180 -w 160 -h 70 --label "Gateway" --bg "#86efac" --stroke "#15803d")
AUTH=$(   add rectangle --x 680 --y 180 -w 160 -h 70 --label "Auth"    --bg "#86efac" --stroke "#15803d")

# Timeline spines (vertical lines below each participant)
add line --x 280 --y 260 --points "0,0 0,400" --stroke "#e2e8f0" --sw 1 > /dev/null
add line --x 520 --y 260 --points "0,0 0,400" --stroke "#e2e8f0" --sw 1 > /dev/null
add line --x 760 --y 260 --points "0,0 0,400" --stroke "#e2e8f0" --sw 1 > /dev/null

# Step markers (small ellipses on spine)
add ellipse --x 274 --y 300 -w 12 -h 12 --bg "#3b82f6" --stroke "#1e40af" --fill-style solid --roughness 0 > /dev/null
add ellipse --x 514 --y 340 -w 12 -h 12 --bg "#3b82f6" --stroke "#1e40af" --fill-style solid --roughness 0 > /dev/null

# Step labels
add text --x 296 --y 293 --fs 13 --ff 2 --color "#1e293b" -t "POST /login" > /dev/null
add text --x 296 --y 313 --fs 12 --ff 3 --color "#6b7280" -t '{"email":"user@co","password":"..."}' > /dev/null

# Horizontal sequence arrows between participants
SEQ1=$(add rectangle --x 200 --y 300 -w 1 -h 1 --label "" --bg "#transparent" --stroke "#transparent")
conn "$USER" "$GW" "POST /login" "#1e1e1e"
```

---

## Pre-Build Checklist

Run this mental check before writing any CLI commands:

```
□ Every node has x, y, w, h assigned in a planning table
□ All labels checked against min_width formula (Rule 3)
□ Zone backgrounds listed first in command order (Rule 6)
□ Zone padding verified: 15px all sides, 40px top for label (Rule 7)
□ All x ≥ 200, y ≥ 150 (Rule 1)
□ Node gaps: ≥ 40px horizontal, ≥ 30px vertical (Rule 2)
□ Inter-zone gap: ≥ 80px (Rule 5)
□ No long cross-lane diagonals planned (Rule 12)
□ Terminal nodes are rightmost/bottommost (Rule 13)
□ All text --fs ≥ 12 (Rule 14)
□ Arrow styles vary (Rule 15)
□ Sequence diagram arrows: explicit add arrow coords, labels as separate text 20px above
□ Decision branches: left branch x≥200, 60px gap both sides of diamond
□ Mind maps: left-to-right tree layout, not radial
□ Fan-out with 4+ targets: zone column grouping, not plain fan-out
□ Same-row nodes: ≥60px gap to prevent double-arrow routing
```

## Post-Build Checklist (After PNG Export)

```
□ No text overflow: node labels visible, not cut off
□ No zone boundary bleeding (Rule 11)
□ Arrows land on correct elements (not dangling)
□ All text legible at export resolution (Rule 14)
□ Composition balanced: no large empty regions, no overcrowded clusters
□ Eye flow: left→right or top→bottom follows the narrative
□ Structure passes isomorphism test: remove all text — shape alone communicates concept
```
