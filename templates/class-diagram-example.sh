#!/usr/bin/env bash
# class-diagram-example.sh — Blog System Class Diagram
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/class-diagram-template-preview.png
#
# Classes: User, Post, Comment
# Relationships:
#   Post ---(authored by)---> User   (association, arrow)
#   Comment ---(belongs to)-> Post   (composition, arrow with heavier stroke)
#   Comment ---(authored by)-> User  (association, arrow)
#
# Grid: GRID_START_X=100, GRID_START_Y=120, H_SPACING=280
# Class structure: rectangle + divider line + attribute text rows
#
# Rule 21: Title at y=15 (baseline≈37), first class at y=120 → 83px clearance ✓
# Rule 22: Class fill #ddd6fe (light) + stroke #6d28d9 (dark) = high contrast ✓

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/class-diagram-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/class-diagram-template-preview.png"

# ── Named grid/spacing variables ───────────────────────────────────────────────
GRID_START_X=100
GRID_START_Y=120
H_SPACING=340         # horizontal distance between class left edges (340 gives 140px gap for labels)
CLASS_W=200
CLASS_NAME_H=40       # height of the class name header section
FIELD_ROW_H=22        # height per attribute row
BOTTOM_PAD=10         # bottom padding inside class box

# Height formula: CLASS_NAME_H + (num_fields * FIELD_ROW_H) + BOTTOM_PAD
# User:    4 fields → 40 + 88 + 10 = 138
# Post:    5 fields → 40 + 110 + 10 = 160
# Comment: 4 fields → 40 + 88 + 10 = 138

USER_H=138
POST_H=160
COMMENT_H=138

# Helper: add element and capture ID
add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

# ── Create project ─────────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "class-diagram-example" --output "$P" > /dev/null

# ── Title ──────────────────────────────────────────────────────────────────────
# y=15, fs=20 → baseline ≈ y=37. First class at y=120 → 83px clearance (Rule 21 ✓)
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "Blog System — Class Diagram" > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS: User  (col=0, x=100, y=120)
# ═══════════════════════════════════════════════════════════════════════════════
USER_X=$GRID_START_X
USER_Y=$GRID_START_Y

USER=$(add rectangle \
  --x "$USER_X" --y "$USER_Y" -w "$CLASS_W" -h "$USER_H" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)

# Class name header text — top of box + 12px (avoids center-render overlap with attributes)
add text --x $((USER_X + 10)) --y $((USER_Y + 12)) \
  --fs 14 --ff 2 --color "#6d28d9" -t "User" > /dev/null

# Divider line: y = USER_Y + CLASS_NAME_H = 120 + 40 = 160
add line \
  --x "$USER_X" --y $((USER_Y + CLASS_NAME_H)) \
  --points "0,0 200,0" \
  --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null

# Attribute text (starts at divider_y + 6, step FIELD_ROW_H=22)
ATTR_X=$((USER_X + 10))
ATTR_Y=$((USER_Y + CLASS_NAME_H + 6))
add text --x "$ATTR_X" --y "$ATTR_Y"            --fs 12 --ff 3 --color "#6d28d9" -t "id: Long"        > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 22))     --fs 12 --ff 3 --color "#6d28d9" -t "username: String" > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 44))     --fs 12 --ff 3 --color "#6d28d9" -t "email: String"   > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 66))     --fs 12 --ff 3 --color "#6d28d9" -t "createdAt: Date" > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS: Post  (col=1, x=380, y=120)
# ═══════════════════════════════════════════════════════════════════════════════
POST_X=$((GRID_START_X + H_SPACING))    # 100 + 280 = 380
POST_Y=$GRID_START_Y

POST=$(add rectangle \
  --x "$POST_X" --y "$POST_Y" -w "$CLASS_W" -h "$POST_H" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)

# Class name header text
add text --x $((POST_X + 10)) --y $((POST_Y + 12)) \
  --fs 14 --ff 2 --color "#6d28d9" -t "Post" > /dev/null

# Divider line: y = 120 + 40 = 160
add line \
  --x "$POST_X" --y $((POST_Y + CLASS_NAME_H)) \
  --points "0,0 200,0" \
  --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null

