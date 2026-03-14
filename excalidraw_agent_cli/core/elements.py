"""Element creation and manipulation for Excalidraw CLI.

Handles all element types: rectangle, ellipse, diamond, text, arrow,
line, frame, freedraw.
"""

import random
import time
import uuid
from typing import Any


# ── Element type constants ────────────────────────────────────────────

ELEMENT_TYPES = {
    "rectangle", "ellipse", "diamond", "text", "arrow", "line",
    "frame", "freedraw", "image",
}

FILL_STYLES = {"hachure", "cross-hatch", "solid", "zigzag", "dots"}
STROKE_STYLES = {"solid", "dashed", "dotted"}
ARROWHEAD_TYPES = {None, "arrow", "bar", "dot", "triangle", "triangle_outline",
                   "circle", "circle_outline"}
FONT_FAMILIES = {1: "Virgil", 2: "Helvetica", 3: "Cascadia"}
TEXT_ALIGNS = {"left", "center", "right"}


# ── Base element builder ──────────────────────────────────────────────

def _base_element(
    element_type: str,
    x: float,
    y: float,
    width: float,
    height: float,
    stroke_color: str = "#1e1e1e",
    background_color: str = "transparent",
    fill_style: str = "solid",
    stroke_width: int = 2,
    stroke_style: str = "solid",
    roughness: int = 1,
    opacity: int = 100,
    angle: float = 0.0,
    group_ids: list | None = None,
    frame_id: str | None = None,
    element_id: str | None = None,
) -> dict:
    """Build the common fields shared by all Excalidraw elements."""
    now = int(time.time() * 1000)
    seed = random.randint(1, 2**31 - 1)
    eid = element_id or str(uuid.uuid4())[:20]

    return {
        "id": eid,
        "type": element_type,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": angle,
        "strokeColor": stroke_color,
        "backgroundColor": background_color,
        "fillStyle": fill_style,
        "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roughness": roughness,
        "opacity": opacity,
        "groupIds": group_ids or [],
        "frameId": frame_id,
        "roundness": None,
        "seed": seed,
        "version": 1,
        "versionNonce": random.randint(1, 2**31 - 1),
        "isDeleted": False,
        "boundElements": [],
        "updated": now,
        "link": None,
        "locked": False,
    }


# ── Label auto-sizing ─────────────────────────────────────────────────

# Label text uses 16px Virgil inside shapes. Approximate char width: 16 * 0.6 = 9.6px.
# We add 32px of horizontal padding (16px each side) as a comfortable margin.
_LABEL_CHAR_WIDTH_PX: float = 9.6
_LABEL_PADDING_PX: float = 32.0
_LABEL_MIN_WIDTH_PX: float = 120.0


def _min_width_for_label(label: str) -> float:
    """Return the minimum box width that fits the given label without overflow."""
    max_line = max((len(line) for line in label.split("\n")), default=1)
    return max(_LABEL_MIN_WIDTH_PX, max_line * _LABEL_CHAR_WIDTH_PX + _LABEL_PADDING_PX)


# ── Shape elements ────────────────────────────────────────────────────

def add_rectangle(
    project: dict,
    x: float = 100,
    y: float = 100,
    width: float = 200,
    height: float = 120,
    stroke_color: str = "#1e1e1e",
    background_color: str = "transparent",
    fill_style: str = "solid",
    stroke_width: int = 2,
    roughness: int = 1,
    opacity: int = 100,
    roundness: bool = False,
    label: str | None = None,
    frame_id: str | None = None,
) -> dict:
    """Add a rectangle to the project.

    Args:
        project: The project dict to modify in-place.
        x, y: Top-left position.
        width, height: Dimensions.
        stroke_color: Stroke color (CSS color).
        background_color: Fill color.
        fill_style: One of solid, hachure, cross-hatch, zigzag, dots.
        stroke_width: Line width in pixels.
        roughness: 0=smooth, 1=normal, 2=rough.
        opacity: 0-100.
        roundness: Whether to use rounded corners.
        label: Optional text label inside the rectangle.
        frame_id: Parent frame ID if nested.

    Returns:
        The created element dict.
    """
    if label:
        width = max(width, _min_width_for_label(label))

    el = _base_element(
        "rectangle", x, y, width, height,
        stroke_color=stroke_color,
        background_color=background_color,
        fill_style=fill_style,
        stroke_width=stroke_width,
        roughness=roughness,
        opacity=opacity,
        frame_id=frame_id,
    )
    if roundness:
        el["roundness"] = {"type": 3}

    project["elements"].append(el)

    if label:
        _add_label_to_shape(project, el, label)

    return el


