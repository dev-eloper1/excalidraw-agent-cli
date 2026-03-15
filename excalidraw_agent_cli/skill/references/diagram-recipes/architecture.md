# Architecture Diagram Recipe

## When to use

Use a layered architecture diagram when you need to communicate **how system components are organized into tiers** — clients, gateways, services, data stores. The key signal is a clear separation of concerns across horizontal layers, and arrows that primarily flow top-to-bottom between layers.

Choose this pattern when:
- You have 3–5 distinct tiers (client, edge, services, data, external)
- Components within a tier are peers (e.g., multiple microservices)
- The narrative is "how requests flow through the system"
- Stakeholders need to understand zone boundaries (security perimeters, network segments)

Do NOT use for: time-phased plans (use Gantt), decision logic (use flowchart), or message sequences (use sequence diagram).

---

## Layout template

```
Canvas: 1200 × 800px, origin top-left (0, 0)

Zone layout (4 horizontal bands):

  Client layer:          x=20, y=100, w=1160, h=120
  Gateway/Security layer: x=20, y=240, w=1160, h=120
  Service layer:          x=20, y=380, w=1160, h=160
  Data layer:             x=20, y=560, w=1160, h=120

  CRITICAL: All zone backgrounds must be drawn BEFORE any nodes.
  CRITICAL: Title at y=15 (baseline ≈ y=37). First zone starts at y=100.
            Clearance = 100 - 37 = 63px ≥ 60px minimum (satisfies Rule 21).

Zone labels: x=30, y = zone_top + 10, --fs 14 --ff 2

Node geometry:
  Standard node: w=160, h=70
  Spacing: 200px center-to-center horizontally

Node centering within canvas (1200px wide):
  n nodes → total_span = n * 160 + (n-1) * 40 (40px gaps)
  start_x = (1160 - total_span) / 2 + 20

Node vertical centering within zone:
  node_y = zone_top + (zone_h - node_h) / 2
  (e.g., Client zone: node_y = 100 + (120 - 70) / 2 = 125)

Node column x values (200px apart, for up to 6 nodes centered):
  2 nodes: x = 420, 620
  3 nodes: x = 320, 520, 720
  4 nodes: x = 220, 420, 620, 820
  5 nodes: x = 220, 420, 620, 820, 1020
  6 nodes: x = 220, 390, 560, 730, 900, 1020   (tighten to 170px for 6)
```

**Zone background order (draw in this exact sequence):**
1. Client zone background
2. Gateway zone background
3. Service zone background
4. Data zone background
5. Zone labels
6. Client nodes
7. Gateway nodes
8. Service nodes
9. Data nodes
10. Arrows (element connect)

---

## Color and style defaults

### Zone backgrounds

| Zone | `--bg` | `--stroke` | `--opacity` |
|------|--------|------------|-------------|
| Client layer | `#dbeafe` | `#93c5fd` | `30` |
| Gateway/Security layer | `#ffedd5` | `#fdba74` | `35` |
| Service layer | `#dcfce7` | `#86efac` | `35` |
| Data layer | `#ede9fe` | `#c4b5fd` | `35` |

Zone background style: `--fill-style solid --sw 1`

### Node fills

| Node type | `--bg` | `--stroke` |
|-----------|--------|------------|
| Client (browser, mobile) | `#bfdbfe` | `#1e40af` |
| API Gateway / Load Balancer | `#bbf7d0` | `#15803d` |
| Auth / Security service | `#fed7aa` | `#c2410c` |
| Application service | `#86efac` | `#15803d` |
| Async queue / message broker | `#fef08a` | `#92400e` |
| Database (SQL/NoSQL) | `#ddd6fe` | `#6d28d9` |
| Cache (Redis, Memcached) | `#fef08a` | `#92400e` |
| External / third-party | `#fed7aa` | `#c2410c` |

Node style: `--fill-style solid --roughness 0 --sw 2`

### Zone label colors

| Zone | `--color` |
|------|-----------|
| Client layer | `#1e40af` |
| Gateway/Security layer | `#c2410c` |
| Service layer | `#15803d` |
| Data layer | `#6d28d9` |

### Arrow colors

| Relationship | `--stroke` | `--stroke-style` |
|-------------|-----------|-----------------|
| Primary request flow | `#1e1e1e` | `solid` |
| Auth / security check | `#c2410c` | `solid` |
| Async event / queue | `#a16207` | `dashed` |
| Data read/write | `#6d28d9` | `solid` |
| External API call | `#0891b2` | `dashed` |

Arrow width: `--sw 2` for primary flows, `--sw 1` for secondary/async.

---

## Common pitfalls

1. **Zone backgrounds added after nodes.** Excalidraw renders in insertion order. If you add a zone background after the nodes inside it, the background will paint on top and hide the nodes. Always follow the strict draw order: all zone backgrounds first, then all nodes, then arrows. See Rule 6.

2. **Title overlap with first zone.** Title baseline is approximately `y_title + font_size`. With `--y 15 --fs 20`, baseline ≈ 37. First zone at y=100 gives 63px clearance, which satisfies Rule 21's 60px minimum. Do not push the title below y=15 or the first zone above y=100.

3. **Async/cache nodes with amber stroke.** `--bg "#fef08a"` with `--stroke "#a16207"` produces muddy yellow text. Use `--stroke "#92400e"` (dark amber-brown) for all yellow-fill nodes. See Rule 22 and color-palette.md Text Contrast Rules.

4. **Too many nodes in a zone causing overflow.** The service layer is 1160px wide. At w=160 per node with 40px gaps, you can fit a maximum of 5–6 nodes. For 7+ services, either reduce node width to 140px or split into a sub-layer.

