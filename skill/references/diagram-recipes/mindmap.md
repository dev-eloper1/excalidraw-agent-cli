# Mind Map Diagram Recipe

## When to use

Use a mind map when you need to communicate **how a central concept branches into related topics**, and those topics may further branch into sub-topics. The key signal is a single root idea with non-linear, associative relationships radiating outward.

Choose this pattern when:
- You have one dominant root concept and 5–10 first-level branches
- Relationships are associative, not sequential (no strict order between branches)
- The narrative is "everything that relates to X" rather than "step 1 → step 2"
- Brainstorming, knowledge mapping, or concept overviews for technical topics (frameworks, languages, systems)

Do NOT use for: ordered processes (use flowchart), time-phased plans (use Gantt), layered system architectures (use architecture diagram), or message sequences (use sequence diagram).

> **Rule 18 note:** The layout-rules.md Rule 18 describes a left-to-right tree layout as the default. The radial layout described here is an alternative for concept-centric mind maps where the root has roughly equal branches on all sides. Both are valid; choose radial when the root concept has balanced coverage in all directions, choose left-to-right tree when branches have a natural reading order.

---

## Layout template

```
Canvas: 1200 × 800px, origin top-left (0, 0)

Title: x=20, y=15, --fs 20 --ff 2   (baseline ≈ y=37, Rule 21)
First element at y=97 minimum (37 + 60 = 97, Rule 21 satisfied)

Root ellipse (center of canvas):
  ROOT_X=510   ROOT_Y=370   ROOT_W=180  ROOT_H=100
  center_x = ROOT_X + ROOT_W/2 = 600
  center_y = ROOT_Y + ROOT_H/2 = 420

Branch ellipse geometry (level-1 nodes):
  BRANCH_W=160   BRANCH_H=60

Branch positions (8 compass points, anchored by top-left x,y):
  Right-center:  x=830,  y=390   → center (910, 420)
  Right-top:     x=830,  y=280   → center (910, 310)
  Right-bottom:  x=830,  y=500   → center (910, 530)
  Left-center:   x=210,  y=390   → center (290, 420)
  Left-top:      x=210,  y=280   → center (290, 310)
  Left-bottom:   x=210,  y=500   → center (290, 530)
  Top-center:    x=520,  y=180   → center (600, 210)  [≥ y=97 ✓]
  Bottom-center: x=520,  y=590   → center (600, 620)

Leaf ellipse geometry (level-2 nodes):
  LEAF_W=130   LEAF_H=45

  Leaves hang off each branch — example for Right-top branch at (830, 280):
    Leaf 1: x=990,  y=245   (to the right and slightly above)
    Leaf 2: x=990,  y=305   (to the right and slightly below)
  Mirror pattern for Left-top branch.

Named spacing variables:
  H_BRANCH_GAP=230    # horizontal distance from root center to branch center
  V_BRANCH_STEP=110   # vertical spacing between branch rows on same side
  H_LEAF_OFFSET=160   # horizontal offset from branch right edge to leaf left edge
  V_LEAF_STEP=60      # vertical spacing between sibling leaves
  ROOT_W=180          # root ellipse width
  ROOT_H=100          # root ellipse height
  BRANCH_W=160        # branch ellipse width
  BRANCH_H=60         # branch ellipse height
  LEAF_W=130          # leaf ellipse width
  LEAF_H=45           # leaf ellipse height
```

**Draw order:**
1. Title text
2. Root ellipse (dark navy)
3. Branch ellipses (level-1, color by topic)
4. Leaf ellipses (level-2, lighter fill)
5. Lines: root → each branch (`add line`, not `add arrow` — no arrowheads)
6. Lines: branch → each leaf

**Coordinate planning table (placeholder labels):**

| ID var   | Label        | x    | y    | w    | h   | Role         |
|----------|--------------|------|------|------|-----|--------------|
| ROOT     | ROOT_TOPIC   | 510  | 370  | 180  | 100 | Root         |
| BR_R     | BRANCH_R     | 830  | 390  | 160  | 60  | Right-center |
| BR_RT    | BRANCH_RT    | 830  | 280  | 160  | 60  | Right-top    |
| BR_RB    | BRANCH_RB    | 830  | 500  | 160  | 60  | Right-bottom |
| BR_L     | BRANCH_L     | 210  | 390  | 160  | 60  | Left-center  |
| BR_LT    | BRANCH_LT    | 210  | 280  | 160  | 60  | Left-top     |
| BR_LB    | BRANCH_LB    | 210  | 500  | 160  | 60  | Left-bottom  |
| BR_T     | BRANCH_T     | 520  | 180  | 160  | 60  | Top          |
| BR_B     | BRANCH_B     | 520  | 590  | 160  | 60  | Bottom       |

---

## Color and style defaults

### Root node

| Property      | Value       | Notes                                      |
|---------------|-------------|---------------------------------------------|
| `--bg`        | `#1e293b`   | Dark navy                                   |
| `--stroke`    | `#e2e8f0`   | Near-white — controls BOTH border AND label |
| `--fill-style`| `solid`     |                                             |
| `--roughness` | `0`         | Clean professional look                     |
| `--sw`        | `2`         |                                             |

