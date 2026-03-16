#!/usr/bin/env bash
# mindmap-example.sh — React Concepts Mind Map (tree layout)
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/mindmap-template-preview.png
#
# Layout: left-to-right hierarchical tree
#   Root  ──→  Level-1 branches (vertical stack)  ──→  Level-2 leaves
#
#   ROOT (x=80, w=140, h=80, center_y=340)
#   BRANCHES (x=300, w=160, h=50, 80px center-to-center spacing):
#     Components y=75  (center=100) — right: Functional/Class leaves
#     State      y=155 (center=180)
#     Props      y=235 (center=260)
#     Hooks      y=315 (center=340) — right: useEffect/useState leaves
#     Context    y=395 (center=420)
#     Lifecycle  y=475 (center=500)
#     Rendering  y=555 (center=580)
#   LEAVES (x=510, w=130, h=40):
#     Functional y=55  (center=75,  under Components ±25)
#     Class      y=105 (center=125, under Components ±25)
#     useEffect  y=295 (center=315, under Hooks ±25)
#     useState   y=345 (center=365, under Hooks ±25)
#
# Arrow pattern (Rule 23/24): explicit add arrow, start-arrowhead none, end-arrowhead arrow
#   Root exit points staggered within root height (y=306..374, step≈11)
#   Leaf arrows from branch right edge to leaf left edge
#
# Rule 21: Title at y=15 (baseline≈37), first branch at y=75 → 38px clearance ✓
# Rule 22: Root dark bg + light stroke; branches light bg + dark stroke ✓

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/mindmap-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/mindmap-template-preview.png"

# ── Named spacing variables ────────────────────────────────────────────────────
ROOT_X=80;   ROOT_Y=300;  ROOT_W=140;  ROOT_H=80    # center_y=340
BRANCH_X=300; BRANCH_W=160; BRANCH_H=50             # branch right edge=460
LEAF_X=510;  LEAF_W=130;  LEAF_H=40                 # leaf left edge=510

# Helper: add element and capture ID
add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

# ── Create project ─────────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "mindmap-example" --output "$P" > /dev/null

# ── Title ──────────────────────────────────────────────────────────────────────
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "React Concepts" > /dev/null

# ── Root ellipse (dark navy, center_y=340) ─────────────────────────────────────
ROOT=$(add ellipse \
  --x "$ROOT_X" --y "$ROOT_Y" -w "$ROOT_W" -h "$ROOT_H" \
  --label "React" \
  --bg "#1e293b" --stroke "#e2e8f0" --fill-style solid --roughness 0 --sw 2)
# Root right edge: x=80+140=220, center_y=340

# ── Level-1 branch ellipses (stacked at 80px intervals) ───────────────────────
# Components (y=75, center=100) — App/Service green
BR_COMP=$(add ellipse \
  --x "$BRANCH_X" --y 75 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Components" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# State (y=155, center=180) — Data/Storage purple
BR_STATE=$(add ellipse \
  --x "$BRANCH_X" --y 155 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "State" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)

# Props (y=235, center=260) — Clients/Users blue
BR_PROPS=$(add ellipse \
  --x "$BRANCH_X" --y 235 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Props" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# Hooks (y=315, center=340) — Async/Events amber (dark stroke for readability Rule 22)
BR_HOOKS=$(add ellipse \
  --x "$BRANCH_X" --y 315 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Hooks" \
  --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 2)

# Context (y=395, center=420) — Security orange
BR_CTX=$(add ellipse \
  --x "$BRANCH_X" --y 395 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Context" \
  --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)

# Lifecycle (y=475, center=500) — Neutral
BR_LC=$(add ellipse \
  --x "$BRANCH_X" --y 475 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Lifecycle" \
  --bg "#e2e8f0" --stroke "#334155" --fill-style solid --roughness 0 --sw 2)

# Rendering (y=555, center=580) — Gateway green
BR_REND=$(add ellipse \
  --x "$BRANCH_X" --y 555 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Rendering" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# ── Root → Branch arrows (Rule 24) ─────────────────────────────────────────────
# Start at root right edge (x=220) at staggered Y within root height (300-380).
# End at branch left edge (x=300) at branch center_y.
# Stagger 7 exits: y = 306, 317, 328, 340, 352, 363, 374

# Root → Components (center=100)
add arrow --x 220 --y 306 --ex 300 --ey 100 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Root → State (center=180)
add arrow --x 220 --y 317 --ex 300 --ey 180 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Root → Props (center=260)
add arrow --x 220 --y 328 --ex 300 --ey 260 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Root → Hooks (center=340) — horizontal, root center to hooks center
add arrow --x 220 --y 340 --ex 300 --ey 340 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Root → Context (center=420)
add arrow --x 220 --y 352 --ex 300 --ey 420 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Root → Lifecycle (center=500)
add arrow --x 220 --y 363 --ex 300 --ey 500 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Root → Rendering (center=580)
add arrow --x 220 --y 374 --ex 300 --ey 580 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Level-2 leaf ellipses under Components ────────────────────────────────────
# Branch right edge x=460; leaf left edge x=510. Leaves ±25 from branch center (100).
L_FC=$(add ellipse \
  --x "$LEAF_X" --y 55 -w "$LEAF_W" -h "$LEAF_H" \
  --label "Functional" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)

L_CL=$(add ellipse \
  --x "$LEAF_X" --y 105 -w "$LEAF_W" -h "$LEAF_H" \
  --label "Class" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)

# Components right edge (460, 100) → leaf left edges at (510, center_y)
# Functional center_y = 55+20=75; Class center_y = 105+20=125
add arrow --x 460 --y 100 --ex 510 --ey 75 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add arrow --x 460 --y 100 --ex 510 --ey 125 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Level-2 leaf ellipses under Hooks ─────────────────────────────────────────
# Leaves ±25 from Hooks center (340): centers at 315 and 365
L_UE=$(add ellipse \
  --x "$LEAF_X" --y 295 -w "$LEAF_W" -h "$LEAF_H" \
  --label "useEffect" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)

L_US=$(add ellipse \
  --x "$LEAF_X" --y 345 -w "$LEAF_W" -h "$LEAF_H" \
  --label "useState" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)

# Hooks right edge (460, 340) → leaf left edges at (510, center_y)
# useEffect center_y = 295+20=315; useState center_y = 345+20=365
add arrow --x 460 --y 340 --ex 510 --ey 315 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add arrow --x 460 --y 340 --ex 510 --ey 365 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Export PNG ─────────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$OUT")"
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
