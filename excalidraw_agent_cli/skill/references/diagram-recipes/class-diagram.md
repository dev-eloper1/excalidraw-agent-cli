# Class Diagram Recipe

## When to use

Use a class diagram when you need to communicate **the static structure of a system** — what entities exist, what data they hold, and how they relate to each other. The key signal is a set of named types with fields/methods and typed relationships (inheritance, composition, association).

Choose this pattern when:
- You have 2–8 domain classes with named attributes
- Relationships include inheritance (`extends`/`implements`), composition (`has-a`), or association (`knows-about`)
- The narrative is "what is in the system and how types connect"
- Stakeholders need to understand the data model, ORM schema, or domain model

Do NOT use for: runtime behavior (use sequence diagram), deployment topology (use architecture diagram), or scheduled work (use Gantt).

---

## Layout template

```
Canvas: 1200 × 800px, origin top-left (0, 0)

Title: x=20, y=15, --fs 20 --ff 2   (baseline ≈ y=37, Rule 21)
First element at y=120 minimum (37 + 60 = 97 → use 120 for clean grid, Rule 21 ✓)

Grid layout:
  GRID_START_X=100       # left edge of first column
  GRID_START_Y=120       # top edge of first row
  H_SPACING=280          # horizontal distance between class box left edges
  V_SPACING=200          # vertical distance between class box top edges

  Column x values:
    Col 0: x = 100
    Col 1: x = 100 + 280  = 380
    Col 2: x = 100 + 560  = 660
    Col 3: x = 100 + 840  = 940  (optional 4th column)

  Row y values:
    Row 0: y = 120
    Row 1: y = 120 + 200  = 320
    Row 2: y = 120 + 400  = 520  (optional 3rd row)

Class box geometry:
  CLASS_W=200            # class box width (fits most 2-word names + fields)
  CLASS_NAME_H=40        # height reserved for class name header
  FIELD_ROW_H=22         # height per attribute row
  CLASS_H = CLASS_NAME_H + (num_fields * FIELD_ROW_H) + 10  (bottom padding)

  Example with 3 fields: CLASS_H = 40 + (3*22) + 10 = 116 → use 120
  Example with 5 fields: CLASS_H = 40 + (5*22) + 10 = 160

Divider line (separates class name header from attributes):
  x = CLASS_X              # same x as class box
  y = CLASS_Y + CLASS_NAME_H   # just below the header area
  --points "0,0 CLASS_W,0"     # horizontal line spanning full class width

Attribute text block (placed inside box, below divider):
  x = CLASS_X + 10        # 10px indent
  y = CLASS_Y + CLASS_NAME_H + 6   # 6px padding below divider
  --ff 3 (monospace) --fs 12 --color "#6d28d9"

Named spacing variables:
  GRID_START_X=100
  GRID_START_Y=120
  H_SPACING=280
  V_SPACING=200
  CLASS_W=200
  CLASS_NAME_H=40
  FIELD_ROW_H=22
```

**CRITICAL — Class name rendering:**
Do NOT use `--label` on the class box rectangle. `--label` renders text at the vertical center of the box, which overlaps the attribute fields. Instead:
- Add the class box rectangle with NO `--label`
- Add a separate `add text` for the class name, positioned in the header zone:
  `add text --x <CLASS_X + 10> --y <CLASS_Y + 12> --fs 14 --ff 2 --color "#6d28d9" -t "ClassName"`

**Draw order:**
1. Title text
2. Class box rectangles (NO `--label` — class names added as separate text in step 3)
3. Class name text elements (`add text` in header zone: y = CLASS_Y + 12)
4. Divider lines (one per class, separating name from attributes)
5. Attribute text elements (field names inside each class box)
6. Relationship arrows (`element connect`)

**Coordinate planning table (placeholder labels):**

| ID var    | Label       | x    | y    | w    | h    | col | row |
|-----------|-------------|------|------|------|------|-----|-----|
| CLASS_A   | ClassA      | 100  | 120  | 200  | 120  | 0   | 0   |
| CLASS_B   | ClassB      | 380  | 120  | 200  | 120  | 1   | 0   |
| CLASS_C   | ClassC      | 660  | 120  | 200  | 120  | 2   | 0   |
| CLASS_D   | ClassD      | 100  | 320  | 200  | 120  | 0   | 1   |
| CLASS_E   | ClassE      | 380  | 320  | 200  | 120  | 1   | 1   |

---

## Color and style defaults

### Class boxes

| Node type       | `--bg`    | `--stroke` | `--fill-style` | Notes                   |
|-----------------|-----------|------------|----------------|--------------------------|
| Concrete class  | `#ddd6fe` | `#6d28d9`  | `solid`        | Data/Storage semantic    |
| Abstract class  | `#ede9fe` | `#6d28d9`  | `hachure`      | Lighter/sketchy to signal abstract |
| Interface       | `#ede9fe` | `#6d28d9`  | `hachure`      | Visually lighter than concrete class |
| Enum            | `#e2e8f0` | `#334155`  | `solid`        | Neutral — enums are value types |

Class box style: `--roughness 0 --sw 2`