> **CRITICAL (Rule 22):** `--stroke` in Excalidraw controls BOTH the border color AND the label text color inside shapes. Using a dark stroke on a dark background makes the label invisible. The root uses `--bg "#1e293b"` (dark navy), so you MUST use `--stroke "#e2e8f0"` (near-white) to keep the label readable.

### Branch level-1 nodes (semantic colors by topic area)

| Topic area          | `--bg`    | `--stroke` | `--fill-style` |
|---------------------|-----------|------------|----------------|
| Clients / Users     | `#bfdbfe` | `#1e40af`  | `solid`        |
| Application/Service | `#86efac` | `#15803d`  | `solid`        |
| Data / Storage      | `#ddd6fe` | `#6d28d9`  | `solid`        |
| Async / Events      | `#fef08a` | `#92400e`  | `solid`        |
| Security            | `#fed7aa` | `#c2410c`  | `solid`        |
| Neutral / Base      | `#e2e8f0` | `#334155`  | `solid`        |

### Branch level-2 nodes (leaves — lighter fill, same hue as parent)

Use `--fill-style hachure` or a lighter `--bg` from the same hue family to visually recede relative to level-1 nodes. Alternatively, use solid fill with `--opacity 70` on level-2 nodes.

Example leaf colors (matching parent hue):
| Parent bg   | Leaf `--bg` | Leaf `--stroke` |
|-------------|-------------|-----------------|
| `#bfdbfe`   | `#dbeafe`   | `#1e40af`       |
| `#86efac`   | `#bbf7d0`   | `#15803d`       |
| `#ddd6fe`   | `#ede9fe`   | `#6d28d9`       |
| `#fef08a`   | `#fef9c3`   | `#92400e`       |

### Connecting lines

| Property        | Value      | Notes                                         |
|-----------------|------------|-----------------------------------------------|
| `--stroke`      | `#94a3b8`  | Slate gray — hub-to-spoke color (color-palette.md) |
| `--sw`          | `1`        | Thin lines keep visual weight on nodes        |
| `--stroke-style`| `solid`    |                                               |
| Command         | `add line` | NOT `add arrow` — mind maps have no arrowheads |

### Font families

| Use              | `--ff` | Name     |
|------------------|--------|----------|
| Title            | `2`    | Helvetica (clean header) |
| Branch labels    | `1`    | Virgil (handwritten, casual feel) |
| Annotations      | `1`    | Virgil |

---

## Common pitfalls

1. **Using `add arrow` instead of `add line` for branch connections.** Mind maps have no arrowheads — they show association, not direction. Use `add line --points "0,0 dx,dy"` where dx/dy are the relative offsets from the line's starting point to its end. The `--points` values are relative to `--x,--y`.

2. **Dark root node with dark stroke — unreadable label.** If you use `--bg "#1e293b"` (the recommended dark navy for the root) but forget to set `--stroke "#e2e8f0"`, the label text will be invisible (dark text on dark background). This is the single most common error. Always pair dark `--bg` with light `--stroke`.

3. **Left-side branch labels overlapping node edges.** Text annotations placed beside left-side branches must be at `x < 150` to avoid colliding with the branch ellipses which start at x=210. If you need to annotate left branches, place text at x=20–140 with right alignment, or omit text annotations for left branches entirely.

4. **Lines drawn before nodes — disconnected appearance.** While draw order matters less for `add line` (which uses absolute coordinates), it is still best practice to draw all ellipses first so the line endpoints are visually grounded on top of the nodes.

5. **Leaves placed too close together vertically.** Use `V_LEAF_STEP=60` minimum between leaf centers to prevent label overflow from adjacent leaves colliding.

6. **Title overlap with top branch.** Title at y=15 with fs=20 has baseline ≈ y=37. The top branch is at y=180. Clearance = 143px, well above the 60px Rule 21 minimum. Do not move the top branch above y=97.

7. **All branches same color.** Use semantic colors from color-palette.md to distinguish topic areas. A monochrome mind map loses the visual grouping benefit.

---

## Worked example

**Scenario:** React Concepts mind map — root "React", 7 branches: Components, State, Props, Hooks, Context, Lifecycle, Rendering.

**Color assignments (by semantic area):**
- Components → Application/Service green: `#86efac` / `#15803d`
- State → Data/Storage purple: `#ddd6fe` / `#6d28d9`
- Props → Clients/Users blue: `#bfdbfe` / `#1e40af`
- Hooks → Async/Events amber: `#fef08a` / `#92400e`
- Context → Security orange: `#fed7aa` / `#c2410c`
- Lifecycle → Neutral: `#e2e8f0` / `#334155`
- Rendering → Gateway green: `#bbf7d0` / `#15803d`

**Branch positions (7 branches — skip Right-bottom, use all others):**
```
Components  → Right-center: x=830, y=390
State       → Right-top:    x=830, y=280
Props       → Right-bottom: x=830, y=500
Hooks       → Left-center:  x=210, y=390
Context     → Left-top:     x=210, y=280
Lifecycle   → Left-bottom:  x=210, y=500
Rendering   → Top-center:   x=520, y=180
```

