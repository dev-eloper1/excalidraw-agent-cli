# Sequence Diagram Recipe

## When to use

Use a sequence diagram when you need to communicate **the order of messages exchanged between named participants** — auth flows, API request/response cycles, event-driven protocols, RPC chains. The defining signal is "who sends what to whom, and in what order."

Choose this pattern when:
- There are 2–6 named participants (browser, service, DB, queue, etc.)
- Time order matters — steps must be read top-to-bottom
- Return messages (responses) need to be visually distinguished from requests
- Readers need to trace a specific message path and see which side initiates each step

Do NOT use for: component topology (use architecture diagram), conditional branching without message exchange (use flowchart), or scheduled timelines (use Gantt).

---

## Layout template

```
Canvas: 1200 × 800px, origin top-left (0, 0)

PARTICIPANT ROW — fixed at top
  y=100, h=50
  w=160 per participant (adjust for longer labels using Rule 3)
  Horizontal spacing: COL_W=200 (center-to-center)

  For N participants, center the row on the 1200px canvas:
    total_span = N * 160 + (N-1) * 40   (40px gaps between boxes)
    start_x = (1200 - total_span) / 2
    participant center_x = start_x + (i * COL_W) + 80   (80 = w/2)

  4 participants example (centered):
    P1: x=200, center_x=280
    P2: x=400, center_x=480
    P3: x=600, center_x=680
    P4: x=800, center_x=880

LIFELINES — vertical dashed lines below each participant
  x = participant center_x
  y_start = 160   (participant bottom + 10px)
  y_end = 760     (near canvas bottom)
  Style: --stroke "#cbd5e1" --sw 1 --stroke-style dashed

MESSAGE ARROWS — horizontal lines between lifelines, descending
  First message: MSG_Y=220
  Spacing:       MSG_STEP=70   (70px per message row)
  Subsequent:    MSG_Y + n*MSG_STEP

  Named variables:
    MSG1_Y=220
    MSG2_Y=290
    MSG3_Y=360
    MSG4_Y=430
    MSG5_Y=500

MESSAGE LABELS — free-floating text ABOVE each arrow
  label_y = MSG_Y - 26   (26px above arrow line — enough clearance to avoid overlapping dashed arrow lines)
  label_x = midpoint_x - estimated_label_width/2

  Use Rule 3 to estimate label width: max(60, len(label) * 7)
```

**CRITICAL: NEVER use `element connect` for sequence diagram arrows.** (Rule 16, Rule 20)

`element connect` between same-row participants produces bidirectional curved arrows due to bounding box normalization. Always use explicit `add arrow` with calculated coordinates for all message arrows in sequence diagrams.

---

## Color and style defaults

### Participant boxes

| Node type | `--bg` | `--stroke` | Notes |
|-----------|--------|------------|-------|
| Browser / Client | `#bfdbfe` | `#1e40af` | Clients / Users color |
| API Gateway / Router | `#86efac` | `#15803d` | Gateway / Routing color |
| Auth / Security service | `#fed7aa` | `#c2410c` | Security / Edge color |
| Application service | `#86efac` | `#15803d` | Application Services color |
| Database / Storage | `#ddd6fe` | `#6d28d9` | Data / Storage color |
| External / Third-party | `#fed7aa` | `#c2410c` | External / Third-party color |
| Neutral (generic participant) | `#e2e8f0` | `#334155` | Neutral / Base color |

Participant style: `--fill-style solid --roughness 0 --sw 2`

### Lifeline style

```bash
add line --x <center_x> --y 160 --points "0,0 0,600" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null
```

### Message arrow types

| Message type | `--stroke` | `--stroke-style` | `--sw` | Arrowheads |
|-------------|-----------|-----------------|--------|------------|
| Synchronous request (left→right) | `#1e1e1e` | `solid` | `2` | `--start-arrowhead none --end-arrowhead arrow` |
| Response / return (right→left) | `#a16207` | `dashed` | `1` | `--start-arrowhead none --end-arrowhead arrow` |
| Auth / security call | `#c2410c` | `solid` | `2` | `--start-arrowhead none --end-arrowhead arrow` |
| Error response | `#dc2626` | `dashed` | `2` | `--start-arrowhead none --end-arrowhead arrow` |
| Async / fire-and-forget | `#a16207` | `dashed` | `1` | `--start-arrowhead none --end-arrowhead arrow` |

