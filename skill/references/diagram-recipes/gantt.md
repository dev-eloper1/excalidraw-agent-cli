# Gantt Diagram Recipe

## When to use

Use a Gantt chart when you need to communicate a **time-phased plan** — project timelines, sprint schedules, release roadmaps, or resource allocation across parallel workstreams. The key signal is that tasks have a start date and a duration, and multiple tasks may overlap.

Choose Gantt over other diagram types when:
- You have 3–12 tasks spanning a discrete number of time units (weeks, sprints, months)
- Stakeholders need to see parallelism and dependencies at a glance
- The narrative is "what happens when" rather than "how components connect"

Do NOT use for: system architecture, data flows, decision trees, or anything where time is not the primary axis.

---

## Layout template

```
Canvas: 1200 × 800px, origin top-left (0, 0)

Constants:
  LABEL_COL_W = 180    ← left column width for task name labels
  COL_W       = 150    ← width per time unit (week/sprint/month)
  HEADER_Y    = 80     ← y for time axis text labels
  TASK_START_Y = 120   ← y for top of first task row
  ROW_H       = 55     ← height of each task bar
  ROW_GAP     = 8      ← vertical gap between rows
  DIAGRAM_X   = 20     ← left margin

Time axis labels (column headers):
  x = LABEL_COL_W + col_index * COL_W + COL_W/2
  y = HEADER_Y
  (col_index is 0-based, so col 1 → x = 180 + 0*150 + 75 = 255)

Task row positions:
  row_y(n) = TASK_START_Y + n * (ROW_H + ROW_GAP)   (n = 0, 1, 2 ...)
  row_center_y(n) = row_y(n) + ROW_H / 2

Task bar geometry:
  bar_x = LABEL_COL_W + (start_unit - 1) * COL_W
  bar_w = duration_units * COL_W - 4    ← 4px gap to next column edge
  bar_h = ROW_H

Task name label:
  x = 25
  y = row_center_y(n)  (vertically centered with bar)

Horizontal grid lines (row separators):
  x = DIAGRAM_X, y = row_y(n) - ROW_GAP/2
  w = LABEL_COL_W + num_cols * COL_W, h = 1
  opacity = 20, stroke = #e2e8f0

Axis divider line (below header):
  x = DIAGRAM_X, y = HEADER_Y + 20
  w = LABEL_COL_W + num_cols * COL_W, h = 1
  stroke = #94a3b8, opacity = 60
```

**Coordinate worked example (6 columns / weeks):**

| Element | x | y | w |
|---------|---|---|---|
| "Week 1" label | 255 | 80 | — |
| "Week 2" label | 405 | 80 | — |
| "Week 3" label | 555 | 80 | — |
| Task 0 bar (row 0) | 180 | 120 | varies |
| Task 1 bar (row 1) | 180 | 183 | varies |
| Task 2 bar (row 2) | 180 | 246 | varies |

---

## Color and style defaults

Colors encode phase type. Always pass both `--bg` and `--stroke`.

| Phase | `--bg` | `--stroke` | Notes |
|-------|--------|------------|-------|
| Design / Planning | `#bfdbfe` | `#1e40af` | Clients/Users palette |
| Development / Engineering | `#86efac` | `#15803d` | Application Services palette |
| Testing / QA | `#fef08a` | `#92400e` | IMPORTANT: use `#92400e` not `#a16207` — dark amber-brown provides readable contrast on yellow fill |
| Launch / Deployment | `#a7f3d0` | `#047857` | End/Success palette |
| Infrastructure / DevOps | `#fed7aa` | `#c2410c` | Security/Edge palette |
| Milestone (point) | `#fecdd3` | `#be123c` | Use a narrow bar (w=8) as a diamond-like marker |

**Fill style:** always `solid` for task bars.
**Roughness:** `0` for clean professional output, `1` for sketch aesthetic.
**Stroke width:** `--sw 1` for task bars (keeps them compact at ROW_H=55).

**Header text:**
- Time axis labels: `--fs 13 --ff 2 --color "#374151"`
- Task name labels: `--fs 13 --ff 2 --color "#1e293b"`
- Diagram title: `--fs 20 --ff 2 --color "#1e293b"` at y=15

**Grid lines:** `--bg "#e2e8f0" --stroke "#e2e8f0" --opacity 20 --sw 1`

---

## Common pitfalls

1. **Yellow bars need dark-brown stroke.** `--bg "#fef08a"` with `--stroke "#a16207"` is muddy and hard to read. Always use `--stroke "#92400e"` (dark amber-brown) for QA/Testing tasks on yellow fill. See color-palette.md Text Contrast Rules.

2. **off-by-one in column math.** The first time unit is `start_unit = 1`, so its bar_x = `LABEL_COL_W + (1-1)*COL_W = LABEL_COL_W`. A task starting at week 2 uses `(2-1)*COL_W`. Do not use 0-based indexing here.

3. **Bar width gap.** Use `duration_units * COL_W - 4` (not `- 2` or `- 0`) for a clean 4px visual gap between adjacent same-row bars. Without the gap, touching bars blend together.