### Divider lines

| Property        | Value      |
|-----------------|------------|
| `--stroke`      | `#6d28d9`  | Matches class stroke color |
| `--sw`          | `1`        | Thin horizontal divider |
| `--stroke-style`| `solid`    |

### Attribute text

| Property    | Value      | Notes                               |
|-------------|------------|--------------------------------------|
| `--ff`      | `3`        | Cascadia monospace — code feel       |
| `--fs`      | `12`       | Minimum readable (Rule 14)           |
| `--color`   | `#6d28d9`  | Matches class theme                  |

### Relationship arrows

| Relationship              | `--end-arrowhead` | `--start-arrowhead` | `--stroke` | `--stroke-style` | `--sw` |
|---------------------------|-------------------|---------------------|------------|------------------|--------|
| Inheritance (`extends`)   | `triangle`        | `none`              | `#6d28d9`  | `solid`          | `2`    |
| Implementation (`implements`) | `triangle`    | `none`              | `#6d28d9`  | `dashed`         | `2`    |
| Composition (`has-a, owns`) | `arrow`         | `none`              | `#6d28d9`  | `solid`          | `2`    |
| Association (`references`) | `arrow`          | `none`              | `#94a3b8`  | `solid`          | `1`    |
| Dependency (`uses`)       | `arrow`           | `none`              | `#94a3b8`  | `dashed`         | `1`    |

> **Available arrowhead values:** `arrow`, `bar`, `dot`, `triangle`, `circle`, or omit for none.
> Use `--end-arrowhead triangle` for inheritance (open triangle pointing to parent/interface).
> Composition "filled diamond" is not a native arrowhead type — approximate by adding a `--label "◆"` on the arrow or by placing a small diamond shape at the source end.

---

## Common pitfalls

1. **Class name label not fitting the box width.** Apply Rule 3: `min_width = max(120, len(label) * 9.6 + 32)`. For "BlogPost" (8 chars): max(120, 109) = 120. For "CommentAuthor" (13 chars): max(120, 157) = 160 → use 170. Always check before setting `CLASS_W`.

2. **Divider line width not matching class box width.** The `--points` for the divider must be `"0,0 CLASS_W,0"` — a horizontal segment exactly as wide as the class box. If CLASS_W=200, use `--points "0,0 200,0"`.

3. **Attribute text placed outside class box.** Attribute text y must satisfy: `CLASS_Y + CLASS_NAME_H + 6 ≤ text_y ≤ CLASS_Y + CLASS_H - 12`. For each additional field row, add `FIELD_ROW_H=22` to the y of the previous field.

4. **All relationship arrows look the same.** Use `--stroke-style dashed` for implements/dependency and `--stroke-style solid` for concrete relationships. Use `--end-arrowhead triangle` for inheritance vs `arrow` for association — this is the primary visual differentiator (Rule 15).

5. **Classes too close together — arrows visually merge.** With CLASS_W=200 and H_SPACING=280, the gap between class right edge and next class left edge is 280-200=80px, which satisfies Rule 2 (≥40px). Do not reduce H_SPACING below 250 (50px gap minimum).

6. **Title overlap with first row.** Title at y=15, fs=20 → baseline ≈ y=37. First class box at y=120 → clearance = 83px ≥ 60px (Rule 21 satisfied). Do not place classes above y=97.

7. **Text inside dark-bg class box unreadable.** The recommended class fill `#ddd6fe` is light purple — `#6d28d9` stroke provides good contrast. If you switch to a dark fill for emphasis, remember to use `--stroke "#e2e8f0"` (Rule 22).

8. **Inheritance arrow direction confusion.** The arrowhead points TO the parent (superclass), not to the child. Draw `element connect --from ChildClass --to ParentClass --end-arrowhead triangle`. The child "extends" the parent, so the arrow runs child → parent.

---

## Worked example

**Scenario:** Blog system — `Post`, `Comment`, `User` classes with fields and relationships.

**Class definitions:**
```
User:
  - id: Long
  - username: String
  - email: String
  - createdAt: Date

Post:
  - id: Long
  - title: String
  - body: String
  - authorId: Long
  - createdAt: Date

Comment:
  - id: Long
  - text: String
  - postId: Long
  - authorId: Long
```

**Relationships:**
- `Post` has-a `User` (author): association arrow Post → User
- `Comment` has-a `Post` (belongs to): composition arrow Comment → Post
- `Comment` has-a `User` (author): association arrow Comment → User

**Grid placement:**
```
User:    col=0, row=0  → x=100, y=120, h=128 (4 fields: 40+4*22+10)
Post:    col=1, row=0  → x=380, y=120, h=150 (5 fields: 40+5*22+10)
Comment: col=2, row=0  → x=660, y=120, h=128 (4 fields: 40+4*22+10)
```

