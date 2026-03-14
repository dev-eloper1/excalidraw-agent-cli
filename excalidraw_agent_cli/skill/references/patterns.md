# Visual Pattern Library

CLI examples for each visual pattern. Every pattern also shows the corresponding `conn()` calls.
Colors come from `color-palette.md`.

---

## Fan-Out (One-to-Many)

One central node fans out to multiple targets. Use for: API gateways dispatching to services, a parent spawning children, a hub routing to types.

```
     ○ Service A
    ↗
□ → ○ Service B
    ↘
     ○ Service C
```

```bash
GW=$(add rectangle --x 200 --y 340 -w 200 -h 80 --label "API Gateway" \
  --bg "#bbf7d0" --stroke "#15803d")
SVC_A=$(add rectangle --x 500 --y 200 -w 180 -h 72 --label "Auth Service" \
  --bg "#86efac" --stroke "#15803d")
SVC_B=$(add rectangle --x 500 --y 320 -w 180 -h 72 --label "Core API" \
  --bg "#86efac" --stroke "#15803d")
SVC_C=$(add rectangle --x 500 --y 440 -w 180 -h 72 --label "Billing" \
  --bg "#86efac" --stroke "#15803d")

conn "$GW" "$SVC_A" "" "#15803d"
conn "$GW" "$SVC_B" "" "#15803d"
conn "$GW" "$SVC_C" "" "#15803d"
```

**Hub centering rule**: Center the hub over its targets.
```
hub_x = (leftmost_target_center + rightmost_target_center) / 2 - hub_width / 2
```

---

## Convergence (Many-to-One)

Multiple sources merge into a single destination. Use for: aggregation, funnels, log collectors.

```
  ○ ↘
  ○ → □
  ○ ↗
```

```bash
LOG1=$(add rectangle --x 200 --y 200 -w 160 -h 70 --label "Auth Service" \
  --bg "#86efac" --stroke "#15803d")
LOG2=$(add rectangle --x 200 --y 310 -w 160 -h 70 --label "Core API" \
  --bg "#86efac" --stroke "#15803d")
LOG3=$(add rectangle --x 200 --y 420 -w 160 -h 70 --label "Billing" \
  --bg "#86efac" --stroke "#15803d")
AGG=$(add rectangle  --x 480 --y 310 -w 180 -h 70 --label "Log Aggregator" \
  --bg "#fecdd3" --stroke "#be123c")

conn "$LOG1" "$AGG" "logs" "#be123c" "dashed"
conn "$LOG2" "$AGG" "logs" "#be123c" "dashed"
conn "$LOG3" "$AGG" "logs" "#be123c" "dashed"
```

---

## Swim Lanes (Horizontal Layered Architecture)

Horizontal bands for each layer. Best for 4+ layer architectures. Each band has a semi-transparent zone background added before the nodes.

```
y=200:  [Client A]  [Client B]  [Client C]        ← CLIENT zone (blue)
y=350:  [──────── API Gateway ────────]            ← SERVICE zone (green)
y=500:  [DB]  [Cache]  [Search]                   ← DATA zone (purple)
```

```bash
# Step 1: Zone backgrounds first
add rectangle --x 185 --y 155 -w 820 -h 140 \
  --bg "#dbeafe" --stroke "#93c5fd" --fill-style solid --opacity 15 --sw 1 > /dev/null
add rectangle --x 185 --y 315 -w 820 -h 140 \
  --bg "#dcfce7" --stroke "#86efac" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 185 --y 475 -w 820 -h 140 \
  --bg "#ede9fe" --stroke "#c4b5fd" --fill-style solid --opacity 20 --sw 1 > /dev/null

# Step 2: Zone labels
add text --x 195 --y 163 --fs 14 --ff 2 --color "#1e40af" -t "CLIENTS"  > /dev/null
add text --x 195 --y 323 --fs 14 --ff 2 --color "#15803d" -t "SERVICES" > /dev/null
add text --x 195 --y 483 --fs 14 --ff 2 --color "#6d28d9" -t "DATA"     > /dev/null

# Step 3: Nodes
WEB=$(    add rectangle --x 205 --y 195 -w 160 -h 72 --label "Web App"    --bg "#bfdbfe" --stroke "#1e40af")
MOBILE=$( add rectangle --x 415 --y 195 -w 160 -h 72 --label "Mobile App" --bg "#bfdbfe" --stroke "#1e40af")
GW=$(     add rectangle --x 205 --y 355 -w 575 -h 72 --label "API Gateway" --bg "#86efac" --stroke "#15803d")
DB=$(     add rectangle --x 205 --y 515 -w 160 -h 72 --label "PostgreSQL"  --bg "#ddd6fe" --stroke "#6d28d9")
CACHE=$(  add rectangle --x 415 --y 515 -w 160 -h 72 --label "Redis"       --bg "#ddd6fe" --stroke "#6d28d9")
```

