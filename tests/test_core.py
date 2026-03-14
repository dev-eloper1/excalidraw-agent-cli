"""Unit tests for excalidraw-agent-cli core modules.

All tests use synthetic data — no external dependencies, no Node.js required.
"""

import copy
import json
import os
import tempfile

import pytest

from excalidraw_agent_cli.core import elements as elem_mod
from excalidraw_agent_cli.core import project as proj_mod
from excalidraw_agent_cli.core.session import Session


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def empty_project():
    return proj_mod.create_project(name="Test", background="#ffffff")


@pytest.fixture
def project_with_elements(empty_project):
    p = empty_project
    elem_mod.add_rectangle(p, x=50, y=50, width=200, height=100)
    elem_mod.add_ellipse(p, x=300, y=50, width=120, height=100)
    elem_mod.add_text(p, "Hello World", x=50, y=200)
    return p


# ── project.py tests ──────────────────────────────────────────────────

class TestCreateProject:
    def test_default_values(self):
        p = proj_mod.create_project()
        assert p["type"] == "excalidraw"
        assert p["version"] == 2
        assert p["elements"] == []
        assert p["files"] == {}
        assert isinstance(p["appState"], dict)

    def test_custom_name(self):
        p = proj_mod.create_project(name="My Diagram")
        assert p["_meta"]["name"] == "My Diagram"

    def test_custom_background(self):
        p = proj_mod.create_project(background="#333333")
        assert p["appState"]["viewBackgroundColor"] == "#333333"

    def test_grid_enabled(self):
        p = proj_mod.create_project(grid=True)
        assert p["appState"]["gridSize"] == 20

    def test_grid_disabled(self):
        p = proj_mod.create_project(grid=False)
        assert p["appState"]["gridSize"] is None

    def test_has_meta_timestamps(self):
        p = proj_mod.create_project()
        assert "created" in p["_meta"]
        assert "modified" in p["_meta"]


class TestSaveLoadProject:
    def test_save_creates_file(self, tmp_dir, empty_project):
        path = os.path.join(tmp_dir, "test")
        saved = proj_mod.save_project(empty_project, path)
        assert os.path.exists(saved)
        assert saved.endswith(".excalidraw")

    def test_save_valid_json(self, tmp_dir, empty_project):
        path = os.path.join(tmp_dir, "test.excalidraw")
        proj_mod.save_project(empty_project, path)
        with open(path) as f:
            data = json.load(f)
        assert data["type"] == "excalidraw"
        assert data["version"] == 2

    def test_save_strips_meta(self, tmp_dir, empty_project):
        path = os.path.join(tmp_dir, "test.excalidraw")
        proj_mod.save_project(empty_project, path)
        with open(path) as f:
            data = json.load(f)
        assert "_meta" not in data

    def test_load_valid_file(self, tmp_dir, empty_project):
        path = os.path.join(tmp_dir, "test.excalidraw")
        proj_mod.save_project(empty_project, path)
        loaded = proj_mod.load_project(path)
        assert loaded["type"] == "excalidraw"
        assert isinstance(loaded["elements"], list)

    def test_load_missing_file(self, tmp_dir):
        with pytest.raises(FileNotFoundError):
            proj_mod.load_project(os.path.join(tmp_dir, "nope.excalidraw"))

    def test_load_invalid_type(self, tmp_dir):
        path = os.path.join(tmp_dir, "bad.excalidraw")
        with open(path, "w") as f:
            json.dump({"type": "svg", "elements": []}, f)
        with pytest.raises(ValueError, match="Not a valid"):
            proj_mod.load_project(path)

    def test_roundtrip_preserves_elements(self, tmp_dir, project_with_elements):
        path = os.path.join(tmp_dir, "roundtrip.excalidraw")
        orig_count = len(project_with_elements["elements"])
        proj_mod.save_project(project_with_elements, path)
        loaded = proj_mod.load_project(path)
        assert len(loaded["elements"]) == orig_count


class TestGetProjectInfo:
    def test_empty_project(self, empty_project):
        info = proj_mod.get_project_info(empty_project)
        assert info["element_count"] == 0
        assert info["bounds"] is None
        assert info["name"] == "Test"

    def test_element_count(self, project_with_elements):
        info = proj_mod.get_project_info(project_with_elements)
        assert info["element_count"] == 3

    def test_type_breakdown(self, project_with_elements):
        info = proj_mod.get_project_info(project_with_elements)
        assert "rectangle" in info["element_types"]
        assert "ellipse" in info["element_types"]
        assert "text" in info["element_types"]

    def test_bounds_calculated(self, empty_project):
        p = empty_project
        elem_mod.add_rectangle(p, x=10, y=20, width=100, height=50)
        elem_mod.add_rectangle(p, x=50, y=10, width=200, height=100)
        info = proj_mod.get_project_info(p)
        b = info["bounds"]
        assert b["x"] == 10
        assert b["y"] == 10
        assert b["width"] == 240   # max(x+w) - min(x) = 250 - 10
        assert b["height"] == 100  # max(y+h) - min(y) = 110 - 10


