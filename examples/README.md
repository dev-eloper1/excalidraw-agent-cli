# Excalidraw Agent CLI — Example Diagrams

Seven diagrams generated with `excalidraw-agent-cli`. Each example includes:
- A **Claude prompt** — what you'd say to an AI agent using the excalidraw skill
- A **bash script** — the equivalent manual CLI commands

---

## 1. Flowchart — User Signup

![Flowchart](./flowchart.png)

### Claude prompt
```
Draw a user signup flowchart. Start with "User signs up" → validate email (Email valid? diamond) → yes: Hash password → Save to Postgres → Send verify email → Account created. No branch: Return 422.
```

### Bash script
```bash
#!/usr/bin/env bash
set -e
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
CLI="excalidraw-agent-cli"
P="/tmp/flowchart.excalidraw"

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("-l" "$3")
  [[ -n "$4" ]] && args+=("--stroke" "$4")
  $CLI --project "$P" --json element connect "${args[@]}" \
    --start-arrowhead none --end-arrowhead arrow > /dev/null
}

rm -f "$P"
$CLI --json project new --name "User Signup" --output "$P" > /dev/null

# Nodes
START=$(add ellipse  --x 250 --y 30  -w 200 -h 60  --label "User signs up"     --bg "#99f6e4" --stroke "#0d9488" --fill-style solid --roughness 0)
VAL=$(add rectangle  --x 225 --y 140 -w 250 -h 65  --label "Validate email"    --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0)
DEC=$(add diamond    --x 225 --y 265 -w 250 -h 100 --label "Email valid?"      --bg "#fef3c7" --stroke "#b45309" --fill-style solid --roughness 0)
ERR=$(add rectangle  --x 20  --y 290 -w 160 -h 60  --label "Return 422"        --bg "#fecaca" --stroke "#dc2626" --fill-style solid --roughness 0)
HASH=$(add rectangle --x 490 --y 265 -w 190 -h 65  --label "Hash password"     --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0)
SAVE=$(add rectangle --x 490 --y 385 -w 190 -h 65  --label "Save to Postgres"  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0)
MAIL=$(add rectangle --x 490 --y 505 -w 190 -h 65  --label "Send verify email" --bg "#fef08a" --stroke "#854d0e" --fill-style solid --roughness 0)
DONE=$(add ellipse   --x 505 --y 625 -w 160 -h 60  --label "Account created"   --bg "#99f6e4" --stroke "#0d9488" --fill-style solid --roughness 0)

# Connections
conn "$START" "$VAL"
conn "$VAL"   "$DEC"
conn "$DEC"   "$ERR"  "no"  "#dc2626"
conn "$DEC"   "$HASH" "yes" "#15803d"
conn "$HASH"  "$SAVE"
conn "$SAVE"  "$MAIL"
conn "$MAIL"  "$DONE"

$CLI --project "$P" export png --output ./flowchart.png --overwrite
```

---

## 2. Architecture Diagram — Three-Tier Web App

![Architecture](./arch.png)

### Claude prompt
```
Draw a three-tier web architecture diagram with swim lanes: CLIENTS (Web App, Mobile App, Partner API all pointing to API Gateway), SERVICES (API Gateway wide bar, Auth Service, Core API, Notification Svc below), DATA (PostgreSQL, Redis Cache, SQS Queue at bottom). Use color-coded zones.
```

