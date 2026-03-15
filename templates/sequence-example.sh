#!/usr/bin/env bash
# sequence-example.sh — Authentication Sequence Diagram
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/sequence-template-preview.png
#
# Participants (left-to-right):
#   Browser     x=200  center_x=280
#   API Gateway x=400  center_x=480
#   Auth Service x=600 center_x=680
#   Database    x=800  center_x=880
#
# Messages (top-to-bottom, MSG_STEP=70):
#   1. Browser → Gateway:  POST /auth/login        y=220  (sync, black solid)
#   2. Gateway → Auth:     verify(email, pw)        y=290  (auth, orange solid)
#   3. Auth → DB:          SELECT user              y=360  (data, purple solid)
#   4. DB → Auth:          user record              y=430  (return, amber dashed)
#   5. Auth → Gateway:     JWT token                y=500  (return, amber dashed)
#   6. Gateway → Browser:  200 OK + token           y=570  (return, amber dashed)
#
# CRITICAL: NEVER use element connect for sequence arrows (Rules 16 & 20).
#           All message arrows use explicit add arrow coordinates.
#           Labels are separate add text elements 18px above each arrow.

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/sequence-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/sequence-template-preview.png"

# ── Layout constants ──────────────────────────────────────────────────────────
COL_W=200       # center-to-center column spacing
PART_W=160      # participant box width
PART_H=50       # participant box height
PART_Y=100      # participant row top y
MSG_STEP=70     # vertical spacing between message rows
FIRST_MSG_Y=220 # y of first message arrow

# Participant x positions (start of box)
P1_X=200; P1_CX=280    # Browser:       center = 200+80
P2_X=400; P2_CX=480    # API Gateway:   center = 400+80
P3_X=600; P3_CX=680    # Auth Service:  center = 600+80
P4_X=800; P4_CX=880    # Database:      center = 800+80

add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

# ── Create project ────────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "sequence-example" --output "$P" > /dev/null

# ── Title ─────────────────────────────────────────────────────────────────────
# y=15 fs=20 → baseline≈37. Participants at y=100 → 63px clearance (Rule 21 ✓)
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "Authentication Flow" > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 1: Participant boxes
# ════════════════════════════════════════════════════════════════════════════

add rectangle --x $P1_X --y $PART_Y -w $PART_W -h $PART_H \
  --label "Browser" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2 > /dev/null

add rectangle --x $P2_X --y $PART_Y -w $PART_W -h $PART_H \
  --label "API Gateway" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 > /dev/null

add rectangle --x $P3_X --y $PART_Y -w $PART_W -h $PART_H \
  --label "Auth Service" \
  --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2 > /dev/null

add rectangle --x $P4_X --y $PART_Y -w $PART_W -h $PART_H \
  --label "Database" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: Lifelines — vertical dashed lines below each participant
# y_start = PART_Y + PART_H + 10 = 160; length = 500px
# ════════════════════════════════════════════════════════════════════════════

add line --x $P1_CX --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null
add line --x $P2_CX --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null
add line --x $P3_CX --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null
add line --x $P4_CX --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null

# ════════════════════════════════════════════════════════════════════════════
# STEP 3: Message arrows — explicit coordinates only (Rule 16, Rule 20)
# Pattern: add text label 18px above, then add arrow at msg_y
# Label x = midpoint of the two participant center_x values, offset left by ~half label width
# ════════════════════════════════════════════════════════════════════════════

# ── Message 1: Browser → API Gateway (POST /auth/login) ──────────────────────
MSG1_Y=$FIRST_MSG_Y
add text --x 330 --y $(( MSG1_Y - 18 )) --fs 13 --ff 2 --color "#1e293b" \
  -t "1. POST /auth/login" > /dev/null
add arrow --x $P1_CX --y $MSG1_Y --ex $P2_CX --ey $MSG1_Y \
  --stroke "#1e1e1e" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 2: API Gateway → Auth Service (verify credentials) ───────────────
MSG2_Y=$(( FIRST_MSG_Y + MSG_STEP ))
add text --x 530 --y $(( MSG2_Y - 18 )) --fs 13 --ff 2 --color "#c2410c" \
  -t "2. verify(email, pw)" > /dev/null
add arrow --x $P2_CX --y $MSG2_Y --ex $P3_CX --ey $MSG2_Y \
  --stroke "#c2410c" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 3: Auth Service → Database (SELECT query) ────────────────────────
MSG3_Y=$(( FIRST_MSG_Y + MSG_STEP * 2 ))
add text --x 730 --y $(( MSG3_Y - 18 )) --fs 13 --ff 2 --color "#6d28d9" \
  -t "3. SELECT user" > /dev/null
add arrow --x $P3_CX --y $MSG3_Y --ex $P4_CX --ey $MSG3_Y \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 4: Database → Auth Service (user record) ─────────────────────────
MSG4_Y=$(( FIRST_MSG_Y + MSG_STEP * 3 ))
add text --x 730 --y $(( MSG4_Y - 18 )) --fs 13 --ff 2 --color "#6b7280" \
  -t "4. user record" > /dev/null
add arrow --x $P4_CX --y $MSG4_Y --ex $P3_CX --ey $MSG4_Y \
  --stroke "#a16207" --sw 1 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 5: Auth Service → API Gateway (JWT token) ────────────────────────
MSG5_Y=$(( FIRST_MSG_Y + MSG_STEP * 4 ))
add text --x 530 --y $(( MSG5_Y - 18 )) --fs 13 --ff 2 --color "#6b7280" \
  -t "5. JWT token" > /dev/null
add arrow --x $P3_CX --y $MSG5_Y --ex $P2_CX --ey $MSG5_Y \
  --stroke "#a16207" --sw 1 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 6: API Gateway → Browser (200 OK + token) ────────────────────────
MSG6_Y=$(( FIRST_MSG_Y + MSG_STEP * 5 ))
add text --x 330 --y $(( MSG6_Y - 18 )) --fs 13 --ff 2 --color "#6b7280" \
  -t "6. 200 OK + token" > /dev/null
add arrow --x $P2_CX --y $MSG6_Y --ex $P1_CX --ey $MSG6_Y \
  --stroke "#a16207" --sw 1 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Export PNG ────────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$OUT")"
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