ATTR_X=$((POST_X + 10))
ATTR_Y=$((POST_Y + CLASS_NAME_H + 6))
add text --x "$ATTR_X" --y "$ATTR_Y"            --fs 12 --ff 3 --color "#6d28d9" -t "id: Long"       > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 22))     --fs 12 --ff 3 --color "#6d28d9" -t "title: String"  > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 44))     --fs 12 --ff 3 --color "#6d28d9" -t "body: String"   > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 66))     --fs 12 --ff 3 --color "#6d28d9" -t "authorId: Long" > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 88))     --fs 12 --ff 3 --color "#6d28d9" -t "createdAt: Date"> /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS: Comment  (col=2, x=660, y=120)
# ═══════════════════════════════════════════════════════════════════════════════
CMT_X=$((GRID_START_X + H_SPACING * 2))   # 100 + 560 = 660
CMT_Y=$GRID_START_Y

COMMENT=$(add rectangle \
  --x "$CMT_X" --y "$CMT_Y" -w "$CLASS_W" -h "$COMMENT_H" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)

# Class name header text
add text --x $((CMT_X + 10)) --y $((CMT_Y + 12)) \
  --fs 14 --ff 2 --color "#6d28d9" -t "Comment" > /dev/null

# Divider line: y = 120 + 40 = 160
add line \
  --x "$CMT_X" --y $((CMT_Y + CLASS_NAME_H)) \
  --points "0,0 200,0" \
  --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null

ATTR_X=$((CMT_X + 10))
ATTR_Y=$((CMT_Y + CLASS_NAME_H + 6))
add text --x "$ATTR_X" --y "$ATTR_Y"            --fs 12 --ff 3 --color "#6d28d9" -t "id: Long"       > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 22))     --fs 12 --ff 3 --color "#6d28d9" -t "text: String"   > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 44))     --fs 12 --ff 3 --color "#6d28d9" -t "postId: Long"   > /dev/null
add text --x "$ATTR_X" --y $((ATTR_Y + 66))     --fs 12 --ff 3 --color "#6d28d9" -t "authorId: Long" > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# Rule 23: use explicit add arrow --x --y --ex --ey (NOT element connect)
# when multiple arrows share a source or target node.
# Stagger Y-exit/entry by 30px; skip connections route above all boxes (y=108).
# ═══════════════════════════════════════════════════════════════════════════════
# Class edges (H_SPACING=340):
#   User:    x=100-300, right x=300, center_y=189
#   Post:    x=440-640, left x=440, right x=640, center_y=200
#   Comment: x=780-980, left x=780, center_y=189
#   All boxes top y=120 → skip-connection route at y=108 (above all boxes)
# Gap between User and Post: 300-440 = 140px — enough for labels

# Post ---authored by---> User (association: gray, horizontal at y=175)
# Exit Post left at y=175, enter User right at y=175
add arrow --x 440 --y 175 --ex 300 --ey 175 \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
# Label centered in 140px gap between x=300 and x=440: midpoint=370
add text --x 328 --y 159 --fs 12 --ff 2 --color "#6b7280" -t "authored by" > /dev/null

# Comment ---belongs to---> Post (composition: purple, horizontal at y=200)
# Exit Comment left at y=200, enter Post right at y=200
add arrow --x 780 --y 200 --ex 640 --ey 200 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
# Label centered in 140px gap between x=640 and x=780: midpoint=710
add text --x 668 --y 184 --fs 12 --ff 2 --color "#6b7280" -t "belongs to" > /dev/null

# Comment ---authored by---> User (dashed, SKIPS Post)
# Route ABOVE all boxes at y=108 (box tops at y=120, so 12px clearance)
# Exit Comment left at y=108, enter User right at y=108
add arrow --x 780 --y 108 --ex 300 --ey 108 \
  --stroke "#94a3b8" --sw 1 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
# Label at midpoint of span 300-780 = 540, adjusted for text width
add text --x 498 --y 92 --fs 12 --ff 2 --color "#6b7280" -t "authored by" > /dev/null

# ── Export PNG ─────────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$OUT")"
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
