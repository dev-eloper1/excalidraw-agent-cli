# How the Excalidraw CLI Skill Works

The Excalidraw CLI skill is a structured, repeatable system for turning a natural-language diagramming request into a production-ready PNG (or SVG) embedded in a document. When a user asks to "draw a flowchart", "sketch the architecture", or "visualize this process", the skill activates a six-step pipeline rather than generating ad-hoc CLI commands. The pipeline starts with a **User Request** — the raw intent — and immediately moves to **Type Selection**, where the skill consults a diagram-type rubric to silently choose the best diagram category (flowchart, architecture, sequence, mind-map, etc.) before writing a single line of code. This front-loading of structure prevents the most common failure mode in diagram generation: choosing the wrong visual vocabulary for the concept.

Once a diagram type is confirmed, the skill performs **Content Sourcing** — either reading relevant source files and summarising discovered nodes and relationships (for codebase tasks) or deriving structure directly from the user's message (for conceptual tasks). It then **reads the recipe** file for the chosen type, which supplies a coordinate template, color palette defaults, and a list of common pitfalls. Armed with that layout blueprint, it **generates a bash script** that issues a sequence of `element add` and `element connect` commands against the CLI, places every node at pre-computed coordinates, and **exports the result** to a PNG using Puppeteer-backed rendering. No coordinates are guessed; every node's width is computed from its label length before the script runs.

![Flowchart diagram showing the excalidraw skill generation workflow](skill-workflow.png)

The export step hands off to a mandatory **Self-Inspection loop**. The skill reads the exported PNG visually and checks seven items: all nodes labeled and readable, no label text overlapping borders, all expected connections present, arrow directions correct, title clearance from the first element, light strokes on dark-background nodes, and color coding consistent with recipe defaults. If any item fails, the script is corrected and the export/inspect cycle repeats — up to three iterations. Only after the inspection passes does the skill produce the **Embed** snippet: a relative-path markdown image tag pointing to the exported file. This quality gate is what separates the skill from a one-shot code generator; diagrams that fail visual inspection are never delivered to the user unchanged.

---

## Structural Inventory

### Nodes

| Node | Shape | Role |
|------|-------|------|
| Start | Rounded rectangle (blue) | Entry point |
| User Request | Rectangle (green) | Captures the raw diagramming intent |
| Type Selection | Rectangle (green) | Consults diagram-type rubric, picks best type |
| Content Sourcing | Rectangle (green) | Reads source files or derives structure from message |
| Read Recipe | Rectangle (green) | Loads layout template and color defaults for chosen type |
| Generate Script | Rectangle (green) | Produces the bash CLI script with pre-computed coordinates |
| Export PNG | Rectangle (green) | Runs Puppeteer-backed render, writes PNG to disk |
| Self-Inspection | Rectangle (green) | Reads PNG; checks 7-item quality checklist |
| Inspection passes? | Diamond (amber) | Decision node — branches on pass/fail |
| Embed in Doc | Rectangle (green) | Inserts relative-path markdown image tag |
| Fix & Regenerate | Rectangle (red) | Corrects failing items, loops back (max 3x) |
| Done | Rounded rectangle (teal) | Terminal success state |

### Connections

| From | To | Label | Style |
|------|----|-------|-------|
| Start | User Request | — | Solid black |
| User Request | Type Selection | — | Solid black |
| Type Selection | Content Sourcing | — | Solid black |
| Content Sourcing | Read Recipe | — | Solid black |
| Read Recipe | Generate Script | — | Solid black |
| Generate Script | Export PNG | — | Solid black |
| Export PNG | Self-Inspection | — | Solid black |
| Self-Inspection | Inspection passes? | — | Solid black |
| Inspection passes? | Embed in Doc | yes | Solid green |
| Inspection passes? | Fix & Regenerate | no (max 3x) | Dashed red |
| Fix & Regenerate | Generate Script | retry | Dashed amber |
| Embed in Doc | Done | — | Solid green |
