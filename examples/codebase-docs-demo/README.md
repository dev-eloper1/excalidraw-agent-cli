# Excalidraw Skill System — Codebase Documentation Demo

This example documents the file structure of the `excalidraw` Claude skill — the set of markdown files that tell Claude Code how to generate Excalidraw diagrams. The skill is loaded at conversation start and gives Claude a vocabulary of shapes, colors, layout rules, and diagram-type recipes to draw from.

The skill is organized around a single entry point (`SKILL.md`) that references five supporting files for specifics. Those reference files cover the color palette, layout coordinate templates, visual patterns, CLI command syntax, and a rubric for choosing which diagram type fits a given request. A dedicated `diagram-recipes/` folder holds one per-type recipe file for each of the eight supported diagram types: flowchart, sequence, mind map, class diagram, state diagram, ER diagram, Gantt chart, and architecture diagram.

When Claude receives a diagramming request it reads `SKILL.md` first, then pulls in whichever reference files and recipe are needed for that specific task. The result is a layered, on-demand loading strategy: the core philosophy and workflow live in one place, while the detailed lookup tables and coordinate templates stay in separate files to avoid overwhelming the context window.

## Architecture Diagram

![Architecture diagram showing the excalidraw skill file structure](skill-architecture.png)

## Structural Inventory

### Nodes visible in the diagram

| Node | Zone | Description |
|------|------|-------------|
| `SKILL.md` | Core Skill File (center, dark) | Entry point — workflow, philosophy, quality checklist |
| `color-palette.md` | Reference Files (left, green) | All hex values for fills, strokes, arrows, and zones |
| `layout-rules.md` | Reference Files (left, green) | Coordinate templates and spacing rules |
| `patterns.md` | Reference Files (left, green) | Visual pattern library with CLI examples |
| `cli-reference.md` | Reference Files (left, green) | Full CLI command syntax and bash helper patterns |
| `diagram-type-rubric.md` | Reference Files (left, light green) | Decision table for selecting diagram type |
| `diagram-recipes/` | Recipes Folder (right, purple) | Folder node — bridge between SKILL.md and recipe files |
| `flowchart.md` | Recipe Files (right, lavender) | Layout template + color defaults for flowcharts |
| `sequence.md` | Recipe Files (right, lavender) | Layout template + pitfalls for sequence diagrams |
| `mindmap.md` | Recipe Files (right, lavender) | Layout template for mind maps |
| `class-diagram.md` | Recipe Files (right, lavender) | Layout template for UML class diagrams |
| `state-diagram.md` | Recipe Files (right, lavender) | Layout template for state machines |
| `er-diagram.md` | Recipe Files (right, lavender) | Layout template for entity-relationship diagrams |
| `gantt.md` | Recipe Files (right, lavender) | Layout template for Gantt / timeline charts |
| `architecture.md` | Recipe Files (right, lavender) | Layout template for layered architecture diagrams |

### Connections visible in the diagram

| From | To | Style | Meaning |
|------|----|-------|---------|
| `SKILL.md` | `color-palette.md` | Gray solid arrow | SKILL.md reads this reference file |
| `SKILL.md` | `layout-rules.md` | Gray solid arrow | SKILL.md reads this reference file |
| `SKILL.md` | `patterns.md` | Gray solid arrow | SKILL.md reads this reference file |
| `SKILL.md` | `cli-reference.md` | Gray solid arrow | SKILL.md reads this reference file |
| `SKILL.md` | `diagram-type-rubric.md` | Gray solid arrow | SKILL.md reads this reference file |
| `SKILL.md` | `diagram-recipes/` | Purple solid arrow | SKILL.md references the recipes folder |
| `diagram-recipes/` | `flowchart.md` | Purple dashed arrow | Folder contains this recipe |
| `diagram-recipes/` | `sequence.md` | Purple dashed arrow | Folder contains this recipe |
| `diagram-recipes/` | `mindmap.md` | Purple dashed arrow | Folder contains this recipe |
| `diagram-recipes/` | `class-diagram.md` | Purple dashed arrow | Folder contains this recipe |
| `diagram-recipes/` | `state-diagram.md` | Purple dashed arrow | Folder contains this recipe |
| `diagram-recipes/` | `er-diagram.md` | Purple dashed arrow | Folder contains this recipe |
| `diagram-recipes/` | `gantt.md` | Purple dashed arrow | Folder contains this recipe |
| `diagram-recipes/` | `architecture.md` | Purple dashed arrow | Folder contains this recipe |
