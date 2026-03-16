# ER Diagram Recipe

## When to use

Use an ER (Entity-Relationship) diagram when you need to show the structure of a relational data model — the tables, their columns, and how tables relate to each other.

Choose this recipe when:
- Designing or documenting a database schema
- Communicating data ownership in a service-oriented architecture
- Reviewing foreign-key relationships and cardinality before writing migrations

Do NOT use for: showing runtime data flow between services (use architecture diagram), or for showing how a user interacts with the system (use sequence or flowchart).

---

## Layout template

### Grid: 3 columns × 2 rows

```
Canvas: 1400px wide × 700px tall

Entity boxes: w=200, h=varies (use 160 for 4-5 attributes, 200 for 6-8)
Column spacing: 280px (center-to-center, so gap = 280-200 = 80px  ✓ Rule 2)
Row spacing:    220px (row top to row top)

Grid origin: x=80, y=100

Col 1 x: 80
Col 2 x: 360   (80 + 280)
Col 3 x: 640   (360 + 280)

Row 1 y: 100
Row 2 y: 320   (100 + 220)
```

### Entity box structure

Each entity uses a single **rectangle** whose label is the entity name. Attributes are added as separate `add text` elements placed inside the box, below the entity name header.

```
Entity box:      x=80,  y=100, w=200, h=160
Entity name:     --label "users"   (rendered centered by Excalidraw)
Attribute line 1: add text --x 90 --y 140 --fs 12 --ff 3 ...
Attribute line 2: add text --x 90 --y 158 --fs 12 --ff 3 ...
...
Row height per attribute: 18px
```

The entity name is styled with `--ff 2` (Helvetica). Attribute text uses `--ff 3` (Cascadia monospace) for a technical data feel.

**Primary keys**: prefix with `🔑 ` or `PK ` in the text label so they stand out visually.
**Foreign keys**: prefix with `FK ` to indicate the relationship target.

---

## Color and style defaults

| Element | `--bg` | `--stroke` | `--fill-style` | Notes |
|---------|--------|------------|----------------|-------|
| Regular entity | `#ddd6fe` | `#6d28d9` | `solid` | Standard table |
| Weak entity | `#ddd6fe` | `#6d28d9` | `hachure` | Dependent table (e.g. post_tags junction) |
| Entity name text | — | — | — | Inside shape; use `--ff 2` on the box label |
| Attribute text | `#374151` | — | — | `add text` with `--ff 3`, `--fs 12`, `--color "#374151"` |
| PK attribute text | `#1e40af` | — | — | `--color "#1e40af"` to highlight primary key |
| FK attribute text | `#6d28d9` | — | — | `--color "#6d28d9"` to match relationship arrow color |

| Arrow type | `--stroke` | `--stroke-style` | `--sw` | Notes |
|-----------|-----------|-----------------|--------|-------|
| One-to-many (1:N) | `#6d28d9` | `solid` | `2` | Standard FK relationship |
| Many-to-many (M:N) | `#6d28d9` | `dashed` | `2` | Via junction table |
| One-to-one (1:1) | `#6d28d9` | `solid` | `1` | Thinner to distinguish |
| Optional (0..1) | `#6d28d9` | `dotted` | `1` | Optional FK |

### Relationship arrows (Rule 23 — explicit coordinates, never `element connect`)

**Do NOT use `element connect`** for ER relationships. When multiple arrows share a source or target entity, Excalidraw's auto-router bundles them at the same edge point, causing visual overlap. Use explicit `add arrow --x --y --ex --ey` with staggered Y coordinates instead.

**Pattern:**
```bash
# Exit source right edge at y=EDGE_Y, enter target left edge at same y
add arrow --x SOURCE_RIGHT --y EDGE_Y --ex TARGET_LEFT --ey EDGE_Y \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
# Cardinality label 16px above arrow midpoint
add text --x MID_X --y $((EDGE_Y - 16)) --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null
```

**Stagger Y by 30px** when multiple arrows exit or enter the same edge:
- First arrow: `EDGE_Y = entity_center_y - 15`
- Second arrow: `EDGE_Y = entity_center_y + 15`

**Skip connections** (arrow that must bypass an intermediate entity): use a **diagonal** — exit source at `y = center_y + 15`, enter target at `y = center_y - 15`. The diagonal angle makes it visually distinct from horizontal same-row arrows.

| Relationship | label | `--stroke` | `--sw` | `--stroke-style` |
|---|---|---|---|---|
| One-to-many (1:N) | `"1..N"` | `#6d28d9` | `2` | `solid` |
| Many-to-many (M:N) | `"M..N"` | `#6d28d9` | `2` | `dashed` |
| One-to-one (1:1) | `"1..1"` | `#6d28d9` | `1` | `solid` |
| Optional (0..1) | `"0..1"` | `#6d28d9` | `1` | `dotted` |

