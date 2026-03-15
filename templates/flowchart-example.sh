#!/usr/bin/env bash
# flowchart-example.sh — User Signup Flowchart
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/flowchart-template-preview.png
#
# Layout constants:
#   ROW_H=100   (vertical distance between row top edges: node_h=60 + gap=40)
#   COL_W=200   (horizontal distance between column centers)
#   CENTER_X=600 (canvas midpoint; single-column nodes at x=510 for w=180)
#
# Node plan (top-to-bottom):
#   START        y=100   x=510  w=180 h=60  rounded rect  Start/Trigger
#   VALIDATE     y=200   x=510  w=180 h=60  rect          Application Services
#   DECIDE       y=310   x=500  w=200 h=80  diamond       Decision Diamond
#     YES branch (exists) → x=220 y=430    rect           Error/Reject
#     NO branch  (new)    → x=730 y=430    rect           Application Services
#   CREATE       y=430   x=730  w=200 h=60  rect          Application Services
#   SEND_EMAIL   y=530   x=730  w=200 h=60  rect          Application Services
#   END          y=640   x=510  w=180 h=60  rounded rect  End/Success
#
# CRITICAL: Title at y=15 fs=20 → baseline≈37. START at y=100 → 63px clearance (Rule 21 ✓)
# CRITICAL: Diamond min w=200 for "User Exists?" (12 chars; Rule 17, pitfall 1)
# CRITICAL: element connect used for all connections (NOT add arrow) — flowchart rule

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/flowchart-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/flowchart-template-preview.png"

# ── Shell variable layout constants ──────────────────────────────────────────
ROW_H=100
COL_W=200
CENTER_X=600

add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

conn() {
  local from="$1" to="$2" label="$3" color="$4" style="$5"
  local args=("--from" "$from" "--to" "$to")
  [[ -n "$label" ]] && args+=("-l" "$label")
  [[ -n "$color" ]] && args+=("--stroke" "$color")
  [[ -n "$style" ]] && args+=("--stroke-style" "$style")
  $CLI -p "$P" --json element connect "${args[@]}" > /dev/null
}

# ── Create project ────────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "flowchart-example" --output "$P" > /dev/null

# ── Title ─────────────────────────────────────────────────────────────────────
# y=15, fs=20 → baseline≈37. First node at y=100 → 63px clearance (Rule 21 ✓)
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "User Signup Flow" > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# NODES — top to bottom, then branches
# ════════════════════════════════════════════════════════════════════════════

# Start node (rounded rectangle — Start/Trigger: #dbeafe / #1e40af)
# x = CENTER_X - w/2 = 600 - 90 = 510
START=$(add rectangle --x 510 --y 100 -w 180 -h 60 --roundness \
  --label "Start" \
  --bg "#dbeafe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# Step 1: Validate Email (Application Services: #86efac / #15803d)
VALIDATE=$(add rectangle --x 510 --y 200 -w 180 -h 60 \
  --label "Validate Email" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# Decision diamond: User Exists? (Decision Diamond: #fef3c7 / #b45309)
# w=200 for "User Exists?" (12 chars → min_w = max(140, 12*9.6+32) = 147 → 200 for safety)
# x = CENTER_X - w/2 = 600 - 100 = 500
# y=310 gives 30px gap below VALIDATE bottom edge (200+60=260, 310-260=50 ✓)
DECIDE=$(add diamond --x 500 --y 310 -w 200 -h 80 \
  --label "User Exists?" \
  --bg "#fef3c7" --stroke "#b45309" --fill-style solid --roughness 0 --sw 2)

# YES branch: Return 409 (Error/Reject: #fecaca / #b91c1c)
# Left of diamond: x=220 (Rule 17: diamond right edge=700, left branch x≥220)
# Diamond left edge=500; left branch at x=220, right edge=380; gap=500-380=120 ✓
EXISTS_ERR=$(add rectangle --x 220 --y 430 -w 160 -h 60 \
  --label "Return 409" \
  --bg "#fecaca" --stroke "#b91c1c" --fill-style solid --roughness 0 --sw 2)

# NO branch: Create Account (Application Services: #86efac / #15803d)
# Right of diamond: x=730 (diamond right edge=700; gap=730-700=30 ✓ min=60? push to 770)
# Rule 17: diamond right edge=500+200=700; right branch x≥700+60=760 → use x=760
CREATE=$(add rectangle --x 760 --y 430 -w 200 -h 60 \
  --label "Create Account" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# Step after create: Send Welcome Email
SEND_EMAIL=$(add rectangle --x 760 --y 530 -w 200 -h 60 \
  --label "Send Welcome Email" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# End node (rounded rectangle — End/Success: #a7f3d0 / #047857)
END=$(add rectangle --x 510 --y 640 -w 180 -h 60 --roundness \
  --label "End" \
  --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2)

# ════════════════════════════════════════════════════════════════════════════
# CONNECTIONS — use element connect (auto-routing handles all paths)
# Arrow style vocabulary (Rule 15):
#   Primary flow:   #1e1e1e solid sw=2
#   Success branch: #15803d solid sw=2
#   Error branch:   #b91c1c dashed sw=2
# ════════════════════════════════════════════════════════════════════════════

conn "$START"      "$VALIDATE"   ""    "#1e1e1e" "solid"
conn "$VALIDATE"   "$DECIDE"     ""    "#1e1e1e" "solid"
conn "$DECIDE"     "$EXISTS_ERR" "yes" "#b91c1c" "dashed"   # user already exists → 409
conn "$DECIDE"     "$CREATE"     "no"  "#15803d" "solid"    # new user → proceed
conn "$EXISTS_ERR" "$END"        ""    "#b91c1c" "dashed"
conn "$CREATE"     "$SEND_EMAIL" ""    "#1e1e1e" "solid"
conn "$SEND_EMAIL" "$END"        ""    "#1e1e1e" "solid"

# ── Export PNG ────────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$OUT")"
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
