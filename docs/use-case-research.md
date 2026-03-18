# Use Case Research & Expansion Brainstorm

*Recorded: 2026-03-17*

This document captures research into how Excalidraw is used today and where `excalidraw-agent-cli` has the highest leverage for new templates, recipes, and skill capabilities.

---

## What Excalidraw is used for today

### Official use cases (excalidraw.com / plus.excalidraw.com)

| Category | Types |
|---|---|
| Software & Architecture | System design, microservices, cloud (AWS/Azure/GCP), network topology, deployment diagrams |
| UML | Class, sequence, use case, activity, state machine, component |
| Product & UX | Wireframes (lo-fi and hi-fi), UI mockups, user flows, storyboards |
| Business & Ops | Flowcharts, BPMN process diagrams, org charts, workflow documentation |
| Planning | Mind maps, Gantt charts, project timelines, roadmaps |
| Education | Visual note-taking, concept maps, lesson planning, collaborative sessions |
| Game Design | Level layouts, character planning, dialogue trees, HUD mockups |
| Creative | Brainstorming, logo sketching, freeform annotation |
| Presentations | Frame-based slide decks (Excalidraw+ native feature) |

### Community library categories (libraries.excalidraw.com)

- AWS / Azure / GCP / Kubernetes architecture icons
- UI/UX wireframing component sets (buttons, inputs, cards, modals)
- ERD shapes (community library)
- Network topology icons
- Microsoft Fabric architecture icons
- UML shape packs

### Integrations & ecosystem

- Mermaid → Excalidraw conversion (open-source, official)
- Confluence plugin
- VSCode extension
- Text-to-diagram AI (Excalidraw+ — 100 req/day)
- Wireframe-to-Code AI (Excalidraw+ — converts wireframes to functional code)

### What makes Excalidraw different

The hand-drawn aesthetic is a feature, not a limitation. Users consistently report that the "sketchy" look signals *work in progress*, which lowers the psychological barrier to iteration. Diagrams feel exploratory rather than authoritative — better for early-stage design and agentic reasoning visualization.

---

## Current gallery coverage

| Example | Type | Direction |
|---|---|---|
| k8s-cluster | Zoned architecture | TB |
| saas-platform | Full stack architecture | TB |
| microservices | Service mesh | TB |
| arch | 3-tier web app | TB |
| auth-sequence | Sequence diagram | CLI |
| cicd | Feedback loop / pipeline | LR |
| data-pipeline | ETL pipeline | LR |
| flowchart | Decision flowchart | TB |
| recipe-flowchart | Non-technical flowchart | TB |
| customer-journey | Swimlane user journey | TB |
| org-chart | Hierarchy | TB |
| mindmap-software-eng | Deep mind map | LR |
| react-ecosystem | Asymmetric mind map | LR |
| mindmap | General mind map | LR |
| agent-debug-session | Freeform reasoning / agentic | LR |
| skill-pipeline | Process flow | LR |
| skill-files | File tree | LR |

**Covered well**: architecture, mind maps, flowcharts, sequence diagrams, org charts, customer journeys, agentic reasoning.

**Not covered**: ERD, BPMN, state machines, decision trees, Gantt/timeline, network topology, wireframe screens, data models, product roadmaps.

---

## Expansion opportunities — ranked by value

### Tier 1 — High fit, clear gap, broad demand

#### 1. ERD (Entity-Relationship Diagram)
- **Why**: Databases are universal — every app has a schema. Every team documents it.
- **Fit**: Dagre is perfect. Tables as nodes with column-list labels (e.g. `User\n─────\nid: uuid PK\nemail: text\ncreated_at: timestamp`), FK arrows, cardinality labels on edges.
- **Pattern**: New node label convention for column lists. Possibly a recipe.
- **Gap**: Zero coverage in current gallery.

#### 2. BPMN / Business Process Swimlane
- **Why**: Huge in enterprise — finance, HR, legal, operations. Describes *who does what and when*.
- **Fit**: Dagre handles pool + swimlane perfectly. Zones = actors (Customer, System, Finance). Nodes = tasks (rectangles), gateways (diamonds), events (ellipses). Edges = flow with labels.
- **Pattern**: Horizontal swimlanes (LR direction), zone = actor/role, node shapes encode element type.
- **Gap**: Zero coverage. Community has a standalone BPMN project but nothing in our skill.

#### 3. Decision Tree
- **Why**: Pricing calculators, onboarding logic, support triage, feature flag trees, medical protocols. Very common need.
- **Fit**: Diamond nodes for decisions, Yes/No edge labels, terminal nodes (ellipses) for outcomes. Dagre TB direction is natural.
- **Pattern**: Extends flowchart recipe with explicit decision conventions. The `compares` diamond in customer-journey is a preview.
- **Gap**: Flowchart example exists but doesn't model Yes/No branching explicitly.