### Bash script
```bash
#!/usr/bin/env bash
set -e
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
CLI="excalidraw-agent-cli"
P="/tmp/arch.excalidraw"

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

rm -f "$P"
$CLI --json project new --name "Web Architecture" --output "$P" > /dev/null

# Zone backgrounds (add BEFORE nodes)
add rectangle --x 20 --y 40 -w 1000 -h 140 \
  --bg "#bfdbfe" --stroke "#93c5fd" --fill-style solid --opacity 30 --sw 1 --roughness 0 > /dev/null
add text --x 28 --y 48 --fs 13 --ff 2 --color "#1e40af" -t "CLIENTS" > /dev/null

add rectangle --x 20 --y 200 -w 1000 -h 240 \
  --bg "#99f6e4" --stroke "#5eead4" --fill-style solid --opacity 30 --sw 1 --roughness 0 > /dev/null
add text --x 28 --y 208 --fs 13 --ff 2 --color "#0f766e" -t "SERVICES" > /dev/null

add rectangle --x 20 --y 460 -w 1000 -h 150 \
  --bg "#ddd6fe" --stroke "#c4b5fd" --fill-style solid --opacity 35 --sw 1 --roughness 0 > /dev/null
add text --x 28 --y 468 --fs 13 --ff 2 --color "#5b21b6" -t "DATA" > /dev/null

# Client nodes
WEB=$(add rectangle    --x 60  --y 65  -w 180 -h 80 --label "Web App"      --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)
MOB=$(add rectangle    --x 420 --y 65  -w 180 -h 80 --label "Mobile App"   --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)
API=$(add rectangle    --x 780 --y 65  -w 180 -h 80 --label "Partner API"  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# Service nodes
GW=$(add rectangle     --x 65  --y 225 -w 900 -h 65 --label "API Gateway"      --bg "#a7f3d0" --stroke "#059669" --fill-style solid --roughness 0 --sw 2)
AUTH=$(add rectangle   --x 65  --y 340 -w 220 -h 70 --label "Auth Service"     --bg "#a7f3d0" --stroke "#059669" --fill-style solid --roughness 0 --sw 2)
CORE=$(add rectangle   --x 400 --y 340 -w 220 -h 70 --label "Core API"         --bg "#a7f3d0" --stroke "#059669" --fill-style solid --roughness 0 --sw 2)
NOTIF=$(add rectangle  --x 740 --y 340 -w 210 -h 70 --label "Notification Svc" --bg "#a7f3d0" --stroke "#059669" --fill-style solid --roughness 0 --sw 2)

# Data nodes
PG=$(add rectangle     --x 65  --y 480 -w 220 -h 90 --label "PostgreSQL"   --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
REDIS=$(add rectangle  --x 400 --y 480 -w 220 -h 90 --label "Redis Cache"  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
SQS=$(add rectangle    --x 740 --y 480 -w 210 -h 90 --label "SQS Queue"    --bg "#fef08a" --stroke "#854d0e" --fill-style solid --roughness 0 --sw 2)

# Connections
for C in "$WEB" "$MOB" "$API"; do
  $CLI --project "$P" --json element connect --from "$C" --to "$GW" \
    --stroke "#1e40af" --sw 2 --start-arrowhead none --end-arrowhead arrow > /dev/null
done
$CLI --project "$P" --json element connect --from "$GW" --to "$AUTH"  --stroke "#c2410c" --sw 2 --start-arrowhead none --end-arrowhead arrow > /dev/null
$CLI --project "$P" --json element connect --from "$GW" --to "$CORE"  --stroke "#1e1e1e" --sw 2 --start-arrowhead none --end-arrowhead arrow > /dev/null
$CLI --project "$P" --json element connect --from "$GW" --to "$NOTIF" --stroke "#92400e" --sw 2 --start-arrowhead none --end-arrowhead arrow > /dev/null
$CLI --project "$P" --json element connect --from "$AUTH"  --to "$PG"    --stroke "#6d28d9" --sw 2 --start-arrowhead none --end-arrowhead arrow > /dev/null
$CLI --project "$P" --json element connect --from "$CORE"  --to "$REDIS" --stroke "#6d28d9" --sw 2 --start-arrowhead none --end-arrowhead arrow > /dev/null
$CLI --project "$P" --json element connect --from "$NOTIF" --to "$SQS"   --stroke "#92400e" --sw 2 --start-arrowhead none --end-arrowhead arrow > /dev/null

$CLI --project "$P" export png --output ./arch.png --overwrite
```

---

## 3. Sequence Diagram — JWT Authentication

![Auth Sequence](./auth-sequence.png)

### Claude prompt
```
Draw a JWT authentication sequence diagram with 4 participants: Browser, API Gateway, Auth Service, PostgreSQL. Show the full login flow: POST /auth/login (with payload annotation), verify credentials, SELECT user WHERE email=?, user row (dashed return), sign JWT RS256 (dashed return), 200 OK + Set-Cookie (dashed return).
```

