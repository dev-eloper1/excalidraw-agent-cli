# excalidraw-agent-cli

A command-line tool for creating, editing, and exporting [Excalidraw](https://excalidraw.com) diagrams — built for AI agents and scripting.

- **No browser needed** — pure Python mutations, real Excalidraw rendering via Node.js
- **AI-native** — `--json` mode on every command outputs element IDs for chaining
- **Full element support** — rectangles, ellipses, diamonds, text, arrows, lines, frames
- **Claude skill included** — drop `skill/SKILL.md` into Claude Code and it builds diagrams for you automatically

---

## Install

```bash
pip install excalidraw-agent-cli
```

**Requires Node.js ≥ 18** for SVG/PNG export (`brew install node` or [nodejs.org](https://nodejs.org)).
Node dependencies are auto-installed on first export — nothing else needed.

---

## Quick start

```bash
# 1. Create a project
excalidraw-agent-cli project new --name "my-diagram" --output diagram.excalidraw

# 2. Add shapes
excalidraw-agent-cli --project diagram.excalidraw \
  element add rectangle --x 200 --y 200 -w 180 -h 80 \
  --label "API Gateway" --bg "#86efac" --stroke "#15803d"

# 3. Export
excalidraw-agent-cli --project diagram.excalidraw \
  export svg --output diagram.svg --overwrite
```

---

## Examples

### Example 1 — Simple flowchart

```bash
CLI="excalidraw-agent-cli"
P="/tmp/flowchart.excalidraw"

$CLI project new --name "flowchart" --output "$P"

# Helper: add element and capture its ID
add() { $CLI --project "$P" --json element add "$@" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

# Helper: connect two elements (use bash arrays to avoid shell quoting issues)
conn() {
  local args=("--from" "$1" "--to" "$2")
  [[ -n "$3" ]] && args+=("-l" "$3")
  [[ -n "$4" ]] && args+=("--stroke" "$4")
  [[ -n "$5" ]] && args+=("--stroke-style" "$5")
  $CLI --project "$P" --json element connect "${args[@]}" > /dev/null
}

START=$(add ellipse  --x 350 --y 200 -w 160 -h 70 --label "Start"           --bg "#a7f3d0" --stroke "#047857")
STEP1=$(add rectangle --x 330 --y 320 -w 200 -h 70 --label "Validate input"  --bg "#bfdbfe" --stroke "#1e40af")
DECIDE=$(add diamond --x 310 --y 450 -w 240 -h 100 --label "Valid?"          --bg "#fef3c7" --stroke "#b45309")
OK=$(   add rectangle --x 560 --y 460 -w 160 -h 70 --label "Process request" --bg "#86efac" --stroke "#15803d")
ERR=$(  add rectangle --x 100 --y 460 -w 160 -h 70 --label "Return 400"      --bg "#fecaca" --stroke "#b91c1c")
END=$(  add ellipse   --x 350 --y 610 -w 160 -h 70 --label "End"             --bg "#a7f3d0" --stroke "#047857")

conn "$START" "$STEP1"
conn "$STEP1" "$DECIDE"
conn "$DECIDE" "$OK"  "yes" "#15803d"
conn "$DECIDE" "$ERR" "no"  "#b91c1c"
conn "$OK"  "$END"
conn "$ERR" "$END"

$CLI --project "$P" export svg --output /tmp/flowchart.svg --overwrite
```

---

### Example 2 — System architecture diagram

```bash
CLI="excalidraw-agent-cli"
P="/tmp/arch.excalidraw"
$CLI project new --name "arch" --output "$P"

add() { $CLI --project "$P" --json element add "$@" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }

# Zone backgrounds (added first so they appear behind nodes)
add rectangle --x 185 --y 155 -w 820 -h 140 \
  --bg "#dbeafe" --stroke "#93c5fd" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 185 --y 315 -w 820 -h 140 \
  --bg "#dcfce7" --stroke "#86efac" --fill-style solid --opacity 20 --sw 1 > /dev/null
add rectangle --x 185 --y 475 -w 820 -h 140 \
  --bg "#ddd6fe" --stroke "#c4b5fd" --fill-style solid --opacity 20 --sw 1 > /dev/null

# Layer labels
add text --x 195 --y 163 --fs 14 --ff 2 --color "#1e40af" -t "CLIENTS" > /dev/null
add text --x 195 --y 323 --fs 14 --ff 2 --color "#15803d" -t "SERVICES" > /dev/null
add text --x 195 --y 483 --fs 14 --ff 2 --color "#6d28d9" -t "DATA" > /dev/null

# Client layer
WEB=$(    add rectangle --x 205 --y 195 -w 160 -h 72 --label "Web App"     --bg "#bfdbfe" --stroke "#1e40af")
MOBILE=$( add rectangle --x 415 --y 195 -w 160 -h 72 --label "Mobile App"  --bg "#bfdbfe" --stroke "#1e40af")
PARTNER=$(add rectangle --x 625 --y 195 -w 160 -h 72 --label "Partner API" --bg "#bfdbfe" --stroke "#1e40af")

# Services layer
GW=$(   add rectangle --x 205 --y 355 -w 575 -h 72 --label "API Gateway"      --bg "#86efac" --stroke "#15803d")
AUTH=$( add rectangle --x 205 --y 355 -w 160 -h 72 --label "Auth Service"     --bg "#86efac" --stroke "#15803d")
CORE=$( add rectangle --x 415 --y 355 -w 160 -h 72 --label "Core API"         --bg "#86efac" --stroke "#15803d")
NOTIF=$(add rectangle --x 625 --y 355 -w 165 -h 72 --label "Notification Svc" --bg "#86efac" --stroke "#15803d")

# Data layer
DB=$(    add rectangle --x 205 --y 515 -w 160 -h 72 --label "PostgreSQL"    --bg "#ddd6fe" --stroke "#6d28d9")
CACHE=$( add rectangle --x 415 --y 515 -w 160 -h 72 --label "Redis Cache"   --bg "#ddd6fe" --stroke "#6d28d9")
STORAGE=$(add rectangle --x 625 --y 515 -w 165 -h 72 --label "S3 Storage"   --bg "#ddd6fe" --stroke "#6d28d9")

# Connections
for client in "$WEB" "$MOBILE" "$PARTNER"; do
  $CLI --project "$P" --json element connect --from "$client" --to "$GW" \
    --stroke "#1e40af" > /dev/null
done
$CLI --project "$P" --json element connect --from "$GW"   --to "$AUTH"  > /dev/null
$CLI --project "$P" --json element connect --from "$GW"   --to "$CORE"  > /dev/null
$CLI --project "$P" --json element connect --from "$GW"   --to "$NOTIF" > /dev/null
$CLI --project "$P" --json element connect --from "$AUTH" --to "$DB"    --stroke "#6d28d9" > /dev/null
$CLI --project "$P" --json element connect --from "$CORE" --to "$DB"    --stroke "#6d28d9" > /dev/null
$CLI --project "$P" --json element connect --from "$CORE" --to "$CACHE" --stroke "#6d28d9" > /dev/null
$CLI --project "$P" --json element connect --from "$NOTIF" --to "$STORAGE" --stroke "#6d28d9" > /dev/null

$CLI --project "$P" export svg --output /tmp/arch.svg --overwrite
```

---

### Example 3 — Mind map

```bash
CLI="excalidraw-agent-cli"
P="/tmp/mindmap.excalidraw"
$CLI project new --name "mindmap" --output "$P"

add() { $CLI --project "$P" --json element add "$@" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"; }
spoke() {
  $CLI --project "$P" --json element connect \
    --from "$1" --to "$2" --stroke "#94a3b8" --stroke-style dotted --sw 1 > /dev/null
}

# Hub
HUB=$(add ellipse --x 600 --y 400 -w 180 -h 80 --label "excalidraw-agent-cli" \
  --bg "#334155" --stroke "#0f172a" --roughness 0 --sw 3)

# Topic nodes
CREATE=$(add rectangle --x 250 --y 200 -w 160 -h 70 --label "Create"   --bg "#bfdbfe" --stroke "#1e40af")
EDIT=$(  add rectangle --x 250 --y 420 -w 160 -h 70 --label "Edit"     --bg "#bbf7d0" --stroke "#15803d")
EXPORT=$(add rectangle --x 960 --y 200 -w 160 -h 70 --label "Export"   --bg "#fef08a" --stroke "#a16207")
AGENT=$( add rectangle --x 960 --y 420 -w 160 -h 70 --label "AI Agent" --bg "#fed7aa" --stroke "#c2410c")
UNDO=$(  add rectangle --x 590 --y 620 -w 160 -h 70 --label "Undo/Redo" --bg "#ddd6fe" --stroke "#6d28d9")

spoke "$HUB" "$CREATE"
spoke "$HUB" "$EDIT"
spoke "$HUB" "$EXPORT"
spoke "$HUB" "$AGENT"
spoke "$HUB" "$UNDO"

# Sub-topics
RECT=$( add text --x 90  --y 170 --fs 13 --ff 1 --color "#1e40af" -t "rectangle / ellipse / diamond")
TXT=$(  add text --x 90  --y 220 --fs 13 --ff 1 --color "#1e40af" -t "text / arrow / line / frame")
UPD=$(  add text --x 80  --y 400 --fs 13 --ff 1 --color "#15803d" -t "update / move / delete")
CONN=$( add text --x 80  --y 450 --fs 13 --ff 1 --color "#15803d" -t "connect (auto-positioned)")
SVG=$(  add text --x 1140 --y 185 --fs 13 --ff 1 --color "#a16207" -t "SVG (vector)")
PNG=$(  add text --x 1140 --y 225 --fs 13 --ff 1 --color "#a16207" -t "PNG (raster)")
JSON=$( add text --x 1140 --y 265 --fs 13 --ff 1 --color "#a16207" -t ".excalidraw (JSON)")
JSONFLAG=$(add text --x 1140 --y 405 --fs 13 --ff 1 --color "#c2410c" -t "--json flag on every cmd")
CHAIN=$(   add text --x 1140 --y 445 --fs 13 --ff 1 --color "#c2410c" -t "element IDs for chaining")

$CLI --project "$P" export svg --output /tmp/mindmap.svg --overwrite
```

---

### Example 4 — Using the REPL interactively

```
$ excalidraw-agent-cli
excalidraw> project new --name "scratch" -o /tmp/scratch.excalidraw
✓ Project created: scratch

excalidraw> --project /tmp/scratch.excalidraw element add rectangle --x 200 --y 200 --label "Hello"
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
project   new / open / save / info / validate
element   add rectangle / ellipse / diamond / text / arrow / line / frame
element   list / get / update / delete / move / connect
export    svg / png / json
session   status / undo / redo / history
backend   check
```

Global flags (before the subcommand):
```
--project  -p   Path to .excalidraw file
--json          Output as JSON (for scripting/agents)
```

---

## Arrow & connection options

```bash
# Styled connection between two elements
excalidraw-agent-cli --project "$P" --json element connect \
  --from "$A" --to "$B" \
  -l "calls" \
  --stroke "#6d28d9" \
  --stroke-style dashed \
  --sw 2 \
  --start-arrowhead arrow \
  --end-arrowhead triangle

# Standalone arrow (for legends)
excalidraw-agent-cli --project "$P" --json element add arrow \
  --x 200 --y 300 --ex 500 --ey 300 \
  --stroke "#dc2626" --stroke-style dashed --roughness 2 \
  --start-arrowhead dot --end-arrowhead triangle \
  -l "bidirectional"
```

| Flag | Values |
|------|--------|
| `--stroke-style` | `solid`, `dashed`, `dotted` |
| `--end-arrowhead` / `--start-arrowhead` | `arrow`, `triangle`, `dot`, `bar`, `circle`, `None` |
| `--roughness` | `0` (clean) · `1` (default) · `2` (hand-drawn) |
| `--sw` | stroke width in px |

---

## Color palette (recommended)

| Layer | `--bg` | `--stroke` |
|-------|--------|------------|
| Clients | `#bfdbfe` | `#1e40af` |
| Services / API | `#86efac` | `#15803d` |
| Async / Queue | `#fef08a` | `#a16207` |
| Data / Storage | `#ddd6fe` | `#6d28d9` |
| Security / Edge | `#fed7aa` | `#c2410c` |
| Observability | `#fecdd3` | `#be123c` |
| Success / End | `#a7f3d0` | `#047857` |
| Error / Reject | `#fecaca` | `#b91c1c` |

---

## Claude Code skill

The `skill/SKILL.md` teaches Claude Code to use this CLI automatically. Install once:

```bash
mkdir -p ~/.claude/skills/excalidraw
cp skill/SKILL.md ~/.claude/skills/excalidraw/SKILL.md
```

After that, just ask Claude:
> *"Draw a system architecture for a three-tier web app"*
> *"Create a flowchart for the user signup process"*
> *"Diagram the data flow between these services"*

Claude will run `excalidraw-agent-cli` commands to build the diagram and export an SVG.

---

## License

MIT — see [LICENSE](LICENSE)
