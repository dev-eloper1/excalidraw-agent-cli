"""End-to-end tests for excalidraw-agent-cli.

Includes:
1. File pipeline tests (JSON structure validation, no Node.js needed)
2. Node.js backend tests (SVG/PNG export via real Excalidraw engine)
3. CLI subprocess tests (installed `excalidraw-agent-cli` command)
"""

import json
import os
import subprocess
import sys
import tempfile
import zipfile

import pytest

from excalidraw_agent_cli.core import elements as elem_mod
from excalidraw_agent_cli.core import export as export_mod
from excalidraw_agent_cli.core import project as proj_mod


# ── CLI resolver ──────────────────────────────────────────────────────

def _resolve_cli(name):
    """Resolve installed CLI command; falls back to python -m for dev.

    Set env CLI_ANYTHING_FORCE_INSTALLED=1 to require the installed command.
    """
    import shutil
    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = shutil.which(name)
    if path:
        print(f"[_resolve_cli] Using installed command: {path}")
        return [path]
    if force:
        raise RuntimeError(
            f"{name} not found in PATH. Install with:\n"
            f"  cd agent-harness && pip install -e ."
        )
    module = "excalidraw_agent_cli.cli"
    print(f"[_resolve_cli] Falling back to: {sys.executable} -m {module}")
    return [sys.executable, "-m", module]


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def base_project():
    return proj_mod.create_project(name="E2E Test", background="#ffffff")


# ── File Pipeline E2E Tests ───────────────────────────────────────────