### Bash script
```bash
#!/usr/bin/env bash
set -e
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
CLI="excalidraw-agent-cli"
P="/tmp/auth-sequence.excalidraw"

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

rm -f "$P"
$CLI --json project new --name "JWT Auth Flow" --output "$P" > /dev/null

add text --x 220 --y 20 --fs 20 --ff 1 --color "#111827" -t "JWT Authentication Flow" > /dev/null

# Participant headers (4 columns: x=80, 330, 580, 830)
P1=$(add rectangle --x 30  --y 55 -w 160 -h 60 --label "Browser"     --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2 --roundness)
P2=$(add rectangle --x 280 --y 55 -w 160 -h 60 --label "API Gateway" --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 --roundness)
P3=$(add rectangle --x 530 --y 55 -w 160 -h 60 --label "Auth Service" --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 --roundness)
P4=$(add rectangle --x 780 --y 55 -w 160 -h 60 --label "PostgreSQL"  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)

# Lifelines (vertical dashed lines)
for X in 110 360 610 860; do
  add line --x $X --y 115 --points "0,0 0,580" \
    --stroke "#94a3b8" --sw 1 --stroke-style dashed --roughness 0 > /dev/null
done

# Step 1: Browser → API Gateway
add arrow --x 110 --y 195 --ex 360 --ey 195 \
  --stroke "#c2410c" --sw 2 --roughness 0 --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 113 --y 178 --fs 13 --ff 2 --color "#c2410c" -t "1. POST /auth/login" > /dev/null
add text --x 113 --y 209 --fs 11 --ff 3 --color "#64748b" -t '{"email":"…", "password":"…"}' > /dev/null

# Step 2: API GW → Auth Service
add arrow --x 360 --y 285 --ex 610 --ey 285 \
  --stroke "#1e1e1e" --sw 2 --roughness 0 --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 363 --y 268 --fs 13 --ff 2 --color "#1e1e1e" -t "2. verify credentials" > /dev/null

# Step 3: Auth Service → PostgreSQL
add arrow --x 610 --y 370 --ex 860 --ey 370 \
  --stroke "#6d28d9" --sw 2 --roughness 0 --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 613 --y 353 --fs 13 --ff 2 --color "#6d28d9" -t "3. SELECT user WHERE email=?" > /dev/null

# Step 4: PostgreSQL → Auth (return, dashed)
add arrow --x 610 --y 455 --ex 860 --ey 455 \
  --stroke "#6d28d9" --sw 2 --stroke-style dashed --roughness 0 \
  --start-arrowhead arrow --end-arrowhead none > /dev/null
add text --x 640 --y 438 --fs 13 --ff 2 --color "#6d28d9" -t "4. user row" > /dev/null

# Step 5: Auth → API GW (JWT signed, dashed)
add arrow --x 360 --y 535 --ex 610 --ey 535 \
  --stroke "#15803d" --sw 2 --stroke-style dashed --roughness 0 \
  --start-arrowhead arrow --end-arrowhead none > /dev/null
add text --x 363 --y 518 --fs 13 --ff 2 --color "#15803d" -t "5. sign JWT (RS256)" > /dev/null

# Step 6: API GW → Browser (200 OK, dashed)
add arrow --x 110 --y 618 --ex 360 --ey 618 \
  --stroke "#15803d" --sw 2 --stroke-style dashed --roughness 0 \
  --start-arrowhead arrow --end-arrowhead none > /dev/null
add text --x 113 --y 601 --fs 13 --ff 2 --color "#15803d" -t "6. 200 OK + Set-Cookie: token=eyJ…" > /dev/null

$CLI --project "$P" export png --output ./auth-sequence.png --overwrite
```

---

## 4. Mind Map — excalidraw-agent-cli Features

![Mind Map](./mindmap.png)

### Claude prompt
```
Draw a left-to-right mind map for excalidraw-agent-cli. Root node (dark ellipse) on the left. Five branches fanning right: Create (rectangle / ellipse / diamond / text / arrow / line / frame), Edit (update label/position/size, move by delta, connect auto), Export (SVG vector, PNG raster, .excalidraw JSON), AI/Claude (--json flag, element IDs for chaining, REPL + subprocess), Skill (install-skill command, --global/--codebase, SKILL.md + references).
```

