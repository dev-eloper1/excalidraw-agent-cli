# CLI Reference

Full command reference for `excalidraw-agent-cli`. All examples assume:

```bash
CLI=$(which excalidraw-agent-cli)
P=/tmp/my-diagram.excalidraw
```

---

## Critical: Flag Placement

`--project` and `--json` are **global flags** — they go BEFORE the subcommand:

```bash
✅  $CLI --project $P --json element add rectangle --x 200 --y 150
❌  $CLI element add rectangle --project $P --x 200 --y 150   # errors
```

Arrow labels **must use `-l`** (short form) to handle spaces correctly:
```bash
✅  $CLI --project $P --json element connect --from $A --to $B -l "calls DB"
❌  --label "calls DB"  # may fail with spaces
```

---

## Bash Helper Pattern

Use these helpers at the top of every diagram script. They prevent the most common bugs.

```bash
#!/usr/bin/env bash
set -e

CLI=$(which excalidraw-agent-cli)
P=/tmp/my-diagram.excalidraw

# add: run any 'element add' command and return the element ID
add() {
  $CLI --project "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

# conn: connect two elements with optional label, color, style
# IMPORTANT: use bash arrays to avoid hex color quoting issues
conn() {
  local from="$1" to="$2" label="$3" color="$4" style="$5"
  local args=("--from" "$from" "--to" "$to")
  [[ -n "$label" ]] && args+=("-l" "$label")
  [[ -n "$color" ]] && args+=("--stroke" "$color")
  [[ -n "$style" ]] && args+=("--stroke-style" "$style")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

# Create project
rm -f "$P"
$CLI --json project new --name "my-diagram" --output "$P" > /dev/null
```

---

## Project Commands

```bash
# New project
$CLI --json project new --name "name" --output /path/to/file.excalidraw

# Open existing
$CLI --json project open --file /path/to/file.excalidraw

# Save to new location
$CLI --json project save --output /new/path.excalidraw

# Project info (element count, bounds, theme)
$CLI --project $P --json project info

# Validate (returns list of errors, empty = valid)
$CLI --project $P --json project validate
```

---

## Element Add Commands

### Rectangle
```bash
ID=$(add rectangle \
  --x 200 --y 200 \
  -w 180 -h 80 \
  --label "Auth Service" \
  --bg "#86efac" --stroke "#15803d" --fill-style solid \
  --roughness 0 --sw 2 --opacity 100 \
  --roundness)       # optional: rounded corners
```

### Ellipse
```bash
ID=$(add ellipse \
  --x 200 --y 200 \
  -w 160 -h 70 \
  --label "User" \
  --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid)
```

### Diamond (decision)
```bash
ID=$(add diamond \
  --x 300 --y 400 \
  -w 200 -h 100 \
  --label "Valid?" \
  --bg "#fef3c7" --stroke "#b45309" --fill-style solid)
```

### Text (free-floating)
```bash
# Text uses -t flag, NOT --label
add text \
  --x 200 --y 165 \
  --fs 14 --ff 2 --color "#1e40af" \
  -t "CLIENT LAYER" > /dev/null

# Font families: --ff 1 = Virgil, --ff 2 = Helvetica, --ff 3 = Cascadia (monospace)
# Font sizes: --fs 12 minimum, --fs 14-16 for headers, --fs 20+ for titles
```

### Arrow (freestanding, for legends / annotations)
```bash
ID=$(add arrow \
  --x 200 --y 300 --ex 400 --ey 300 \
  --stroke "#dc2626" --sw 2 --stroke-style dashed --roughness 0 \
  --start-arrowhead arrow --end-arrowhead triangle \
  -l "bidirectional")
```

### Line (structural — dividers, timelines, tree branches)
```bash
# Horizontal divider
add line \
  --x 200 --y 500 \
  --points "0,0 900,0" \
  --stroke "#e2e8f0" --sw 1 --stroke-style dashed > /dev/null

# Vertical tree trunk
add line \
  --x 400 --y 200 \
  --points "0,0 0,300" \
  --stroke "#64748b" --sw 2 > /dev/null

# Multi-point polyline path
add line \
  --x 400 --y 300 \
  --points "0,0 0,100 200,100 200,0" \
  --stroke "#6d28d9" --sw 2 --stroke-style dashed > /dev/null
```

Points are **relative** to `--x`/`--y`.

### Frame (container / grouping)
```bash
FRAME=$(add frame \
  -w 400 -h 300 \
  --name "User Flow" \
  --stroke "#bbb")

# Children of a frame use --frame-id (rectangles only)
add rectangle --frame-id "$FRAME" --x 50 --y 50 -w 180 -h 80 --label "Step 1"
```