4. **Task label placement.** Task names go at `x=25` as free-floating text, NOT as a `--label` inside the bar. The bar starts at x=180; a label inside would be cut off at the left column boundary.

5. **Rule 1 (x ≥ 200, y ≥ 150) applies to nodes, but the Gantt layout is deliberately compact.** The left margin (DIAGRAM_X=20) and header (HEADER_Y=80) intentionally sit below Rule 1's coordinates for a full-canvas timeline. Free-floating text at x=25 is acceptable for task labels because it is structural metadata, not a node. If you need to comply strictly with Rule 1 for node elements, shift LABEL_COL_W and DIAGRAM_X right to x=200+.

6. **Grid line element IDs.** Add grid lines with `> /dev/null` — you do not need their IDs. They should never be wired with `conn`.

7. **Column header alignment.** Use the center of the column (`LABEL_COL_W + col_index*COL_W + COL_W/2`) so labels align visually with bar positions, not with the left edge of each column.

---

## Worked example

**Scenario:** 6-week feature launch with 5 tasks

| Task | Phase | Start Week | Duration |
|------|-------|-----------|---------|
| Design & Planning | Design | 1 | 2 |
| Backend Dev | Development | 2 | 2 |
| Frontend Dev | Development | 3 | 3 |
| Testing & QA | Testing | 4 | 2 |
| Launch | Deployment | 6 | 1 |

**Coordinate calculations:**
```
LABEL_COL_W=180, COL_W=150, TASK_START_Y=120, ROW_H=55, ROW_GAP=8

Row y values:
  row 0: y=120,  center=147   (Design)
  row 1: y=183,  center=210   (Backend)
  row 2: y=246,  center=273   (Frontend)
  row 3: y=309,  center=336   (Testing)
  row 4: y=372,  center=399   (Launch)

Bar positions:
  Design:   bar_x = 180+(1-1)*150=180, bar_w = 2*150-4=296
  Backend:  bar_x = 180+(2-1)*150=330, bar_w = 2*150-4=296
  Frontend: bar_x = 180+(3-1)*150=480, bar_w = 3*150-4=446
  Testing:  bar_x = 180+(4-1)*150=630, bar_w = 2*150-4=296
  Launch:   bar_x = 180+(6-1)*150=930, bar_w = 1*150-4=146

Time axis labels (col_index 0–5):
  Week 1: x=255, Week 2: x=405, Week 3: x=555
  Week 4: x=705, Week 5: x=855, Week 6: x=1005
```

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"
CLI=$(which excalidraw-agent-cli)
P=/tmp/gantt-worked-example.excalidraw

add() { $CLI -p "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

rm -f "$P"
$CLI --json project new --name "gantt-worked-example" --output "$P" > /dev/null

# Title
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" -t "6-Week Feature Launch" > /dev/null

# Axis divider line
add rectangle --x 20 --y 99 -w 1090 -h 1 \
  --bg "#94a3b8" --stroke "#94a3b8" --fill-style solid --opacity 60 --sw 1 > /dev/null

# Time axis labels (Week 1–6)
add text --x 218 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 1" > /dev/null
add text --x 368 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 2" > /dev/null
add text --x 518 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 3" > /dev/null
add text --x 668 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 4" > /dev/null
add text --x 818 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 5" > /dev/null
add text --x 968 --y 80 --fs 13 --ff 2 --color "#374151" -t "Week 6" > /dev/null

# Grid lines
add rectangle --x 20 --y 178 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 20 --y 241 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 20 --y 304 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 20 --y 367 -w 1090 -h 1 \
  --bg "#e2e8f0" --stroke "#e2e8f0" --fill-style solid --opacity 20 --sw 1 > /dev/null

# Task name labels (left column)
add text --x 25 --y 140 --fs 13 --ff 2 --color "#1e293b" -t "Design & Planning" > /dev/null
add text --x 25 --y 203 --fs 13 --ff 2 --color "#1e293b" -t "Backend Dev"       > /dev/null
add text --x 25 --y 266 --fs 13 --ff 2 --color "#1e293b" -t "Frontend Dev"      > /dev/null
add text --x 25 --y 329 --fs 13 --ff 2 --color "#1e293b" -t "Testing & QA"      > /dev/null
add text --x 25 --y 392 --fs 13 --ff 2 --color "#1e293b" -t "Launch"            > /dev/null

# Task bars
add rectangle --x 180 --y 120 -w 296 -h 55 \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 1 > /dev/null
add rectangle --x 330 --y 183 -w 296 -h 55 \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1 > /dev/null
add rectangle --x 480 --y 246 -w 446 -h 55 \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 1 > /dev/null
add rectangle --x 630 --y 309 -w 296 -h 55 \
  --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 1 > /dev/null
add rectangle --x 930 --y 372 -w 146 -h 55 \
  --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 1 > /dev/null

$CLI -p "$P" export png --output /tmp/gantt-worked-example.png --overwrite
echo "Exported: /tmp/gantt-worked-example.png"
```