For arrowheads use `--end-arrowhead arrow` (FK direction, points to "many" side), `--start-arrowhead none`.

---

## Common pitfalls

1. **Entity name overlaps attribute text** — NEVER use `--label` on entity rectangles. The `--label` option renders text at the vertical center of the box, overlapping attributes. Instead: add a separate `add text` at `entity_y + 12` for the name, a `add line` at `entity_y + 34` for the divider, and start attributes at `entity_y + 46`.

2. **Junction tables look the same as regular tables** — Use `--fill-style hachure` for weak or junction entities (e.g. `post_tags`, `order_items`) to distinguish them visually from strong entities.

3. **Too many attributes per box** — Limit displayed attributes to 5–7 most important fields. Add a trailing `...` text line if there are more. A full schema dump in a diagram is unreadable.

4. **Entity boxes too narrow** — Entity names and attributes use `w=200`. For longer entity names (> 12 chars), check Rule 3: `min_w = max(120, len * 9.6 + 32)`. For "post_tags" (9 chars): 9×9.6+32=123.4 → use 130, but 200 is fine as it's wider.

5. **Arrow label collision** — When multiple relationships connect to the same entity, their labels can overlap. Offset relationship arrows by connecting to different sides of the entity. The CLI auto-routes, but placing source entities at different grid positions naturally distributes connection angles.

6. **Forgetting row 2 y-offset** (Rule 1) — Row 2 at y=320 is fine (≥ 150). But if you add a title or legend above, verify the first entity row y ≥ 150.

7. **Same-column adjacent entities at same y** (Rule 20) — Entities in the same row share y-coordinate. Ensure ≥ 60px gap (280px center spacing with 200px width = 80px gap — compliant).

---

## Worked example

Blog schema: `users`, `posts`, `comments`, `tags`, `post_tags`

### Entity definitions

| Entity | Attributes (displayed) | Grid position |
|--------|------------------------|---------------|
| users | PK id, name, email, created_at | col1 row1 |
| posts | PK id, FK user_id, title, body, published_at | col2 row1 |
| comments | PK id, FK post_id, FK user_id, body, created_at | col3 row1 |
| tags | PK id, name, slug | col1 row2 |
| post_tags | PK post_id (FK), PK tag_id (FK) | col2 row2 (junction) |

### Relationships

| From | To | Cardinality | Notes |
|------|----|-------------|-------|
| users | posts | 1..N | A user writes many posts |
| posts | comments | 1..N | A post has many comments |
| users | comments | 1..N | A user writes many comments |
| posts | post_tags | 1..N | A post has many tag associations |
| tags | post_tags | 1..N | A tag has many post associations |

### Planning table

| Entity | x | y | w | h |
|--------|---|---|---|---|
| users | 80 | 100 | 200 | 160 |
| posts | 360 | 100 | 200 | 180 |
| comments | 640 | 100 | 200 | 180 |
| tags | 80 | 320 | 200 | 140 |
| post_tags | 360 | 320 | 200 | 140 |

### Shell commands

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"

CLI=$(which excalidraw-agent-cli)
P=/tmp/blog-er.excalidraw
OUT="/tmp/blog-er.png"

add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

rm -f "$P"
$CLI --json project new --name "blog-er" --output "$P" > /dev/null

# Title
add text --x 80 --y 30 --fs 20 --ff 2 --color "#1e293b" \
  -t "Blog Schema — Entity Relationship Diagram" > /dev/null