---

## Element Connect Command

Connect two elements with an auto-positioned arrow:

```bash
# Simple connection
conn "$A" "$B"

# Labeled
conn "$A" "$B" "calls"

# Colored + styled
conn "$A" "$B" "async" "#a16207" "dashed"

# Full control (bidirectional, custom arrowheads)
$CLI --project "$P" --json element connect \
  --from "$A" --to "$B" \
  -l "read / write" \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead arrow --end-arrowhead arrow > /dev/null
```

### element connect flags

| Flag | Values | Default |
|------|--------|---------|
| `--from`, `--to` | element IDs | required |
| `-l` | any string | none |
| `--stroke` | hex color | `#1e1e1e` |
| `--sw` | int | `2` |
| `--stroke-style` | `solid`, `dashed`, `dotted` | `solid` |
| `--roughness` | `0`–`2` | `1` |
| `--start-arrowhead` | `arrow`, `triangle`, `dot`, `bar`, `circle`, or omit | none |
| `--end-arrowhead` | `arrow`, `triangle`, `dot`, `bar`, `circle`, `None` | `arrow` |

### Arrowhead types

| Value | Shape | Use for |
|-------|-------|---------|
| `arrow` | Open arrowhead | Default flow |
| `triangle` | Filled triangle | Strong direction, important flow |
| `dot` | Circle endpoint | Association, soft link |
| `bar` | Perpendicular bar | Terminus, bus, stop |
| `None` | No arrowhead | Plain structural line |

---

## Element Mutate Commands

```bash
# Update position, size, label
$CLI --project $P --json element update --id $ID --x 200 --y 200 --label "New Label"

# Move by delta
$CLI --project $P --json element move --id $ID --dx 50 --dy 0

# Delete
$CLI --project $P --json element delete $ID

# List all elements
$CLI --project $P --json element list

# List by type
$CLI --project $P --json element list --type rectangle
```

---

## Export Commands

```bash
# SVG (vector, best for embedding in markdown)
$CLI --project $P export svg --output /tmp/diagram.svg --overwrite

# PNG (raster, best for viewing and validation)
$CLI --project $P export png --output /tmp/diagram.png --overwrite

# Dark mode export
$CLI --project $P export svg --output /tmp/diagram-dark.svg --dark-mode --overwrite

# Raw JSON export
$CLI --project $P export json --output /tmp/diagram.excalidraw --overwrite
```

---

## Session Commands

```bash
# Undo last mutation
$CLI --project $P session undo

# Redo
$CLI --project $P session redo

# Session status (modified flag, undo stack depth)
$CLI --project $P --json session status

# History log (operation names + timestamps)
$CLI --project $P --json session history
```

---

## Backend Check

```bash
$CLI --json backend check
# → {"available": true, "node_path": "...", "helper_path": "...", "issues": []}
```

On first run after install, node dependencies are auto-installed to `~/.cache/excalidraw-agent-cli/`. Takes ~5 seconds, happens once.

---

## Zone Background Pattern

Zone backgrounds must be added **before** the nodes that sit on top of them:

```bash
# 1. Add zone bg first
add rectangle \
  --x 185 --y 155 -w 820 -h 145 \
  --bg "#dbeafe" --stroke "#93c5fd" \
  --fill-style solid --opacity 15 --sw 1 > /dev/null

# 2. Add zone label
add text --x 195 --y 163 --fs 14 --ff 2 --color "#1e40af" -t "CLIENT LAYER" > /dev/null

# 3. Now add nodes inside the zone
CLIENT=$(add rectangle --x 205 --y 195 -w 160 -h 72 \
  --label "Web App" --bg "#bfdbfe" --stroke "#1e40af" --fill-style solid)
```

---

## Complete Minimal Example

```bash
#!/usr/bin/env bash
set -e
CLI=$(which excalidraw-agent-cli)
P=/tmp/example.excalidraw

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("-l" "$3")
  [[ -n "$4" ]] && args+=("--stroke" "$4")
  [[ -n "$5" ]] && args+=("--stroke-style" "$5")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "example" --output "$P" > /dev/null

A=$(add rectangle --x 200 --y 200 -w 180 -h 80 --label "Service A" --bg "#86efac" --stroke "#15803d")
B=$(add rectangle --x 500 --y 200 -w 180 -h 80 --label "Service B" --bg "#ddd6fe" --stroke "#6d28d9")
conn "$A" "$B" "calls" "#15803d"

$CLI --project "$P" export svg --output /tmp/example.svg --overwrite
$CLI --project "$P" export png --output /tmp/example.png --overwrite
```