class TestValidateProject:
    def test_valid_project(self, empty_project):
        issues = proj_mod.validate_project(empty_project)
        assert issues == []

    def test_missing_type(self):
        p = {"version": 2, "elements": []}
        issues = proj_mod.validate_project(p)
        assert any("type" in i for i in issues)

    def test_duplicate_ids(self, empty_project):
        elem_mod.add_rectangle(empty_project, x=0, y=0)
        elem_mod.add_rectangle(empty_project, x=0, y=0)
        # Force duplicate
        empty_project["elements"][1]["id"] = empty_project["elements"][0]["id"]
        issues = proj_mod.validate_project(empty_project)
        assert any("Duplicate" in i for i in issues)

    def test_missing_element_id(self, empty_project):
        elem_mod.add_rectangle(empty_project, x=0, y=0)
        del empty_project["elements"][0]["id"]
        issues = proj_mod.validate_project(empty_project)
        assert any("missing" in i.lower() and "id" in i.lower() for i in issues)


# ── elements.py tests ─────────────────────────────────────────────────

class TestAddRectangle:
    def test_type_and_position(self, empty_project):
        el = elem_mod.add_rectangle(empty_project, x=10, y=20, width=100, height=50)
        assert el["type"] == "rectangle"
        assert el["x"] == 10
        assert el["y"] == 20
        assert el["width"] == 100
        assert el["height"] == 50

    def test_added_to_project(self, empty_project):
        el = elem_mod.add_rectangle(empty_project)
        assert el in empty_project["elements"]

    def test_has_unique_id(self, empty_project):
        el1 = elem_mod.add_rectangle(empty_project)
        el2 = elem_mod.add_rectangle(empty_project)
        assert el1["id"] != el2["id"]

    def test_roundness_flag(self, empty_project):
        el = elem_mod.add_rectangle(empty_project, roundness=True)
        assert el["roundness"] is not None

    def test_label_creates_text_child(self, empty_project):
        el = elem_mod.add_rectangle(empty_project, label="My Box")
        assert len(empty_project["elements"]) == 2
        text_el = empty_project["elements"][1]
        assert text_el["type"] == "text"
        assert text_el["text"] == "My Box"
        assert text_el["containerId"] == el["id"]

    def test_custom_colors(self, empty_project):
        el = elem_mod.add_rectangle(
            empty_project, stroke_color="#ff0000", background_color="#00ff00"
        )
        assert el["strokeColor"] == "#ff0000"
        assert el["backgroundColor"] == "#00ff00"


class TestAddEllipse:
    def test_type(self, empty_project):
        el = elem_mod.add_ellipse(empty_project)
        assert el["type"] == "ellipse"

    def test_dimensions(self, empty_project):
        el = elem_mod.add_ellipse(empty_project, x=5, y=10, width=80, height=60)
        assert el["width"] == 80
        assert el["height"] == 60


class TestAddDiamond:
    def test_type(self, empty_project):
        el = elem_mod.add_diamond(empty_project)
        assert el["type"] == "diamond"

    def test_label(self, empty_project):
        elem_mod.add_diamond(empty_project, label="Decision")
        text_els = [e for e in empty_project["elements"] if e["type"] == "text"]
        assert len(text_els) == 1
        assert text_els[0]["text"] == "Decision"


class TestAddText:
    def test_type_and_content(self, empty_project):
        el = elem_mod.add_text(empty_project, "Hello")
        assert el["type"] == "text"
        assert el["text"] == "Hello"
        assert el["originalText"] == "Hello"

    def test_font_size(self, empty_project):
        el = elem_mod.add_text(empty_project, "X", font_size=32)
        assert el["fontSize"] == 32

    def test_font_family(self, empty_project):
        el = elem_mod.add_text(empty_project, "X", font_family=2)
        assert el["fontFamily"] == 2

    def test_multiline_height(self, empty_project):
        el = elem_mod.add_text(empty_project, "Line 1\nLine 2\nLine 3", font_size=20)
        assert el["height"] > 20 * 2  # must be tall enough for 3 lines

    def test_text_align(self, empty_project):
        el = elem_mod.add_text(empty_project, "Centered", text_align="center")
        assert el["textAlign"] == "center"