```bash
#!/usr/bin/env bash
set -e

export PATH="/Users/bhushan/Documents/excalidraw/agent-harness/.venv/bin:/Users/bhushan/.nvm/versions/node/v22.9.0/bin:$PATH"
CLI=$(which excalidraw-agent-cli)
P=/tmp/class-diagram-worked-example.excalidraw

add() {
  $CLI -p "$P" --json element add "$@" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])"
}

rm -f "$P"
$CLI --json project new --name "class-diagram-worked-example" --output "$P" > /dev/null

# ── Title (Rule 21: y=15, baseline≈37; first class at y=120 → 83px clearance ✓) ──
add text --x 20 --y 15 --fs 20 --ff 2 --color "#1e293b" \
  -t "Blog System — Class Diagram" > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS: User  (col=0, x=100, y=120, w=200, h=128)
# ═══════════════════════════════════════════════════════════════════════════════
USER=$(add rectangle --x 100 --y 120 -w 200 -h 128 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
# Class name as separate text in header zone (y = CLASS_Y + 12)
add text --x 110 --y 132 --fs 14 --ff 2 --color "#6d28d9" -t "User" > /dev/null

# Divider line below class name header (y = 120 + 40 = 160)
add line --x 100 --y 160 --points "0,0 200,0" \
  --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null

# Attribute text (y starts at 160 + 6 = 166, step 22px)
add text --x 110 --y 166 --fs 12 --ff 3 --color "#6d28d9" -t "id: Long"         > /dev/null
add text --x 110 --y 188 --fs 12 --ff 3 --color "#6d28d9" -t "username: String"  > /dev/null
add text --x 110 --y 210 --fs 12 --ff 3 --color "#6d28d9" -t "email: String"     > /dev/null
add text --x 110 --y 232 --fs 12 --ff 3 --color "#6d28d9" -t "createdAt: Date"   > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS: Post  (col=1, x=380, y=120, w=200, h=150)
# ═══════════════════════════════════════════════════════════════════════════════
POST=$(add rectangle --x 380 --y 120 -w 200 -h 150 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 390 --y 132 --fs 14 --ff 2 --color "#6d28d9" -t "Post" > /dev/null

# Divider line (y = 120 + 40 = 160)
add line --x 380 --y 160 --points "0,0 200,0" \
  --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null

# Attributes
add text --x 390 --y 166 --fs 12 --ff 3 --color "#6d28d9" -t "id: Long"         > /dev/null
add text --x 390 --y 188 --fs 12 --ff 3 --color "#6d28d9" -t "title: String"    > /dev/null
add text --x 390 --y 210 --fs 12 --ff 3 --color "#6d28d9" -t "body: String"     > /dev/null
add text --x 390 --y 232 --fs 12 --ff 3 --color "#6d28d9" -t "authorId: Long"   > /dev/null
add text --x 390 --y 254 --fs 12 --ff 3 --color "#6d28d9" -t "createdAt: Date"  > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS: Comment  (col=2, x=660, y=120, w=200, h=128)
# ═══════════════════════════════════════════════════════════════════════════════
COMMENT=$(add rectangle --x 660 --y 120 -w 200 -h 128 \
  --bg "#ddd6fe" --stroke "#6d28d9" --fill-style solid --roughness 0 --sw 2)
add text --x 670 --y 132 --fs 14 --ff 2 --color "#6d28d9" -t "Comment" > /dev/null

# Divider line (y = 120 + 40 = 160)
add line --x 660 --y 160 --points "0,0 200,0" \
  --stroke "#6d28d9" --sw 1 --stroke-style solid > /dev/null

# Attributes
add text --x 670 --y 166 --fs 12 --ff 3 --color "#6d28d9" -t "id: Long"         > /dev/null
add text --x 670 --y 188 --fs 12 --ff 3 --color "#6d28d9" -t "text: String"     > /dev/null
add text --x 670 --y 210 --fs 12 --ff 3 --color "#6d28d9" -t "postId: Long"     > /dev/null
add text --x 670 --y 232 --fs 12 --ff 3 --color "#6d28d9" -t "authorId: Long"   > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════════════════
# Post →(authored by)→ User: association (Post knows User via authorId)
$CLI -p "$P" --json element connect \
  --from "$POST" --to "$USER" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --end-arrowhead arrow --start-arrowhead none > /dev/null

# Comment →(belongs to)→ Post: composition (Comment owns ref to Post)
$CLI -p "$P" --json element connect \
  --from "$COMMENT" --to "$POST" \
  --stroke "#6d28d9" --sw 2 --stroke-style solid \
  --end-arrowhead arrow --start-arrowhead none > /dev/null

# Comment →(authored by)→ User: association
$CLI -p "$P" --json element connect \
  --from "$COMMENT" --to "$USER" \
  --stroke "#94a3b8" --sw 1 --stroke-style solid \
  --end-arrowhead arrow --start-arrowhead none > /dev/null

# ── Relationship labels (free text below arrow midpoints) ─────────────────────
add text --x 240 --y 290 --fs 12 --ff 2 --color "#6b7280" -t "authored by" > /dev/null
add text --x 530 --y 290 --fs 12 --ff 2 --color "#6b7280" -t "belongs to"  > /dev/null

$CLI -p "$P" export png --output /tmp/class-diagram-worked-example.png --overwrite
echo "Exported: /tmp/class-diagram-worked-example.png"
```
