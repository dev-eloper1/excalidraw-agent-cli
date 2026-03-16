# Animated Diagrams — Research & Architecture Plan

**Date:** 2026-03-16  
**Status:** Research complete, implementation pending  
**Motivation:** ByteByteGo-style animated diagram sequences with moving arrows, glow, sequential reveal

---

## What ByteByteGo Actually Does

ByteByteGo produces **screen-recorded MP4 video**, not interactive SVG. The animation technique is:
- After Effects, Apple Motion, or Keynote + screen recording
- Core technique: **sequential reveal** — elements appear one at a time, arrows draw in, labels fade in
- Animation sophistication is low; diagram design quality is high

**What's NOT happening:** No Manim, D3, or real-time SVG animation.

**Implication:** We can match the visual quality with CSS alone. The production gap is not animation complexity — it's that no tool takes an *existing diagram file* and animates it semantically.

---

## Core Animation Techniques (from Animated Mermaid)

Mermaid renders to queryable SVG (nodes as `<g>/<rect>`, edges as `<path>`). These techniques layer on top:

### 1. Arrow Draw-On (stroke-dashoffset trick)
```css
/* 1. Measure path.getTotalLength() → L */
/* 2. Set both to L (arrow hidden) */
.arrow { stroke-dasharray: L; stroke-dashoffset: L; }
/* 3. Animate offset to 0 → arrow draws itself */
@keyframes drawArrow {
  from { stroke-dashoffset: L; }
  to   { stroke-dashoffset: 0; }
}
```

### 2. Flowing Dashes (data-flow effect)
```css
.edge path {
  stroke-dasharray: 8 4;
  animation: flow 1s linear infinite;
}
@keyframes flow {
  from { stroke-dashoffset: 12; }
  to   { stroke-dashoffset: 0; }
}
```
Dashes appear to travel along the arrow path, showing direction of data flow.

### 3. Sequential Reveal
```css
/* Enumerate nodes/edges in topological sort order */
.node:nth-child(1) { animation: fadeIn 0.4s ease 0.0s both; }
.node:nth-child(2) { animation: fadeIn 0.4s ease 0.4s both; }
.node:nth-child(3) { animation: fadeIn 0.4s ease 0.8s both; }
```

### 4. Glow / Pulse
```svg
<filter id="glow">
  <feGaussianBlur stdDeviation="3" result="blur"/>
  <feBlend in="SourceGraphic" in2="blur" mode="normal"/>
</filter>
```
Toggle via CSS animation: `filter: url(#glow)` on/off.

### 5. Scale-In (for nodes)
```css
.node {
  transform-box: fill-box;      /* critical for SVG elements */
  transform-origin: center;
  animation: scaleIn 0.3s ease-out both;
}
@keyframes scaleIn {
  from { transform: scale(0); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}
```

---

## SVG Animation Primitives

### Three layers available:

| Layer | Best for | Notes |
|-------|----------|-------|
| **SMIL** (`<animate>`, `<animateMotion>`) | Path-following ("packet traveling") | Supported but not recommended for new projects |
| **CSS keyframes** | Sequential reveal, stroke-draw, fade, glow | Modern standard. Cannot morph path shape (`d` attr) |
| **JavaScript (GSAP / Anime.js / WAAPI)** | Complex timeline sequencing, state machines | Full control; GSAP is industry standard |

### Key gotchas:
- `transform-box: fill-box` + `transform-origin: center` required for scale/rotate on SVG elements
- `animation-fill-mode: both` critical — keeps elements invisible before their animation starts
- Animated SVG in `<img>` tag is **frozen** — must be inline `<svg>` or `<object>`
- `<foreignObject>` text (used by Excalidraw for labels) cannot receive SVG filter effects on interior HTML
- Path morphing (`d` attribute) requires JS or SMIL; CSS cannot do it

---

## The Product Gap

No existing tool takes an **existing diagram file** and applies semantically-aware animation:

| Tool | Approach | Gap |
|------|----------|-----|
| Motion Canvas | Code-first TypeScript scenes | Must author from scratch |
| Remotion | React component per frame | Must author from scratch |
| D3.js | Data-join + transitions | Low-level, interactive only |
| Manim | Python scenes | Offline render, math-focused |
| Rive | Visual editor + state machine | Proprietary format |
| LottieFiles | After Effects → JSON | Requires AE authoring |
| **Us** | `.excalidraw` → animated SVG/HTML/GIF | **Unoccupied space** |

---

## Proposed Architecture: `excalidraw-animate`

### What Excalidraw gives us (two complementary artifacts)
1. **`.excalidraw` JSON** — semantic graph: element IDs, types, edge bindings (which nodes connect to which), labels, directionality
2. **Exported SVG** — rendered visuals with `data-id` attributes matching the JSON IDs

### Post-processor pipeline
```
Input:
  diagram.excalidraw  (JSON: element graph with IDs)
  diagram.svg         (rendered SVG with matching data-id attributes)

Steps:
  1. Parse .excalidraw JSON → build semantic graph (nodes, edges, labels)
  2. Parse SVG → build element map {id -> SVGElement}
  3. Topological sort of graph → default animation timeline
  4. Apply animation spec: inject <style> keyframes + <defs> filters
  5. Compute arrow path lengths (svg-path-properties or Puppeteer)
  6. Output: animated_diagram.svg or .html

Optional MP4/GIF:
  Puppeteer frame-grab → ffmpeg encode
```

### Effect Library (5 effects, 90% of use cases)