def add_ellipse(
    project: dict,
    x: float = 100,
    y: float = 100,
    width: float = 160,
    height: float = 120,
    stroke_color: str = "#1e1e1e",
    background_color: str = "transparent",
    fill_style: str = "solid",
    stroke_width: int = 2,
    roughness: int = 1,
    opacity: int = 100,
    label: str | None = None,
    frame_id: str | None = None,
) -> dict:
    """Add an ellipse to the project."""
    if label:
        width = max(width, _min_width_for_label(label))

    el = _base_element(
        "ellipse", x, y, width, height,
        stroke_color=stroke_color,
        background_color=background_color,
        fill_style=fill_style,
        stroke_width=stroke_width,
        roughness=roughness,
        opacity=opacity,
        frame_id=frame_id,
    )
    project["elements"].append(el)

    if label:
        _add_label_to_shape(project, el, label)

    return el


def add_diamond(
    project: dict,
    x: float = 100,
    y: float = 100,
    width: float = 160,
    height: float = 160,
    stroke_color: str = "#1e1e1e",
    background_color: str = "transparent",
    fill_style: str = "solid",
    stroke_width: int = 2,
    roughness: int = 1,
    opacity: int = 100,
    label: str | None = None,
    frame_id: str | None = None,
) -> dict:
    """Add a diamond to the project."""
    if label:
        width = max(width, _min_width_for_label(label))

    el = _base_element(
        "diamond", x, y, width, height,
        stroke_color=stroke_color,
        background_color=background_color,
        fill_style=fill_style,
        stroke_width=stroke_width,
        roughness=roughness,
        opacity=opacity,
        frame_id=frame_id,
    )
    project["elements"].append(el)

    if label:
        _add_label_to_shape(project, el, label)

    return el


# ── Text elements ─────────────────────────────────────────────────────

def add_text(
    project: dict,
    text: str,
    x: float = 100,
    y: float = 100,
    font_size: int = 20,
    font_family: int = 1,
    text_align: str = "left",
    stroke_color: str = "#1e1e1e",
    opacity: int = 100,
    frame_id: str | None = None,
) -> dict:
    """Add a text element to the project.

    Args:
        project: The project dict.
        text: The text content.
        x, y: Position.
        font_size: Font size in px.
        font_family: 1=Virgil (hand-drawn), 2=Helvetica, 3=Cascadia (mono).
        text_align: left, center, or right.
        stroke_color: Text color.
        opacity: 0-100.
        frame_id: Parent frame ID.

    Returns:
        The created element dict.
    """
    # Approximate width/height based on text and font size
    lines = text.split("\n")
    max_chars = max(len(line) for line in lines) if lines else 1
    width = max(max_chars * font_size * 0.6, 50)
    height = len(lines) * font_size * 1.25
    line_height = 1.25

    el = _base_element(
        "text", x, y, width, height,
        stroke_color=stroke_color,
        opacity=opacity,
        frame_id=frame_id,
    )
    el.update({
        "text": text,
        "fontSize": font_size,
        "fontFamily": font_family,
        "textAlign": text_align,
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "lineHeight": line_height,
        "autoResize": True,
    })

    project["elements"].append(el)
    return el


# ── Line / Arrow elements ─────────────────────────────────────────────

def add_line(
    project: dict,
    points: list[list[float]],
    x: float = 0,
    y: float = 0,
    stroke_color: str = "#1e1e1e",
    stroke_width: int = 2,
    stroke_style: str = "solid",
    roughness: int = 1,
    opacity: int = 100,
    frame_id: str | None = None,
) -> dict:
    """Add a line element defined by points.

    Args:
        project: The project dict.
        points: List of [dx, dy] offsets from (x, y). First point is [0, 0].
        x, y: Starting position.

    Returns:
        The created element dict.
    """
    # Width/height from bounding box of points
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    width = max(width, 1)
    height = max(height, 1)

    el = _base_element(
        "line", x, y, width, height,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        stroke_style=stroke_style,
        roughness=roughness,
        opacity=opacity,
        frame_id=frame_id,
    )
    el.update({
        "points": points,
        "lastCommittedPoint": None,
    })

    project["elements"].append(el)
    return el


