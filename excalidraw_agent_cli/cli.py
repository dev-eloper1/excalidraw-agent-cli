"""excalidraw-agent-cli — CLI harness for Excalidraw.

Provides a stateful CLI (and REPL) for creating, editing, and exporting
Excalidraw diagrams. Designed for agentic use: every command supports
--json output and operates on .excalidraw native files.

Usage:
    excalidraw-agent-cli                      # Enter REPL
    excalidraw-agent-cli project new -o diagram.excalidraw
    excalidraw-agent-cli --project diagram.excalidraw element add rectangle
    excalidraw-agent-cli --project diagram.excalidraw export svg -o out.svg
"""

import json
import os
import sys

import click

from excalidraw_agent_cli.core import elements as elem_mod
from excalidraw_agent_cli.core import export as export_mod
from excalidraw_agent_cli.core import project as project_mod
from excalidraw_agent_cli.core.session import get_session
from excalidraw_agent_cli.utils.repl_skin import ReplSkin

VERSION = "1.0.0"
skin = ReplSkin("excalidraw", version=VERSION)


# ── Helpers ───────────────────────────────────────────────────────────

def _out(data: dict, as_json: bool):
    """Print output as JSON or human-readable."""
    if as_json:
        click.echo(json.dumps(data, indent=2))
    else:
        for k, v in data.items():
            if isinstance(v, dict):
                skin.status(k, "")
                for sk, sv in v.items():
                    skin.status(f"  {sk}", str(sv))
            elif isinstance(v, list):
                skin.status(k, f"[{len(v)} items]")
            else:
                skin.status(k, str(v))


def _require_project(ctx):
    """Get current project from session or abort."""
    session = get_session()
    if session.project is None:
        raise click.ClickException(
            "No project open. Use 'project new' or 'project open <path>'."
        )
    return session.project


def _autosave(session):
    """Auto-save project to disk if a path is known."""
    if session.project is not None and session.project_path:
        project_mod.save_project(session.project, session.project_path)


def _load_project_from_option(project_path: str | None):
    """If project_path given, load it into session."""
    session = get_session()
    if project_path and (session.project is None or session.project_path != project_path):
        project = project_mod.load_project(project_path)
        session.set_project(project, project_path)


# ── Root command ──────────────────────────────────────────────────────

@click.group(invoke_without_command=True)
@click.option("--project", "-p", default=None, envvar="EXCALIDRAW_PROJECT",
              help="Path to .excalidraw project file.")
@click.option("--json", "as_json", is_flag=True, default=False,
              help="Output results as JSON.")
@click.version_option(version=VERSION, prog_name="excalidraw-agent-cli")
@click.pass_context
def cli(ctx, project, as_json):
    """excalidraw-agent-cli — Agentic CLI for Excalidraw diagrams.

    Create, edit, and export .excalidraw files from the command line.
    When invoked without a subcommand, enters interactive REPL mode.
    """
    ctx.ensure_object(dict)
    ctx.obj["as_json"] = as_json

    _load_project_from_option(project)

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


# ── REPL ──────────────────────────────────────────────────────────────

@cli.command()
def repl():
    """Enter the interactive REPL mode."""
    from shlex import split as shlex_split

    session = get_session()
    skin.print_banner()

    pt_session = skin.create_prompt_session()

    COMMANDS = {
        "project new":     "Create a new project",
        "project open":    "Open a .excalidraw file",
        "project save":    "Save the current project",
        "project info":    "Show project info",
        "element add":     "Add an element (rect/ellipse/diamond/text/arrow/line/frame)",
        "element list":    "List all elements",
        "element get":     "Get element details",
        "element update":  "Update element properties",
        "element delete":  "Delete an element",
        "element connect": "Connect two elements with an arrow",
        "export svg":      "Export to SVG",
        "export png":      "Export to PNG",
        "export json":     "Export as JSON",
        "session status":  "Show session status",
        "session undo":    "Undo last operation",
        "session redo":    "Redo last operation",
        "session history": "Show operation history",
        "backend check":   "Check Node.js backend status",
        "help":            "Show this help",
        "quit":            "Exit the REPL",
    }

    while True:
        project_name = ""
        modified = False
        if session.project is not None:
            project_name = session.project.get("_meta", {}).get("name", "Untitled")
            modified = session.modified

        try:
            line = skin.get_input(pt_session, project_name=project_name, modified=modified)
        except (EOFError, KeyboardInterrupt):
            skin.print_goodbye()
            break

        if not line:
            continue

        if line.lower() in ("quit", "exit", "q"):
            skin.print_goodbye()
            break

        if line.lower() in ("help", "?"):
            skin.help(COMMANDS)
            continue

        # Parse and dispatch via Click
        try:
            args = shlex_split(line)
            # Run the CLI with these args
            standalone = cli.make_context(
                "excalidraw", args,
                parent=None,
                standalone_mode=False,
            )
            cli.invoke(standalone)
        except SystemExit:
            pass
        except click.ClickException as e:
            skin.error(str(e))
        except click.exceptions.Exit:
            pass
        except Exception as e:
            skin.error(f"{type(e).__name__}: {e}")