**Line points (root center = 600,420; branch centers computed from top-left + w/2, h/2):**
```
Root → Components (right-center):  start=(600,420), end=(910,420) → dx=310, dy=0
Root → State (right-top):          start=(600,420), end=(910,310) → dx=310, dy=-110
Root → Props (right-bottom):       start=(600,420), end=(910,530) → dx=310, dy=110
Root → Hooks (left-center):        start=(600,420), end=(290,420) → dx=-310, dy=0
Root → Context (left-top):         start=(600,420), end=(290,310) → dx=-310, dy=-110
Root → Lifecycle (left-bottom):    start=(600,420), end=(290,530) → dx=-310, dy=110
Root → Rendering (top):            start=(600,420), end=(600,210) → dx=0, dy=-210
```

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"
CLI=$(which excalidraw-agent-cli)
P=/tmp/mindmap-worked-example.excalidraw

add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

rm -f "$P"
$CLI --json project new --name "mindmap-worked-example" --output "$P" > /dev/null

# ── Title (Rule 21: y=15, baseline≈37, first node at y=180 → 143px clearance ✓) ──
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "React Concepts" > /dev/null

# ── Root ellipse (dark navy + light stroke → readable label, Rule 22 ✓) ─────────
ROOT=$(add ellipse --x 510 --y 370 -w 180 -h 100 \
  --label "React" \
  --bg "#1e293b" --stroke "#e2e8f0" --fill-style solid --roughness 0 --sw 2)

# ── Branch level-1 ellipses ───────────────────────────────────────────────────────
# Right-center: Components (green)
BR_COMP=$(add ellipse --x 830 --y 390 -w 160 -h 60 \
  --label "Components" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# Right-top: State (purple)
BR_STATE=$(add ellipse --x 830 --y 280 -w 160 -h 60 \
  --label "State" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)

# Right-bottom: Props (blue)
BR_PROPS=$(add ellipse --x 830 --y 500 -w 160 -h 60 \
  --label "Props" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# Left-center: Hooks (amber — uses dark brown stroke for contrast, Rule 22)
BR_HOOKS=$(add ellipse --x 210 --y 390 -w 160 -h 60 \
  --label "Hooks" \
  --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 2)

# Left-top: Context (orange/security)
BR_CTX=$(add ellipse --x 210 --y 280 -w 160 -h 60 \
  --label "Context" \
  --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)

# Left-bottom: Lifecycle (neutral)
BR_LC=$(add ellipse --x 210 --y 500 -w 160 -h 60 \
  --label "Lifecycle" \
  --bg "#e2e8f0" --stroke "#334155" --fill-style solid --roughness 0 --sw 2)

# Top: Rendering (gateway green)
BR_REND=$(add ellipse --x 520 --y 180 -w 160 -h 60 \
  --label "Rendering" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# ── Connecting lines (root center = 600,420; no arrowheads) ──────────────────────
# Root → Components: dx=310, dy=0
add line --x 600 --y 420 --points "0,0 310,0" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# Root → State: dx=310, dy=-110
add line --x 600 --y 420 --points "0,0 310,-110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# Root → Props: dx=310, dy=110
add line --x 600 --y 420 --points "0,0 310,110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# Root → Hooks: dx=-310, dy=0
add line --x 600 --y 420 --points "0,0 -310,0" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# Root → Context: dx=-310, dy=-110
add line --x 600 --y 420 --points "0,0 -310,-110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# Root → Lifecycle: dx=-310, dy=110
add line --x 600 --y 420 --points "0,0 -310,110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# Root → Rendering: dx=0, dy=-210
add line --x 600 --y 420 --points "0,0 0,-210" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# ── Leaf nodes for Components branch (right side) ─────────────────────────────────
# Branch center: (910, 420). Leaves extend further right.
L_FC=$(add ellipse --x 1010 --y 395 -w 130 -h 45 \
  --label "Functional" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)
L_CL=$(add ellipse --x 1010 --y 450 -w 130 -h 45 \
  --label "Class" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)

# Lines: Components → leaves
add line --x 990 --y 420 --points "0,0 20,-8" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null
add line --x 990 --y 420 --points "0,0 20,48" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# ── Leaf nodes for Hooks branch (left side) ───────────────────────────────────────
# Branch center: (290, 420). Leaves extend further left at x<150.
L_UE=$(add ellipse --x 60 --y 395 -w 130 -h 45 \
  --label "useEffect" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)
L_US=$(add ellipse --x 60 --y 450 -w 130 -h 45 \
  --label "useState" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)

# Lines: Hooks → leaves (start at branch left edge x=210, center y=420)
add line --x 210 --y 420 --points "0,0 -120,-8" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null
add line --x 210 --y 420 --points "0,0 -120,48" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

$CLI -p "$P" export png --output /tmp/mindmap-worked-example.png --overwrite
echo "Exported: /tmp/mindmap-worked-example.png"
```