def add_arrow(
    project: dict,
    x: float = 100,
    y: float = 100,
    end_x: float = 300,
    end_y: float = 100,
    stroke_color: str = "#1e1e1e",
    stroke_width: int = 2,
    stroke_style: str = "solid",
    roughness: int = 1,
    opacity: int = 100,
    start_arrowhead: str | None = None,
    end_arrowhead: str = "arrow",
    from_id: str | None = None,
    to_id: str | None = None,
    label: str | None = None,
    frame_id: str | None = None,
) -> dict:
    """Add an arrow element.

    Args:
        project: The project dict.
        x, y: Start position.
        end_x, end_y: End position.
        from_id: Optional element ID to bind start to.
        to_id: Optional element ID to bind end to.
        start_arrowhead: None, 'arrow', 'bar', 'dot', 'triangle'.
        end_arrowhead: None, 'arrow', 'bar', 'dot', 'triangle'.
        label: Optional label text on the arrow.

    Returns:
        The created element dict.
    """
    dx = end_x - x
    dy = end_y - y
    width = max(abs(dx), 1)
    height = max(abs(dy), 1)
    points = [[0, 0], [dx, dy]]

    el = _base_element(
        "arrow", x, y, width, height,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        stroke_style=stroke_style,
        roughness=roughness,
        opacity=opacity,
        frame_id=frame_id,
    )
    el.update({
        "points": points,
        "lastCommittedPoint": None,
        "startArrowhead": start_arrowhead,
        "endArrowhead": end_arrowhead,
        "startBinding": None,
        "endBinding": None,
        "elbowed": False,
    })

    # If from_id/to_id given, set up bindings and update boundElements
    if from_id:
        from_el = get_element(project, from_id)
        if from_el:
            el["startBinding"] = {
                "elementId": from_id,
                "focus": 0,
                "gap": 5,
            }
            from_el.setdefault("boundElements", [])
            from_el["boundElements"].append({"type": "arrow", "id": el["id"]})

    if to_id:
        to_el = get_element(project, to_id)
        if to_el:
            el["endBinding"] = {
                "elementId": to_id,
                "focus": 0,
                "gap": 5,
            }
            to_el.setdefault("boundElements", [])
            to_el["boundElements"].append({"type": "arrow", "id": el["id"]})

    project["elements"].append(el)

    if label:
        _add_label_to_arrow(project, el, label)

    return el


def connect_elements(
    project: dict,
    from_id: str,
    to_id: str,
    label: str | None = None,
    stroke_color: str = "#1e1e1e",
    stroke_style: str = "solid",
    stroke_width: int = 2,
    roughness: int = 1,
    start_arrowhead: str | None = None,
    end_arrowhead: str = "arrow",
) -> dict:
    """Connect two elements with an arrow.

    Automatically positions the arrow between element centers.

    Args:
        project: The project dict.
        from_id: Source element ID.
        to_id: Target element ID.
        label: Optional label on the arrow.

    Returns:
        The created arrow element.
    """
    from_el = get_element(project, from_id)
    to_el = get_element(project, to_id)

    if not from_el:
        raise ValueError(f"Element not found: {from_id}")
    if not to_el:
        raise ValueError(f"Element not found: {to_id}")

    # Start/end at centers of the elements
    x1 = from_el["x"] + from_el.get("width", 0) / 2
    y1 = from_el["y"] + from_el.get("height", 0) / 2
    x2 = to_el["x"] + to_el.get("width", 0) / 2
    y2 = to_el["y"] + to_el.get("height", 0) / 2

    return add_arrow(
        project, x1, y1, x2, y2,
        stroke_color=stroke_color,
        stroke_style=stroke_style,
        stroke_width=stroke_width,
        roughness=roughness,
        start_arrowhead=start_arrowhead,
        end_arrowhead=end_arrowhead,
        from_id=from_id,
        to_id=to_id,
        label=label,
    )


# ── Frame element ─────────────────────────────────────────────────────

def add_frame(
    project: dict,
    x: float = 50,
    y: float = 50,
    width: float = 400,
    height: float = 300,
    name: str = "Frame",
    stroke_color: str = "#bbb",
    background_color: str = "transparent",
) -> dict:
    """Add a frame container element.

    Args:
        project: The project dict.
        name: Frame label displayed at the top.

    Returns:
        The created frame element.
    """
    now = int(time.time() * 1000)
    eid = str(uuid.uuid4())[:20]

    el = {
        "id": eid,
        "type": "frame",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": background_color,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": random.randint(1, 2**31 - 1),
        "version": 1,
        "versionNonce": random.randint(1, 2**31 - 1),
        "isDeleted": False,
        "boundElements": [],
        "updated": now,
        "link": None,
        "locked": False,
        "name": name,
    }
    project["elements"].append(el)
    return el


# ── Element query/mutation ────────────────────────────────────────────

def get_element(project: dict, element_id: str) -> dict | None:
    """Get element by ID.

    Args:
        project: The project dict.
        element_id: Element ID to find.

    Returns:
        Element dict or None if not found.
    """
    for el in project.get("elements", []):
        if el.get("id") == element_id:
            return el
    return None


def list_elements(
    project: dict,
    element_type: str | None = None,
    frame_id: str | None = None,
    include_deleted: bool = False,
) -> list[dict]:
    """List elements in the project.

    Args:
        project: The project dict.
        element_type: Filter by element type.
        frame_id: Filter by parent frame ID.
        include_deleted: Whether to include soft-deleted elements.

    Returns:
        List of matching element dicts.
    """
    elements = project.get("elements", [])

    if not include_deleted:
        elements = [e for e in elements if not e.get("isDeleted")]

    if element_type:
        elements = [e for e in elements if e.get("type") == element_type]

    if frame_id is not None:
        elements = [e for e in elements if e.get("frameId") == frame_id]

    return elements


