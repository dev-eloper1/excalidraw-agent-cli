# Mind Map Diagram Recipe

## When to use

Use a mind map when you need to communicate **how a central concept branches into related topics**, and those topics may further branch into sub-topics. The key signal is a single root idea with associative relationships radiating outward.

Choose this pattern when:
- You have one dominant root concept and 5–10 first-level branches
- Relationships are associative, not sequential (no strict order between branches)
- The narrative is "everything that relates to X" rather than "step 1 → step 2"
- Brainstorming, knowledge mapping, or concept overviews for technical topics (frameworks, languages, systems)

Do NOT use for: ordered processes (use flowchart), time-phased plans (use Gantt), layered system architectures (use architecture diagram), or message sequences (use sequence diagram).

## Layout choice: Tree (default) vs Radial

**Use LEFT-TO-RIGHT TREE layout (default):** Root on the left, branches stacked vertically on the right, leaves further right. This gives clear visual hierarchy — the eye reads left-to-right following the depth level. Preferred for most mindmaps because it's easier to read and shows branch depth clearly.

**Use RADIAL layout only when:** The topic has equal branches in all compass directions AND there are few enough branches (≤8) that the center doesn't get cluttered. Radial works for pure brainstorm dumps where no branch is more important than others.

**Why tree beats radial:** A radial mindmap with 7 branches all radiating from a center looks like a spider web with no visual hierarchy. Readers struggle to distinguish level-1 branches from each other. Tree layout makes hierarchy obvious at a glance.

---

## Layout template — Tree (left-to-right, default)

```
Canvas: 700 × 650px (adjust height based on branch count)

Title: x=20, y=15, --fs 20 --ff 2  (baseline ≈ y=37, Rule 21)
First branch at y=75 minimum.

Named variables:
  ROOT_X=80   ROOT_Y=(center_y - ROOT_H/2)  ROOT_W=140  ROOT_H=80
  BRANCH_X=300  BRANCH_W=160  BRANCH_H=50    (right edge x=460)
  LEAF_X=510    LEAF_W=130    LEAF_H=40      (left edge x=510)

Branch Y-center spacing: 80px between branches (center-to-center)
For N branches: center_y_first=(80+40)/2=60  (adjust for canvas top clearance)
  Branch centers at: 100, 180, 260, 340, 420, 500, 580 (for 7 branches)
  Root center_y = (first_center + last_center) / 2 = (100+580)/2 = 340

Root (right edge = ROOT_X + ROOT_W = 220):
  ROOT_Y = center_y - ROOT_H/2 = 340 - 40 = 300

Branch positions (x=BRANCH_X=300, anchored by top-left):
  Branch 1: y=75   center_y=100
  Branch 2: y=155  center_y=180
  Branch 3: y=235  center_y=260
  Branch 4: y=315  center_y=340  ← aligned with root
  ...and so on at +80 per branch

Leaf positions (x=LEAF_X=510, ±25 from parent branch center):
  Parent branch center=100 → leaves at y=55 (center=75) and y=105 (center=125)
  Parent branch center=340 → leaves at y=295 (center=315) and y=345 (center=365)
```

**Draw order:**
1. Title text
2. Root ellipse (dark navy, left side)
3. Branch ellipses (level-1, stacked vertically, color by topic)
4. Leaf ellipses (level-2, lighter fill, ±25 from branch center)
5. Arrows: root → each branch (Rule 24: `add arrow --start-arrowhead none --end-arrowhead arrow`)
6. Arrows: branch → each leaf (same pattern)

**Root → Branch arrow pattern (Rule 24):**
Stagger 7 exit points within root height (ROOT_Y to ROOT_Y+ROOT_H), step = ROOT_H/6:
```
Root right edge x=220, stagger Y: 306, 317, 328, 340, 352, 363, 374
add arrow --x 220 --y 306 --ex 300 --ey 100   # → Branch 1
add arrow --x 220 --y 317 --ex 300 --ey 180   # → Branch 2
add arrow --x 220 --y 340 --ex 300 --ey 340   # → Branch 4 (horizontal)
```

**Branch → Leaf arrow pattern:**
```
Branch right edge x=460, branch center_y=100
add arrow --x 460 --y 100 --ex 510 --ey 75    # → Leaf above
add arrow --x 460 --y 100 --ex 510 --ey 125   # → Leaf below
```
6. Arrows: branch → each leaf (same pattern)

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

### Connecting arrows