5. **Arrows crossing multiple zones diagonally.** Route through intermediate gateway nodes instead of drawing a direct diagonal from client to data. See Rule 12.

6. **Zone label sitting inside a node.** Zone labels use `y = zone_top + 10`. Nodes start at `zone_top + 25` or later. If a zone label and a node overlap, increase the gap by starting nodes lower (`node_y = zone_top + 35`).

7. **Forgetting `> /dev/null` on zone backgrounds.** Zone background IDs are never referenced by `conn`. Always suppress their output to keep the script clean and prevent ID variable pollution.

---

## Worked example

**Scenario:** Microservices system — API Gateway, Auth Service, Order Service, Inventory Service, Notification Service, Postgres, Redis

**Zone assignments:**
- Client layer: Web App, Mobile App
- Gateway layer: API Gateway
- Service layer: Auth Service, Order Service, Inventory Service, Notification Service
- Data layer: Postgres, Redis

**Node x positions (centered in 1200px canvas):**
```
Client (2 nodes):   Web App x=420, Mobile App x=620
Gateway (1 node):   API Gateway x=520
Service (4 nodes):  Auth x=220, Order x=420, Inventory x=620, Notification x=820
Data (2 nodes):     Postgres x=420, Redis x=620
```

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"
CLI=$(which excalidraw-agent-cli)
P=/tmp/arch-worked-example.excalidraw

add() { $CLI -p "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local from="$1" to="$2" label="$3" color="$4" style="$5"
  local args=("--from" "$from" "--to" "$to")
  [[ -n "$label" ]] && args+=("-l" "$label")
  [[ -n "$color" ]] && args+=("--stroke" "$color")
  [[ -n "$style" ]] && args+=("--stroke-style" "$style")
  $CLI -p "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "arch-worked-example" --output "$P" > /dev/null

# Title
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "Microservices Architecture" > /dev/null

# ── Zone backgrounds FIRST ──────────────────────────────────────────────────
add rectangle --x 20 --y 100 -w 1160 -h 120 \
  --bg "#dbeafe" --stroke "#93c5fd" --fill-style solid --opacity 30 --sw 1 > /dev/null
add rectangle --x 20 --y 240 -w 1160 -h 120 \
  --bg "#ffedd5" --stroke "#fdba74" --fill-style solid --opacity 35 --sw 1 > /dev/null
add rectangle --x 20 --y 380 -w 1160 -h 160 \
  --bg "#dcfce7" --stroke "#86efac" --fill-style solid --opacity 35 --sw 1 > /dev/null
add rectangle --x 20 --y 560 -w 1160 -h 120 \
  --bg "#ede9fe" --stroke "#c4b5fd" --fill-style solid --opacity 35 --sw 1 > /dev/null

# Zone labels
add text --x 30 --y 110 --fs 14 --ff 2 --color "#1e40af"  -t "CLIENT LAYER"   > /dev/null
add text --x 30 --y 250 --fs 14 --ff 2 --color "#c2410c"  -t "GATEWAY / SECURITY" > /dev/null
add text --x 30 --y 390 --fs 14 --ff 2 --color "#15803d"  -t "SERVICES"       > /dev/null
add text --x 30 --y 570 --fs 14 --ff 2 --color "#6d28d9"  -t "DATA"           > /dev/null

# ── Client layer nodes ──────────────────────────────────────────────────────
WEB=$(    add rectangle --x 420 --y 125 -w 160 -h 70 \
  --label "Web App"    --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)
MOBILE=$( add rectangle --x 620 --y 125 -w 160 -h 70 \
  --label "Mobile App" --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# ── Gateway layer nodes ─────────────────────────────────────────────────────
GW=$(     add rectangle --x 470 --y 265 -w 260 -h 70 \
  --label "API Gateway" --bg "#bbf7d0" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# ── Service layer nodes ─────────────────────────────────────────────────────
AUTH=$(   add rectangle --x 220 --y 415 -w 160 -h 70 \
  --label "Auth Service"        --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)
ORDER=$(  add rectangle --x 420 --y 415 -w 160 -h 70 \
  --label "Order Service"       --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
INV=$(    add rectangle --x 620 --y 415 -w 170 -h 70 \
  --label "Inventory Service"   --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
NOTIF=$(  add rectangle --x 830 --y 415 -w 190 -h 70 \
  --label "Notification Service" --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

# ── Data layer nodes ────────────────────────────────────────────────────────
PG=$(     add rectangle --x 420 --y 585 -w 160 -h 70 \
  --label "Postgres"   --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
REDIS=$(  add rectangle --x 620 --y 585 -w 160 -h 70 \
  --label "Redis"      --bg "#fef08a" --stroke "#92400e" --fill-style solid --roughness 0 --sw 2)

# ── Connections ─────────────────────────────────────────────────────────────
conn "$WEB"    "$GW"    "" "#1e1e1e" "solid"
conn "$MOBILE" "$GW"    "" "#1e1e1e" "solid"
conn "$GW"     "$AUTH"  "" "#c2410c" "solid"
conn "$GW"     "$ORDER" "" "#1e1e1e" "solid"
conn "$GW"     "$INV"   "" "#1e1e1e" "solid"
conn "$GW"     "$NOTIF" "" "#1e1e1e" "solid"
conn "$ORDER"  "$PG"    "" "#6d28d9" "solid"
conn "$INV"    "$PG"    "" "#6d28d9" "solid"
conn "$ORDER"  "$REDIS" "" "#a16207" "dashed"
conn "$NOTIF"  "$REDIS" "" "#a16207" "dashed"

$CLI -p "$P" export png --output /tmp/arch-worked-example.png --overwrite
echo "Exported: /tmp/arch-worked-example.png"
```