### Bash script
```bash
#!/usr/bin/env bash
set -e
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
CLI="excalidraw-agent-cli"
P="/tmp/mindmap.excalidraw"

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

rm -f "$P"
$CLI --json project new --name "excalidraw-agent-cli" --output "$P" > /dev/null

add text --x 10 --y 10 --fs 15 --ff 2 --color "#374151" -t "excalidraw-agent-cli" > /dev/null

# Root node (dark ellipse)
ROOT=$(add ellipse --x 30 --y 230 -w 220 -h 150 \
  --label "excalidraw-agent-cli" \
  --bg "#1e293b" --stroke "#0f172a" --fill-style solid --roughness 0 --sw 2)

# Branch nodes (y positions: 40, 140, 265, 390, 490 for 5 branches)
BRANCH_X=330; BRANCH_W=200; BRANCH_H=55
B_CREATE=$(add rectangle  --x $BRANCH_X --y 40  -w $BRANCH_W -h $BRANCH_H --label "Create"   --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2 --roundness)
B_EDIT=$(add rectangle    --x $BRANCH_X --y 140 -w $BRANCH_W -h $BRANCH_H --label "Edit"     --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 --roundness)
B_EXPORT=$(add rectangle  --x $BRANCH_X --y 265 -w $BRANCH_W -h $BRANCH_H --label "Export"   --bg "#fef08a" --stroke "#854d0e" --fill-style solid --roughness 0 --sw 2 --roundness)
B_AI=$(add rectangle      --x $BRANCH_X --y 390 -w $BRANCH_W -h $BRANCH_H --label "AI / Claude" --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2 --roundness)
B_SKILL=$(add rectangle   --x $BRANCH_X --y 490 -w $BRANCH_W -h $BRANCH_H --label "Skill"    --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)

# Connector arrows
for B in "$B_CREATE" "$B_EDIT" "$B_EXPORT" "$B_AI" "$B_SKILL"; do
  $CLI --project "$P" --json element connect --from "$ROOT" --to "$B" \
    --stroke "#94a3b8" --sw 1 --start-arrowhead none --end-arrowhead arrow > /dev/null
done

# Annotation text (right of each branch)
ANN_X=545
add text --x $ANN_X --y 43  --fs 12 --ff 2 --color "#1e40af" -t "rectangle / ellipse / diamond" > /dev/null
add text --x $ANN_X --y 58  --fs 12 --ff 2 --color "#1e40af" -t "text / arrow / line / frame" > /dev/null
add text --x $ANN_X --y 143 --fs 12 --ff 2 --color "#15803d" -t "update label / position / size" > /dev/null
add text --x $ANN_X --y 158 --fs 12 --ff 2 --color "#15803d" -t "move by delta (--dx --dy)" > /dev/null
add text --x $ANN_X --y 173 --fs 12 --ff 2 --color "#15803d" -t "connect (auto-positioned)" > /dev/null
add text --x $ANN_X --y 268 --fs 12 --ff 2 --color "#854d0e" -t "SVG (vector, scalable)" > /dev/null
add text --x $ANN_X --y 283 --fs 12 --ff 2 --color "#854d0e" -t "PNG (raster, viewable)" > /dev/null
add text --x $ANN_X --y 298 --fs 12 --ff 2 --color "#854d0e" -t ".excalidraw (JSON, raw)" > /dev/null
add text --x $ANN_X --y 393 --fs 12 --ff 2 --color "#c2410c" -t "--json flag on every cmd" > /dev/null
add text --x $ANN_X --y 408 --fs 12 --ff 2 --color "#c2410c" -t "element IDs for chaining" > /dev/null
add text --x $ANN_X --y 423 --fs 12 --ff 2 --color "#c2410c" -t "REPL + subprocess modes" > /dev/null
add text --x $ANN_X --y 493 --fs 12 --ff 2 --color "#6d28d9" -t "install-skill command" > /dev/null
add text --x $ANN_X --y 508 --fs 12 --ff 2 --color "#6d28d9" -t "--global / --codebase" > /dev/null
add text --x $ANN_X --y 523 --fs 12 --ff 2 --color "#6d28d9" -t "SKILL.md + references/" > /dev/null

$CLI --project "$P" export png --output ./mindmap.png --overwrite
```

---

## 5. CI/CD Pipeline — Cycle with Fail Path

![CI/CD Pipeline](./cicd.png)

### Claude prompt
```
Draw a CI/CD pipeline as a cycle: 2×3 grid with Code→Build→Test (top row) and Plan←Monitor←Deploy (bottom row), connected as a clockwise cycle. Add a red dashed "fail" path from Test back to Code that goes around the outside of the diagram. Label "pass" near Deploy and "feedback" near Plan.
```