#### 4. State Machine / FSM
- **Why**: Auth state, subscription lifecycle, order status, UI component states. Standard developer communication tool.
- **Fit**: Perfect for dagre. States = nodes, transitions = directed edges with event labels, initial state = ellipse, terminal = double-border (approximated with bold stroke), error states = red.
- **Pattern**: New convention for initial/terminal/error state visual encoding.
- **Gap**: cicd diagram is a cycle but not an explicit state machine.

#### 5. Gantt / Project Timeline
- **Why**: Broadly used in business — sprint planning, project planning, roadmaps. Excalidraw+ explicitly highlights this.
- **Fit**: Horizontal bands (one per person/team), nodes = tasks with width proportional to duration, zones = project phases or time periods (Q1, Q2, Sprint 1, etc.).
- **Challenge**: Dagre doesn't natively handle "width proportional to duration" — needs a new convention where node `width` encodes time.
- **Pattern**: LR direction, time-as-zone approach, standardized node widths (e.g. 1 week = 60px).

---

### Tier 2 — Good fit, more effort or narrower audience

#### 6. Data Model / Schema Diagram
- **What**: TypeScript interface trees, Prisma schema, OpenAPI response shapes, JSON structure visualization.
- **Fit**: LR mind-map style. Root = API or model name, branches = fields, leaves = types. Can reuse mind map pattern.
- **Audience**: Backend/fullstack developers.

#### 7. Feature Map / Product Roadmap
- **What**: Now/Next/Later columns, features as nodes, themes as zones. Product team staple.
- **Fit**: LR direction, zones = time horizons, nodes = features with status colors.
- **Audience**: Product managers, founders.

#### 8. Network Topology / Home Lab
- **What**: Routers, switches, VLANs, servers, firewalls. Niche but highly engaged community.
- **Fit**: Dagre works. Needs device-type shape conventions.
- **Audience**: DevOps, homelab enthusiasts.

#### 9. Learning Path / Prerequisite Map
- **What**: Skill trees, concept dependency graphs, course curricula.
- **Fit**: Dagre LR or TB. Nodes = concepts, edges = prerequisites, zones = topic areas.
- **Audience**: Educators, learners, documentation writers.

#### 10. Incident / Post-Mortem Timeline
- **What**: Timestamped event sequence — detection, mitigation, resolution phases. Root cause highlighted.
- **Fit**: LR direction, time-ordered. Similar to agent-debug-session but with explicit timestamps and phases as zones.
- **Audience**: SRE, platform, on-call engineers.

---

### Tier 3 — Needs new capability or different approach

#### 11. Wireframe Screens
- **What**: Actual UI screens with input boxes, buttons, form fields, navigation.
- **Why special**: Can't be coerced into dagre's graph model — needs a 2D canvas approach.
- **Proof of concept**: Login journey wireframe (2026-03-17) — 141 elements generated via Python script writing `.excalidraw` JSON directly. Proved the pattern is viable.
- **What's needed**: A dedicated recipe/template that:
  - Documents the "generate `.excalidraw` JSON directly" pattern
  - Provides Python helper functions for common UI elements (input, button, screen chrome, nav bar)
  - Handles screen-to-screen flow arrows with clean routing
  - Sets consistent sizing conventions (mobile: 390×780, desktop: 1280×800)
- **Key insight**: Dagre for the *flow* between screens + direct JSON for *content within* each screen. Hybrid approach.

#### 12. Presentations / Slide Decks
- **What**: Excalidraw+ has native frame-based slides. Each frame = one slide.
- **Approach**: The CLI could generate frame-by-frame content. Very different from graph layout.
- **Status**: Needs more design work before attempting.

#### 13. Floor Plan / Spatial Layout
- **What**: Rooms, furniture, physical spaces.
- **Fit**: Pure 2D spatial — graph topology model doesn't apply. Direct coordinate approach only.
- **Status**: Lower priority, narrow audience.

---

## The wireframe lesson

The login journey wireframe experiment (2026-03-17) revealed an important generalization:

> **Excalidraw is not just a graph renderer — it's a 2D canvas. Anything that can be expressed as positioned rectangles, text, and arrows can be generated.**

The dagre approach solves the hardest part of *most* diagrams: topology-to-layout. But for use cases where layout is intrinsically 2D (wireframes, floor plans, spatial diagrams, slide decks), the right approach is generating `.excalidraw` JSON directly.

This suggests two tracks for skill expansion:
- **Track A**: New graph.json recipes for dagre (ERD, BPMN, state machine, Gantt, decision tree)
- **Track B**: New direct-JSON generators for canvas-native use cases (wireframes, slides)

---

## Recommended next steps

1. **ERD recipe** — add to `diagram-recipes/` in the skill. Highest ROI: universal need, perfect dagre fit, zero coverage.
2. **State machine recipe** — clean conventions (initial/terminal/error states), developer-focused.
3. **BPMN recipe** — enterprise reach, unique visual pattern, no other agentic tool does this well.
4. **Decision tree recipe** — quick to build on top of flowchart pattern.
5. **Wireframe skill/recipe** — document the direct-JSON pattern with Python helper library. Formalize what the login journey proved.
6. **Gantt recipe** — needs time-as-zone convention designed first.
