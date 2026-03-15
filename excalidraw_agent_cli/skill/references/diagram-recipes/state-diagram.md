# State Diagram Recipe

## When to use

Use a state diagram when you need to model the lifecycle of an entity — an order, a user account, a payment, a request — where the entity moves through discrete named states and the transitions between states are triggered by events or conditions.

Choose this recipe (not a flowchart) when:
- The same state can be re-entered multiple times (e.g. `retry`)
- Multiple paths lead to the same terminal state (e.g. `cancelled`, `failed`)
- You need to communicate which events drive transitions, not just the steps

Do NOT use for: step-by-step processes where every step happens once (use flowchart), or for showing concurrent behavior (use sequence or swim-lane).

---

## Layout template

### Orientation: left-to-right

State diagrams flow **left to right** for linear happy paths. Alternative paths (cancel, error, refund) go in a **second row below** the main path.

```
Canvas: 1400px wide × 600px tall

Row 1 (happy path):   y=250, state h=60
Row 2 (error/cancel): y=370 (120px below row 1 top)

Start ellipse: w=40, h=40 (small filled bullet)
State rectangles: w=160, h=60, --roundness flag
End ellipse: w=50, h=50 (filled terminal circle)

Horizontal state spacing: 220px (center-to-center)
  → state w=160, gap = 220-160 = 60px  ✓ Rule 2

Column positions (start from x=220):
  Start bullet: x=220
  State 1:      x=290   (220 + 40 + 30 gap)
  State 2:      x=510   (290 + 160 + 60 gap)
  State 3:      x=730
  State 4:      x=950
  State 5:      x=1170
  End ellipse:  x=1390
```

### Coordinate formula

```
state_x[n] = start_x + start_w + gap + (n * 220)
  where start_x=220, start_w=40, gap=30, n=0,1,2...

Row 2 y: row1_y + 120  (120px gap between row tops)
```

---

## Color and style defaults

| Element | `--bg` | `--stroke` | `--fill-style` | Notes |
|---------|--------|------------|----------------|-------|
| Start state | `#dbeafe` | `#1e40af` | `solid` | Small ellipse w=40, h=40 |
| Happy-path states | `#86efac` | `#15803d` | `solid` | Rounded rectangles |
| End/success state | `#a7f3d0` | `#047857` | `solid` | Ellipse w=50, h=50 |
| Error/cancel states | `#fecaca` | `#b91c1c` | `solid` | Row 2, rounded rects |
| Refund/compensating states | `#fed7aa` | `#c2410c` | `solid` | Row 2 variations |

| Arrow type | `--stroke` | `--stroke-style` | `--sw` |
|-----------|-----------|-----------------|--------|
| Normal transition | `#1e1e1e` | `solid` | `2` |
| Cancel path | `#dc2626` | `dashed` | `2` |
| Error path | `#dc2626` | `dashed` | `2` |
| Compensating (e.g. refund) | `#c2410c` | `dashed` | `2` |

All shapes: `--roughness 0` for a clean, professional look.
All labels inside states: rendered by Excalidraw using the `--stroke` color — ensure contrast (Rule 22).

---

## Common pitfalls

1. **Start/end ellipses at wrong size** — The start state must be visually distinct: small (w=40, h=40) and filled. The end state is slightly larger (w=50, h=50). Do not use regular-sized ellipses for these.

2. **Crowded transition labels** — Long labels on `element connect` arrows render on the arrow line and can overlap adjacent states. Keep labels short (≤ 20 chars). For longer conditions, add a `add text` annotation below the arrow.

3. **Forgetting `--roundness`** — States in state diagrams use rounded rectangles. Always pass `--roundness` to `element add rectangle` for every state node.

4. **Row 2 states misaligned** — Error/cancel states should be positioned directly below the state they branch from. Use the same x-coordinate as the source state.

5. **Same-row arrows doubling** (Rule 20) — When connecting states in the same row (same y), ensure ≥ 60px horizontal gap between them. If gap < 60px, use `add arrow` with explicit coordinates instead of `element connect`.

6. **Start bullet too far left** (Rule 1) — Keep x ≥ 200 for all elements. The start ellipse (w=40) at x=220 gives a left edge of 220 — compliant.

7. **Missing `--label` on start/end ellipses** — The start ellipse should have no label (or label="" to keep it clean). The end ellipse can have a short label like "●" or "done".

---

## Worked example

Order lifecycle: `placed → payment_pending → paid → fulfillment → shipped → delivered`
With cancel paths from `placed` and `paid`, and a `refunded` path from `delivered`.

### Planning table