### Bash script
```bash
#!/usr/bin/env bash
set -e
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
CLI="excalidraw-agent-cli"
P="/tmp/cicd.excalidraw"

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

rm -f "$P"
$CLI --json project new --name "CI/CD Pipeline" --output "$P" > /dev/null

add text --x 285 --y 18 --fs 22 --ff 1 --color "#111827" -t "CI/CD Pipeline" > /dev/null

CODE=$(add rectangle    --x 160 --y 90  -w 170 -h 70 --label "Code"    --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2 --roundness)
BUILD=$(add rectangle   --x 390 --y 90  -w 170 -h 70 --label "Build"   --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 --roundness)
TEST=$(add rectangle    --x 620 --y 90  -w 170 -h 70 --label "Test"    --bg "#fef08a" --stroke "#854d0e" --fill-style solid --roughness 0 --sw 2 --roundness)
PLAN=$(add rectangle    --x 160 --y 270 -w 170 -h 70 --label "Plan"    --bg "#e0e7ff" --stroke "#4338ca" --fill-style solid --roughness 0 --sw 2 --roundness)
MONITOR=$(add rectangle --x 390 --y 270 -w 170 -h 70 --label "Monitor" --bg "#fce7f3" --stroke "#be185d" --fill-style solid --roughness 0 --sw 2 --roundness)
DEPLOY=$(add rectangle  --x 620 --y 270 -w 170 -h 70 --label "Deploy"  --bg "#d1fae5" --stroke "#047857" --fill-style solid --roughness 0 --sw 2 --roundness)

add text --x 618 --y 348 --fs 12 --ff 2 --color "#047857" -t "pass" > /dev/null
add text --x 163 --y 348 --fs 12 --ff 2 --color "#4338ca" -t "feedback" > /dev/null

# Main cycle (element connect handles routing cleanly)
for PAIR in "$CODE $BUILD" "$BUILD $TEST" "$TEST $DEPLOY" "$DEPLOY $MONITOR" "$MONITOR $PLAN" "$PLAN $CODE"; do
  FROM=$(echo $PAIR | cut -d' ' -f1)
  TO=$(echo $PAIR   | cut -d' ' -f2)
  $CLI --project "$P" --json element connect --from "$FROM" --to "$TO" \
    --start-arrowhead none --end-arrowhead arrow --sw 2 --roughness 0 > /dev/null
done

# Fail path: three segments around the outside
add line --x 705 --y 160 --points "0,0 0,225" \
  --stroke "#dc2626" --sw 2 --stroke-style dashed --roughness 0 > /dev/null
add line --x 115 --y 385 --points "0,0 590,0" \
  --stroke "#dc2626" --sw 2 --stroke-style dashed --roughness 0 > /dev/null
add line --x 115 --y 125 --points "0,0 0,260" \
  --stroke "#dc2626" --sw 2 --stroke-style dashed --roughness 0 > /dev/null
add arrow --x 115 --y 125 --ex 158 --ey 125 \
  --stroke "#dc2626" --sw 2 --roughness 0 \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 430 --y 393 --fs 13 --ff 2 --color "#dc2626" -t "fail" > /dev/null

$CLI --project "$P" export png --output ./cicd.png --overwrite
```

---

## 6. ETL Data Pipeline — Zone Swim Lanes

![Data Pipeline](./data-pipeline.png)

### Claude prompt
```
Draw an ETL data pipeline with three vertical zone columns: SOURCES (MySQL DB, Kafka Stream, S3 Raw Files), TRANSFORM (Ingest/Validate → Enrich/Join → Aggregate), DESTINATIONS (Snowflake DWH, Elasticsearch, S3 Parquet). Color each source distinctly. Show arrows from each source to appropriate transform stage, and from each transform to appropriate destination.
```

