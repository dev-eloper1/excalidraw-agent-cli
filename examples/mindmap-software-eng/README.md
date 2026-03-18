# Modern Software Engineering — Mind Map

A 3-level asymmetric mind map with 50+ nodes. Branches have different depths:
Frontend has 4 levels (root → Frontend → React/Vue → Hooks & State), while
some Architecture leaves have no children. Dagre computes all positions automatically.

![Mind Map](./diagram.png)

## Prompt

```
Draw a comprehensive mind map of Modern Software Engineering. Root node at left.
Five main branches: Frontend (React/Vue, TypeScript, Styling, Testing — each with
2 sub-tools), Backend (Node/Python, API Design, Auth — each with 2 sub-tools),
Data (PostgreSQL, Caching, Search — each with 2 sub-tools), DevOps (Containers,
CI/CD, Observability — each with 2 sub-tools), Architecture (Patterns, Messaging,
Security — each with 2 sub-tools). Color-code each branch distinctly.
```

## Generation time

~6 seconds (dagre layout + Puppeteer render)

## Files generated

| File | Description |
|------|-------------|
| `graph.json` | Declarative graph: nodes, edges, colors — no coordinates |
| `diagram.excalidraw` | Full Excalidraw JSON with dagre-computed positions |
| `diagram.svg` | Vector output — scalable, embeddable |
| `diagram.png` | Raster output — for docs and previews |

## Commands

```bash
# 1. Compute layout and produce the .excalidraw file
node dagre-layout.js examples/mindmap-software-eng/graph.json \
  --output examples/mindmap-software-eng/diagram.excalidraw

# 2. Export to PNG (Puppeteer renders the real Excalidraw engine)
excalidraw-agent-cli \
  --project examples/mindmap-software-eng/diagram.excalidraw \
  export png --output examples/mindmap-software-eng/diagram.png --overwrite

# 3. Export to SVG (vector, infinitely scalable)
excalidraw-agent-cli \
  --project examples/mindmap-software-eng/diagram.excalidraw \
  export svg --output examples/mindmap-software-eng/diagram.svg --overwrite
```

## Why dagre for mind maps

Mind maps with 50+ nodes would require computing hundreds of x,y coordinates
manually. Dagre's `LR` (left-to-right) rank layout handles this automatically:
each "rank" (depth level) gets its own column, nodes within a rank are spaced
evenly, and branches with more children get proportionally more vertical space.
The asymmetry — some branches going 3 levels deep, others only 2 — emerges
naturally from the edge structure.