| Property        | Value      | Notes                                         |
|-----------------|------------|-----------------------------------------------|
| `--stroke`      | `#94a3b8`  | Slate gray — hub-to-spoke color (color-palette.md) |
| `--sw`          | `1`        | Thin lines keep visual weight on nodes        |
| `--stroke-style`| `solid`    |                                               |
| Command         | `add arrow --start-arrowhead none --end-arrowhead arrow` | Shows direction from hub to branch; NOT `add line`, NOT `element connect` |
| Endpoint        | BRANCH NEAREST EDGE, not center | Prevents arrow from penetrating the branch node (Rule 24) |

### Font families

| Use              | `--ff` | Name     |
|------------------|--------|----------|
| Title            | `2`    | Helvetica (clean header) |
| Branch labels    | `1`    | Virgil (handwritten, casual feel) |
| Annotations      | `1`    | Virgil |

---

## Common pitfalls

1. **Using `element connect` for branch connections.** This produces auto-routed lines that pass through node centers rather than terminating at boundaries, and overlap when multiple spokes share a root. Always use `add arrow --x ROOT_CX --y ROOT_CY --ex BRANCH_EDGE_X --ey BRANCH_EDGE_Y --start-arrowhead none --end-arrowhead arrow` with the endpoint at the branch's nearest edge (Rule 23, Rule 24).

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

**Arrow endpoints (root center = 600,420; branch NEAREST EDGE per Rule 24):**
```
Root → Components (right: branch left edge):  ex=830, ey=420   (branch_x=830, cy=390+30=420)
Root → State (right: branch left edge):       ex=830, ey=310   (branch_x=830, cy=280+30=310)
Root → Props (right: branch left edge):       ex=830, ey=530   (branch_x=830, cy=500+30=530)
Root → Hooks (left: branch right edge):       ex=370, ey=420   (branch_x+w=370, cy=390+30=420)
Root → Context (left: branch right edge):     ex=370, ey=310   (branch_x+w=370, cy=280+30=310)
Root → Lifecycle (left: branch right edge):   ex=370, ey=530   (branch_x+w=370, cy=500+30=530)
Root → Rendering (top: branch bottom edge):   ex=600, ey=240   (cx=520+80=600, branch_y+h=180+60=240)
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

# ── Spoke arrows (root center=600,420 → branch nearest edge; Rule 23, Rule 24) ───
# Right branches → endpoint = (branch_x, branch_center_y)
add arrow --x 600 --y 420 --ex 830 --ey 420 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null   # → Components

add arrow --x 600 --y 420 --ex 830 --ey 310 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null   # → State

add arrow --x 600 --y 420 --ex 830 --ey 530 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null   # → Props

# Left branches → endpoint = (branch_x + branch_w, branch_center_y)
add arrow --x 600 --y 420 --ex 370 --ey 420 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null   # → Hooks

add arrow --x 600 --y 420 --ex 370 --ey 310 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null   # → Context

add arrow --x 600 --y 420 --ex 370 --ey 530 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null   # → Lifecycle

# Top branch → endpoint = (branch_center_x, branch_y + branch_h)
add arrow --x 600 --y 420 --ex 600 --ey 240 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null   # → Rendering

# ── Leaf nodes for Components branch (right side) ─────────────────────────────────
# Branch right edge: x=990, center y=420. Leaves at x=1010 (20px gap).
L_FC=$(add ellipse --x 1010 --y 395 -w 130 -h 45 \
  --label "Functional" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)
L_CL=$(add ellipse --x 1010 --y 450 -w 130 -h 45 \
  --label "Class" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)

# Arrows: branch right edge (990,420) → leaf left edge (1010, leaf_center_y)
add arrow --x 990 --y 420 --ex 1010 --ey 417 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add arrow --x 990 --y 420 --ex 1010 --ey 472 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Leaf nodes for Hooks branch (left side) ───────────────────────────────────────
# Branch left edge: x=210, center y=420. Leaves at x=60 (right edge=190).
L_UE=$(add ellipse --x 60 --y 395 -w 130 -h 45 \
  --label "useEffect" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)
L_US=$(add ellipse --x 60 --y 450 -w 130 -h 45 \
  --label "useState" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)

# Arrows: branch left edge (210,420) → leaf right edge (190, leaf_center_y)
add arrow --x 210 --y 420 --ex 190 --ey 417 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add arrow --x 210 --y 420 --ex 190 --ey 472 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

$CLI -p "$P" export png --output /tmp/mindmap-worked-example.png --overwrite
echo "Exported: /tmp/mindmap-worked-example.png"
```