### Bash script
```bash
#!/usr/bin/env bash
set -e
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
CLI="excalidraw-agent-cli"
P="/tmp/data-pipeline.excalidraw"

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("--stroke" "$3")
  [[ -n "$4" ]] && args+=("--stroke-style" "$4")
  $CLI --project "$P" --json element connect "${args[@]}" \
    --start-arrowhead none --end-arrowhead arrow --sw 2 > /dev/null
}

rm -f "$P"
$CLI --json project new --name "ETL Data Pipeline" --output "$P" > /dev/null

add text --x 230 --y 18 --fs 20 --ff 1 --color "#111827" -t "ETL Data Pipeline" > /dev/null

# Zone backgrounds
add rectangle --x 20  --y 45 -w 220 -h 390 \
  --bg "#bfdbfe" --stroke "#93c5fd" --fill-style solid --opacity 30 --sw 1 --roughness 0 > /dev/null
add text --x 28 --y 53 --fs 13 --ff 2 --color "#1e40af" -t "SOURCES" > /dev/null

add rectangle --x 255 --y 45 -w 240 -h 390 \
  --bg "#bbf7d0" --stroke "#86efac" --fill-style solid --opacity 35 --sw 1 --roughness 0 > /dev/null
add text --x 263 --y 53 --fs 13 --ff 2 --color "#15803d" -t "TRANSFORM" > /dev/null

add rectangle --x 510 --y 45 -w 220 -h 390 \
  --bg "#ddd6fe" --stroke "#c4b5fd" --fill-style solid --opacity 30 --sw 1 --roughness 0 > /dev/null
add text --x 518 --y 53 --fs 13 --ff 2 --color "#5b21b6" -t "DESTINATIONS" > /dev/null

# Sources
MYSQL=$(add rectangle  --x 35  --y 80  -w 190 -h 70 --label "MySQL DB"     --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2 --roundness)
KAFKA=$(add rectangle  --x 35  --y 200 -w 190 -h 70 --label "Kafka Stream" --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 2 --roundness)
S3IN=$(add rectangle   --x 35  --y 320 -w 190 -h 70 --label "S3 Raw Files" --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)

# Transform stages
INGEST=$(add rectangle --x 265 --y 80  -w 220 -h 70 --label "Ingest / Validate" --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 --roundness)
ENRICH=$(add rectangle --x 265 --y 200 -w 220 -h 70 --label "Enrich / Join"     --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 --roundness)
AGGR=$(add rectangle   --x 265 --y 320 -w 220 -h 70 --label "Aggregate"         --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2 --roundness)

# Destinations
SNOW=$(add rectangle   --x 520 --y 80  -w 200 -h 70 --label "Snowflake DWH" --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)
ES=$(add rectangle     --x 520 --y 200 -w 200 -h 70 --label "Elasticsearch" --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)
S3OUT=$(add rectangle  --x 520 --y 320 -w 200 -h 70 --label "S3 Parquet"   --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)

# Source → Transform
conn "$MYSQL" "$INGEST" "#1e40af"
conn "$KAFKA" "$INGEST" "#92400e"
conn "$S3IN"  "$INGEST" "#6d28d9"
# Transform chain
conn "$INGEST" "$ENRICH" "#15803d"
conn "$ENRICH" "$AGGR"   "#15803d"
# Transform → Destinations
conn "$INGEST" "$SNOW"  "#6d28d9"
conn "$ENRICH" "$ES"    "#6d28d9"
conn "$AGGR"   "$S3OUT" "#6d28d9"

$CLI --project "$P" export png --output ./data-pipeline.png --overwrite
```

---

## 7. Microservices Architecture — Three Zones

![Microservices](./microservices.png)

### Claude prompt
```
Draw a microservices architecture diagram with three vertical zones: EDGE (CloudFront CDN → API Gateway), SERVICES (Auth, User, Order, Payment, Notif services — all connected from API Gateway), DATA/EXTERNAL (Auth Cache Redis, Users DB, Orders DB, Stripe API, EventBus SNS). Add service-to-data connections. Show the event flow: Order Service publishes "OrderPlaced" to EventBus SNS, and EventBus SNS triggers Notif Service with a dashed reverse arrow.
```