# ── project commands ──────────────────────────────────────────────────

@cli.group()
@click.pass_context
def project(ctx):
    """Project lifecycle: new, open, save, info, validate."""
    pass


@project.command("new")
@click.option("--output", "-o", default=None, help="Output file path.")
@click.option("--name", "-n", default="Untitled", help="Project name.")
@click.option("--background", default="#ffffff", help="Background color.")
@click.option("--grid", is_flag=True, default=False, help="Enable grid.")
@click.pass_context
def project_new(ctx, output, name, background, grid):
    """Create a new empty Excalidraw project."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()

    proj = project_mod.create_project(name=name, background=background, grid=grid)
    session.set_project(proj, output)

    saved_path = None
    if output:
        saved_path = project_mod.save_project(proj, output)
        session.project_path = saved_path

    result = {
        "status": "created",
        "name": name,
        "path": saved_path,
        "background": background,
        "grid": grid,
    }

    if not as_json:
        skin.success(f"Created project '{name}'" + (f" → {saved_path}" if saved_path else ""))
    _out(result, as_json)


@project.command("open")
@click.argument("path")
@click.pass_context
def project_open(ctx, path):
    """Open an existing .excalidraw file."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()

    proj = project_mod.load_project(path)
    session.set_project(proj, path)

    info = project_mod.get_project_info(proj)
    result = {"status": "opened", "path": os.path.abspath(path), **info}

    if not as_json:
        skin.success(f"Opened '{info['name']}' ({info['element_count']} elements)")
    _out(result, as_json)


@project.command("save")
@click.option("--output", "-o", default=None, help="Output path (default: current path).")
@click.pass_context
def project_save(ctx, output):
    """Save the current project."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    save_path = output or session.project_path
    if not save_path:
        raise click.ClickException("No output path specified. Use -o <path>.")

    saved = project_mod.save_project(proj, save_path)
    session.project_path = saved
    session.modified = False

    result = {"status": "saved", "path": saved}
    if not as_json:
        skin.success(f"Saved → {saved}")
    _out(result, as_json)


@project.command("info")
@click.pass_context
def project_info(ctx):
    """Show project metadata and statistics."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    proj = _require_project(ctx)

    info = project_mod.get_project_info(proj)
    if not as_json:
        skin.section("Project Info")
        skin.status("Name", info["name"])
        skin.status("Elements", str(info["element_count"]))
        skin.status("Background", info["background"])
        skin.status("Grid", "on" if info["grid"] else "off")
        skin.status("Theme", info["theme"])
        if info["element_types"]:
            skin.status("Types", ", ".join(f"{t}×{n}" for t, n in info["element_types"].items()))
        if info["bounds"]:
            b = info["bounds"]
            skin.status("Bounds", f"({b['x']:.0f},{b['y']:.0f}) {b['width']:.0f}×{b['height']:.0f}")
    _out(info, as_json)


