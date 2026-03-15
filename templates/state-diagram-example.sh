#!/usr/bin/env bash
# state-diagram-example.sh — Order Lifecycle State Diagram
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/state-diagram-template-preview.png
#
# States (happy path, row 1, y=250):
#   start → placed → payment_pending → paid → fulfillment → shipped → delivered → end
#
# States (cancel/refund, row 2, y=390):
#   cancelled  (reachable from: placed, paid)
#   refunded   (reachable from: delivered)
#
# Layout:
#   Row 1: y=250, state h=60, w=160, 220px center-to-center spacing
#   Row 2: y=390 (140px below row 1 top — enough vertical gap)
#   Start x=220 (small ellipse), first state x=290
#
# Color reference (from color-palette.md):
#   Start:         bg=#1e40af stroke=#1e40af (filled blue bullet)
#   Happy states:  bg=#86efac stroke=#15803d (Application Services green)
#   End:           bg=#047857 stroke=#047857 (filled green terminal)
#   Delivered:     bg=#a7f3d0 stroke=#047857 (End/Success)
#   Cancelled:     bg=#fecaca stroke=#b91c1c (Error/Reject)
#   Refunded:      bg=#fed7aa stroke=#c2410c (Security/External orange)
#   Normal arrows: #1e1e1e solid sw=2
#   Cancel arrows: #dc2626 dashed sw=2
#   Refund arrow:  #c2410c dashed sw=2

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/state-diagram-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/state-diagram-template-preview.png"

# ── Helpers ──────────────────────────────────────────────────────────────────
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
$CLI --json project new --name "state-diagram-example" --output "$P" > /dev/null

# ── Title ─────────────────────────────────────────────────────────────────────
# Rule 21: title y=180, fs=20 → baseline ≈ y=200. First element (start ellipse)
# at y=250 → 50px clearance (sufficient given canvas starts high).
add text --x 220 --y 180 --fs 20 --ff 2 --color "#1e293b" \
  -t "Order Lifecycle — State Diagram" > /dev/null

# Legend
add text --x 220 --y 210 --fs 13 --ff 2 --color "#374151" \
  -t "Happy path: green  |  Cancel: red dashed  |  Refund: orange dashed" > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 1: Start state (small filled blue ellipse — bullet)
# ════════════════════════════════════════════════════════════════════════════
# x=220, y=270 (centers at 240, 290 — vertically centered on row1 states at y=250..310)
START=$(add ellipse --x 220 --y 270 -w 40 -h 40 \
  --bg "#1e40af" --stroke "#e2e8f0" --fill-style solid --roughness 0 --sw 2)

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: Happy-path states (row 1, y=250, h=60, w=160, --roundness)
# Spacing: 220px center-to-center → gap = 220-160 = 60px ✓
# Col positions:
#   placed:          x=290
#   payment_pending: x=510   (290+220)
#   paid:            x=730   (510+220)
#   fulfillment:     x=950   (730+220)
#   shipped:         x=1170  (950+220)
#   delivered:       x=1390  (1170+220)
# "payment_pending" = 15 chars → min_w = max(120, 15*9.6+32) = max(120,176) = 176 → use 160
#   (acceptable; Excalidraw will render the label inside at smaller font if needed,
#    or we can widen to 180 — keeping 160 for uniform spacing)
# ════════════════════════════════════════════════════════════════════════════
PLACED=$(add rectangle --x 290 --y 250 -w 160 -h 60 --roundness \
  --label "placed" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

PAYMENT=$(add rectangle --x 510 --y 250 -w 160 -h 60 --roundness \
  --label "payment_pending" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

PAID=$(add rectangle --x 730 --y 250 -w 160 -h 60 --roundness \
  --label "paid" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

FULFILLMENT=$(add rectangle --x 950 --y 250 -w 160 -h 60 --roundness \
  --label "fulfillment" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

SHIPPED=$(add rectangle --x 1170 --y 250 -w 160 -h 60 --roundness \
  --label "shipped" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

DELIVERED=$(add rectangle --x 1390 --y 250 -w 160 -h 60 --roundness \
  --label "delivered" \
  --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2)

# ════════════════════════════════════════════════════════════════════════════
# STEP 3: End state (small filled green ellipse — terminal bullet)
# ════════════════════════════════════════════════════════════════════════════
END=$(add ellipse --x 1610 --y 265 -w 50 -h 50 \
  --bg "#047857" --stroke "#e2e8f0" --fill-style solid --roughness 0 --sw 2)

# ════════════════════════════════════════════════════════════════════════════
# STEP 4: Cancel and refund states (row 2, y=390)
# cancelled at x=290 (below placed) and x=730 (below paid)
# refunded at x=1390 (below delivered)
# Row gap: 390-250 = 140px ✓ (≥ 30px Rule 2, states are 60px tall so gap = 140-60 = 80px)
# ════════════════════════════════════════════════════════════════════════════
CANCELLED_FROM_PLACED=$(add rectangle --x 290 --y 390 -w 160 -h 60 --roundness \
  --label "cancelled" \
  --bg "#fecaca" --stroke "#b91c1c" --fill-style solid --roughness 0 --sw 2)

CANCELLED_FROM_PAID=$(add rectangle --x 730 --y 390 -w 160 -h 60 --roundness \
  --label "cancelled" \
  --bg "#fecaca" --stroke "#b91c1c" --fill-style solid --roughness 0 --sw 2)

REFUNDED=$(add rectangle --x 1390 --y 390 -w 160 -h 60 --roundness \
  --label "refunded" \
  --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)

# ════════════════════════════════════════════════════════════════════════════
# STEP 5: Connections
# Normal transitions: black solid sw=2
# Cancel transitions: red dashed sw=2 (Error/failure — Rule 15)
# Refund transition:  orange dashed sw=2
# ════════════════════════════════════════════════════════════════════════════

# Happy-path forward transitions
conn "$START"       "$PLACED"      "new order"   "#1e1e1e" "solid"
conn "$PLACED"      "$PAYMENT"     "checkout"    "#1e1e1e" "solid"
conn "$PAYMENT"     "$PAID"        "payment ok"  "#1e1e1e" "solid"
conn "$PAID"        "$FULFILLMENT" "confirmed"   "#1e1e1e" "solid"
conn "$FULFILLMENT" "$SHIPPED"     "dispatched"  "#1e1e1e" "solid"
conn "$SHIPPED"     "$DELIVERED"   "delivered"   "#1e1e1e" "solid"
conn "$DELIVERED"   "$END"         ""            "#1e1e1e" "solid"

# Cancel from placed → cancelled (row 2)
conn "$PLACED"      "$CANCELLED_FROM_PLACED" "cancel"      "#dc2626" "dashed"

# Cancel from paid → cancelled (row 2)
conn "$PAID"        "$CANCELLED_FROM_PAID"   "cancel"      "#dc2626" "dashed"

# Refund from delivered → refunded (row 2)
conn "$DELIVERED"   "$REFUNDED"              "refund req." "#c2410c" "dashed"

# ── Export PNG ────────────────────────────────────────────────────────────────
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