| Effect | Mechanism | Best for |
|--------|-----------|----------|
| `fadeIn` | `opacity: 0→1` | Zone backgrounds, labels |
| `drawArrow` | `stroke-dashoffset: L→0` | Showing connections being established |
| `flowDashes` | Infinite `stroke-dashoffset` loop | Data streams, continuous flows |
| `glowPulse` | `feGaussianBlur` filter toggled | Emphasizing the "current" component |
| `scaleIn` | `transform: scale(0)→scale(1)` | Node appearing in system |

### Animation Spec (JSON)
```json
[
  { "id": "abc123", "effect": "fadeIn",     "t": 0.0, "duration": 0.4 },
  { "id": "def456", "effect": "drawArrow",  "t": 0.5, "duration": 0.6 },
  { "id": "ghi789", "effect": "flowDashes", "t": 1.1, "duration": null },
  { "id": "jkl012", "effect": "glowPulse",  "t": 1.2, "duration": null }
]
```

### Auto-spec (zero user input required)
The `.excalidraw` graph has edge directionality → topological sort → assign:
- `fadeIn` delay = `rank × 0.4s` for nodes
- `drawArrow` at `t = source_rank × 0.4s + 0.3s` for each edge

This produces a useful sequential reveal animation automatically.

### CLI Design
```bash
# Output animated HTML (inline SVG + CSS)
excalidraw-agent-cli animate --input arch.excalidraw --output arch-animated.html

# Output GIF (via Puppeteer + ffmpeg)
excalidraw-agent-cli animate --input arch.excalidraw --output arch.gif --fps 24

# Animation presets
excalidraw-agent-cli animate --input arch.excalidraw --preset flow    # flowing dashes only
excalidraw-agent-cli animate --input arch.excalidraw --preset reveal  # sequential node reveal
excalidraw-agent-cli animate --input arch.excalidraw --preset none    # just static + CSS classes

# Custom spec
excalidraw-agent-cli animate --input arch.excalidraw --spec anim.json --output out.html
```

---

## Cognitive Value — Which Animations Actually Help

### High-value (comprehension-improving):

**Sequential node reveal** — builds mental model incrementally, reduces overwhelm from full graph  
Rule: reveal source nodes before destination nodes; animate connecting arrow after both endpoints visible

**Data flow animation** — answers "which direction does data go?" and "how does data get from A to B?"  
- Moving dashes: continuous flow (stream, pipe)
- Moving dot/packet: discrete message passing (RPC, queue)

**Emphasis via glow** — keeps spatial attention aligned with narration/text  
Should de-emphasize other nodes simultaneously (dim non-relevant nodes)

**State transition** — shows system before/after: new service appears, connection is re-routed  
The animation IS the information

### Low-value (avoid):
- Bounce/elastic easing — visual noise
- Continuous animations while other content is being processed
- Too-fast reveals (< 200ms) — viewer misses it
- All elements animating simultaneously — no sequential information

### Key timing rules:
- Min pause between reveals: **300-500ms**
- Arrow draw-on duration: **400-800ms**
- Flow dashes cycle: **~800ms per cycle**
- Total before user can pause: **< 10 seconds** (or add playback control)
- Contiguity principle: animate element AND its label simultaneously

---

## Technical Constraints

### Arrow draw-on path length
Must compute `path.getTotalLength()` server-side:
- Node.js: `svg-path-properties` package (pure JS, handles cubic Beziers)
- Or: Puppeteer `page.evaluate(() => el.getTotalLength())`

### Arrowhead timing
Arrowhead must appear at END of draw sequence:
- Set arrowhead `opacity: 0` initially
- Trigger `opacity: 1` at `t + duration` of the drawArrow effect

### `<foreignObject>` limitation
Excalidraw uses `<foreignObject>` for multi-line text. SVG filters won't apply to inner HTML.  
Workaround: apply glow to the parent shape element, not the text.

### Output formats
| Format | Embed method | Animations |
|--------|-------------|-----------|
| Animated SVG | Inline `<svg>` in HTML | ✓ CSS + SMIL |
| Animated SVG in `<img>` | Frozen — DO NOT USE | ✗ |
| HTML file | Full page | ✓ CSS + JS |
| GIF | Via Puppeteer + ffmpeg | ✓ (baked) |
| MP4 | Via Puppeteer + ffmpeg | ✓ (baked) |

---

## Implementation Phases

### Phase 1 — Static foundation
- `excalidraw-agent-cli animate` subcommand
- Parse `.excalidraw` + SVG, inject CSS `<style>` block
- `fadeIn` preset only: sequential reveal via topological sort
- Output: self-contained animated HTML

### Phase 2 — Arrow draw-on
- Integrate `svg-path-properties` for path length computation
- `drawArrow` effect
- Arrowhead reveal timing

### Phase 3 — Flow effects
- `flowDashes` effect (infinite loop)
- `glowPulse` effect (SVG filter injection)
- `scaleIn` effect

### Phase 4 — Export
- Puppeteer frame-grab pipeline
- ffmpeg GIF/MP4 encoding
- `--fps` and `--duration` controls

### Phase 5 — Skill integration
- Update `excalidraw` skill to offer `animate` as post-step
- Add `--animated` flag to skill output step
- Template: "Export animated version? `export html -o diagram.html --animate`"

---

## Dependencies

```json
{
  "svg-path-properties": "^1.3.0",  // path length calculation
  "puppeteer": "^21.0.0",           // already installed for PNG export
  "ffmpeg-static": "^5.2.0"        // optional: bundled ffmpeg for GIF/MP4
}
```

---

*Research synthesized from: ByteByteGo analysis, animated Mermaid implementations, SVG animation spec, cognitive load theory (Mayer 2009), Sweller's cognitive theory of multimedia learning.*