@project.command("validate")
@click.pass_context
def project_validate(ctx):
    """Validate the project file structure."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    proj = _require_project(ctx)

    issues = project_mod.validate_project(proj)
    result = {"valid": len(issues) == 0, "issues": issues}

    if not as_json:
        if issues:
            skin.warning(f"{len(issues)} validation issue(s):")
            for issue in issues:
                skin.error(f"  • {issue}")
        else:
            skin.success("Project is valid")
    _out(result, as_json)


# ── element commands ──────────────────────────────────────────────────

@cli.group()
@click.pass_context
def element(ctx):
    """Element CRUD: add, list, get, update, delete, connect."""
    pass


@element.group("add")
def element_add():
    """Add elements to the project."""
    pass


@element_add.command("rectangle")
@click.option("--x", default=100.0, type=float, help="X position.")
@click.option("--y", default=100.0, type=float, help="Y position.")
@click.option("--width", "-w", default=200.0, type=float, help="Width.")
@click.option("--height", "-h", default=120.0, type=float, help="Height.")
@click.option("--stroke-color", "--stroke", default="#1e1e1e", help="Stroke color.")
@click.option("--background-color", "--bg", default="transparent", help="Background color.")
@click.option("--fill-style", default="solid", type=click.Choice(["solid","hachure","cross-hatch","zigzag","dots"]))
@click.option("--stroke-width", "--sw", default=2, type=int)
@click.option("--roughness", default=1, type=int, help="0=smooth, 1=normal, 2=rough.")
@click.option("--opacity", default=100, type=int)
@click.option("--roundness", is_flag=True, default=False, help="Rounded corners.")
@click.option("--label", "-l", default=None, help="Text label inside the rectangle.")
@click.option("--frame-id", default=None, help="Parent frame ID.")
@click.pass_context
def add_rectangle(ctx, x, y, width, height, stroke_color, background_color,
                   fill_style, stroke_width, roughness, opacity, roundness, label, frame_id):
    """Add a rectangle element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("add rectangle")
    el = elem_mod.add_rectangle(
        proj, x=x, y=y, width=width, height=height,
        stroke_color=stroke_color, background_color=background_color,
        fill_style=fill_style, stroke_width=stroke_width, roughness=roughness,
        opacity=opacity, roundness=roundness, label=label, frame_id=frame_id,
    )
    session.mark_modified()
    _autosave(session)

    result = {"status": "added", "id": el["id"], "type": "rectangle", "x": x, "y": y, "width": width, "height": height}
    if not as_json:
        skin.success(f"Added rectangle [{el['id']}]")
    _out(result, as_json)


@element_add.command("ellipse")
@click.option("--x", default=100.0, type=float)
@click.option("--y", default=100.0, type=float)
@click.option("--width", "-w", default=160.0, type=float)
@click.option("--height", "-h", default=120.0, type=float)
@click.option("--stroke-color", "--stroke", default="#1e1e1e")
@click.option("--background-color", "--bg", default="transparent")
@click.option("--fill-style", default="solid", type=click.Choice(["solid","hachure","cross-hatch","zigzag","dots"]))
@click.option("--stroke-width", "--sw", default=2, type=int)
@click.option("--roughness", default=1, type=int)
@click.option("--opacity", default=100, type=int)
@click.option("--label", "-l", default=None)
@click.pass_context
def add_ellipse(ctx, x, y, width, height, stroke_color, background_color,
                 fill_style, stroke_width, roughness, opacity, label):
    """Add an ellipse element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("add ellipse")
    el = elem_mod.add_ellipse(
        proj, x=x, y=y, width=width, height=height,
        stroke_color=stroke_color, background_color=background_color,
        fill_style=fill_style, stroke_width=stroke_width,
        roughness=roughness, opacity=opacity, label=label,
    )
    session.mark_modified()
    _autosave(session)

    result = {"status": "added", "id": el["id"], "type": "ellipse", "x": x, "y": y}
    if not as_json:
        skin.success(f"Added ellipse [{el['id']}]")
    _out(result, as_json)


@element_add.command("diamond")
@click.option("--x", default=100.0, type=float)
@click.option("--y", default=100.0, type=float)
@click.option("--width", "-w", default=160.0, type=float)
@click.option("--height", "-h", default=160.0, type=float)
@click.option("--stroke-color", "--stroke", default="#1e1e1e")
@click.option("--background-color", "--bg", default="transparent")
@click.option("--fill-style", default="solid", type=click.Choice(["solid","hachure","cross-hatch","zigzag","dots"]))
@click.option("--stroke-width", "--sw", default=2, type=int)
@click.option("--roughness", default=1, type=int)
@click.option("--opacity", default=100, type=int)
@click.option("--label", "-l", default=None)
@click.pass_context
def add_diamond(ctx, x, y, width, height, stroke_color, background_color,
                 fill_style, stroke_width, roughness, opacity, label):
    """Add a diamond element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("add diamond")
    el = elem_mod.add_diamond(
        proj, x=x, y=y, width=width, height=height,
        stroke_color=stroke_color, background_color=background_color,
        fill_style=fill_style, stroke_width=stroke_width,
        roughness=roughness, opacity=opacity, label=label,
    )
    session.mark_modified()
    _autosave(session)

    result = {"status": "added", "id": el["id"], "type": "diamond", "x": x, "y": y}
    if not as_json:
        skin.success(f"Added diamond [{el['id']}]")
    _out(result, as_json)


