"""Export pipeline for Excalidraw CLI.

Exports .excalidraw projects to SVG, PNG, and JSON using the real
Excalidraw engine (Node.js + Puppeteer) as the rendering backend.
"""

import json
import os
import subprocess
import tempfile

from excalidraw_agent_cli.utils.backend import (
    find_node,
    get_export_helper_script,
)


# ── JSON export (no backend needed) ──────────────────────────────────

def export_json(
    project: dict,
    output_path: str,
    overwrite: bool = False,
    pretty: bool = True,
) -> dict:
    """Export project as raw .excalidraw JSON.

    Args:
        project: The project dict.
        output_path: Output file path.
        overwrite: Whether to overwrite existing files.
        pretty: Whether to pretty-print JSON.

    Returns:
        Result dict with 'output', 'format', 'file_size'.
    """
    if not overwrite and os.path.exists(output_path):
        raise FileExistsError(
            f"Output file already exists: {output_path}. Use --overwrite to replace."
        )

    if not output_path.endswith(".excalidraw"):
        output_path += ".excalidraw"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)

    # Strip internal metadata for clean export
    out = {k: v for k, v in project.items() if k != "_meta"}
    out.setdefault("type", "excalidraw")
    out.setdefault("version", 2)
    out.setdefault("source", "excalidraw-agent-cli")

    indent = 2 if pretty else None
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=indent, ensure_ascii=False)

    size = os.path.getsize(output_path)
    return {
        "output": os.path.abspath(output_path),
        "format": "excalidraw",
        "file_size": size,
        "method": "json-direct",
    }


# ── SVG export (via Node.js + Excalidraw) ─────────────────────────────

def export_svg(
    project: dict,
    output_path: str,
    overwrite: bool = False,
    dark_mode: bool = False,
    padding: int = 10,
    embed_scene: bool = True,
) -> dict:
    """Export project to SVG using the Excalidraw Node.js backend.

    The real Excalidraw engine (via Node.js) renders the SVG, ensuring
    faithful reproduction of all element styles, fonts, and roughness.

    Args:
        project: The project dict.
        output_path: Output .svg file path.
        overwrite: Whether to overwrite existing files.
        dark_mode: Whether to render in dark mode.
        padding: Export padding in pixels.
        embed_scene: Whether to embed the scene data in the SVG.

    Returns:
        Result dict with 'output', 'format', 'file_size', 'method'.
    """
    if not overwrite and os.path.exists(output_path):
        raise FileExistsError(
            f"Output file already exists: {output_path}. Use --overwrite to replace."
        )

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)

    with tempfile.NamedTemporaryFile(
        suffix=".excalidraw", mode="w", delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(project, tmp)
        tmp_input = tmp.name

    try:
        result = _invoke_export_helper(
            input_path=tmp_input,
            output_path=output_path,
            format="svg",
            dark_mode=dark_mode,
            padding=padding,
            embed_scene=embed_scene,
        )
    finally:
        os.unlink(tmp_input)

    return result


# ── PNG export (via Node.js + Puppeteer) ──────────────────────────────

def export_png(
    project: dict,
    output_path: str,
    overwrite: bool = False,
    dark_mode: bool = False,
    scale: float = 1.0,
    padding: int = 10,
) -> dict:
    """Export project to PNG using Puppeteer (headless Chrome).

    Args:
        project: The project dict.
        output_path: Output .png file path.
        overwrite: Whether to overwrite existing files.
        dark_mode: Whether to render in dark mode.
        scale: Export scale factor (1.0 = original size).
        padding: Export padding in pixels.

    Returns:
        Result dict with 'output', 'format', 'file_size', 'method'.
    """
    if not overwrite and os.path.exists(output_path):
        raise FileExistsError(
            f"Output file already exists: {output_path}. Use --overwrite to replace."
        )

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)

    with tempfile.NamedTemporaryFile(
        suffix=".excalidraw", mode="w", delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(project, tmp)
        tmp_input = tmp.name

    try:
        result = _invoke_export_helper(
            input_path=tmp_input,
            output_path=output_path,
            format="png",
            dark_mode=dark_mode,
            scale=scale,
            padding=padding,
        )
    finally:
        os.unlink(tmp_input)

    return result


# ── Node.js helper invocation ─────────────────────────────────────────

def _invoke_export_helper(
    input_path: str,
    output_path: str,
    format: str,
    **options,
) -> dict:
    """Invoke the Node.js export helper script.

    Args:
        input_path: Path to .excalidraw input file.
        output_path: Path for output file.
        format: 'svg' or 'png'.
        **options: Additional options passed as JSON.

    Returns:
        Result dict from the helper.

    Raises:
        RuntimeError: If Node.js or the helper script is not found.
        subprocess.CalledProcessError: If export fails.
    """
    node = find_node()
    helper = get_export_helper_script()

    # Convert snake_case Python keys to camelCase for JavaScript
    key_map = {"dark_mode": "darkMode", "embed_scene": "embedScene"}
    js_options = {key_map.get(k, k): v for k, v in options.items()}

    opts_json = json.dumps({
        "format": format,
        "input": input_path,
        "output": os.path.abspath(output_path),
        **js_options,
    })

    cmd = [node, helper, opts_json]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Export timed out after 120s. Is Puppeteer installed?")

    if proc.returncode != 0:
        raise RuntimeError(
            f"Export failed (exit {proc.returncode}):\n"
            f"  stdout: {proc.stdout.strip()}\n"
            f"  stderr: {proc.stderr.strip()}"
        )

    # Parse result JSON from helper stdout
    try:
        result = json.loads(proc.stdout.strip())
    except json.JSONDecodeError:
        # Helper printed non-JSON — treat as success with basic result
        result = {}

    file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
    result.update({
        "output": os.path.abspath(output_path),
        "format": format,
        "file_size": file_size,
        "method": "excalidraw-node",
    })

    return result
