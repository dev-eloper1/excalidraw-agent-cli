#!/usr/bin/env bash
# mindmap-example.sh — React Concepts Mind Map
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/mindmap-template-preview.png
#
# Layout: radial, root ellipse centered at (600, 420)
# Branches at 8 compass positions (7 used for 7 React concepts)
# Lines from root to branches — add line (NOT add arrow, no arrowheads)
# Leaf nodes on Components (right) and Hooks (left) branches.
#
# CRITICAL: Root uses --bg "#1e293b" + --stroke "#e2e8f0" (Rule 22 — light stroke
#           controls label text color; dark stroke on dark bg = unreadable label)
# Rule 21: Title at y=15 (baseline≈37), first node at y=180 → 143px clearance ✓

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/mindmap-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/mindmap-template-preview.png"

# ── Named spacing variables ────────────────────────────────────────────────────
ROOT_X=510;  ROOT_Y=370;  ROOT_W=180;  ROOT_H=100
BRANCH_W=160; BRANCH_H=60
LEAF_W=130;  LEAF_H=45

# Helper: add element and capture ID
add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

# ── Create project ─────────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "mindmap-example" --output "$P" > /dev/null

# ── Title ──────────────────────────────────────────────────────────────────────
# y=15, fs=20 → baseline ≈ y=37. First node at y=180 → 143px clearance (Rule 21 ✓)
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "React Concepts" > /dev/null

# ── Root ellipse ───────────────────────────────────────────────────────────────
# Dark navy fill + near-white stroke = readable label (Rule 22 ✓)
# root center = (600, 420)
ROOT=$(add ellipse \
  --x "$ROOT_X" --y "$ROOT_Y" -w "$ROOT_W" -h "$ROOT_H" \
  --label "React" \
  --bg "#1e293b" --stroke "#e2e8f0" --fill-style solid --roughness 0 --sw 2)

# ── Branch level-1 ellipses ───────────────────────────────────────────────────
# Right-center (x=830, y=390): Components — App/Service green
BR_COMP=$(add ellipse \
  --x 830 --y 390 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Components" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# Right-top (x=830, y=280): State — Data/Storage purple
BR_STATE=$(add ellipse \
  --x 830 --y 280 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "State" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)

# Right-bottom (x=830, y=500): Props — Clients/Users blue
BR_PROPS=$(add ellipse \
  --x 830 --y 500 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Props" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# Left-center (x=210, y=390): Hooks — Async/Events amber (dark brown stroke, Rule 22)
BR_HOOKS=$(add ellipse \
  --x 210 --y 390 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Hooks" \
  --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 2)

# Left-top (x=210, y=280): Context — Security orange
BR_CTX=$(add ellipse \
  --x 210 --y 280 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Context" \
  --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)

# Left-bottom (x=210, y=500): Lifecycle — Neutral
BR_LC=$(add ellipse \
  --x 210 --y 500 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Lifecycle" \
  --bg "#e2e8f0" --stroke "#334155" --fill-style solid --roughness 0 --sw 2)

# Top-center (x=520, y=180): Rendering — Gateway green
# y=180 ≥ 97 (Rule 21 first-element minimum ✓)
BR_REND=$(add ellipse \
  --x 520 --y 180 -w "$BRANCH_W" -h "$BRANCH_H" \
  --label "Rendering" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# ── Lines: root center (600,420) to each branch center ────────────────────────
# add line uses --points as relative offsets from --x,--y
# Branch center = branch_x + branch_w/2, branch_y + branch_h/2

# → Components (center 910, 420): dx=+310, dy=0
add line --x 600 --y 420 --points "0,0 310,0" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# → State (center 910, 310): dx=+310, dy=-110
add line --x 600 --y 420 --points "0,0 310,-110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# → Props (center 910, 530): dx=+310, dy=+110
add line --x 600 --y 420 --points "0,0 310,110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# → Hooks (center 290, 420): dx=-310, dy=0
add line --x 600 --y 420 --points "0,0 -310,0" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# → Context (center 290, 310): dx=-310, dy=-110
add line --x 600 --y 420 --points "0,0 -310,-110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# → Lifecycle (center 290, 530): dx=-310, dy=+110
add line --x 600 --y 420 --points "0,0 -310,110" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# → Rendering (center 600, 210): dx=0, dy=-210
add line --x 600 --y 420 --points "0,0 0,-210" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# ── Leaf nodes: Components branch (right side) ────────────────────────────────
# Branch center: (910, 420). Leaves at x=1010 (right of branch right edge x=990)
L_FC=$(add ellipse \
  --x 1010 --y 395 -w "$LEAF_W" -h "$LEAF_H" \
  --label "Functional" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)
L_CL=$(add ellipse \
  --x 1010 --y 450 -w "$LEAF_W" -h "$LEAF_H" \
  --label "Class" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1)

# Lines: Components right edge (990,420) → leaf centers
add line --x 990 --y 420 --points "0,0 20,-8" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null
add line --x 990 --y 420 --points "0,0 20,48" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# ── Leaf nodes: Hooks branch (left side) ──────────────────────────────────────
# Branch left edge x=210; leaves at x=60–190 (x<150 avoids branch overlap per recipe)
L_UE=$(add ellipse \
  --x 60 --y 395 -w "$LEAF_W" -h "$LEAF_H" \
  --label "useEffect" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)
L_US=$(add ellipse \
  --x 60 --y 450 -w "$LEAF_W" -h "$LEAF_H" \
  --label "useState" \
  --bg "#fef9c3" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1)

# Lines: Hooks left edge (210,420) → leaf centers
add line --x 210 --y 420 --points "0,0 -85,-8" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null
add line --x 210 --y 420 --points "0,0 -85,48" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid > /dev/null

# ── Export PNG ─────────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$OUT")"
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