def update_element(
    project: dict,
    element_id: str,
    **kwargs,
) -> dict:
    """Update element properties.

    Supported kwargs: x, y, width, height, angle, stroke_color,
    background_color, fill_style, stroke_width, stroke_style,
    roughness, opacity, text, font_size, locked, link.

    Args:
        project: The project dict (modified in-place).
        element_id: ID of element to update.
        **kwargs: Properties to update.

    Returns:
        Updated element dict.

    Raises:
        ValueError: If element not found.
    """
    el = get_element(project, element_id)
    if not el:
        raise ValueError(f"Element not found: {element_id}")

    # Map CLI-friendly names to Excalidraw JSON keys
    field_map = {
        "x": "x",
        "y": "y",
        "width": "width",
        "height": "height",
        "angle": "angle",
        "stroke_color": "strokeColor",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "stroke_width": "strokeWidth",
        "stroke_style": "strokeStyle",
        "roughness": "roughness",
        "opacity": "opacity",
        "text": "text",
        "font_size": "fontSize",
        "font_family": "fontFamily",
        "text_align": "textAlign",
        "locked": "locked",
        "link": "link",
        "name": "name",
    }

    for key, value in kwargs.items():
        json_key = field_map.get(key, key)
        el[json_key] = value

    el["updated"] = int(time.time() * 1000)
    el["version"] = el.get("version", 1) + 1

    return el


def delete_element(project: dict, element_id: str) -> dict:
    """Soft-delete an element (sets isDeleted=True).

    Args:
        project: The project dict (modified in-place).
        element_id: ID of element to delete.

    Returns:
        The deleted element.

    Raises:
        ValueError: If element not found.
    """
    el = get_element(project, element_id)
    if not el:
        raise ValueError(f"Element not found: {element_id}")

    el["isDeleted"] = True
    el["updated"] = int(time.time() * 1000)
    return el


def move_element(
    project: dict,
    element_id: str,
    dx: float = 0,
    dy: float = 0,
) -> dict:
    """Move an element by a delta.

    Args:
        project: The project dict.
        element_id: Element to move.
        dx: X offset.
        dy: Y offset.

    Returns:
        Updated element.
    """
    el = get_element(project, element_id)
    if not el:
        raise ValueError(f"Element not found: {element_id}")

    el["x"] = el.get("x", 0) + dx
    el["y"] = el.get("y", 0) + dy
    el["updated"] = int(time.time() * 1000)
    return el


# ── Internal helpers ──────────────────────────────────────────────────

def _add_label_to_shape(project: dict, shape_el: dict, text: str) -> dict:
    """Add a text label bound to a container shape."""
    cx = shape_el["x"] + shape_el.get("width", 0) / 2
    cy = shape_el["y"] + shape_el.get("height", 0) / 2
    font_size = 16

    lines = text.split("\n")
    max_chars = max(len(line) for line in lines) if lines else 1
    w = max(max_chars * font_size * 0.6, 30)
    h = len(lines) * font_size * 1.25

    text_el = _base_element(
        "text",
        cx - w / 2, cy - h / 2, w, h,
        stroke_color=shape_el.get("strokeColor", "#1e1e1e"),
    )
    text_el.update({
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": shape_el["id"],
        "originalText": text,
        "lineHeight": 1.25,
        "autoResize": True,
    })

    shape_el.setdefault("boundElements", [])
    shape_el["boundElements"].append({"type": "text", "id": text_el["id"]})

    project["elements"].append(text_el)
    return text_el


def _add_label_to_arrow(project: dict, arrow_el: dict, text: str) -> dict:
    """Add a text label bound to an arrow."""
    points = arrow_el.get("points", [[0, 0], [100, 0]])
    mid_x = arrow_el["x"] + (points[0][0] + points[-1][0]) / 2
    mid_y = arrow_el["y"] + (points[0][1] + points[-1][1]) / 2
    font_size = 14

    lines = text.split("\n")
    max_chars = max(len(line) for line in lines) if lines else 1
    w = max(max_chars * font_size * 0.6, 30)
    h = len(lines) * font_size * 1.25

    text_el = _base_element(
        "text",
        mid_x - w / 2, mid_y - h / 2, w, h,
        stroke_color=arrow_el.get("strokeColor", "#1e1e1e"),
    )
    text_el.update({
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": arrow_el["id"],
        "originalText": text,
        "lineHeight": 1.25,
        "autoResize": True,
    })

    arrow_el.setdefault("boundElements", [])
    arrow_el["boundElements"].append({"type": "text", "id": text_el["id"]})

    project["elements"].append(text_el)
    return text_el