### Message label text

```bash
add text --x <label_x> --y <msg_y - 26> --fs 13 --ff 2 --color "#1e293b" \
  -t "1. POST /auth/login" > /dev/null
```

Secondary / metadata labels: `--fs 12 --ff 3 --color "#6b7280"` (monospace, muted)

### Title text

```bash
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" -t "Auth Flow"
```

---

## Common pitfalls

1. **Using `element connect` for horizontal arrows.** This is the most common mistake. `element connect` normalizes bounding boxes and produces curved or doubled arrows between same-row elements. Always use `add arrow --x <sx> --y <sy> --ex <ex> --ey <ey>` with explicit coordinates. See Rule 16 and Rule 20.

2. **Arrow y-coordinates misaligned.** Both `--y` and `--ey` must be identical for a perfectly horizontal arrow. Any difference creates a diagonal. Use a single named variable: `MSG1_Y=220` and pass it to both `--y` and `--ey`.

3. **Label text placed ON the arrow line.** The `-l` flag on `add arrow` renders text directly on the line — unreadable. Always use a separate `add text` element placed 18–20px above the arrow midpoint. See Rule 16.

4. **Too many participants causing overlap.** At COL_W=200, 5 participants need 200*4+160=960px which fits in 1200px. For 6 participants reduce COL_W to 170 and node w to 140. Never let participant boxes overlap or gap < 40px (Rule 2).

5. **Lifelines drawn after messages.** Lifelines are visual guides only — they do not anchor arrows. Draw them immediately after participant boxes, before any message arrows. Since lifelines are cosmetic, their z-order matters only for clarity.

6. **Response arrows going left-to-right when they should go right-to-left.** For a return message from service B back to service A (where B is to the right of A), set `--x B_center_x --ex A_center_x`. The arrow always travels from the `--x,--y` point to the `--ex,--ey` point.

7. **Participant center_x miscalculated.** Participant at `--x 400 -w 160` has center_x = 400 + 80 = 480. Always add half the width when computing center positions for arrow endpoints.

---

## Worked example

**Scenario:** Auth flow — Browser sends login credentials to API Gateway, which forwards to Auth Service, which queries the DB, returns a JWT to the service, which returns it to the browser.

**Participants:**

| ID | Label | x | center_x |
|----|-------|---|----------|
| BROWSER | Browser | 200 | 280 |
| GATEWAY | API Gateway | 400 | 480 |
| AUTH | Auth Service | 600 | 680 |
| DB | Database | 800 | 880 |

**Message plan:**

| # | From | To | Label | Direction | y |
|---|------|----|-------|-----------|---|
| 1 | Browser | Gateway | POST /auth/login | → | 220 |
| 2 | Gateway | Auth | verify(email, pw) | → | 290 |
| 3 | Auth | DB | SELECT user WHERE email | → | 360 |
| 4 | DB | Auth | user record | ← | 430 |
| 5 | Auth | Gateway | JWT token | ← | 500 |
| 6 | Gateway | Browser | 200 OK + token | ← | 570 |

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"
CLI=$(which excalidraw-agent-cli)
P=/tmp/sequence-worked-example.excalidraw

add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

rm -f "$P"
$CLI --json project new --name "sequence-worked-example" --output "$P" > /dev/null

# Title — y=15 fs=20 → baseline≈37. Participants at y=100 → 63px clearance (Rule 21 ✓)
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "Authentication Flow" > /dev/null

# ── Participant boxes ─────────────────────────────────────────────────────────
# COL_W=200, w=160, center_x = x + 80
# Centered on 1200px: 4 participants, total_span=4*160+3*40=760, start_x=(1200-760)/2=220
# → adjusted to x=200 for clean numbers

BROWSER=$(add rectangle --x 200 --y 100 -w 160 -h 50 \
  --label "Browser"      --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)
