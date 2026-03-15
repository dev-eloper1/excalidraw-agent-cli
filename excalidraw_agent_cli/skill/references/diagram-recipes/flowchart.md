# Flowchart Diagram Recipe

## When to use

Use a flowchart when you need to communicate **step-by-step logic with conditional branching** — user journeys, request lifecycles, decision trees, validation pipelines. The defining signal is a sequence of actions where at least one step asks a yes/no question that splits the path.

Choose this pattern when:
- The narrative is "what happens, in what order, under what conditions"
- At least one step is a decision point with two or more exits
- Readers need to trace a specific path from start to end
- The flow terminates at one or more distinct outcomes (success, error, retry)

Do NOT use for: component relationships (use architecture diagram), time-phased schedules (use Gantt), or message sequences between systems (use sequence diagram).

---

## Layout template

```
Canvas: 1200 × 800px, origin top-left (0, 0)

Orientation: top-to-bottom (TD) default
Center axis: x = 600 (canvas midpoint)

Node geometry:
  Start / End (rounded rect):  w=180, h=60
  Process step (rectangle):    w=180, h=60
  Decision (diamond):          w=200, h=80   ← min w=140 to avoid label clip

Column positions (for left/right branches from a diamond):
  Left branch:    x=220,  w=160  → right edge=380
  Center column:  x=510,  w=200  (diamond; center_x=610)
  Right branch:   x=730,  w=160  → left edge=730, gap from diamond right=730-710=20 ✓
  ─ Adjust if diamond is wider; maintain ≥60px gap on both sides (Rule 17)

Row spacing (named variables):
  ROW_H=100     ← vertical distance between row top edges (node_h=60 + gap=40)
  COL_W=200     ← horizontal distance between column centers

Rows (top-to-bottom):
  TITLE_Y=15          (title text baseline ≈ y=37; first element at y≥97 → Rule 21)
  START_Y=100         (start node)
  STEP1_Y=200         (first process step; START_Y + ROW_H)
  STEP2_Y=300         (second process step)
  DECIDE_Y=400        (decision diamond)
  BRANCH_Y=520        (yes/no branch nodes; extra space for diamond height)
  END_Y=640           (end node; merged path)

Single-column layout (no branching):
  All nodes at x = (1200 - node_w) / 2 = 510 for w=180
  y increments by ROW_H=100

Branching layout (left/right exits from diamond):
  Diamond:       x=510, w=200, center_x=610
  YES branch:    x=730, y=BRANCH_Y, w=180
  NO branch:     x=220, y=BRANCH_Y, w=180
  Merge / End:   x=510, y=END_Y, w=180
```

---

## Color and style defaults

### Node fills (from color-palette.md)

| Node type | `--bg` | `--stroke` | Shape |
|-----------|--------|------------|-------|
| Start | `#dbeafe` | `#1e40af` | `rectangle --roundness` |
| End / Success | `#a7f3d0` | `#047857` | `rectangle --roundness` |
| Process step | `#86efac` | `#15803d` | `rectangle` |
| Decision diamond | `#fef3c7` | `#b45309` | `diamond` |
| Error / Reject path node | `#fecaca` | `#b91c1c` | `rectangle` |

Node style for all: `--fill-style solid --roughness 0 --sw 2`

### Arrow colors (from color-palette.md)

| Path type | `--stroke` | `--stroke-style` | `--sw` |
|-----------|-----------|-----------------|--------|
| Primary / default flow | `#1e1e1e` | `solid` | `2` |
| Yes / success branch | `#15803d` | `solid` | `2` |
| No / error branch | `#b91c1c` | `dashed` | `2` |
| Retry / loop back | `#a16207` | `dashed` | `1` |

### Title text

```bash
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" -t "Your Flowchart Title"
```

---

## Common pitfalls

1. **Diamond label clipped.** Diamond shape clips label text when `w < 140`. Use `w=200` for labels up to 16 characters. Apply Rule 3: `min_w = max(140, len(label) * 9.6 + 32)`, round up to nearest 10.

2. **Using `add arrow` instead of `element connect` for flowcharts.** Flowchart nodes are vertically stacked — `element connect` auto-routes correctly. Use `element connect` for all flowchart connections. Reserve explicit `add arrow` coordinates for sequence diagrams only (Rule 16).

