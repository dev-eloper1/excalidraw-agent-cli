#!/usr/bin/env bash
# CI/CD Pipeline — Diamond feedback cycle
# 4 stages in diamond: Plan (top), Build (right), Deploy (bottom), Observe (left)
# Clockwise flow with dashed red feedback arrow from Observe to Plan
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/Users/bhushan/Documents/excalidraw-agent-cli/examples/cicd/cicd-work.excalidraw
OUT=/Users/bhushan/Documents/excalidraw-agent-cli/examples/cicd

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

# COLOR PLAN
# Plan (top)     → bg "#bfdbfe"  stroke "#1e40af"   (blue)
# Build (right)  → bg "#86efac"  stroke "#15803d"   (green)
# Deploy (bottom)→ bg "#fef08a"  stroke "#92400e"   (amber, dark-brown stroke for contrast)
# Observe (left) → bg "#fecdd3"  stroke "#9f1239"   (pink, dark-rose stroke for contrast)
# Feedback arrow → stroke "#dc2626" dashed red

# COORDINATE PLAN (diamond layout, canvas ~900x900)
# Canvas center ~(550, 500)
# Plan    (top):    x=470, y=200, w=160, h=72  → center_x=550, center_y=236
# Build   (right):  x=750, y=464, w=160, h=72  → center_x=830, center_y=500
# Deploy  (bottom): x=470, y=728, w=160, h=72  → center_x=550, center_y=764
# Observe (left):   x=190, y=464, w=160, h=72  → center_x=270, center_y=500
#
# ARROW ROUTING (explicit coords, edge-to-edge):
# Plan→Build:    from Plan right edge (630,236)  to Build top edge (830,464)
# Build→Deploy:  from Build bottom edge (830,536) to Deploy right edge (630,764)
# Deploy→Observe:from Deploy left edge (470,764)  to Observe bottom edge (270,536)
# Observe→Plan:  from Observe top edge (270,464) to Plan left edge (470,236)
# Feedback:      from Observe top (270,464) to Plan left (470,236)  — dashed red, offset

rm -f "$P"
$CLI --json project new --name "cicd-pipeline" --output "$P" > /dev/null

# -- Title --
add text --x 440 --y 155 --fs 20 --ff 2 --color "#1e293b" -t "CI/CD Pipeline" > /dev/null

# -- Stage nodes --
PLAN=$(    add rectangle --x 470 --y 200 -w 160 -h 72 \
  --label "Plan" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid \
  --roughness 1 --sw 2 --roundness)

BUILD=$(   add rectangle --x 750 --y 464 -w 160 -h 72 \
  --label "Build" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid \
  --roughness 1 --sw 2 --roundness)

DEPLOY=$(  add rectangle --x 470 --y 728 -w 160 -h 72 \
  --label "Deploy" \
  --bg "#fef08a" --stroke "#92400e" --fill-style solid \
  --roughness 1 --sw 2 --roundness)

OBSERVE=$( add rectangle --x 190 --y 464 -w 160 -h 72 \
  --label "Observe" \
  --bg "#fecdd3" --stroke "#9f1239" --fill-style solid \
  --roughness 1 --sw 2 --roundness)

# -- Clockwise primary flow arrows (solid black, explicit edge coordinates) --
# Plan → Build: from Plan right-center (630, 236) to Build top-center (830, 464)
add arrow --x 630 --y 236 --ex 830 --ey 464 \
  --stroke "#1e1e1e" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Build → Deploy: from Build bottom-center (830, 536) to Deploy right-center (630, 764)
add arrow --x 830 --y 536 --ex 630 --ey 764 \
  --stroke "#1e1e1e" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Deploy → Observe: from Deploy left-center (470, 764) to Observe bottom-center (270, 536)
add arrow --x 470 --y 764 --ex 270 --ey 536 \
  --stroke "#1e1e1e" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# Observe → Plan (main flow): from Observe top-center (270, 464) to Plan left-center (470, 236)
add arrow --x 270 --y 464 --ex 470 --ey 236 \
  --stroke "#1e1e1e" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# -- Feedback arrow: Observe → Plan (dashed red, offset to left of main flow arrow) --
# Offset the feedback arrow 35px to the left so it doesn't overlap the main flow arrow
# Main flow: (270,464) to (470,236) — midpoint ~(370, 350)
# Feedback: route via offset start (235, 445) → end (455, 218)
add arrow --x 235 --y 445 --ex 455 --ey 218 \
  --stroke "#dc2626" --sw 2 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# -- Feedback label as separate text element (not on arrow line) --
# Midpoint of feedback arrow: ~(345, 332)
# Place label to the LEFT of the midpoint so it clears both arrows
add text --x 260 --y 318 --fs 13 --ff 2 --color "#dc2626" -t "feedback" > /dev/null

# -- Export all three formats --
$CLI --project "$P" export png  --output "$OUT/cicd.png"  --overwrite
$CLI --project "$P" export svg  --output "$OUT/cicd.svg"  --overwrite
$CLI --project "$P" export json --output "$OUT/cicd.excalidraw" --overwrite

echo "Done. Exports:"
echo "  $OUT/cicd.png"
echo "  $OUT/cicd.svg"
echo "  $OUT/cicd.excalidraw"