class TestExcalidrawFileE2E:
    """Tests that verify .excalidraw file generation is structurally correct."""

    def test_empty_project_json(self, tmp_dir, base_project):
        """Save and verify minimal valid .excalidraw JSON structure."""
        path = os.path.join(tmp_dir, "empty.excalidraw")
        proj_mod.save_project(base_project, path)

        assert os.path.exists(path)
        size = os.path.getsize(path)
        assert size > 0, "File is empty"
        print(f"\n  excalidraw: {path} ({size:,} bytes)")

        with open(path) as f:
            data = json.load(f)

        assert data["type"] == "excalidraw"
        assert data["version"] == 2
        assert isinstance(data["elements"], list)
        assert isinstance(data["appState"], dict)
        assert isinstance(data["files"], dict)
        assert "_meta" not in data  # Internal field stripped on save

    def test_rectangle_roundtrip(self, tmp_dir, base_project):
        """Rectangle element survives save → load with correct fields."""
        el = elem_mod.add_rectangle(
            base_project, x=50, y=60, width=200, height=100,
            stroke_color="#ff0000", background_color="#eeeeee",
        )
        path = os.path.join(tmp_dir, "rect.excalidraw")
        proj_mod.save_project(base_project, path)

        loaded = proj_mod.load_project(path)
        loaded_el = next(e for e in loaded["elements"] if e["id"] == el["id"])

        assert loaded_el["type"] == "rectangle"
        assert loaded_el["x"] == 50
        assert loaded_el["y"] == 60
        assert loaded_el["width"] == 200
        assert loaded_el["height"] == 100
        assert loaded_el["strokeColor"] == "#ff0000"
        assert loaded_el["backgroundColor"] == "#eeeeee"

    def test_multi_element_project(self, tmp_dir, base_project):
        """All element types are saved and reloaded correctly."""
        rect = elem_mod.add_rectangle(base_project, x=50, y=50, width=150, height=80)
        ellipse = elem_mod.add_ellipse(base_project, x=250, y=50, width=120, height=100)
        diamond = elem_mod.add_diamond(base_project, x=50, y=200, width=120, height=120)
        text = elem_mod.add_text(base_project, "Hello!", x=250, y=200)
        line = elem_mod.add_line(base_project, [[0, 0], [100, 50], [200, 0]], x=50, y=380)
        frame = elem_mod.add_frame(base_project, x=0, y=0, width=500, height=600, name="Main Frame")

        path = os.path.join(tmp_dir, "multi.excalidraw")
        proj_mod.save_project(base_project, path)
        print(f"\n  excalidraw: {path} ({os.path.getsize(path):,} bytes)")

        loaded = proj_mod.load_project(path)
        el_ids = {e["id"] for e in loaded["elements"]}

        assert rect["id"] in el_ids
        assert ellipse["id"] in el_ids
        assert diamond["id"] in el_ids
        assert text["id"] in el_ids
        assert line["id"] in el_ids
        assert frame["id"] in el_ids

        type_map = {e["id"]: e["type"] for e in loaded["elements"]}
        assert type_map[frame["id"]] == "frame"

    def test_connect_elements_binding_persists(self, tmp_dir, base_project):
        """Arrow bindings (startBinding/endBinding) survive save/load."""
        r1 = elem_mod.add_rectangle(base_project, x=50, y=100, width=120, height=80)
        r2 = elem_mod.add_rectangle(base_project, x=300, y=100, width=120, height=80)
        arrow = elem_mod.connect_elements(base_project, r1["id"], r2["id"], label="link")

        path = os.path.join(tmp_dir, "connected.excalidraw")
        proj_mod.save_project(base_project, path)

        loaded = proj_mod.load_project(path)
        loaded_arrow = next(
            e for e in loaded["elements"]
            if e["id"] == arrow["id"]
        )

        assert loaded_arrow["type"] == "arrow"
        assert loaded_arrow["startBinding"]["elementId"] == r1["id"]
        assert loaded_arrow["endBinding"]["elementId"] == r2["id"]

    def test_undo_redo_cycle(self, tmp_dir, base_project):
        """5 adds, undo 3, redo 2 → correct final element count."""
        from excalidraw_agent_cli.core.session import Session
        s = Session()
        s.set_project(base_project)

        # Add 5 elements with checkpoints
        for i in range(5):
            s.checkpoint(f"add-{i}")
            elem_mod.add_rectangle(base_project, x=i*60, y=0)

        # After 5 adds: 5 active elements in project (checkpoints saved states 0..4)
        active = [e for e in s.project["elements"] if not e.get("isDeleted")]
        assert len(active) == 5

        # Undo 3 times
        for _ in range(3):
            s.undo()

        active_after_undo = [e for e in s.project["elements"] if not e.get("isDeleted")]
        assert len(active_after_undo) == 2

        # Redo 2 times
        for _ in range(2):
            s.redo()

        active_after_redo = [e for e in s.project["elements"] if not e.get("isDeleted")]
        assert len(active_after_redo) == 4

    def test_validate_valid_project(self, base_project):
        """A well-formed project passes validation."""
        elem_mod.add_rectangle(base_project)
        elem_mod.add_text(base_project, "Label")
        issues = proj_mod.validate_project(base_project)
        assert issues == [], f"Unexpected issues: {issues}"

    def test_validate_corrupt_project(self):
        """Missing type and duplicate IDs are caught by validator."""
        bad = {"version": 2, "elements": [
            {"id": "same", "type": "rectangle", "x": 0, "y": 0, "width": 1, "height": 1},
            {"id": "same", "type": "ellipse", "x": 0, "y": 0, "width": 1, "height": 1},
        ], "appState": {}, "files": {}}
        issues = proj_mod.validate_project(bad)
        assert len(issues) >= 2  # missing type + duplicate id

    def test_project_info_bounds(self, base_project):
        """Bounding box is correctly computed for known element layout."""
        elem_mod.add_rectangle(base_project, x=100, y=100, width=200, height=100)
        elem_mod.add_rectangle(base_project, x=400, y=200, width=100, height=150)

        info = proj_mod.get_project_info(base_project)
        b = info["bounds"]

        assert b["x"] == 100
        assert b["y"] == 100
        # max X = 400+100=500, min X = 100 → width = 400
        assert b["width"] == 400
        # max Y = 200+150=350, min Y = 100 → height = 250
        assert b["height"] == 250


# ── Node.js Export E2E Tests ──────────────────────────────────────────