@element_add.command("text")
@click.argument("text_content", default="")
@click.option("--text", "-t", default=None, help="Text content (alternative to positional arg).")
@click.option("--x", default=100.0, type=float)
@click.option("--y", default=100.0, type=float)
@click.option("--font-size", "--fs", default=20, type=int)
@click.option("--font-family", "--ff", default=1, type=click.Choice(["1","2","3"]), help="1=Virgil, 2=Helvetica, 3=Cascadia.")
@click.option("--text-align", default="left", type=click.Choice(["left","center","right"]))
@click.option("--stroke-color", "--color", default="#1e1e1e")
@click.option("--opacity", default=100, type=int)
@click.pass_context
def add_text(ctx, text_content, text, x, y, font_size, font_family, text_align, stroke_color, opacity):
    """Add a text element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    content = text or text_content
    if not content:
        raise click.ClickException("Text content is required. Use -t 'Hello World'")

    session.checkpoint("add text")
    el = elem_mod.add_text(
        proj, content, x=x, y=y, font_size=font_size,
        font_family=int(font_family), text_align=text_align,
        stroke_color=stroke_color, opacity=opacity,
    )
    session.mark_modified()
    _autosave(session)

    result = {"status": "added", "id": el["id"], "type": "text", "text": content[:50]}
    if not as_json:
        skin.success(f"Added text [{el['id']}]: {content[:40]!r}")
    _out(result, as_json)


@element_add.command("arrow")
@click.option("--x", default=100.0, type=float, help="Start X.")
@click.option("--y", default=100.0, type=float, help="Start Y.")
@click.option("--end-x", "--ex", default=300.0, type=float, help="End X.")
@click.option("--end-y", "--ey", default=100.0, type=float, help="End Y.")
@click.option("--stroke-color", "--stroke", default="#1e1e1e")
@click.option("--stroke-width", "--sw", default=2, type=int)
@click.option("--stroke-style", default="solid", type=click.Choice(["solid","dashed","dotted"]))
@click.option("--roughness", default=1, type=int)
@click.option("--start-arrowhead", default=None)
@click.option("--end-arrowhead", default="arrow", help="None, arrow, bar, dot, triangle.")
@click.option("--from", "from_id", default=None, help="Source element ID to bind to.")
@click.option("--to", "to_id", default=None, help="Target element ID to bind to.")
@click.option("--label", "-l", default=None)
@click.pass_context
def add_arrow(ctx, x, y, end_x, end_y, stroke_color, stroke_width, stroke_style,
               roughness, start_arrowhead, end_arrowhead, from_id, to_id, label):
    """Add an arrow element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("add arrow")
    el = elem_mod.add_arrow(
        proj, x=x, y=y, end_x=end_x, end_y=end_y,
        stroke_color=stroke_color, stroke_width=stroke_width,
        stroke_style=stroke_style, roughness=roughness,
        start_arrowhead=start_arrowhead if start_arrowhead != "None" else None,
        end_arrowhead=end_arrowhead if end_arrowhead != "None" else None,
        from_id=from_id, to_id=to_id, label=label,
    )
    session.mark_modified()
    _autosave(session)

    result = {"status": "added", "id": el["id"], "type": "arrow"}
    if not as_json:
        skin.success(f"Added arrow [{el['id']}]")
    _out(result, as_json)


