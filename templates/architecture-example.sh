#!/usr/bin/env bash
# architecture-example.sh — Microservices Architecture Diagram
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/architecture-template-preview.png
#
# Components:
#   Client layer:   Web App, Mobile App
#   Gateway layer:  API Gateway
#   Service layer:  Auth Service, Order Service, Inventory Service, Notification Service
#   Data layer:     Postgres, Redis
#
# CRITICAL draw order: ALL zone backgrounds → zone labels → nodes → arrows
# (Excalidraw renders in insertion order — backgrounds drawn after nodes cover them)

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/architecture-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/architecture-template-preview.png"

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

# ── Create project ───────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "architecture-example" --output "$P" > /dev/null

# ── Title ────────────────────────────────────────────────────────────────────
# y=15, fs=20 → baseline ≈ y=37. First zone at y=100 → 63px clearance (Rule 21 ✓)
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "Microservices Architecture" > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 1: Zone backgrounds — ALL FOUR drawn before any node
# ════════════════════════════════════════════════════════════════════════════

# Client layer: y=100, h=120
add rectangle --x 20 --y 100 -w 1160 -h 120 \
  --bg "#dbeafe" --stroke "#93c5fd" --fill-style solid --opacity 30 --sw 1 > /dev/null

# Gateway/Security layer: y=240, h=120
add rectangle --x 20 --y 240 -w 1160 -h 120 \
  --bg "#ffedd5" --stroke "#fdba74" --fill-style solid --opacity 35 --sw 1 > /dev/null

# Service layer: y=380, h=160
add rectangle --x 20 --y 380 -w 1160 -h 160 \
  --bg "#dcfce7" --stroke "#86efac" --fill-style solid --opacity 35 --sw 1 > /dev/null

# Data layer: y=560, h=120
add rectangle --x 20 --y 560 -w 1160 -h 120 \
  --bg "#ede9fe" --stroke "#c4b5fd" --fill-style solid --opacity 35 --sw 1 > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: Zone labels (text overlays, placed after backgrounds, before nodes)
# ════════════════════════════════════════════════════════════════════════════

add text --x 30 --y 110 --fs 14 --ff 2 --color "#1e40af" -t "CLIENT LAYER"       > /dev/null
add text --x 30 --y 250 --fs 14 --ff 2 --color "#c2410c" -t "GATEWAY / SECURITY" > /dev/null
add text --x 30 --y 390 --fs 14 --ff 2 --color "#15803d" -t "SERVICES"           > /dev/null
add text --x 30 --y 570 --fs 14 --ff 2 --color "#6d28d9" -t "DATA"               > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 3: Nodes — added after all zone backgrounds
# ════════════════════════════════════════════════════════════════════════════

# ── Client layer (y=100, h=120) ──────────────────────────────────────────────
# node_y = 100 + (120-70)/2 = 125
# 2 nodes centered: x=420, x=620
WEB=$(    add rectangle --x 420 --y 125 -w 160 -h 70 \
  --label "Web App" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)
MOBILE=$( add rectangle --x 620 --y 125 -w 160 -h 70 \
  --label "Mobile App" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# ── Gateway/Security layer (y=240, h=120) ────────────────────────────────────
# node_y = 240 + (120-70)/2 = 265
# 1 node centered: x=470, w=260 (wider for longer label)
GW=$(     add rectangle --x 470 --y 265 -w 260 -h 70 \
  --label "API Gateway" \
  --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# ── Service layer (y=380, h=160) ─────────────────────────────────────────────
# node_y = 380 + (160-70)/2 = 425
# 4 nodes, 200px apart: x=220, 420, 620, 820
# "Inventory Service" = 17 chars → min_w = max(120, 17*9.6+32) = 195 → 200
# "Notification Service" = 20 chars → min_w = max(120, 20*9.6+32) = 224 → 230
AUTH=$(   add rectangle --x 220 --y 425 -w 160 -h 70 \
  --label "Auth Service" \
  --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)
ORDER=$(  add rectangle --x 420 --y 425 -w 160 -h 70 \
  --label "Order Service" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
INV=$(    add rectangle --x 620 --y 425 -w 200 -h 70 \
  --label "Inventory Service" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
NOTIF=$(  add rectangle --x 860 --y 425 -w 230 -h 70 \
  --label "Notification Service" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# ── Data layer (y=560, h=120) ─────────────────────────────────────────────────
# node_y = 560 + (120-70)/2 = 585
# 2 nodes centered: x=420, x=620
# Redis uses yellow fill → must use dark amber-brown stroke (#92400e) for contrast (Rule 22)
PG=$(     add rectangle --x 420 --y 585 -w 160 -h 70 \
  --label "Postgres" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
REDIS=$(  add rectangle --x 620 --y 585 -w 160 -h 70 \
  --label "Redis" \
  --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 2)

# ════════════════════════════════════════════════════════════════════════════
# STEP 4: Connections
# Arrow colors follow color-palette.md:
#   Primary call: #1e1e1e (black, solid)
#   Auth/security: #c2410c (orange, solid)
#   Data read/write: #6d28d9 (purple, solid)
#   Async/event: #a16207 (amber, dashed)
# ════════════════════════════════════════════════════════════════════════════

# Client → Gateway
conn "$WEB"    "$GW"    "" "#1e1e1e" "solid"
conn "$MOBILE" "$GW"    "" "#1e1e1e" "solid"

# Gateway → Services
conn "$GW"     "$AUTH"  "" "#c2410c" "solid"
conn "$GW"     "$ORDER" "" "#1e1e1e" "solid"
conn "$GW"     "$INV"   "" "#1e1e1e" "solid"
conn "$GW"     "$NOTIF" "" "#1e1e1e" "solid"

# Services → Data
conn "$ORDER"  "$PG"    "" "#6d28d9" "solid"
conn "$INV"    "$PG"    "" "#6d28d9" "solid"
conn "$ORDER"  "$REDIS" "" "#a16207" "dashed"
conn "$NOTIF"  "$REDIS" "" "#a16207" "dashed"

# ── Export PNG ───────────────────────────────────────────────────────────────
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