# ── ENTITY: users (col1, row1) x=80, y=100, w=200, h=160
# Note: NO --label; add entity name as text at entity_y+12 to avoid center overlap
USERS=$(add rectangle --x 80 --y 100 -w 200 -h 160 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 92 --y 112 --fs 13 --ff 2 --color "#6d28d9" -t "users" > /dev/null
add line --x 80 --y 134 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 90 --y 146 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 90 --y 164 --fs 12 --ff 3 --color "#374151" -t "    name" > /dev/null
add text --x 90 --y 182 --fs 12 --ff 3 --color "#374151" -t "    email" > /dev/null
add text --x 90 --y 200 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null
add text --x 90 --y 218 --fs 12 --ff 3 --color "#374151" -t "    password_hash" > /dev/null

# ── ENTITY: posts (col2, row1) x=360, y=100, w=200, h=180
POSTS=$(add rectangle --x 360 --y 100 -w 200 -h 180 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 372 --y 112 --fs 13 --ff 2 --color "#6d28d9" -t "posts" > /dev/null
add line --x 360 --y 134 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 370 --y 146 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 370 --y 164 --fs 12 --ff 3 --color "#6d28d9" -t "FK  user_id" > /dev/null
add text --x 370 --y 182 --fs 12 --ff 3 --color "#374151" -t "    title" > /dev/null
add text --x 370 --y 200 --fs 12 --ff 3 --color "#374151" -t "    body" > /dev/null
add text --x 370 --y 218 --fs 12 --ff 3 --color "#374151" -t "    published_at" > /dev/null
add text --x 370 --y 236 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: comments (col3, row1) x=640, y=100, w=200, h=180
COMMENTS=$(add rectangle --x 640 --y 100 -w 200 -h 180 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 652 --y 112 --fs 13 --ff 2 --color "#6d28d9" -t "comments" > /dev/null
add line --x 640 --y 134 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 650 --y 146 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 650 --y 164 --fs 12 --ff 3 --color "#6d28d9" -t "FK  post_id" > /dev/null
add text --x 650 --y 182 --fs 12 --ff 3 --color "#6d28d9" -t "FK  user_id" > /dev/null
add text --x 650 --y 200 --fs 12 --ff 3 --color "#374151" -t "    body" > /dev/null
add text --x 650 --y 218 --fs 12 --ff 3 --color "#374151" -t "    created_at" > /dev/null

# ── ENTITY: tags (col1, row2) x=80, y=320, w=200, h=130
TAGS=$(add rectangle --x 80 --y 320 -w 200 -h 130 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 92 --y 332 --fs 13 --ff 2 --color "#6d28d9" -t "tags" > /dev/null
add line --x 80 --y 354 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 90 --y 366 --fs 12 --ff 3 --color "#1e40af" -t "PK  id" > /dev/null
add text --x 90 --y 384 --fs 12 --ff 3 --color "#374151" -t "    name" > /dev/null
add text --x 90 --y 402 --fs 12 --ff 3 --color "#374151" -t "    slug" > /dev/null

# ── ENTITY: post_tags (col2, row2) x=360, y=320, w=200, h=100  [junction — hachure]
POST_TAGS=$(add rectangle --x 360 --y 320 -w 200 -h 100 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style hachure --roughness 0 --sw 2)
add text --x 372 --y 332 --fs 13 --ff 2 --color "#6d28d9" -t "post_tags" > /dev/null
add line --x 360 --y 354 --points "0,0 200,0" --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null
add text --x 370 --y 366 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK  post_id" > /dev/null
add text --x 370 --y 384 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK  tag_id" > /dev/null

# ── Relationships (Rule 23 — explicit add arrow, staggered Y, NO element connect)
# Entity edges: users right=280 cy=180, posts left=360 right=560 cy=190,
#               comments left=640 cy=190, tags right=280 cy=385, post_tags left=360 cy=370

# users → posts: exit users right at y=170, enter posts left at y=170
add arrow --x 280 --y 170 --ex 360 --ey 170 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 296 --y 154 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# users → comments (skip: diagonal exits users at y=200, enters comments at y=150)
add arrow --x 280 --y 200 --ex 640 --ey 150 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 430 --y 156 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# posts → comments: exit posts right at y=200, enter comments left at y=200
add arrow --x 560 --y 200 --ex 640 --ey 200 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 578 --y 184 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# posts → post_tags: vertical, posts bottom-center → post_tags top-center
add arrow --x 460 --y 280 --ex 460 --ey 320 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 468 --y 293 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

# tags → post_tags: exit tags right at y=385, enter post_tags left at y=370
add arrow --x 280 --y 370 --ex 360 --ey 370 \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --start-arrowhead none --end-arrowhead arrow > /dev/null
add text --x 296 --y 354 --fs 11 --ff 2 --color "#6d28d9" -t "1..N" > /dev/null

$CLI -p "$P" export png --output "$OUT" --overwrite
echo "Exported: $OUT"
```

### Visual grid

```
Col 1             Col 2             Col 3
┌──────────┐      ┌──────────┐      ┌──────────┐
│  users   │─1:N─▶│  posts   │─1:N─▶│ comments │
│ PK id    │      │ PK id    │      │ PK id    │
│ name     │      │ FK user_id│     │ FK post_id│
│ email    │      │ title    │      │ FK user_id│
│ ...      │─1:N──┼──────────┼──1:N─▶ body    │
└──────────┘      │ body     │      └──────────┘
     │            └──────────┘
     │                 │ 1:N
     │                 ▼
┌──────────┐      ┌──────────┐
│  tags    │─1:N─▶│post_tags │
│ PK id    │      │PK FK post_id│
│ name     │      │PK FK tag_id│
│ slug     │      └──────────┘
└──────────┘      (hachure fill = junction/weak)
```