3. **Title overlap with start node.** Title at `y=15 fs=20` has baseline ≈ y=37. First element must start at y ≥ 97 (Rule 21). `START_Y=100` satisfies this with 63px clearance.

4. **Long labels truncated.** Keep labels to ≤ 20 characters per line. For multi-word labels, use `\n` to break lines: `--label "Validate\nInput"`. Increase node height to `h=72` if using two-line labels.

5. **Branch nodes too close to diamond.** When diamond exits left and right, ensure ≥ 60px gap between diamond edge and branch node edge (Rule 17). Diamond at x=510 w=200 has right edge x=710; YES branch node must start at x ≥ 770.

6. **Error branch visually indistinct from success.** Always use red stroke (`#b91c1c`) and dashed style for the NO/error exit arrow. Never let success and error paths look identical (Rule 15).

7. **Merge arrows colliding at end node.** When two branches merge back into one End node, `element connect` from both branch nodes to End works correctly. No special handling needed — auto-routing keeps them separate.

---

## Worked example

**Scenario:** User signup flow — validate email, check if existing user, create account or return error, send welcome email, done.

**Node plan:**

| ID | Label | Shape | x | y | w | h |
|----|-------|-------|---|---|---|---|
| START | Start | roundness rect | 510 | 100 | 180 | 60 |
| VALIDATE | Validate Email | rect | 510 | 200 | 180 | 60 |
| DECIDE_EXISTS | User Exists? | diamond | 500 | 310 | 200 | 80 |
| EXISTS_ERR | Return 409 | rect | 220 | 430 | 160 | 60 |
| CREATE | Create Account | rect | 730 | 430 | 180 | 60 |
| SEND_EMAIL | Send Welcome\nEmail | rect | 730 | 530 | 180 | 60 |
| END | End | roundness rect | 510 | 640 | 180 | 60 |

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"
CLI=$(which excalidraw-agent-cli)
P=/tmp/flowchart-worked-example.excalidraw

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
$CLI --json project new --name "flowchart-worked-example" --output "$P" > /dev/null

# Title — y=15 fs=20 → baseline≈37. START_Y=100 → 63px clearance (Rule 21 ✓)
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "User Signup Flow" > /dev/null

# Nodes — top to bottom
START=$(    add rectangle --x 510 --y 100 -w 180 -h 60 --roundness \
  --label "Start"           --bg "#dbeafe" --stroke "#1e40af" --fill-style solid --roughness 0 --sw 2)
VALIDATE=$( add rectangle --x 510 --y 200 -w 180 -h 60 \
  --label "Validate Email"  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
DECIDE=$(   add diamond    --x 500 --y 310 -w 200 -h 80 \
  --label "User Exists?"    --bg "#fef3c7" --stroke "#b45309" --fill-style solid --roughness 0 --sw 2)
EXISTS_ERR=$(add rectangle --x 220 --y 430 -w 160 -h 60 \
  --label "Return 409"      --bg "#fecaca" --stroke "#b91c1c" --fill-style solid --roughness 0 --sw 2)
CREATE=$(   add rectangle --x 730 --y 430 -w 180 -h 60 \
  --label "Create Account"  --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
SEND=$(     add rectangle --x 730 --y 530 -w 180 -h 60 \
  --label "Send Welcome Email" --bg "#86efac" --stroke "#15803d" --fill-style solid --roughness 0 --sw 2)
END=$(      add rectangle --x 510 --y 640 -w 180 -h 60 --roundness \
  --label "End"             --bg "#a7f3d0" --stroke "#047857" --fill-style solid --roughness 0 --sw 2)

# Connections
conn "$START"      "$VALIDATE"  ""    "#1e1e1e" "solid"
conn "$VALIDATE"   "$DECIDE"    ""    "#1e1e1e" "solid"
conn "$DECIDE"     "$EXISTS_ERR" "yes" "#b91c1c" "dashed"   # user already exists → error
conn "$DECIDE"     "$CREATE"    "no"  "#15803d" "solid"     # new user → create
conn "$EXISTS_ERR" "$END"       ""    "#b91c1c" "dashed"
conn "$CREATE"     "$SEND"      ""    "#1e1e1e" "solid"
conn "$SEND"       "$END"       ""    "#1e1e1e" "solid"

$CLI -p "$P" export png --output /tmp/flowchart-worked-example.png --overwrite
echo "Exported: /tmp/flowchart-worked-example.png"
```