| Element | x | y | w | h | Color |
|---------|---|---|---|---|-------|
| Start bullet | 220 | 270 | 40 | 40 | `#dbeafe`/`#1e40af` |
| placed | 290 | 250 | 160 | 60 | `#86efac`/`#15803d` |
| payment_pending | 510 | 250 | 160 | 60 | `#86efac`/`#15803d` |
| paid | 730 | 250 | 160 | 60 | `#86efac`/`#15803d` |
| fulfillment | 950 | 250 | 160 | 60 | `#86efac`/`#15803d` |
| shipped | 1170 | 250 | 160 | 60 | `#86efac`/`#15803d` |
| delivered | 1390 | 250 | 160 | 60 | `#a7f3d0`/`#047857` |
| End bullet | 1610 | 265 | 50 | 50 | `#a7f3d0`/`#047857` |
| cancelled | 290 | 370 | 160 | 60 | `#fecaca`/`#b91c1c` |
| refunded | 1390 | 370 | 160 | 60 | `#fed7aa`/`#c2410c` |

### Shell commands

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/order-state.excalidraw
OUT="/tmp/order-state.png"

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

rm -f "$P"
$CLI --json project new --name "order-state" --output "$P" > /dev/null

# Title
add text --x 220 --y 180 --fs 20 --ff 2 --color "#1e293b" \
  -t "Order Lifecycle — State Diagram" > /dev/null

# Start bullet
START=$(add ellipse --x 220 --y 270 -w 40 -h 40 \
  --bg "#1e40af" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)

# Happy path states (row 1, y=250)
PLACED=$(add rectangle --x 290 --y 250 -w 160 -h 60 --roundness \
  --label "placed" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

PAYMENT=$(add rectangle --x 510 --y 250 -w 160 -h 60 --roundness \
  --label "payment_pending" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

PAID=$(add rectangle --x 730 --y 250 -w 160 -h 60 --roundness \
  --label "paid" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

FULFILLMENT=$(add rectangle --x 950 --y 250 -w 160 -h 60 --roundness \
  --label "fulfillment" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

SHIPPED=$(add rectangle --x 1170 --y 250 -w 160 -h 60 --roundness \
  --label "shipped" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)

DELIVERED=$(add rectangle --x 1390 --y 250 -w 160 -h 60 --roundness \
  --label "delivered" \
  --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2)

# End bullet
END=$(add ellipse --x 1610 --y 265 -w 50 -h 50 \
  --bg "#047857" --stroke "#047857" --fill-style solid --roughness 0 --sw 2)

# Cancel/error states (row 2, y=370)
CANCELLED=$(add rectangle --x 290 --y 370 -w 160 -h 60 --roundness \
  --label "cancelled" \
  --bg "#fecaca" --stroke "#b91c1c" --fill-style solid --roughness 0 --sw 2)

REFUNDED=$(add rectangle --x 1390 --y 370 -w 160 -h 60 --roundness \
  --label "refunded" \
  --bg "#fed7aa" --stroke "#c2410c" --fill-style solid --roughness 0 --sw 2)

# Happy-path transitions
conn "$START"    "$PLACED"     "new order"    "#1e1e1e" "solid"
conn "$PLACED"   "$PAYMENT"    "checkout"     "#1e1e1e" "solid"
conn "$PAYMENT"  "$PAID"       "payment ok"   "#1e1e1e" "solid"
conn "$PAID"     "$FULFILLMENT" "confirmed"   "#1e1e1e" "solid"
conn "$FULFILLMENT" "$SHIPPED" "dispatched"   "#1e1e1e" "solid"
conn "$SHIPPED"  "$DELIVERED"  "delivered"    "#1e1e1e" "solid"
conn "$DELIVERED" "$END"       ""             "#1e1e1e" "solid"

# Cancel paths (red dashed)
conn "$PLACED"   "$CANCELLED"  "cancel"       "#dc2626" "dashed"
conn "$PAID"     "$CANCELLED"  "cancel"       "#dc2626" "dashed"

# Refund path (orange dashed)
conn "$DELIVERED" "$REFUNDED"  "refund req."  "#c2410c" "dashed"

$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
```

### Visual result

```
 ●  →  [placed]  →  [payment_pending]  →  [paid]  →  [fulfillment]  →  [shipped]  →  [delivered]  →  ◉
            ↓                                ↓                                               ↓
       [cancelled]                      [cancelled]                                     [refunded]
```

Row 1 (happy path): blue start bullet → green states → green end bullet
Row 2 (alt paths): red cancel states below `placed` and `paid`, orange refunded below `delivered`