class TestNodeJsExportE2E:
    """Tests that verify SVG/PNG export via the real Node.js backend."""

    @pytest.fixture
    def diagram_project(self, base_project):
        """Create a project with several elements for export testing."""
        elem_mod.add_rectangle(base_project, x=100, y=100, width=200, height=120,
                               stroke_color="#1e1e1e", background_color="#f0f0f0",
                               label="Start")
        elem_mod.add_diamond(base_project, x=150, y=300, width=150, height=120,
                             label="Decision?")
        elem_mod.add_ellipse(base_project, x=100, y=500, width=160, height=100,
                             background_color="#d0f0d0", label="End")
        elem_mod.add_text(base_project, "System Diagram", x=80, y=50, font_size=24)

        r_elements = [e for e in base_project["elements"] if e["type"] == "rectangle"]
        d_elements = [e for e in base_project["elements"] if e["type"] == "diamond"]
        if r_elements and d_elements:
            elem_mod.connect_elements(base_project, r_elements[0]["id"], d_elements[0]["id"])

        return base_project

    def test_svg_export(self, tmp_dir, diagram_project):
        """Export to SVG: file exists, size > 0, valid SVG content."""
        output = os.path.join(tmp_dir, "diagram.svg")
        result = export_mod.export_svg(diagram_project, output, overwrite=True)

        assert os.path.exists(result["output"]), "SVG file not created"
        assert result["file_size"] > 0, "SVG file is empty"
        print(f"\n  SVG: {result['output']} ({result['file_size']:,} bytes)")

        with open(result["output"], encoding="utf-8") as f:
            content = f.read()

        assert "<svg" in content, "Not valid SVG: missing <svg tag"
        assert "viewBox" in content, "SVG missing viewBox attribute"
        assert "xmlns" in content, "SVG missing xmlns"

    def test_svg_dark_mode(self, tmp_dir, diagram_project):
        """Dark mode SVG has data-theme=dark attribute."""
        output = os.path.join(tmp_dir, "dark.svg")
        result = export_mod.export_svg(diagram_project, output,
                                        overwrite=True, dark_mode=True)
        print(f"\n  Dark SVG: {result['output']} ({result['file_size']:,} bytes)")

        with open(result["output"], encoding="utf-8") as f:
            content = f.read()
        assert 'data-theme="dark"' in content or "dark" in content.lower()

    def test_svg_with_text_content(self, tmp_dir, base_project):
        """Text elements appear in SVG output."""
        elem_mod.add_text(base_project, "My Unique Label XYZ", x=50, y=50, font_size=20)
        output = os.path.join(tmp_dir, "text.svg")
        result = export_mod.export_svg(base_project, output, overwrite=True)
        print(f"\n  Text SVG: {result['output']} ({result['file_size']:,} bytes)")

        with open(result["output"], encoding="utf-8") as f:
            content = f.read()
        assert "My Unique Label XYZ" in content, "Text not found in SVG output"

    def test_png_export(self, tmp_dir, diagram_project):
        """Export to PNG: file exists, size > 0, PNG magic bytes."""
        output = os.path.join(tmp_dir, "diagram.png")
        result = export_mod.export_png(diagram_project, output, overwrite=True)

        assert os.path.exists(result["output"]), "PNG file not created"
        assert result["file_size"] > 0, "PNG file is empty"
        print(f"\n  PNG: {result['output']} ({result['file_size']:,} bytes)")

        with open(result["output"], "rb") as f:
            magic = f.read(8)
        assert magic[:4] == b"\x89PNG", f"Not a valid PNG (magic bytes: {magic[:4]!r})"

    def test_svg_embed_scene(self, tmp_dir, base_project):
        """When embed_scene=True, SVG contains encoded scene metadata."""
        elem_mod.add_rectangle(base_project, x=0, y=0, width=100, height=100)
        output = os.path.join(tmp_dir, "embedded.svg")
        result = export_mod.export_svg(base_project, output,
                                        overwrite=True, embed_scene=True)
        print(f"\n  Embedded SVG: {result['output']} ({result['file_size']:,} bytes)")

        with open(result["output"], encoding="utf-8") as f:
            content = f.read()
        assert "excalidraw" in content.lower(), "Scene data not embedded in SVG"

    def test_overwrite_protection(self, tmp_dir, base_project):
        """Export raises FileExistsError if output exists and overwrite=False."""
        output = os.path.join(tmp_dir, "test.svg")
        with open(output, "w") as f:
            f.write("existing")

        with pytest.raises(FileExistsError):
            export_mod.export_svg(base_project, output, overwrite=False)


# ── CLI Subprocess E2E Tests ──────────────────────────────────────────