---

## Timeline (Sequence / Protocol)

A vertical or horizontal line with dot markers at each step. Use for: event sequences, protocols, step-by-step processes.

```
  ● ─── Event 1
  │
  ● ─── Event 2
  │
  ● ─── Event 3
```

```bash
# Vertical timeline spine
add line --x 300 --y 200 --points "0,0 0,400" \
  --stroke "#64748b" --sw 2 > /dev/null

# Dot markers (small ellipses at each step)
add ellipse --x 294 --y 200 -w 12 -h 12 \
  --bg "#3b82f6" --stroke "#1e40af" --fill-style solid --roughness 0 > /dev/null
add ellipse --x 294 --y 330 -w 12 -h 12 \
  --bg "#3b82f6" --stroke "#1e40af" --fill-style solid --roughness 0 > /dev/null
add ellipse --x 294 --y 460 -w 12 -h 12 \
  --bg "#3b82f6" --stroke "#1e40af" --fill-style solid --roughness 0 > /dev/null

# Free-floating labels beside each dot
add text --x 320 --y 193 --fs 14 --ff 2 --color "#1e293b" -t "RUN_STARTED"    > /dev/null
add text --x 320 --y 323 --fs 14 --ff 2 --color "#1e293b" -t "STATE_DELTA"    > /dev/null
add text --x 320 --y 453 --fs 14 --ff 2 --color "#1e293b" -t "RUN_FINISHED"   > /dev/null

# Optional: detail text beneath each label
add text --x 320 --y 213 --fs 12 --ff 3 --color "#6b7280" -t '{"runId": "abc"}' > /dev/null
```

---

## Hub-and-Spoke (Type System / Taxonomy)

One central hub node with N spoke nodes radiating around it. Use for: element type systems, categories, options.

**Arrow style rule** (Rule 15):
- Hub → spoke (type fan-out): `--stroke "#94a3b8" --stroke-style dotted --sw 1` (thin gray dotted)
- Cross-connections: `--stroke "#3b82f6" --stroke-style dashed --sw 2` (colored dashed)

```bash
HUB=$(add rectangle --x 640 --y 415 -w 160 -h 78 --label "Base Element" \
  --bg "#e2e8f0" --stroke "#334155" --fill-style solid --roughness 0 --sw 3)

# Spokes in a ring around the hub
RECT=$(    add rectangle --x 330 --y 200 -w 155 -h 72 --label "rectangle" --bg "#bfdbfe" --stroke "#1e40af")
ELLIPSE=$( add ellipse   --x 590 --y 200 -w 140 -h 72 --label "ellipse"   --bg "#bfdbfe" --stroke "#1e40af")
DIAMOND=$( add diamond   --x 860 --y 195 -w 145 -h 90 --label "diamond"   --bg "#bfdbfe" --stroke "#1e40af")
TARROW=$(  add rectangle --x 1000 --y 415 -w 120 -h 70 --label "arrow"    --bg "#fed7aa" --stroke "#c2410c")
TTEXT=$(   add rectangle --x 330  --y 430 -w 120 -h 70 --label "text"     --bg "#bbf7d0" --stroke "#15803d")

# All spokes: dotted gray, thin
for SPOKE in "$RECT" "$ELLIPSE" "$DIAMOND" "$TARROW" "$TTEXT"; do
  $CLI --project "$P" --json element connect \
    --from "$HUB" --to "$SPOKE" \
    --stroke "#94a3b8" --stroke-style dotted --sw 1 > /dev/null
done
```

---

## Cycle (Feedback Loop)

Elements in sequence with an arrow returning to the start. Use for: CI/CD loops, iterative refinement, retry logic.

