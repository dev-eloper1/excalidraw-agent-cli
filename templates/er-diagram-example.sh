#!/usr/bin/env bash
# er-diagram-example.sh — Blog Schema ER Diagram
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/er-diagram-template-preview.png
#
# Entities:
#   users      (col1, row1) x=80,  y=100
#   posts      (col2, row1) x=360, y=100
#   comments   (col3, row1) x=640, y=100
#   tags       (col1, row2) x=80,  y=340
#   post_tags  (col2, row2) x=360, y=340  [junction — hachure fill]
#
# Grid: 3 cols × 2 rows
#   col spacing: 280px (gap = 280-200 = 80px ✓ Rule 2)
#   row spacing: 240px (row y: 100, 340)
#
# Relationships (cardinality as arrow labels):
#   users    → posts      1..N
#   users    → comments   1..N
#   posts    → comments   1..N
#   posts    → post_tags  1..N
#   tags     → post_tags  1..N
#
# Color reference (from color-palette.md):
#   Entity boxes:     bg=#ddd6fe stroke=#6d28d9 (Data/Storage)
#   Junction (weak):  bg=#ddd6fe stroke=#6d28d9 fill=hachure
#   PK text:          color=#1e40af (emphasis blue)
#   FK text:          color=#6d28d9 (emphasis purple)
#   Attribute text:   color=#374151 (primary label)
#   Relationship arrows: stroke=#6d28d9 solid sw=2

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/er-diagram-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/er-diagram-template-preview.png"

# ── Helpers ──────────────────────────────────────────────────────────────────
add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}


# ── Create project ────────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "er-diagram-example" --output "$P" > /dev/null

# ── Title ─────────────────────────────────────────────────────────────────────
# Rule 21: title y=15, fs=20 → first entity at y=100 → 65px clearance ✓
add text --x 80 --y 30 --fs 20 --ff 2 --color "#1e293b" \
  -t "Blog Schema — Entity Relationship Diagram" > /dev/null

add text --x 80 --y 58 --fs 13 --ff 2 --color "#374151" \
  -t "PK = primary key  |  FK = foreign key  |  hachure fill = junction/weak entity" > /dev/null

# Legend: color key
add text --x 80 --y 76 --fs 12 --ff 3 --color "#1e40af" -t "■ PK field" > /dev/null
add text --x 160 --y 76 --fs 12 --ff 3 --color "#6d28d9" -t "■ FK field" > /dev/null
add text --x 240 --y 76 --fs 12 --ff 3 --color "#374151" -t "■ attribute" > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 1: Entity boxes
# Entity name: separate add text at entity_y + 12 (NOT --label, which renders at center)
# Divider line at entity_y + 34
# Attribute text lines use add text with --ff 3 (monospace), 18px row height
# Attribute y start = entity_y + 46
# ════════════════════════════════════════════════════════════════════════════