class TestAddArrow:
    def test_type(self, empty_project):
        el = elem_mod.add_arrow(empty_project, x=0, y=0, end_x=100, end_y=0)
        assert el["type"] == "arrow"

    def test_points(self, empty_project):
        el = elem_mod.add_arrow(empty_project, x=10, y=20, end_x=110, end_y=20)
        assert el["points"][0] == [0, 0]
        assert el["points"][-1] == [100, 0]

    def test_arrowheads(self, empty_project):
        el = elem_mod.add_arrow(empty_project, end_arrowhead="bar", start_arrowhead="dot")
        assert el["endArrowhead"] == "bar"
        assert el["startArrowhead"] == "dot"

    def test_from_to_binding(self, empty_project):
        r1 = elem_mod.add_rectangle(empty_project, x=0, y=0, width=100, height=50)
        r2 = elem_mod.add_rectangle(empty_project, x=200, y=0, width=100, height=50)
        arrow = elem_mod.add_arrow(
            empty_project, x=100, y=25, end_x=200, end_y=25,
            from_id=r1["id"], to_id=r2["id"],
        )
        assert arrow["startBinding"]["elementId"] == r1["id"]
        assert arrow["endBinding"]["elementId"] == r2["id"]
        assert any(b["id"] == arrow["id"] for b in r1["boundElements"])


class TestAddLine:
    def test_type(self, empty_project):
        el = elem_mod.add_line(empty_project, [[0, 0], [100, 50]])
        assert el["type"] == "line"

    def test_points_stored(self, empty_project):
        pts = [[0, 0], [100, 0], [100, 100]]
        el = elem_mod.add_line(empty_project, pts)
        assert el["points"] == pts


class TestAddFrame:
    def test_type_and_name(self, empty_project):
        el = elem_mod.add_frame(empty_project, name="Section A")
        assert el["type"] == "frame"
        assert el["name"] == "Section A"

    def test_dimensions(self, empty_project):
        el = elem_mod.add_frame(empty_project, x=10, y=10, width=500, height=400)
        assert el["width"] == 500
        assert el["height"] == 400


class TestConnectElements:
    def test_creates_arrow(self, empty_project):
        r1 = elem_mod.add_rectangle(empty_project, x=0, y=0, width=100, height=50)
        r2 = elem_mod.add_rectangle(empty_project, x=200, y=0, width=100, height=50)
        arrow = elem_mod.connect_elements(empty_project, r1["id"], r2["id"])
        assert arrow["type"] == "arrow"

    def test_missing_from_raises(self, empty_project):
        r2 = elem_mod.add_rectangle(empty_project)
        with pytest.raises(ValueError, match="not found"):
            elem_mod.connect_elements(empty_project, "bad-id", r2["id"])

    def test_missing_to_raises(self, empty_project):
        r1 = elem_mod.add_rectangle(empty_project)
        with pytest.raises(ValueError, match="not found"):
            elem_mod.connect_elements(empty_project, r1["id"], "bad-id")


class TestElementQuery:
    def test_get_by_id(self, project_with_elements):
        el = project_with_elements["elements"][0]
        found = elem_mod.get_element(project_with_elements, el["id"])
        assert found is el

    def test_get_missing_returns_none(self, empty_project):
        assert elem_mod.get_element(empty_project, "nonexistent") is None

    def test_list_all(self, project_with_elements):
        els = elem_mod.list_elements(project_with_elements)
        assert len(els) == 3

    def test_list_by_type(self, project_with_elements):
        rects = elem_mod.list_elements(project_with_elements, element_type="rectangle")
        assert len(rects) == 1
        assert all(e["type"] == "rectangle" for e in rects)

    def test_list_excludes_deleted(self, project_with_elements):
        el = project_with_elements["elements"][0]
        el["isDeleted"] = True
        els = elem_mod.list_elements(project_with_elements)
        assert len(els) == 2

    def test_list_includes_deleted_when_requested(self, project_with_elements):
        project_with_elements["elements"][0]["isDeleted"] = True
        els = elem_mod.list_elements(project_with_elements, include_deleted=True)
        assert len(els) == 3


