"""Project management for Excalidraw CLI.

Handles creation, loading, saving, and inspection of .excalidraw files.
"""

import json
import os
import time
from typing import Any

EXCALIDRAW_VERSION = 2
DEFAULT_APP_STATE = {
    "viewBackgroundColor": "#ffffff",
    "gridSize": None,
    "currentItemStrokeColor": "#1e1e1e",
    "currentItemBackgroundColor": "transparent",
    "currentItemFillStyle": "solid",
    "currentItemStrokeWidth": 2,
    "currentItemStrokeStyle": "solid",
    "currentItemRoughness": 1,
    "currentItemOpacity": 100,
    "currentItemFontFamily": 1,
    "currentItemFontSize": 20,
    "currentItemTextAlign": "left",
    "currentItemStartArrowhead": None,
    "currentItemEndArrowhead": "arrow",
    "zoom": {"value": 1},
    "theme": "light",
}


def create_project(
    name: str = "Untitled",
    background: str = "#ffffff",
    grid: bool = False,
) -> dict:
    """Create a new empty Excalidraw project.

    Args:
        name: Project display name (stored in metadata).
        background: Canvas background color (CSS color string).
        grid: Whether to enable grid snapping.

    Returns:
        Excalidraw project dict.
    """
    app_state = {**DEFAULT_APP_STATE}
    app_state["viewBackgroundColor"] = background
    app_state["gridSize"] = 20 if grid else None

    return {
        "type": "excalidraw",
        "version": EXCALIDRAW_VERSION,
        "source": "excalidraw-agent-cli",
        "_meta": {
            "name": name,
            "created": time.time(),
            "modified": time.time(),
        },
        "elements": [],
        "appState": app_state,
        "files": {},
    }


def load_project(path: str) -> dict:
    """Load an .excalidraw file from disk.

    Args:
        path: Path to the .excalidraw JSON file.

    Returns:
        Parsed project dict.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a valid Excalidraw file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("type") != "excalidraw":
        raise ValueError(
            f"Not a valid Excalidraw file (missing type=excalidraw): {path}"
        )

    # Ensure _meta exists
    if "_meta" not in data:
        name = os.path.splitext(os.path.basename(path))[0]
        data["_meta"] = {"name": name, "created": time.time(), "modified": time.time()}

    # Ensure required keys
    data.setdefault("elements", [])
    data.setdefault("appState", {**DEFAULT_APP_STATE})
    data.setdefault("files", {})

    return data


def save_project(project: dict, path: str) -> str:
    """Save project to disk as .excalidraw JSON.

    Args:
        project: Project dict.
        path: Output file path. Will add .excalidraw extension if missing.

    Returns:
        Absolute path where the file was saved.
    """
    if not path.endswith(".excalidraw"):
        path = path + ".excalidraw"

    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    # Update modified timestamp
    if "_meta" in project:
        project["_meta"]["modified"] = time.time()

    # Build clean output (strip _meta for compatibility with Excalidraw app)
    output = {k: v for k, v in project.items() if k != "_meta"}
    output["source"] = project.get("source", "excalidraw-agent-cli")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return path


def get_project_info(project: dict) -> dict:
    """Extract project summary information.

    Args:
        project: Project dict.

    Returns:
        Summary dict with name, element count, bounds, etc.
    """
    elements = [e for e in project.get("elements", []) if not e.get("isDeleted")]
    app_state = project.get("appState", {})
    meta = project.get("_meta", {})

    # Calculate bounding box
    bounds = _get_bounds(elements)

    # Count by type
    type_counts: dict[str, int] = {}
    for el in elements:
        t = el.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    return {
        "name": meta.get("name", "Untitled"),
        "version": project.get("version", EXCALIDRAW_VERSION),
        "element_count": len(elements),
        "element_types": type_counts,
        "background": app_state.get("viewBackgroundColor", "#ffffff"),
        "grid": app_state.get("gridSize") is not None,
        "theme": app_state.get("theme", "light"),
        "bounds": bounds,
        "file_count": len(project.get("files", {})),
    }


def validate_project(project: dict) -> list[str]:
    """Validate project structure and return list of issues.

    Args:
        project: Project dict.

    Returns:
        List of validation error strings. Empty list means valid.
    """
    issues = []

    if project.get("type") != "excalidraw":
        issues.append("Missing or incorrect 'type' field (expected 'excalidraw')")

    if project.get("version") != EXCALIDRAW_VERSION:
        issues.append(
            f"Unexpected version {project.get('version')} (expected {EXCALIDRAW_VERSION})"
        )

    if not isinstance(project.get("elements"), list):
        issues.append("'elements' must be a list")
        return issues

    seen_ids = set()
    for i, el in enumerate(project.get("elements", [])):
        if not isinstance(el, dict):
            issues.append(f"Element {i} is not a dict")
            continue
        if "id" not in el:
            issues.append(f"Element {i} missing 'id'")
        elif el["id"] in seen_ids:
            issues.append(f"Duplicate element id: {el['id']}")
        else:
            seen_ids.add(el["id"])

        if "type" not in el:
            issues.append(f"Element {i} ({el.get('id', '?')}) missing 'type'")

    return issues


def _get_bounds(elements: list[dict]) -> dict | None:
    """Get bounding box of all elements."""
    if not elements:
        return None

    xs, ys, x2s, y2s = [], [], [], []
    for el in elements:
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)
        xs.append(x)
        ys.append(y)
        x2s.append(x + w)
        y2s.append(y + h)

    return {
        "x": min(xs),
        "y": min(ys),
        "width": max(x2s) - min(xs),
        "height": max(y2s) - min(ys),
    }