# ── ENTITY: users  x=80, y=100, w=200, h=170
USERS=$(add rectangle --x 80 --y 100 -w 200 -h 170 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 92 --y 112 --fs 13 --ff 2 --color "#6d28d9" -t "users" > /dev/null
add line --x 80 --y 134 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 92 --y 146 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 92 --y 164 --fs 12 --ff 3 --color "#374151" -t "    name" > /dev/null
add text --x 92 --y 182 --fs 12 --ff 3 --color "#374151" -t "    email" > /dev/null
add text --x 92 --y 200 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null
add text --x 92 --y 218 --fs 12 --ff 3 --color "#374151" -t "    password_hash" > /dev/null

# ── ENTITY: posts  x=360, y=100, w=200, h=190
POSTS=$(add rectangle --x 360 --y 100 -w 200 -h 190 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 372 --y 112 --fs 13 --ff 2 --color "#6d28d9" -t "posts" > /dev/null
add line --x 360 --y 134 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 372 --y 146 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 372 --y 164 --fs 12 --ff 3 --color "#6d28d9" -t "FK  user_id" > /dev/null
add text --x 372 --y 182 --fs 12 --ff 3 --color "#374151" -t "    title" > /dev/null
add text --x 372 --y 200 --fs 12 --ff 3 --color "#374151" -t "    body" > /dev/null
add text --x 372 --y 218 --fs 12 --ff 3 --color "#374151" -t "    published_at" > /dev/null
add text --x 372 --y 236 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: comments  x=640, y=100, w=200, h=190
COMMENTS=$(add rectangle --x 640 --y 100 -w 200 -h 190 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 652 --y 112 --fs 13 --ff 2 --color "#6d28d9" -t "comments" > /dev/null
add line --x 640 --y 134 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 652 --y 146 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 652 --y 164 --fs 12 --ff 3 --color "#6d28d9" -t "FK  post_id" > /dev/null
add text --x 652 --y 182 --fs 12 --ff 3 --color "#6d28d9" -t "FK  user_id" > /dev/null
add text --x 652 --y 200 --fs 12 --ff 3 --color "#374151" -t "    body" > /dev/null
add text --x 652 --y 218 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: tags  x=80, y=340, w=200, h=140
TAGS=$(add rectangle --x 80 --y 340 -w 200 -h 140 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 92 --y 352 --fs 13 --ff 2 --color "#6d28d9" -t "tags" > /dev/null
add line --x 80 --y 374 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 92 --y 386 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 92 --y 404 --fs 12 --ff 3 --color "#374151" -t "    name" > /dev/null
add text --x 92 --y 422 --fs 12 --ff 3 --color "#374151" -t "    slug" > /dev/null
add text --x 92 --y 440 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: post_tags  x=360, y=340, w=200, h=140  [junction — hachure]
POST_TAGS=$(add rectangle --x 360 --y 340 -w 200 -h 140 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style hachure --roughness 0 --sw 2)
add text --x 372 --y 352 --fs 13 --ff 2 --color "#6d28d9" -t "post_tags" > /dev/null
add line --x 360 --y 374 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 372 --y 386 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK  post_id" > /dev/null
add text --x 372 --y 404 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK  tag_id" > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: Relationship arrows with cardinality labels
# Rule 23: use explicit add arrow --x --y --ex --ey (NOT element connect)
# when multiple arrows share a source or target node.
# Stagger Y-exit/entry by 30px to prevent bundling at shared edges.
# Skip connections route at a distinct y level so they don't overlap same-row arrows.
# All arrows: purple stroke (#6d28d9) solid sw=2, label positioned 16px above midpoint.
# ════════════════════════════════════════════════════════════════════════════

# Entity edges (for reference):
#   users:     right x=280, center_y=185
#   posts:     left x=360, right x=560, center_y=195
#   comments:  left x=640, center_y=195
#   tags:      right x=280, center_y=410
#   post_tags: left x=360, center_y=410

# users → posts: exit users right at y=170, enter posts left at y=170
add arrow --x 280 --y 170 --ex 360 --ey 170 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 296 --y 154 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# users → comments (skip: diagonal at distinct y levels — exits users at y=200, enters
# comments at y=150; this differentiates it from users→posts and posts→comments at both ends)
add arrow --x 280 --y 200 --ex 640 --ey 150 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 430 --y 156 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# posts → comments: exit posts right at y=200, enter comments left at y=200
add arrow --x 560 --y 200 --ex 640 --ey 200 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 578 --y 184 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# posts → post_tags: vertical, exit posts bottom-center (460,290) → post_tags top-center (460,340)
add arrow --x 460 --y 290 --ex 460 --ey 340 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 468 --y 308 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# tags → post_tags: exit tags right at y=410, enter post_tags left at y=410
add arrow --x 280 --y 410 --ex 360 --ey 410 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 296 --y 394 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# ── Export PNG ────────────────────────────────────────────────────────────────
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