class TestCLISubprocess:
    """Tests the installed excalidraw-agent-cli command end-to-end."""

    CLI_BASE = _resolve_cli("excalidraw-agent-cli")

    def _run(self, args, check=True, env=None):
        return subprocess.run(
            self.CLI_BASE + args,
            capture_output=True, text=True,
            check=check,
            env=env,
        )

    def test_help(self):
        """--help exits 0 and shows expected command groups."""
        result = self._run(["--help"])
        assert result.returncode == 0
        assert "project" in result.stdout
        assert "element" in result.stdout
        assert "export" in result.stdout

    def test_project_new_json(self, tmp_dir):
        """project new --json returns valid JSON with expected fields."""
        out = os.path.join(tmp_dir, "new.excalidraw")
        result = self._run(["--json", "project", "new", "-o", out, "-n", "Test Project"])
        assert result.returncode == 0, f"stderr: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["status"] == "created"
        assert data["name"] == "Test Project"
        assert os.path.exists(data["path"])

    def test_element_add_and_list(self, tmp_dir):
        """Add rectangle, then list → element appears in JSON output."""
        proj_path = os.path.join(tmp_dir, "test.excalidraw")

        # Create project
        self._run(["--json", "project", "new", "-o", proj_path])

        # Add rectangle
        add_result = self._run([
            "--json", "--project", proj_path,
            "element", "add", "rectangle",
            "--x", "50", "--y", "50", "--width", "200", "--height", "100",
        ])
        assert add_result.returncode == 0
        add_data = json.loads(add_result.stdout)
        el_id = add_data["id"]
        assert add_data["type"] == "rectangle"

        # List elements
        list_result = self._run(["--json", "--project", proj_path, "element", "list"])
        assert list_result.returncode == 0
        list_data = json.loads(list_result.stdout)
        el_ids = [e["id"] for e in list_data["elements"]]
        assert el_id in el_ids, f"Added element {el_id} not found in list"

    def test_full_flowchart_workflow(self, tmp_dir):
        """Create project, add 3 shapes, connect, export SVG, verify output."""
        proj_path = os.path.join(tmp_dir, "flowchart.excalidraw")
        svg_path = os.path.join(tmp_dir, "flowchart.svg")

        # Create project
        self._run(["project", "new", "-o", proj_path, "-n", "Flowchart"])

        # Add Start rectangle
        r1 = self._run([
            "--json", "--project", proj_path,
            "element", "add", "rectangle",
            "--x", "100", "--y", "100", "--width", "160", "--height", "80",
            "--label", "Start",
        ])
        r1_id = json.loads(r1.stdout)["id"]

        # Add Decision diamond
        d1 = self._run([
            "--json", "--project", proj_path,
            "element", "add", "diamond",
            "--x", "110", "--y", "260", "--width", "140", "--height", "120",
            "--label", "Valid?",
        ])
        d1_id = json.loads(d1.stdout)["id"]

        # Add End ellipse
        e1 = self._run([
            "--json", "--project", proj_path,
            "element", "add", "ellipse",
            "--x", "110", "--y", "460", "--width", "140", "--height", "80",
            "--label", "Done",
        ])
        e1_id = json.loads(e1.stdout)["id"]

        # Connect Start → Decision
        self._run([
            "--project", proj_path,
            "element", "connect", "--from", r1_id, "--to", d1_id, "--label", "→",
        ])

        # Connect Decision → End
        self._run([
            "--project", proj_path,
            "element", "connect", "--from", d1_id, "--to", e1_id, "--label", "Yes",
        ])

        # Export SVG
        export_result = self._run([
            "--json", "--project", proj_path,
            "export", "svg", "-o", svg_path, "--overwrite",
        ])
        assert export_result.returncode == 0, f"Export failed: {export_result.stderr}"

        export_data = json.loads(export_result.stdout)
        assert os.path.exists(export_data["output"]), "SVG not created"
        assert export_data["file_size"] > 100

        with open(svg_path, encoding="utf-8") as f:
            svg_content = f.read()
        assert "<svg" in svg_content

        print(f"\n  Flowchart SVG: {svg_path} ({export_data['file_size']:,} bytes)")

    def test_session_undo_via_cli(self, tmp_dir):
        """Add element, verify it persists, check session status."""
        proj_path = os.path.join(tmp_dir, "undo_test.excalidraw")

        self._run(["project", "new", "-o", proj_path])

        # Add rectangle (auto-saved to disk)
        add_result = self._run([
            "--json", "--project", proj_path,
            "element", "add", "rectangle",
            "--x", "10", "--y", "10",
        ])
        assert add_result.returncode == 0
        el_id = json.loads(add_result.stdout)["id"]

        # List from a NEW subprocess call: element should be persisted on disk
        list_result = self._run(["--json", "--project", proj_path, "element", "list"])
        list_data = json.loads(list_result.stdout)
        assert list_data["count"] >= 1, \
            "Element not persisted — auto-save may not be working"
        el_ids = [e["id"] for e in list_data["elements"]]
        assert el_id in el_ids, f"Added element {el_id} not found after auto-save"

        # Session status (per-process session, undo stack is fresh in new process)
        status_result = self._run(["--json", "--project", proj_path, "session", "status"])
        assert status_result.returncode == 0
        status_data = json.loads(status_result.stdout)
        assert "element_count" in status_data
        assert status_data["element_count"] >= 1

    def test_backend_check_json(self):
        """backend check --json returns valid JSON with 'available' field."""
        result = self._run(["--json", "backend", "check"], check=False)
        # Don't check returncode — backend may not be available in all envs
        try:
            data = json.loads(result.stdout)
            assert "available" in data
            assert "issues" in data
            print(f"\n  Backend available: {data['available']}")
            if data["node_path"]:
                print(f"  Node.js: {data['node_path']}")
        except json.JSONDecodeError:
            pytest.fail(f"backend check did not return JSON. stdout: {result.stdout[:200]}")