@element_add.command("line")
@click.option("--x", default=100.0, type=float)
@click.option("--y", default=100.0, type=float)
@click.option("--points", default="0,0 200,0", help="Space-separated x,y pairs. E.g. '0,0 100,50 200,0'")
@click.option("--stroke-color", "--stroke", default="#1e1e1e")
@click.option("--stroke-width", "--sw", default=2, type=int)
@click.option("--stroke-style", default="solid", type=click.Choice(["solid","dashed","dotted"]))
@click.option("--roughness", default=1, type=int)
@click.pass_context
def add_line(ctx, x, y, points, stroke_color, stroke_width, stroke_style, roughness):
    """Add a line element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    # Parse points string "0,0 100,50 200,0" → [[0,0],[100,50],[200,0]]
    try:
        pts = [[float(v) for v in pair.split(",")]
               for pair in points.strip().split()]
    except ValueError:
        raise click.ClickException(f"Invalid points format: {points!r}. Use '0,0 100,50 200,0'")

    session.checkpoint("add line")
    el = elem_mod.add_line(
        proj, pts, x=x, y=y,
        stroke_color=stroke_color, stroke_width=stroke_width,
        stroke_style=stroke_style, roughness=roughness,
    )
    session.mark_modified()
    _autosave(session)

    result = {"status": "added", "id": el["id"], "type": "line", "points": len(pts)}
    if not as_json:
        skin.success(f"Added line [{el['id']}] with {len(pts)} points")
    _out(result, as_json)


@element_add.command("frame")
@click.option("--x", default=50.0, type=float)
@click.option("--y", default=50.0, type=float)
@click.option("--width", "-w", default=400.0, type=float)
@click.option("--height", "-h", default=300.0, type=float)
@click.option("--name", "-n", default="Frame", help="Frame label.")
@click.option("--stroke-color", "--stroke", default="#bbb")
@click.pass_context
def add_frame(ctx, x, y, width, height, name, stroke_color):
    """Add a frame (container) element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("add frame")
    el = elem_mod.add_frame(proj, x=x, y=y, width=width, height=height,
                            name=name, stroke_color=stroke_color)
    session.mark_modified()
    _autosave(session)

    result = {"status": "added", "id": el["id"], "type": "frame", "name": name}
    if not as_json:
        skin.success(f"Added frame '{name}' [{el['id']}]")
    _out(result, as_json)


@element.command("connect")
@click.option("--from", "from_id", required=True, help="Source element ID.")
@click.option("--to", "to_id", required=True, help="Target element ID.")
@click.option("--label", "-l", default=None, help="Arrow label.")
@click.option("--stroke-color", "--stroke", default="#1e1e1e")
@click.option("--stroke-width", "--sw", default=2, type=int)
@click.option("--stroke-style", default="solid", type=click.Choice(["solid","dashed","dotted"]))
@click.option("--roughness", default=1, type=int)
@click.option("--start-arrowhead", default=None, help="Start arrowhead: arrow, bar, dot, triangle, circle, or omit for none.")
@click.option("--end-arrowhead", default="arrow", help="End arrowhead: arrow, bar, dot, triangle, circle, or none.")
@click.pass_context
def element_connect(ctx, from_id, to_id, label, stroke_color, stroke_width, stroke_style, roughness, start_arrowhead, end_arrowhead):
    """Connect two elements with an arrow (auto-positioned)."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("connect elements")
    el = elem_mod.connect_elements(proj, from_id, to_id,
                                   label=label,
                                   stroke_color=stroke_color,
                                   stroke_width=stroke_width,
                                   stroke_style=stroke_style,
                                   roughness=roughness,
                                   start_arrowhead=start_arrowhead,
                                   end_arrowhead=end_arrowhead)
    session.mark_modified()
    _autosave(session)

    result = {"status": "connected", "arrow_id": el["id"], "from": from_id, "to": to_id}
    if not as_json:
        skin.success(f"Connected {from_id} → {to_id} with arrow [{el['id']}]")
    _out(result, as_json)


@element.command("list")
@click.option("--type", "-t", "element_type", default=None, help="Filter by element type.")
@click.option("--frame-id", default=None, help="Filter by parent frame.")
@click.option("--include-deleted", is_flag=True, default=False)
@click.pass_context
def element_list(ctx, element_type, frame_id, include_deleted):
    """List elements in the project."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    proj = _require_project(ctx)

    els = elem_mod.list_elements(proj, element_type=element_type,
                                  frame_id=frame_id, include_deleted=include_deleted)

    result = {
        "count": len(els),
        "elements": [
            {
                "id": e["id"],
                "type": e["type"],
                "x": e.get("x", 0),
                "y": e.get("y", 0),
                "width": e.get("width"),
                "height": e.get("height"),
                "text": e.get("text", "")[:40] if e.get("text") else None,
                "isDeleted": e.get("isDeleted", False),
            }
            for e in els
        ],
    }

    if not as_json:
        headers = ["ID", "Type", "X", "Y", "W", "H", "Text/Name"]
        rows = [
            [
                e["id"][:16],
                e["type"],
                str(int(e["x"])),
                str(int(e["y"])),
                str(int(e["width"] or 0)),
                str(int(e["height"] or 0)),
                (e.get("text") or "")[:30],
            ]
            for e in result["elements"]
        ]
        skin.info(f"{len(els)} element(s)")
        skin.table(headers, rows)
    _out(result, as_json)