GATEWAY=$(add rectangle --x 400 --y 100 -w 160 -h 50 \
  --label "API Gateway"  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
AUTH=$(    add rectangle --x 600 --y 100 -w 160 -h 50 \
  --label "Auth Service" --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)
DB=$(      add rectangle --x 800 --y 100 -w 160 -h 50 \
  --label "Database"     --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)

# Participant center_x values (x + w/2):
BROWSER_CX=280
GATEWAY_CX=480
AUTH_CX=680
DB_CX=880

# ── Lifelines ─────────────────────────────────────────────────────────────────
# y_start = participant bottom + 10 = 150 + 10 = 160; y_end = 660
add line --x $BROWSER_CX --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null
add line --x $GATEWAY_CX --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null
add line --x $AUTH_CX    --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null
add line --x $DB_CX      --y 160 --points "0,0 0,500" \
  --stroke "#cbd5e1" --sw 1 --stroke-style dashed > /dev/null

# ── Message 1: Browser → Gateway (POST /auth/login) ──────────────────────────
MSG1_Y=220
MID1_X=$(( (BROWSER_CX + GATEWAY_CX) / 2 - 60 ))
add text --x $MID1_X --y $(( MSG1_Y - 26 )) --fs 13 --ff 2 --color "#1e293b" \
  -t "1. POST /auth/login" > /dev/null
add arrow --x $BROWSER_CX --y $MSG1_Y --ex $GATEWAY_CX --ey $MSG1_Y \
  --stroke "#1e1e1e" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 2: Gateway → Auth (verify credentials) ───────────────────────────
MSG2_Y=290
MID2_X=$(( (GATEWAY_CX + AUTH_CX) / 2 - 55 ))
add text --x $MID2_X --y $(( MSG2_Y - 26 )) --fs 13 --ff 2 --color "#c2410c" \
  -t "2. verify(email, pw)" > /dev/null
add arrow --x $GATEWAY_CX --y $MSG2_Y --ex $AUTH_CX --ey $MSG2_Y \
  --stroke "#c2410c" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 3: Auth → DB (SELECT query) ──────────────────────────────────────
MSG3_Y=360
MID3_X=$(( (AUTH_CX + DB_CX) / 2 - 70 ))
add text --x $MID3_X --y $(( MSG3_Y - 26 )) --fs 13 --ff 2 --color "#6d28d9" \
  -t "3. SELECT user" > /dev/null
add arrow --x $AUTH_CX --y $MSG3_Y --ex $DB_CX --ey $MSG3_Y \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 4: DB → Auth (user record returned) ──────────────────────────────
MSG4_Y=430
MID4_X=$(( (AUTH_CX + DB_CX) / 2 - 50 ))
add text --x $MID4_X --y $(( MSG4_Y - 26 )) --fs 13 --ff 2 --color "#6b7280" \
  -t "4. user record" > /dev/null
add arrow --x $DB_CX --y $MSG4_Y --ex $AUTH_CX --ey $MSG4_Y \
  --stroke "#a16207" --sw 1 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 5: Auth → Gateway (JWT issued) ───────────────────────────────────
MSG5_Y=500
MID5_X=$(( (GATEWAY_CX + AUTH_CX) / 2 - 40 ))
add text --x $MID5_X --y $(( MSG5_Y - 26 )) --fs 13 --ff 2 --color "#6b7280" \
  -t "5. JWT token" > /dev/null
add arrow --x $AUTH_CX --y $MSG5_Y --ex $GATEWAY_CX --ey $MSG5_Y \
  --stroke "#a16207" --sw 1 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

# ── Message 6: Gateway → Browser (200 OK) ────────────────────────────────────
MSG6_Y=570
MID6_X=$(( (BROWSER_CX + GATEWAY_CX) / 2 - 60 ))
add text --x $MID6_X --y $(( MSG6_Y - 26 )) --fs 13 --ff 2 --color "#6b7280" \
  -t "6. 200 OK + token" > /dev/null
add arrow --x $GATEWAY_CX --y $MSG6_Y --ex $BROWSER_CX --ey $MSG6_Y \
  --stroke "#a16207" --sw 1 --stroke-style dashed \
  --start-arrowhead none --end-arrowhead arrow > /dev/null

$CLI -p "$P" export png --output /tmp/sequence-worked-example.png --overwrite
echo "Exported: /tmp/sequence-worked-example.png"
```
