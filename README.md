# excalidraw-agent-cli

A command-line tool for creating, editing, and exporting [Excalidraw](https://excalidraw.com) diagrams — designed for AI agents, scripting, and Claude Code.

- **No browser needed** — pure Python element mutations, real Excalidraw rendering via Node.js
- **AI-native** — `--json` mode on every command outputs element IDs for reliable chaining
- **Full element support** — rectangles, ellipses, diamonds, text, arrows, lines, frames
- **Built-in Claude Code skill** — one command installs a diagram-building skill into Claude Code; just describe what you want and Claude draws it

---

## Install

```bash
pip install excalidraw-agent-cli
```

**Requires Node.js ≥ 18** for SVG/PNG export (`brew install node` or [nodejs.org](https://nodejs.org)).
Node dependencies are auto-installed on first export — nothing else needed.

---

## Claude Code skill

The CLI ships with a built-in skill that teaches Claude Code how to build production-quality Excalidraw diagrams. After installing, Claude will pick up the skill automatically and use this CLI to draw any diagram you describe.

### Install the skill

```bash
# Globally — available in every Claude Code session on this machine
excalidraw-agent-cli install-skill

# Into a specific project — checked into git, shared with the team
excalidraw-agent-cli install-skill --codebase .
excalidraw-agent-cli install-skill --codebase ~/work/myapp

# Overwrite an existing installation
excalidraw-agent-cli install-skill --force
```

### Then just describe your diagram

```
"Draw a system architecture for a three-tier web app"
"Create a flowchart for the user signup and email verification process"
"Diagram the data flow between our auth service, core API, and Postgres"
"Show the CI/CD pipeline as a feedback loop"
"Visualize how JWT tokens flow from login to protected endpoints"
```

Claude will:
1. Choose the right visual pattern (swim lanes, fan-out, cycle, timeline, etc.)
2. Build the diagram with proper colors, spacing, and arrow styles
3. Export a PNG and visually inspect it
4. Fix any layout issues — truncated labels, zone bleeding, diagonal arrows
5. Iterate until both the structure and readability checks pass

### What the skill includes

The skill installs as `SKILL.md` + a `references/` directory loaded on demand:

| File | Purpose |
|------|---------|
| `SKILL.md` | Core philosophy, 6-step process, quality checklist |
| `references/color-palette.md` | All semantic hex color pairs (`--bg` + `--stroke`) |
| `references/cli-reference.md` | Full CLI syntax, bash helper patterns, copy-paste examples |
| `references/patterns.md` | Visual pattern library: fan-out, convergence, swim lanes, timeline, cycle, hub-and-spoke, assembly line, evidence artifacts |
| `references/layout-rules.md` | 15 layout rules, label-width formula, 3 coordinate templates, pre/post-build checklists |

### Skill location after install

| Mode | Path |
|------|------|
| Global (`--global`) | `~/.claude/skills/excalidraw/` |
| Codebase (`--codebase .`) | `./.claude/skills/excalidraw/` |

---

## Quick start (scripting / manual use)

```bash
CLI="excalidraw-agent-cli"
P="/tmp/my-diagram.excalidraw"

# 1. Create a project
$CLI --json project new --name "my-diagram" --output "$P"

# 2. Add shapes
A=$($CLI --project "$P" --json element add rectangle \
  --x 200 --y 200 -w 180 -h 80 \
  --label "API Gateway" --bg "#86efac" --stroke "#15803d" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")

B=$($CLI --project "$P" --json element add rectangle \
  --x 480 --y 200 -w 160 -h 80 \
  --label "Auth Service" --bg "#86efac" --stroke "#15803d" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")

# 3. Connect them
$CLI --project "$P" --json element connect \
  --from "$A" --to "$B" -l "authenticates" --stroke "#15803d" > /dev/null

# 4. Export
$CLI --project "$P" export png --output /tmp/my-diagram.png --overwrite
$CLI --project "$P" export svg --output /tmp/my-diagram.svg --overwrite
```

### Bash helper pattern (recommended for scripts)

Use these helpers at the top of every diagram script to avoid quoting bugs:

```bash
#!/usr/bin/env bash
set -e

CLI=$(which excalidraw-agent-cli)
P=/tmp/my-diagram.excalidraw

# add: run any 'element add' command, return the element ID
add() {
  $CLI --project "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

# conn: connect two elements with optional label, color, style
# Uses bash arrays to prevent hex color quoting issues with Click
conn() {
  local from="$1" to="$2" label="$3" color="$4" style="$5"
  local args=("--from" "$from" "--to" "$to")
  [[ -n "$label" ]] && args+=("-l" "$label")
  [[ -n "$color" ]] && args+=("--stroke" "$color")
  [[ -n "$style" ]] && args+=("--stroke-style" "$style")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "my-diagram" --output "$P" > /dev/null
```

---

## Examples

### Example 1 — Simple flowchart

```bash
#!/usr/bin/env bash
set -e
CLI=$(which excalidraw-agent-cli)
P=/tmp/flowchart.excalidraw

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("-l" "$3")
  [[ -n "$4" ]] && args+=("--stroke" "$4")
  [[ -n "$5" ]] && args+=("--stroke-style" "$5")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "flowchart" --output "$P" > /dev/null

START=$(  add ellipse   --x 350 --y 200 -w 160 -h 70 --label "Start"           --bg "#a7f3d0" --stroke "#047857")
STEP1=$(  add rectangle --x 330 --y 320 -w 200 -h 70 --label "Validate input"  --bg "#bfdbfe" --stroke "#1e40af")
DECIDE=$( add diamond   --x 310 --y 450 -w 240 -h 100 --label "Valid?"         --bg "#fef3c7" --stroke "#b45309")
OK=$(     add rectangle --x 560 --y 460 -w 200 -h 70 --label "Process request" --bg "#86efac" --stroke "#15803d")
ERR=$(    add rectangle --x 100 --y 460 -w 160 -h 70 --label "Return 400"      --bg "#fecaca" --stroke "#b91c1c")
END=$(    add ellipse   --x 350 --y 610 -w 160 -h 70 --label "End"             --bg "#a7f3d0" --stroke "#047857")

conn "$START"  "$STEP1"
conn "$STEP1"  "$DECIDE"
conn "$DECIDE" "$OK"  "yes" "#15803d"
conn "$DECIDE" "$ERR" "no"  "#b91c1c"
conn "$OK"     "$END"
conn "$ERR"    "$END"

$CLI --project "$P" export png --output /tmp/flowchart.png --overwrite
$CLI --project "$P" export svg --output /tmp/flowchart.svg --overwrite
```

---

### Example 2 — Three-tier architecture with swim lanes

```bash
#!/usr/bin/env bash
set -e
CLI=$(which excalidraw-agent-cli)
P=/tmp/arch.excalidraw

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("-l" "$3")
  [[ -n "$4" ]] && args+=("--stroke" "$4")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "arch" --output "$P" > /dev/null

# Zone backgrounds (must be added BEFORE nodes)
add rectangle --x 185 --y 155 -w 820 -h 140 --bg "#dbeafe" --stroke "#93c5fd" --fill-style solid --opacity 15 --sw 1 > /dev/null
add rectangle --x 185 --y 315 -w 820 -h 140 --bg "#dcfce7" --stroke "#86efac" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 185 --y 475 -w 820 -h 140 --bg "#ede9fe" --stroke "#c4b5fd" --fill-style solid --opacity 20 --sw 1 > /dev/null

# Zone labels
add text --x 195 --y 163 --fs 14 --ff 2 --color "#1e40af" -t "CLIENTS"  > /dev/null
add text --x 195 --y 323 --fs 14 --ff 2 --color "#15803d" -t "SERVICES" > /dev/null
add text --x 195 --y 483 --fs 14 --ff 2 --color "#6d28d9" -t "DATA"     > /dev/null

# Client layer
WEB=$(    add rectangle --x 205 --y 195 -w 160 -h 72 --label "Web App"     --bg "#bfdbfe" --stroke "#1e40af")
MOBILE=$( add rectangle --x 415 --y 195 -w 160 -h 72 --label "Mobile App"  --bg "#bfdbfe" --stroke "#1e40af")
PARTNER=$(add rectangle --x 625 --y 195 -w 165 -h 72 --label "Partner API" --bg "#bfdbfe" --stroke "#1e40af")

# Services layer
GW=$(   add rectangle --x 205 --y 355 -w 580 -h 72 --label "API Gateway"      --bg "#86efac" --stroke "#15803d")
AUTH=$( add rectangle --x 205 --y 355 -w 160 -h 72 --label "Auth Service"     --bg "#86efac" --stroke "#15803d")
CORE=$( add rectangle --x 415 --y 355 -w 160 -h 72 --label "Core API"         --bg "#86efac" --stroke "#15803d")
NOTIF=$(add rectangle --x 625 --y 355 -w 165 -h 72 --label "Notification Svc" --bg "#86efac" --stroke "#15803d")

# Data layer
DB=$(    add rectangle --x 205 --y 515 -w 160 -h 72 --label "PostgreSQL"  --bg "#ddd6fe" --stroke "#6d28d9")
CACHE=$( add rectangle --x 415 --y 515 -w 160 -h 72 --label "Redis Cache" --bg "#ddd6fe" --stroke "#6d28d9")
STORAGE=$(add rectangle --x 625 --y 515 -w 165 -h 72 --label "S3 Storage" --bg "#ddd6fe" --stroke "#6d28d9")

# Connections
for client in "$WEB" "$MOBILE" "$PARTNER"; do
  conn "$client" "$GW" "" "#1e40af"
done
conn "$GW"   "$AUTH"    "" "#1e1e1e"
conn "$GW"   "$CORE"    "" "#1e1e1e"
conn "$GW"   "$NOTIF"   "" "#1e1e1e"
conn "$AUTH" "$DB"      "" "#6d28d9"
conn "$CORE" "$DB"      "" "#6d28d9"
conn "$CORE" "$CACHE"   "" "#6d28d9"
conn "$NOTIF" "$STORAGE" "" "#6d28d9"

$CLI --project "$P" export png --output /tmp/arch.png --overwrite
$CLI --project "$P" export svg --output /tmp/arch.svg --overwrite
```

---

### Example 3 — CI/CD feedback cycle

```bash
#!/usr/bin/env bash
set -e
CLI=$(which excalidraw-agent-cli)
P=/tmp/cicd.excalidraw

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("-l" "$3")
  [[ -n "$4" ]] && args+=("--stroke" "$4")
  [[ -n "$5" ]] && args+=("--stroke-style" "$5")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "cicd" --output "$P" > /dev/null

PLAN=$(   add rectangle --x 350 --y 200 -w 160 -h 72 --label "Plan"    --bg "#bfdbfe" --stroke "#1e40af")
BUILD=$(  add rectangle --x 600 --y 350 -w 160 -h 72 --label "Build"   --bg "#86efac" --stroke "#15803d")
DEPLOY=$( add rectangle --x 350 --y 500 -w 160 -h 72 --label "Deploy"  --bg "#fef08a" --stroke "#a16207")
OBSERVE=$(add rectangle --x 100 --y 350 -w 160 -h 72 --label "Observe" --bg "#fecdd3" --stroke "#be123c")

conn "$PLAN"    "$BUILD"   ""         "#1e1e1e"
conn "$BUILD"   "$DEPLOY"  ""         "#1e1e1e"
conn "$DEPLOY"  "$OBSERVE" ""         "#1e1e1e"
conn "$OBSERVE" "$PLAN"    "feedback" "#be123c" "dashed"

$CLI --project "$P" export png --output /tmp/cicd.png --overwrite
```

---

### Example 4 — Mind map (hub-and-spoke)

```bash
#!/usr/bin/env bash
set -e
CLI=$(which excalidraw-agent-cli)
P=/tmp/mindmap.excalidraw

add() { $CLI --project "$P" --json element add "$@" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
spoke() {
  $CLI --project "$P" --json element connect \
    --from "$1" --to "$2" --stroke "#94a3b8" --stroke-style dotted --sw 1 > /dev/null
}

rm -f "$P"
$CLI --json project new --name "mindmap" --output "$P" > /dev/null

HUB=$(add ellipse --x 580 --y 390 -w 200 -h 80 --label "excalidraw-agent-cli" \
  --bg "#334155" --stroke "#0f172a" --roughness 0 --sw 3)

CREATE=$(add rectangle --x 240 --y 190 -w 160 -h 70 --label "Create"    --bg "#bfdbfe" --stroke "#1e40af")
EDIT=$(  add rectangle --x 240 --y 420 -w 160 -h 70 --label "Edit"      --bg "#bbf7d0" --stroke "#15803d")
EXPORT=$(add rectangle --x 960 --y 190 -w 160 -h 70 --label "Export"    --bg "#fef08a" --stroke "#a16207")
AGENT=$( add rectangle --x 960 --y 420 -w 160 -h 70 --label "AI Agent"  --bg "#fed7aa" --stroke "#c2410c")
SKILL=$( add rectangle --x 580 --y 620 -w 200 -h 70 --label "Claude Skill" --bg "#ddd6fe" --stroke "#6d28d9")

spoke "$HUB" "$CREATE"
spoke "$HUB" "$EDIT"
spoke "$HUB" "$EXPORT"
spoke "$HUB" "$AGENT"
spoke "$HUB" "$SKILL"

add text --x 80  --y 170 --fs 13 --ff 1 --color "#1e40af" -t "rectangle / ellipse / diamond" > /dev/null
add text --x 80  --y 215 --fs 13 --ff 1 --color "#1e40af" -t "text / arrow / line / frame"   > /dev/null
add text --x 80  --y 400 --fs 13 --ff 1 --color "#15803d" -t "update / move / delete"        > /dev/null
add text --x 80  --y 445 --fs 13 --ff 1 --color "#15803d" -t "connect (auto-positioned)"     > /dev/null
add text --x 1140 --y 175 --fs 13 --ff 1 --color "#a16207" -t "SVG (vector)"                 > /dev/null
add text --x 1140 --y 220 --fs 13 --ff 1 --color "#a16207" -t "PNG (raster)"                 > /dev/null
add text --x 1140 --y 265 --fs 13 --ff 1 --color "#a16207" -t ".excalidraw (JSON)"           > /dev/null
add text --x 1140 --y 405 --fs 13 --ff 1 --color "#c2410c" -t "--json flag on every cmd"     > /dev/null
add text --x 1140 --y 450 --fs 13 --ff 1 --color "#c2410c" -t "element IDs for chaining"     > /dev/null
add text --x 490  --y 605 --fs 13 --ff 1 --color "#6d28d9" -t "install-skill command"        > /dev/null

$CLI --project "$P" export png --output /tmp/mindmap.png --overwrite
$CLI --project "$P" export svg --output /tmp/mindmap.svg --overwrite
```

---

### Example 5 — Interactive REPL

```
$ excalidraw-agent-cli
excalidraw> project new --name "scratch" -o /tmp/scratch.excalidraw
✓ Project created: scratch

excalidraw> --project /tmp/scratch.excalidraw element add rectangle \
    --x 200 --y 200 --label "Hello" --bg "#86efac" --stroke "#15803d"
✓ Added rectangle abc123

excalidraw> --project /tmp/scratch.excalidraw element list
1 element(s):
  abc123  rectangle  (200, 200)  180×80  "Hello"

excalidraw> --project /tmp/scratch.excalidraw export svg -o /tmp/scratch.svg --overwrite
✓ Exported SVG → /tmp/scratch.svg

excalidraw> exit
```

---

## All commands

```
project        new / open / save / info / validate
element        add rectangle / ellipse / diamond / text / arrow / line / frame
element        list / get / update / delete / move / connect
export         svg / png / json
session        status / undo / redo / history
backend        check
install-skill  [--global] [--codebase DIR] [--force]
```

Global flags (go **before** the subcommand):
```
--project  -p   Path to .excalidraw file
--json          Output as JSON (required for agent/scripting use)
```

---

## Element add flags

### Shapes (rectangle / ellipse / diamond)

| Flag | Description | Default |
|------|-------------|---------|
| `--x`, `--y` | Canvas position (top-left) | required |
| `-w`, `-h` | Width and height in px | `180 × 80` |
| `--label` | Text inside the shape | none |
| `--bg` | Fill color (hex) | `#ffffff` |
| `--stroke` | Border color (hex) | `#1e1e1e` |
| `--fill-style` | `solid`, `hachure`, `cross-hatch`, `dots`, `zigzag` | `hachure` |
| `--sw` | Stroke width in px | `1` |
| `--roughness` | `0` clean · `1` default · `2` sketchy | `1` |
| `--opacity` | 0–100 | `100` |
| `--roundness` | Flag — rounds corners (rectangles only) | off |

### Text (free-floating)

| Flag | Description |
|------|-------------|
| `-t` | Text content (use `-t`, not `--label`) |
| `--fs` | Font size (minimum 12) |
| `--ff` | Font family: `1` Virgil · `2` Helvetica · `3` Cascadia (mono) |
| `--color` | Text color (hex) |

### Arrow / connection

| Flag | Values | Default |
|------|--------|---------|
| `--from`, `--to` | element IDs | required |
| `-l` | Arrow label | none |
| `--stroke` | hex color | `#1e1e1e` |
| `--sw` | stroke width | `2` |
| `--stroke-style` | `solid`, `dashed`, `dotted` | `solid` |
| `--start-arrowhead` | `arrow`, `triangle`, `dot`, `bar`, `circle`, or omit | none |
| `--end-arrowhead` | `arrow`, `triangle`, `dot`, `bar`, `circle`, `None` | `arrow` |

```bash
# Bidirectional arrow
excalidraw-agent-cli --project "$P" --json element connect \
  --from "$A" --to "$B" \
  -l "read / write" \
  --stroke "#6d28d9" --sw 2 \
  --start-arrowhead arrow --end-arrowhead arrow
```

---

## Color palette

All colors are semantic — use the same pair everywhere for the same concept:

| Semantic purpose | `--bg` | `--stroke` |
|-----------------|--------|------------|
| Clients / Users | `#bfdbfe` | `#1e40af` |
| Services / API | `#86efac` | `#15803d` |
| Gateway / Routing | `#bbf7d0` | `#15803d` |
| Async / Queue | `#fef08a` | `#a16207` |
| Data / Storage | `#ddd6fe` | `#6d28d9` |
| Security / Edge | `#fed7aa` | `#c2410c` |
| Observability | `#fecdd3` | `#be123c` |
| AI / LLM | `#ddd6fe` | `#6d28d9` |
| Decision diamond | `#fef3c7` | `#b45309` |
| Start / Trigger | `#dbeafe` | `#1e40af` |
| End / Success | `#a7f3d0` | `#047857` |
| Error / Reject | `#fecaca` | `#b91c1c` |

Arrow color conventions:

| Relationship | `--stroke` |
|-------------|------------|
| Primary call / request | `#1e1e1e` |
| Async / event | `#a16207` |
| Error / failure | `#dc2626` |
| Data read/write | `#6d28d9` |
| Auth / security | `#c2410c` |
| Observability | `#be123c` |
| Hub-to-spoke | `#94a3b8` |

---

## How it works

```
pip install excalidraw-agent-cli
        │
        ▼
excalidraw_agent_cli/   (pure Python)
  ├── cli.py            Click CLI + REPL
  ├── core/             element mutations, project state, export
  ├── utils/            backend manager, REPL skin
  ├── export_helper/    export.js + package.json  (64 KB, no node_modules)
  └── skill/            SKILL.md + references/    (Claude Code skill)
        │
        ▼ first SVG/PNG export
~/.cache/excalidraw-agent-cli/
  ├── export.js         (copied from wheel)
  ├── package.json
  └── node_modules/     (npm install runs once, ~52 MB)
```

No Excalidraw installation required. The Python layer handles all element mutations and saves `.excalidraw` JSON files. Node.js is only invoked for rendering to SVG/PNG.

---

## License

MIT — see [LICENSE](LICENSE)
