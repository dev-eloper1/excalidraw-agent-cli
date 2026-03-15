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
# Entity name rendered centered via --label (uses --ff 2 for entity name font)
# Attribute text lines use add text with --ff 3 (monospace), 18px row height
# Attribute y start = entity_y + 40 (clear centered label)
# ════════════════════════════════════════════════════════════════════════════

# ── ENTITY: users  x=80, y=100, w=200, h=170
USERS=$(add rectangle --x 80 --y 100 -w 200 -h 170 \
  --label "users" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 92 --y 148 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 92 --y 166 --fs 12 --ff 3 --color "#374151" -t "    name" > /dev/null
add text --x 92 --y 184 --fs 12 --ff 3 --color "#374151" -t "    email" > /dev/null
add text --x 92 --y 202 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null
add text --x 92 --y 220 --fs 12 --ff 3 --color "#374151" -t "    password_hash" > /dev/null

# ── ENTITY: posts  x=360, y=100, w=200, h=190
POSTS=$(add rectangle --x 360 --y 100 -w 200 -h 190 \
  --label "posts" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 372 --y 148 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 372 --y 166 --fs 12 --ff 3 --color "#6d28d9" -t "FK  user_id" > /dev/null
add text --x 372 --y 184 --fs 12 --ff 3 --color "#374151" -t "    title" > /dev/null
add text --x 372 --y 202 --fs 12 --ff 3 --color "#374151" -t "    body" > /dev/null
add text --x 372 --y 220 --fs 12 --ff 3 --color "#374151" -t "    published_at" > /dev/null
add text --x 372 --y 238 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: comments  x=640, y=100, w=200, h=190
COMMENTS=$(add rectangle --x 640 --y 100 -w 200 -h 190 \
  --label "comments" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 652 --y 148 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 652 --y 166 --fs 12 --ff 3 --color "#6d28d9" -t "FK  post_id" > /dev/null
add text --x 652 --y 184 --fs 12 --ff 3 --color "#6d28d9" -t "FK  user_id" > /dev/null
add text --x 652 --y 202 --fs 12 --ff 3 --color "#374151" -t "    body" > /dev/null
add text --x 652 --y 220 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: tags  x=80, y=340, w=200, h=140
TAGS=$(add rectangle --x 80 --y 340 -w 200 -h 140 \
  --label "tags" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 92 --y 388 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 92 --y 406 --fs 12 --ff 3 --color "#374151" -t "    name" > /dev/null
add text --x 92 --y 424 --fs 12 --ff 3 --color "#374151" -t "    slug" > /dev/null
add text --x 92 --y 442 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: post_tags  x=360, y=340, w=200, h=140  [junction — hachure]
POST_TAGS=$(add rectangle --x 360 --y 340 -w 200 -h 140 \
  --label "post_tags" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style hachure --roughness 0 --sw 2)
add text --x 372 --y 388 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK  post_id" > /dev/null
add text --x 372 --y 406 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK  tag_id" > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: Relationship arrows with cardinality labels
# All use purple stroke (#6d28d9) — Data read/write convention
# Solid sw=2 for all standard FK relationships
# ════════════════════════════════════════════════════════════════════════════

# users → posts  (1 user writes N posts)
conn "$USERS"     "$POSTS"     "1..N" "#6d28d9" "solid"

# users → comments  (1 user writes N comments)
conn "$USERS"     "$COMMENTS"  "1..N" "#6d28d9" "solid"

# posts → comments  (1 post has N comments)
conn "$POSTS"     "$COMMENTS"  "1..N" "#6d28d9" "solid"

# posts → post_tags  (1 post has N tag associations)
conn "$POSTS"     "$POST_TAGS" "1..N" "#6d28d9" "solid"

# tags → post_tags  (1 tag has N post associations)
conn "$TAGS"      "$POST_TAGS" "1..N" "#6d28d9" "solid"

# ── Export PNG ────────────────────────────────────────────────────────────────
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