@element.command("get")
@click.argument("element_id")
@click.pass_context
def element_get(ctx, element_id):
    """Get element details by ID."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    proj = _require_project(ctx)

    el = elem_mod.get_element(proj, element_id)
    if not el:
        raise click.ClickException(f"Element not found: {element_id}")

    if not as_json:
        skin.section(f"Element: {el['id']}")
        for k, v in el.items():
            if k not in ("boundElements", "groupIds") or v:
                skin.status(k, str(v)[:80])
    _out(el, as_json)


@element.command("update")
@click.argument("element_id")
@click.option("--x", type=float, default=None)
@click.option("--y", type=float, default=None)
@click.option("--width", "-w", type=float, default=None)
@click.option("--height", "-h", type=float, default=None)
@click.option("--stroke-color", "--stroke", default=None)
@click.option("--background-color", "--bg", default=None)
@click.option("--fill-style", default=None, type=click.Choice(["solid","hachure","cross-hatch","zigzag","dots"]))
@click.option("--stroke-width", "--sw", type=int, default=None)
@click.option("--roughness", type=int, default=None)
@click.option("--opacity", type=int, default=None)
@click.option("--text", "-t", default=None, help="Update text content.")
@click.option("--font-size", "--fs", type=int, default=None)
@click.option("--locked", is_flag=True, default=None)
@click.option("--link", default=None)
@click.pass_context
def element_update(ctx, element_id, x, y, width, height, stroke_color,
                    background_color, fill_style, stroke_width, roughness,
                    opacity, text, font_size, locked, link):
    """Update element properties."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    updates = {k: v for k, v in {
        "x": x, "y": y, "width": width, "height": height,
        "stroke_color": stroke_color, "background_color": background_color,
        "fill_style": fill_style, "stroke_width": stroke_width,
        "roughness": roughness, "opacity": opacity,
        "text": text, "font_size": font_size,
        "locked": locked, "link": link,
    }.items() if v is not None}

    if not updates:
        raise click.ClickException("No update fields specified.")

    session.checkpoint("update element")
    el = elem_mod.update_element(proj, element_id, **updates)
    session.mark_modified()
    _autosave(session)

    result = {"status": "updated", "id": el["id"], "updated_fields": list(updates.keys())}
    if not as_json:
        skin.success(f"Updated [{element_id}]: {', '.join(updates.keys())}")
    _out(result, as_json)


@element.command("delete")
@click.argument("element_id")
@click.pass_context
def element_delete(ctx, element_id):
    """Delete (soft-delete) an element."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("delete element")
    el = elem_mod.delete_element(proj, element_id)
    session.mark_modified()
    _autosave(session)

    result = {"status": "deleted", "id": el["id"], "type": el["type"]}
    if not as_json:
        skin.success(f"Deleted {el['type']} [{element_id}]")
    _out(result, as_json)


@element.command("move")
@click.argument("element_id")
@click.option("--dx", default=0.0, type=float, help="X offset.")
@click.option("--dy", default=0.0, type=float, help="Y offset.")
@click.pass_context
def element_move(ctx, element_id, dx, dy):
    """Move an element by dx, dy offset."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    session = get_session()
    proj = _require_project(ctx)

    session.checkpoint("move element")
    el = elem_mod.move_element(proj, element_id, dx=dx, dy=dy)
    session.mark_modified()
    _autosave(session)

    result = {"status": "moved", "id": el["id"], "x": el["x"], "y": el["y"]}
    if not as_json:
        skin.success(f"Moved [{element_id}] to ({el['x']:.0f}, {el['y']:.0f})")
    _out(result, as_json)


# ── export commands ───────────────────────────────────────────────────

@cli.group()
@click.pass_context
def export(ctx):
    """Export: svg, png, json."""
    pass