class TestElementMutation:
    def test_update_position(self, empty_project):
        el = elem_mod.add_rectangle(empty_project, x=10, y=10)
        elem_mod.update_element(empty_project, el["id"], x=50, y=60)
        assert el["x"] == 50
        assert el["y"] == 60

    def test_update_color(self, empty_project):
        el = elem_mod.add_rectangle(empty_project)
        elem_mod.update_element(empty_project, el["id"], stroke_color="#ff0000")
        assert el["strokeColor"] == "#ff0000"

    def test_update_increments_version(self, empty_project):
        el = elem_mod.add_rectangle(empty_project)
        v0 = el["version"]
        elem_mod.update_element(empty_project, el["id"], x=99)
        assert el["version"] == v0 + 1

    def test_update_missing_raises(self, empty_project):
        with pytest.raises(ValueError, match="not found"):
            elem_mod.update_element(empty_project, "bad-id", x=0)

    def test_delete_sets_flag(self, empty_project):
        el = elem_mod.add_rectangle(empty_project)
        elem_mod.delete_element(empty_project, el["id"])
        assert el["isDeleted"] is True

    def test_delete_missing_raises(self, empty_project):
        with pytest.raises(ValueError, match="not found"):
            elem_mod.delete_element(empty_project, "bad")

    def test_move_adds_delta(self, empty_project):
        el = elem_mod.add_rectangle(empty_project, x=100, y=200)
        elem_mod.move_element(empty_project, el["id"], dx=50, dy=-30)
        assert el["x"] == 150
        assert el["y"] == 170


# ── session.py tests ──────────────────────────────────────────────────

class TestSession:
    def test_fresh_session_empty(self):
        s = Session()
        assert s.project is None
        assert s.project_path is None
        assert not s.modified

    def test_set_project(self, empty_project):
        s = Session()
        s.set_project(empty_project, "/tmp/test.excalidraw")
        assert s.project is empty_project
        assert s.project_path == "/tmp/test.excalidraw"

    def test_checkpoint_and_undo(self, empty_project):
        s = Session()
        s.set_project(empty_project)

        el = elem_mod.add_rectangle(empty_project)
        s.checkpoint("add rectangle")
        # The checkpoint saves the state BEFORE adding — but we called it after
        # So: add element, checkpoint (saves current), add another, undo → removes second

        el2 = elem_mod.add_rectangle(empty_project)
        s.checkpoint("add second rectangle")
        elem_mod.add_rectangle(empty_project)  # third element added after checkpoint

        op = s.undo()
        assert op == "add second rectangle"
        # After undo, project goes back to the state captured in the "add second rectangle" checkpoint

    def test_undo_empty_returns_none(self):
        s = Session()
        s.set_project({})
        assert s.undo() is None

    def test_redo_empty_returns_none(self):
        s = Session()
        s.set_project({})
        assert s.redo() is None

    def test_undo_redo_cycle(self, empty_project):
        s = Session()
        s.set_project(empty_project)

        # Checkpoint → add
        s.checkpoint("op1")
        elem_mod.add_rectangle(empty_project)

        # Undo → back to original state (0 elements)
        op = s.undo()
        assert op == "op1"
        # After undo, project is restored to snapshot (empty)
        assert s.project["elements"] == []

        # Redo → back to 1 element
        redo_op = s.redo()
        assert redo_op == "op1"

    def test_get_status(self, empty_project):
        s = Session()
        s.set_project(empty_project, "/tmp/test.excalidraw")
        elem_mod.add_rectangle(empty_project)
        s.mark_modified()

        status = s.get_status()
        assert status["element_count"] == 1
        assert status["modified"] is True
        assert status["project_path"] == "/tmp/test.excalidraw"

    def test_save_load_session(self, tmp_dir, empty_project):
        s = Session()
        s.set_project(empty_project, "/tmp/test.excalidraw")
        session_file = os.path.join(tmp_dir, "session.json")
        s.save_to_disk(session_file)

        s2 = Session()
        restored = s2.load_from_disk(session_file)
        assert restored is True
        assert s2.project_path == "/tmp/test.excalidraw"

    def test_checkpoint_undo_preserves_elements(self, empty_project):
        s = Session()
        s.set_project(empty_project)

        # Before: no elements
        assert len(empty_project["elements"]) == 0

        # Checkpoint captures current state (0 elements), then we add
        s.checkpoint("before add")
        elem_mod.add_rectangle(empty_project)
        elem_mod.add_ellipse(empty_project)
        assert len(empty_project["elements"]) == 2

        # Undo restores to 0
        s.undo()
        assert len(s.project["elements"]) == 0

        # Redo goes back to 2
        s.redo()
        assert len(s.project["elements"]) == 2