### Bash script
```bash
#!/usr/bin/env bash
set -e
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
CLI="excalidraw-agent-cli"
P="/tmp/microservices.excalidraw"

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("-l" "$3")
  [[ -n "$4" ]] && args+=("--stroke" "$4")
  [[ -n "$5" ]] && args+=("--stroke-style" "$5")
  $CLI --project "$P" --json element connect "${args[@]}" \
    --start-arrowhead none --end-arrowhead arrow > /dev/null
}

rm -f "$P"
$CLI --json project new --name "Microservices Architecture" --output "$P" > /dev/null

add text --x 250 --y 18 --fs 22 --ff 1 --color "#111827" -t "Microservices Architecture" > /dev/null

# Zone backgrounds
add rectangle --x 20  --y 50 -w 250 -h 600 --bg "#fed7aa" --stroke "#ea580c" --fill-style solid --opacity 25 --sw 1 --roughness 0 > /dev/null
add text --x 28 --y 58 --fs 13 --ff 2 --color "#9a3412" -t "EDGE" > /dev/null
add rectangle --x 285 --y 50 -w 260 -h 600 --bg "#99f6e4" --stroke "#0d9488" --fill-style solid --opacity 30 --sw 1 --roughness 0 > /dev/null
add text --x 293 --y 58 --fs 13 --ff 2 --color "#0f766e" -t "SERVICES" > /dev/null
add rectangle --x 560 --y 50 -w 320 -h 600 --bg "#ddd6fe" --stroke "#7c3aed" --fill-style solid --opacity 30 --sw 1 --roughness 0 > /dev/null
add text --x 568 --y 58 --fs 13 --ff 2 --color "#5b21b6" -t "DATA / EXTERNAL" > /dev/null

# Nodes
CDN=$(add rectangle     --x 30 --y 88  -w 210 -h 62 --label "CloudFront CDN"      --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2 --roundness)
GW=$(add rectangle      --x 30 --y 305 -w 210 -h 62 --label "API Gateway"         --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2 --roundness)
AUTH=$(add rectangle    --x 295 --y 88  -w 220 -h 62 --label "Auth Service"        --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2 --roundness)
USER=$(add rectangle    --x 295 --y 188 -w 220 -h 62 --label "User Service"        --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2 --roundness)
ORDER=$(add rectangle   --x 295 --y 305 -w 220 -h 62 --label "Order Service"       --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2 --roundness)
PAYMENT=$(add rectangle --x 295 --y 405 -w 220 -h 62 --label "Payment Service"     --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2 --roundness)
NOTIF=$(add rectangle   --x 295 --y 505 -w 220 -h 62 --label "Notif Service"       --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2 --roundness)
ACACHE=$(add rectangle  --x 570 --y 88  -w 220 -h 62 --label "Auth Cache (Redis)"  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)
USERSDB=$(add rectangle --x 570 --y 188 -w 220 -h 62 --label "Users DB (Postgres)" --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)
ORDERSDB=$(add rectangle --x 570 --y 305 -w 220 -h 62 --label "Orders DB (Postgres)" --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2 --roundness)
STRIPE=$(add rectangle  --x 570 --y 405 -w 220 -h 62 --label "Stripe API"          --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2 --roundness)
EVENTBUS=$(add rectangle --x 570 --y 505 -w 220 -h 62 --label "EventBus SNS"       --bg "#fef08a" --stroke "#854d0e" --fill-style solid --roughness 0 --sw 2 --roundness)

# Connections
conn "$CDN"     "$GW"
conn "$GW"      "$AUTH"
conn "$GW"      "$USER"
conn "$GW"      "$ORDER"
conn "$GW"      "$PAYMENT"
conn "$GW"      "$NOTIF"
conn "$AUTH"    "$ACACHE"   ""          "#6d28d9"
conn "$USER"    "$USERSDB"  ""          "#6d28d9"
conn "$ORDER"   "$ORDERSDB" ""          "#6d28d9" "dashed"
conn "$PAYMENT" "$STRIPE"   "charge"   "#c2410c"

# Event flow: Order → EventBus (diagonal, explicit coords)
$CLI --project "$P" --json element add arrow \
  --x 515 --y 336 --ex 570 --ey 536 \
  --stroke "#92400e" --sw 2 --stroke-style dashed --roughness 0 \
  --start-arrowhead none --end-arrowhead arrow -l "OrderPlaced" > /dev/null

# EventBus → Notif (reverse horizontal, explicit coords)
$CLI --project "$P" --json element add arrow \
  --x 570 --y 545 --ex 515 --ey 545 \
  --stroke "#7c3aed" --sw 2 --stroke-style dashed --roughness 0 \
  --start-arrowhead none --end-arrowhead arrow -l "triggers" > /dev/null

$CLI --project "$P" export png --output ./microservices.png --overwrite
```

---

## Usage

Replace `/path/to/.venv/bin` and `/path/to/node/bin` with the actual paths on your system:

```bash
# Find CLI path
which excalidraw-agent-cli

# Find Node path
which node
```

Or use the fully-qualified paths if not on `$PATH`:
```bash
CLI="/path/to/.venv/bin/excalidraw-agent-cli"
export PATH="/path/to/.venv/bin:/path/to/node/bin:$PATH"
```