@export.command("svg")
@click.option("--output", "-o", required=True, help="Output .svg file path.")
@click.option("--overwrite", is_flag=True, default=False)
@click.option("--dark", is_flag=True, default=False, help="Dark mode.")
@click.option("--padding", default=10, type=int)
@click.option("--embed-scene", is_flag=True, default=True, help="Embed scene data in SVG.")
@click.pass_context
def export_svg(ctx, output, overwrite, dark, padding, embed_scene):
    """Export project to SVG using the Excalidraw Node.js engine."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    proj = _require_project(ctx)

    if not as_json:
        skin.info("Exporting to SVG via Node.js...")

    try:
        result = export_mod.export_svg(proj, output, overwrite=overwrite,
                                        dark_mode=dark, padding=padding,
                                        embed_scene=embed_scene)
    except FileExistsError as e:
        raise click.ClickException(str(e))
    except RuntimeError as e:
        raise click.ClickException(str(e))

    if not as_json:
        skin.success(f"Exported SVG → {result['output']} ({result['file_size']:,} bytes)")
        print(f"\n  SVG: {result['output']} ({result['file_size']:,} bytes)")
    _out(result, as_json)


@export.command("png")
@click.option("--output", "-o", required=True, help="Output .png file path.")
@click.option("--overwrite", is_flag=True, default=False)
@click.option("--dark", is_flag=True, default=False, help="Dark mode.")
@click.option("--scale", default=1.0, type=float, help="Scale factor.")
@click.option("--padding", default=10, type=int)
@click.pass_context
def export_png(ctx, output, overwrite, dark, scale, padding):
    """Export project to PNG via Puppeteer (headless Chrome)."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    proj = _require_project(ctx)

    if not as_json:
        skin.info("Exporting to PNG via Puppeteer...")

    try:
        result = export_mod.export_png(proj, output, overwrite=overwrite,
                                        dark_mode=dark, scale=scale, padding=padding)
    except FileExistsError as e:
        raise click.ClickException(str(e))
    except RuntimeError as e:
        raise click.ClickException(str(e))

    if not as_json:
        skin.success(f"Exported PNG → {result['output']} ({result['file_size']:,} bytes)")
        print(f"\n  PNG: {result['output']} ({result['file_size']:,} bytes)")
    _out(result, as_json)


@export.command("json")
@click.option("--output", "-o", required=True, help="Output .excalidraw file path.")
@click.option("--overwrite", is_flag=True, default=False)
@click.option("--compact", is_flag=True, default=False, help="Compact (non-pretty) JSON.")
@click.pass_context
def export_json(ctx, output, overwrite, compact):
    """Export project as .excalidraw JSON."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    proj = _require_project(ctx)

    try:
        result = export_mod.export_json(proj, output, overwrite=overwrite, pretty=not compact)
    except FileExistsError as e:
        raise click.ClickException(str(e))

    if not as_json:
        skin.success(f"Exported JSON → {result['output']} ({result['file_size']:,} bytes)")
    _out(result, as_json)


# ── session commands ──────────────────────────────────────────────────

@cli.group()
@click.pass_context
def session(ctx):
    """Session: status, undo, redo, history."""
    pass


@session.command("status")
@click.pass_context
def session_status(ctx):
    """Show current session status."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    s = get_session()
    result = s.get_status()

    if not as_json:
        skin.section("Session Status")
        skin.status("Project", result["project_path"] or "(none)")
        skin.status("Name", result["project_name"] or "(none)")
        skin.status("Modified", "yes" if result["modified"] else "no")
        skin.status("Elements", str(result["element_count"]))
        skin.status("Undo", f"{result['undo_count']} steps")
        skin.status("Redo", f"{result['redo_count']} steps")
    _out(result, as_json)


@session.command("undo")
@click.pass_context
def session_undo(ctx):
    """Undo the last operation."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    s = get_session()

    op = s.undo()
    result = {"status": "undone" if op else "nothing_to_undo", "operation": op}

    if not as_json:
        if op:
            skin.success(f"Undone: {op}")
        else:
            skin.warning("Nothing to undo")
    _out(result, as_json)


@session.command("redo")
@click.pass_context
def session_redo(ctx):
    """Redo the last undone operation."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    s = get_session()

    op = s.redo()
    result = {"status": "redone" if op else "nothing_to_redo", "operation": op}

    if not as_json:
        if op:
            skin.success(f"Redone: {op}")
        else:
            skin.warning("Nothing to redo")
    _out(result, as_json)


