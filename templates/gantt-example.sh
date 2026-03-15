#!/usr/bin/env bash
# gantt-example.sh — 6-Week Feature Launch Gantt Chart
# Outputs: /Users/bhushan/Documents/excalidraw-agent-cli/examples/gantt-template-preview.png
#
# Layout constants:
#   LABEL_COL_W=180  COL_W=150  HEADER_Y=80
#   TASK_START_Y=120  ROW_H=55  ROW_GAP=8
#
# Phase colors:
#   Design:     #bfdbfe / #1e40af
#   Development:#86efac / #15803d
#   Testing:    #fef08a / #92400e  (dark amber-brown for contrast on yellow)
#   Launch:     #a7f3d0 / #047857

set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/gantt-example.excalidraw
OUT="/Users/bhushan/Documents/excalidraw-agent-cli/examples/gantt-template-preview.png"

add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

# ── Create project ───────────────────────────────────────────────────────────
rm -f "$P"
$CLI --json project new --name "gantt-example" --output "$P" > /dev/null

# ── Title ────────────────────────────────────────────────────────────────────
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "6-Week Feature Launch" > /dev/null

# ── Axis divider (below header row, above first task bar) ────────────────────
add rectangle --x 20 --y 100 -w 1090 -h 1 \
  --bg "#94a3b8" --stroke "#94a3b8" --fill-style solid --opacity 60 --sw 1 > /dev/null

# ── Time axis labels (Week 1–6) ──────────────────────────────────────────────
# x = LABEL_COL_W + col_index*COL_W + COL_W/2 - approx_label_half_width
# "Week N" is ~6 chars × ~8px = ~48px wide; center offset ≈ 24px
add text --x 218 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 1" > /dev/null
add text --x 368 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 2" > /dev/null
add text --x 518 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 3" > /dev/null
add text --x 668 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 4" > /dev/null
add text --x 818 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 5" > /dev/null
add text --x 968 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 6" > /dev/null

# ── Horizontal grid lines (thin, low-opacity separators between rows) ─────────
# Placed at the bottom edge of each row: row_y + ROW_H + ROW_GAP/2
add rectangle --x 20 --y 178 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 20 --y 241 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 20 --y 304 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 20 --y 367 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 20 --y 430 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null

# ── Task name labels (left column, vertically centered with each bar) ─────────
# row_center_y(n) = TASK_START_Y + n*(ROW_H+ROW_GAP) + ROW_H/2 - ~8px font offset
add text --x 25 --y 140 --fs 13 --ff 2 --color "#1e293b" -t "Design & Planning" > /dev/null
add text --x 25 --y 203 --fs 13 --ff 2 --color "#1e293b" -t "Backend Dev"       > /dev/null
add text --x 25 --y 266 --fs 13 --ff 2 --color "#1e293b" -t "Frontend Dev"      > /dev/null
add text --x 25 --y 329 --fs 13 --ff 2 --color "#1e293b" -t "Testing & QA"      > /dev/null
add text --x 25 --y 392 --fs 13 --ff 2 --color "#1e293b" -t "Launch"            > /dev/null

# ── Task bars ────────────────────────────────────────────────────────────────
# bar_x = LABEL_COL_W + (start_week - 1) * COL_W
# bar_w = duration_weeks * COL_W - 4
# bar_y = TASK_START_Y + row * (ROW_H + ROW_GAP)
#
# Row 0 — Design & Planning: wk1–2 (start=1, dur=2)
#   bar_x=180+(1-1)*150=180, bar_w=2*150-4=296, bar_y=120
add rectangle --x 180 --y 120 -w 296 -h 55 \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 1 > /dev/null

# Row 1 — Backend Dev: wk2–3 (start=2, dur=2)
#   bar_x=180+(2-1)*150=330, bar_w=296, bar_y=183
add rectangle --x 330 --y 183 -w 296 -h 55 \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1 > /dev/null

# Row 2 — Frontend Dev: wk3–5 (start=3, dur=3)
#   bar_x=180+(3-1)*150=480, bar_w=3*150-4=446, bar_y=246
add rectangle --x 480 --y 246 -w 446 -h 55 \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1 > /dev/null

# Row 3 — Testing & QA: wk4–5 (start=4, dur=2)
#   bar_x=180+(4-1)*150=630, bar_w=296, bar_y=309
#   NOTE: yellow fill needs dark amber-brown stroke (#92400e) for readable text contrast
add rectangle --x 630 --y 309 -w 296 -h 55 \
  --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1 > /dev/null

# Row 4 — Launch: wk6 (start=6, dur=1)
#   bar_x=180+(6-1)*150=930, bar_w=1*150-4=146, bar_y=372
add rectangle --x 930 --y 372 -w 146 -h 55 \
  --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 1 > /dev/null

# ── Export PNG ───────────────────────────────────────────────────────────────
$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
