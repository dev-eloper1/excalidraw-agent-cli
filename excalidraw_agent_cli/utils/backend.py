"""Backend integration for Excalidraw CLI.

Locates Node.js and the export helper script.
The export helper uses the real Excalidraw engine (via Puppeteer / jsdom)
to render .excalidraw files to SVG and PNG.

export.js and package.json ship inside the Python package at
  excalidraw_agent_cli/export_helper/

On first use, node_modules are installed into a user-writable cache at
  ~/.cache/excalidraw-agent-cli/
so the PyPI wheel stays small (no 52 MB node_modules bundled).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────

# Where export.js ships inside the installed package
_BUNDLED_HELPER_DIR = Path(__file__).parent.parent / "export_helper"

# User cache dir: ~/.cache/excalidraw-agent-cli  (XDG_CACHE_HOME aware)
_CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "excalidraw-agent-cli"


def find_node() -> str:
    """Find the Node.js executable.

    Returns:
        Absolute path to the node binary.

    Raises:
        RuntimeError: If Node.js is not installed.
    """
    node = shutil.which("node") or shutil.which("nodejs")
    if node:
        return node

    raise RuntimeError(
        "Node.js is not installed or not in PATH.\n"
        "Install it with:\n"
        "  brew install node          # macOS\n"
        "  apt install nodejs npm     # Debian/Ubuntu\n"
        "  https://nodejs.org/en/download/"
    )


def _ensure_node_modules() -> Path:
    """Return the directory containing export.js, installing node_modules if needed.

    Strategy:
    1. If the repo-local export_helper/ exists and has node_modules, use it as-is
       (dev / editable-install workflow — no extra work needed).
    2. Otherwise, use the bundled export.js from inside the package and install
       node_modules into ~/.cache/excalidraw-agent-cli/.

    Returns:
        Path to the directory that contains export.js and node_modules/.
    """
    # ── 1. Dev layout: agent-harness/export_helper/ alongside the source ──
    # _BUNDLED_HELPER_DIR = .../agent-harness/excalidraw_agent_cli/export_helper/
    # .parent = excalidraw_agent_cli/  .parent = excalidraw-agent-cli/ (repo root)
    # No dev split layout in standalone repo — always use bundled path
    dev_helper_dir = _BUNDLED_HELPER_DIR.parent.parent / "export_helper"
    if (dev_helper_dir / "export.js").exists() and (dev_helper_dir / "node_modules").exists():
        return dev_helper_dir

    # ── 2. Installed (PyPI / pip install) — use bundled files + cache dir ──
    bundled_js = _BUNDLED_HELPER_DIR / "export.js"
    if not bundled_js.exists():
        raise RuntimeError(
            "export.js not found inside the installed package.\n"
            "Re-install with: pip install --force-reinstall excalidraw-agent-cli"
        )

    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached_js = _CACHE_DIR / "export.js"
    cached_pkg = _CACHE_DIR / "package.json"
    cached_lock = _CACHE_DIR / "package-lock.json"

    # Copy source files to cache dir if they're missing or outdated
    for src, dst in [
        (_BUNDLED_HELPER_DIR / "export.js", cached_js),
        (_BUNDLED_HELPER_DIR / "package.json", cached_pkg),
        (_BUNDLED_HELPER_DIR / "package-lock.json", cached_lock),
    ]:
        if src.exists() and (not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime):
            shutil.copy2(src, dst)

    node_modules = _CACHE_DIR / "node_modules"
    if not node_modules.exists():
        _run_npm_install(_CACHE_DIR)

    return _CACHE_DIR


def _run_npm_install(target_dir: Path) -> None:
    """Run npm install in target_dir, streaming progress to stderr."""
    npm = shutil.which("npm")
    if not npm:
        raise RuntimeError(
            "npm is not in PATH. Install Node.js (which includes npm):\n"
            "  brew install node          # macOS\n"
            "  apt install nodejs npm     # Debian/Ubuntu\n"
            "  https://nodejs.org/en/download/"
        )

    print(
        f"  ● First-time setup: installing Node.js dependencies into {target_dir} …",
        file=sys.stderr,
    )
    result = subprocess.run(
        [npm, "install", "--prefer-offline"],
        cwd=str(target_dir),
        capture_output=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"npm install failed (exit {result.returncode}).\n"
            f"Try running manually: cd {target_dir} && npm install"
        )
    print("  ✓ Node.js dependencies installed.", file=sys.stderr)


def get_export_helper_script() -> str:
    """Return the absolute path to export.js, auto-installing deps if needed.

    Returns:
        Absolute path to export.js (with node_modules present alongside it).

    Raises:
        RuntimeError: If Node.js or npm is not installed, or install fails.
    """
    helper_dir = _ensure_node_modules()
    return str(helper_dir / "export.js")


def check_backend_available() -> dict:
    """Check whether the Node.js backend is available.

    Returns:
        Dict with 'available' (bool), 'node_path', 'helper_path', 'issues'.
    """
    issues = []
    node_path = None
    helper_path = None

    try:
        node_path = find_node()
    except RuntimeError as e:
        issues.append(str(e))

    if node_path:
        try:
            helper_path = get_export_helper_script()
        except RuntimeError as e:
            issues.append(str(e))

    return {
        "available": len(issues) == 0,
        "node_path": node_path,
        "helper_path": helper_path,
        "issues": issues,
    }