@session.command("history")
@click.option("--limit", default=20, type=int)
@click.pass_context
def session_history(ctx, limit):
    """Show operation history."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False
    s = get_session()

    history = s.get_history(limit=limit)
    result = {"count": len(history), "history": history}

    if not as_json:
        if history:
            import datetime
            headers = ["#", "Operation", "Time"]
            rows = [
                [str(i+1), h["operation"],
                 datetime.datetime.fromtimestamp(h["timestamp"]).strftime("%H:%M:%S")]
                for i, h in enumerate(history)
            ]
            skin.table(headers, rows)
        else:
            skin.info("No history yet")
    _out(result, as_json)


# ── backend check command ─────────────────────────────────────────────

@cli.command("backend")
@click.argument("action", default="check")
@click.pass_context
def backend_check(ctx, action):
    """Check Node.js backend availability for SVG/PNG export."""
    as_json = ctx.obj.get("as_json", False) if ctx.obj else False

    from excalidraw_agent_cli.utils.backend import check_backend_available
    result = check_backend_available()

    if not as_json:
        if result["available"]:
            skin.success("Node.js backend is available")
            skin.status("node", result["node_path"])
            skin.status("helper", result["helper_path"])
        else:
            skin.error("Node.js backend not available")
            for issue in result["issues"]:
                skin.warning(issue)
    _out(result, as_json)


# ── install-skill command ─────────────────────────────────────────────

@cli.command("install-skill")
@click.option(
    "--global", "global_install", is_flag=True, default=False,
    help="Install into ~/.claude/skills/excalidraw/ (default when no --codebase flag).",
)
@click.option(
    "--codebase", "codebase_dir", default=None, metavar="DIR",
    help="Install into <DIR>/.claude/skills/excalidraw/ instead of the global location.",
)
@click.option(
    "--force", is_flag=True, default=False,
    help="Overwrite existing skill files without prompting.",
)
@click.pass_context
def install_skill(ctx, global_install, codebase_dir, force):
    """Install the Excalidraw diagram skill for Claude Code.

    By default installs globally to ~/.claude/skills/excalidraw/ so the skill
    is available in every Claude Code session.  Pass --codebase <dir> to
    install it into a specific project instead (useful for sharing the skill
    with a team via git).

    \b
    Examples:
      excalidraw-agent-cli install-skill                   # global
      excalidraw-agent-cli install-skill --global          # same as above
      excalidraw-agent-cli install-skill --codebase .      # current project
      excalidraw-agent-cli install-skill --codebase ~/work/myapp
    """
    import shutil
    from pathlib import Path

    # ── Locate bundled skill directory ────────────────────────────────
    # When installed via pip the skill lives next to this file under
    # excalidraw_agent_cli/skill/.  In the dev layout it lives in the repo root.
    _pkg_dir = Path(__file__).parent
    skill_src = _pkg_dir / "skill"
    if not skill_src.is_dir():
        # Fallback: repo root (dev mode)
        skill_src = _pkg_dir.parent / "skill"
    if not skill_src.is_dir():
        skin.error("Bundled skill directory not found.")
        skin.info("Expected location: " + str(_pkg_dir / "skill"))
        raise SystemExit(1)

    # ── Determine destination ─────────────────────────────────────────
    if codebase_dir is not None:
        dest_base = Path(codebase_dir).expanduser().resolve()
        dest = dest_base / ".claude" / "skills" / "excalidraw"
        scope = f"codebase ({dest_base})"
    else:
        dest = Path.home() / ".claude" / "skills" / "excalidraw"
        scope = "global (~/.claude/skills/excalidraw)"

    # ── Safety check ─────────────────────────────────────────────────
    if dest.exists() and not force:
        skin.warning(f"Skill already installed at: {dest}")
        skin.info("Use --force to overwrite.")
        raise SystemExit(0)

    # ── Copy skill/ → dest ───────────────────────────────────────────
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(skill_src, dest)

    skin.success(f"Skill installed ({scope})")
    skin.status("location", str(dest))
    skin.status("files", str(sum(1 for _ in dest.rglob("*") if _.is_file())))
    skin.info("")
    skin.info("Claude Code will pick up the skill automatically.")
    skin.info("Try: \"draw a system architecture diagram for a three-tier web app\"")


# ── Entry point ───────────────────────────────────────────────────────

def main():
    cli(obj={})


if __name__ == "__main__":
    main()
