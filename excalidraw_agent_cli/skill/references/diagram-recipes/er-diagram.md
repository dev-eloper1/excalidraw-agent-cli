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

### Cardinality labels

Since the CLI does not support crow's foot notation, add cardinality as **short text labels on the arrow** using `-l` in `element connect`:

| Relationship | `-l` value |
|---|---|
| One-to-many | `"1..N"` |
| Many-to-many | `"M..N"` |
| One-to-one | `"1..1"` |
| Zero-or-one | `"0..1"` |

For available arrowhead options, use `excalidraw-agent-cli element connect --help`. Options include: `arrow`, `bar`, `dot`, `triangle`, `circle`, or none. Use `--end-arrowhead arrow` for FK direction (points to the "many" side). Use `--start-arrowhead bar` to indicate the "one" side when supported.

---

## Common pitfalls

1. **Attribute text overlaps entity border** — The entity box label (entity name) renders centered. Attribute text lines must start at `entity_y + 35` to clear the centered name. If the name is large, start attribute text at `entity_y + 45`.

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

conn() {
  local from="$1" to="$2" label="$3" color="$4" style="$5"
  local args=("--from" "$from" "--to" "$to")
  [[ -n "$label" ]] && args+=("-l" "$label")
  [[ -n "$color" ]] && args+=("--stroke" "$color")
  [[ -n "$style" ]] && args+=("--stroke-style" "$style")
  $CLI -p "$P" --json element connect "${args[@]}" > /dev/null
}

rm -f "$P"
$CLI --json project new --name "blog-er" --output "$P" > /dev/null

# Title
add text --x 80 --y 30 --fs 20 --ff 2 --color "#1e293b" \
  -t "Blog Schema — Entity Relationship Diagram" > /dev/null

# ── ENTITY: users (col1, row1) x=80, y=100
USERS=$(add rectangle --x 80 --y 100 -w 200 -h 160 \
  --label "users" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 90 --y 145 --fs 12 --ff 3 --color "#1e40af" -t "PK id" > /dev/null
add text --x 90 --y 163 --fs 12 --ff 3 --color "#374151" -t "name" > /dev/null
add text --x 90 --y 181 --fs 12 --ff 3 --color "#374151" -t "email" > /dev/null
add text --x 90 --y 199 --fs 12 --ff 3 --color "#374151" -t "created_at" > /dev/null
add text --x 90 --y 217 --fs 12 --ff 3 --color "#374151" -t "password_hash" > /dev/null

# ── ENTITY: posts (col2, row1) x=360, y=100
POSTS=$(add rectangle --x 360 --y 100 -w 200 -h 180 \
  --label "posts" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 370 --y 145 --fs 12 --ff 3 --color "#1e40af" -t "PK id" > /dev/null
add text --x 370 --y 163 --fs 12 --ff 3 --color "#6d28d9" -t "FK user_id" > /dev/null
add text --x 370 --y 181 --fs 12 --ff 3 --color "#374151" -t "title" > /dev/null
add text --x 370 --y 199 --fs 12 --ff 3 --color "#374151" -t "body" > /dev/null
add text --x 370 --y 217 --fs 12 --ff 3 --color "#374151" -t "published_at" > /dev/null
add text --x 370 --y 235 --fs 12 --ff 3 --color "#374151" -t "created_at" > /dev/null

# ── ENTITY: comments (col3, row1) x=640, y=100
COMMENTS=$(add rectangle --x 640 --y 100 -w 200 -h 180 \
  --label "comments" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 650 --y 145 --fs 12 --ff 3 --color "#1e40af" -t "PK id" > /dev/null
add text --x 650 --y 163 --fs 12 --ff 3 --color "#6d28d9" -t "FK post_id" > /dev/null
add text --x 650 --y 181 --fs 12 --ff 3 --color "#6d28d9" -t "FK user_id" > /dev/null
add text --x 650 --y 199 --fs 12 --ff 3 --color "#374151" -t "body" > /dev/null
add text --x 650 --y 217 --fs 12 --ff 3 --color "#374151" -t "created_at" > /dev/null

# ── ENTITY: tags (col1, row2) x=80, y=320
TAGS=$(add rectangle --x 80 --y 320 -w 200 -h 140 \
  --label "tags" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 90 --y 363 --fs 12 --ff 3 --color "#1e40af" -t "PK id" > /dev/null
add text --x 90 --y 381 --fs 12 --ff 3 --color "#374151" -t "name" > /dev/null
add text --x 90 --y 399 --fs 12 --ff 3 --color "#374151" -t "slug" > /dev/null

# ── ENTITY: post_tags (col2, row2) x=360, y=320  [junction — hachure]
POST_TAGS=$(add rectangle --x 360 --y 320 -w 200 -h 140 \
  --label "post_tags" \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style hachure --roughness 0 --sw 2)
add text --x 370 --y 363 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK post_id" > /dev/null
add text --x 370 --y 381 --fs 12 --ff 3 --color "#6d28d9" -t "PK FK tag_id" > /dev/null

# ── Relationships
# users → posts (1:N)
conn "$USERS"    "$POSTS"     "1..N" "#6d28d9" "solid"
# posts → comments (1:N)
conn "$POSTS"    "$COMMENTS"  "1..N" "#6d28d9" "solid"
# users → comments (1:N)
conn "$USERS"    "$COMMENTS"  "1..N" "#6d28d9" "solid"
# posts → post_tags (1:N)
conn "$POSTS"    "$POST_TAGS" "1..N" "#6d28d9" "solid"
# tags → post_tags (1:N)
conn "$TAGS"     "$POST_TAGS" "1..N" "#6d28d9" "solid"

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