```bash
PLAN=$(  add rectangle --x 350 --y 200 -w 160 -h 72 --label "Plan"    --bg "#bfdbfe" --stroke "#1e40af")
BUILD=$( add rectangle --x 600 --y 350 -w 160 -h 72 --label "Build"   --bg "#86efac" --stroke "#15803d")
DEPLOY=$(add rectangle --x 350 --y 500 -w 160 -h 72 --label "Deploy"  --bg "#fef08a" --stroke "#a16207")
OBSERVE=$(add rectangle --x 100 --y 350 -w 160 -h 72 --label "Observe" --bg "#fecdd3" --stroke "#be123c")

conn "$PLAN"   "$BUILD"   ""        "#1e1e1e"
conn "$BUILD"  "$DEPLOY"  ""        "#1e1e1e"
conn "$DEPLOY" "$OBSERVE" ""        "#1e1e1e"
conn "$OBSERVE" "$PLAN"  "feedback" "#be123c" "dashed"
```

---

## Assembly Line (Transformation)

Input → process → output with clear before/after. Use for: data pipelines, ETL, build systems.

```bash
INPUT=$(  add ellipse   --x 200 --y 300 -w 160 -h 72 --label "Raw Data"    --bg "#bfdbfe" --stroke "#1e40af")
PROCESS=$(add rectangle --x 450 --y 300 -w 200 -h 72 --label "Transform"   --bg "#86efac" --stroke "#15803d")
OUTPUT=$( add ellipse   --x 750 --y 300 -w 160 -h 72 --label "Clean Data"  --bg "#a7f3d0" --stroke "#047857")

conn "$INPUT"   "$PROCESS" "raw"       "#1e40af"
conn "$PROCESS" "$OUTPUT"  "validated" "#047857"

# Optional: show before/after data as evidence artifacts
add rectangle --x 200 --y 400 -w 160 -h 90 \
  --bg "#1e293b" --stroke "#334155" --fill-style solid --roughness 0 > /dev/null
add text --x 210 --y 410 --fs 12 --ff 3 --color "#94a3b8" -t '{ "date": "03/14",' > /dev/null
add text --x 210 --y 428 --fs 12 --ff 3 --color "#94a3b8" -t '  "val": "12.3x" }' > /dev/null

add rectangle --x 750 --y 400 -w 160 -h 90 \
  --bg "#1e293b" --stroke "#334155" --fill-style solid --roughness 0 > /dev/null
add text --x 760 --y 410 --fs 12 --ff 3 --color "#22c55e" -t '{ "date": "2026-03-14",' > /dev/null
add text --x 760 --y 428 --fs 12 --ff 3 --color "#22c55e" -t '  "value": 12.3 }' > /dev/null
```

---

## Evidence Artifacts

Use to show what things actually look like — not just what they're called.

### Code snippet panel

```bash
# Dark background panel
CODE_BG=$(add rectangle --x 900 --y 300 -w 290 -h 150 \
  --bg "#1e293b" --stroke "#334155" --fill-style solid --roughness 0 --sw 1)

# Header label above the panel
add text --x 900 --y 283 --fs 13 --ff 2 --color "#64748b" -t "SDK usage" > /dev/null

# Code lines inside (monospace, colored)
add text --x 912 --y 312 --fs 12 --ff 3 --color "#e2e8f0" -t "import excalidraw_agent_cli" > /dev/null
add text --x 912 --y 330 --fs 12 --ff 3 --color "#e2e8f0" -t "from cli import main" > /dev/null
add text --x 912 --y 360 --fs 12 --ff 3 --color "#94a3b8" -t "# create project" > /dev/null
add text --x 912 --y 378 --fs 12 --ff 3 --color "#22c55e" -t 'main(["project", "new"])' > /dev/null
```

### JSON payload panel

```bash
JSON_BG=$(add rectangle --x 900 --y 480 -w 290 -h 110 \
  --bg "#1e293b" --stroke "#334155" --fill-style solid --roughness 0 --sw 1)
add text --x 912 --y 492 --fs 12 --ff 3 --color "#22c55e" -t '{ "type": "rectangle",' > /dev/null
add text --x 912 --y 510 --fs 12 --ff 3 --color "#22c55e" -t '  "id": "elem_abc",' > /dev/null
add text --x 912 --y 528 --fs 12 --ff 3 --color "#22c55e" -t '  "x": 200, "y": 200,' > /dev/null
add text --x 912 --y 546 --fs 12 --ff 3 --color "#22c55e" -t '  "label": "My Node" }' > /dev/null
```

---

## Bidirectional Arrow

```bash
$CLI --project "$P" --json element connect \
  --from "$A" --to "$B" \
  -l "read / write" \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead arrow --end-arrowhead arrow > /dev/null
```

---

## Mixed Roughness (Live vs Planned)

```bash
# Live / stable component
add rectangle ... --roughness 0 --fill-style solid

# Planned / future component
add rectangle ... --roughness 2 --fill-style hachure --opacity 70
```
