"""Stateful session management for Excalidraw CLI.

Maintains the currently open project, undo/redo stack, and operation history.
State is persisted to a JSON session file so it survives across CLI invocations.
"""

import copy
import json
import os
import time


SESSION_FILE = os.path.expanduser("~/.excalidraw-agent-cli/session.json")
MAX_HISTORY = 50


class Session:
    """Stateful session holding current project and undo/redo stack."""

    def __init__(self):
        self.project: dict | None = None
        self.project_path: str | None = None
        self.modified: bool = False
        self._undo_stack: list[dict] = []   # snapshots
        self._redo_stack: list[dict] = []
        self._history: list[dict] = []       # operation log

    # ── Project lifecycle ─────────────────────────────────────────────

    def set_project(self, project: dict, path: str | None = None):
        """Set the active project (clears undo/redo)."""
        self.project = project
        self.project_path = path
        self.modified = False
        self._undo_stack.clear()
        self._redo_stack.clear()

    def mark_modified(self):
        """Mark project as having unsaved changes."""
        self.modified = True

    # ── Undo/redo ─────────────────────────────────────────────────────

    def checkpoint(self, operation_name: str):
        """Save a snapshot of current project state before a mutation.

        Call this BEFORE modifying the project.

        Args:
            operation_name: Human-readable name of the operation.
        """
        if self.project is None:
            return

        snapshot = {
            "operation": operation_name,
            "timestamp": time.time(),
            "state": copy.deepcopy(self.project),
        }
        self._undo_stack.append(snapshot)
        self._redo_stack.clear()  # Clear redo on new operation

        # Log to history
        self._history.append({
            "operation": operation_name,
            "timestamp": time.time(),
        })

        # Trim undo stack
        if len(self._undo_stack) > MAX_HISTORY:
            self._undo_stack.pop(0)

    def undo(self) -> str | None:
        """Undo the last operation.

        Returns:
            Name of undone operation, or None if nothing to undo.
        """
        if not self._undo_stack:
            return None

        snapshot = self._undo_stack.pop()

        # Save current state to redo stack
        self._redo_stack.append({
            "operation": snapshot["operation"],
            "timestamp": time.time(),
            "state": copy.deepcopy(self.project),
        })

        self.project = snapshot["state"]
        self.modified = True
        return snapshot["operation"]

    def redo(self) -> str | None:
        """Redo the last undone operation.

        Returns:
            Name of redone operation, or None if nothing to redo.
        """
        if not self._redo_stack:
            return None

        snapshot = self._redo_stack.pop()
        self._undo_stack.append({
            "operation": snapshot["operation"],
            "timestamp": time.time(),
            "state": copy.deepcopy(self.project),
        })

        self.project = snapshot["state"]
        self.modified = True
        return snapshot["operation"]

    def get_history(self, limit: int = 20) -> list[dict]:
        """Get recent operation history.

        Args:
            limit: Maximum number of entries to return.

        Returns:
            List of operation dicts with 'operation' and 'timestamp'.
        """
        return list(reversed(self._history[-limit:]))

    # ── Persistence ───────────────────────────────────────────────────

    def get_status(self) -> dict:
        """Get current session status summary."""
        return {
            "project_path": self.project_path,
            "project_name": (
                self.project.get("_meta", {}).get("name", "Untitled")
                if self.project else None
            ),
            "modified": self.modified,
            "element_count": (
                len([e for e in self.project.get("elements", [])
                     if not e.get("isDeleted")])
                if self.project else 0
            ),
            "can_undo": len(self._undo_stack) > 0,
            "can_redo": len(self._redo_stack) > 0,
            "undo_count": len(self._undo_stack),
            "redo_count": len(self._redo_stack),
        }

    def save_to_disk(self, session_file: str = SESSION_FILE):
        """Persist session metadata (not project content) to disk.

        Args:
            session_file: Path to save session JSON.
        """
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        data = {
            "project_path": self.project_path,
            "modified": self.modified,
            "history": self._history[-MAX_HISTORY:],
            "saved_at": time.time(),
        }
        with open(session_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_disk(self, session_file: str = SESSION_FILE) -> bool:
        """Restore session metadata from disk.

        Args:
            session_file: Path to session JSON.

        Returns:
            True if session was restored, False if no session file found.
        """
        if not os.path.exists(session_file):
            return False

        with open(session_file) as f:
            data = json.load(f)

        self.project_path = data.get("project_path")
        self._history = data.get("history", [])
        return True


# ── Module-level singleton ────────────────────────────────────────────

_session = Session()


def get_session() -> Session:
    """Get the global session singleton."""
    return _session
