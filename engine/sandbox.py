import os
import shutil
import tempfile
import uuid
import atexit
import signal


class Sandbox:
    def __init__(self):
        self.root = None
        self._registered_cleanup = False

    def create(self, level_definition):
        """Create a sandboxed filesystem from a level definition.

        Returns the sandbox root path.
        """
        self.teardown()

        sandbox_id = uuid.uuid4().hex[:8]
        self.root = os.path.join(tempfile.gettempdir(), f"terminal_quest_{sandbox_id}")
        os.makedirs(self.root, exist_ok=True)

        # Create directories
        for dir_path in level_definition.get("dirs", []):
            full_path = os.path.join(self.root, dir_path)
            os.makedirs(full_path, exist_ok=True)

        # Create files with content
        for file_path, content in level_definition.get("files", {}).items():
            full_path = os.path.join(self.root, file_path)
            parent = os.path.dirname(full_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)

        if not self._registered_cleanup:
            atexit.register(self.teardown)
            signal.signal(signal.SIGTERM, lambda s, f: self.teardown())
            self._registered_cleanup = True

        return self.root

    def teardown(self):
        """Remove the sandbox directory."""
        if self.root and os.path.exists(self.root):
            shutil.rmtree(self.root, ignore_errors=True)
            self.root = None

    def is_intact(self):
        """Check if the sandbox root still exists."""
        return self.root is not None and os.path.isdir(self.root)

    def rebuild(self, level_definition):
        """Rebuild the sandbox from scratch."""
        return self.create(level_definition)

    def get_filesystem_state(self, path=None):
        """Get a recursive snapshot of all files and directories."""
        root = path or self.root
        if not root or not os.path.exists(root):
            return {"exists": False}

        state = {"files": {}, "dirs": []}

        for dirpath, dirnames, filenames in os.walk(root):
            rel_dir = os.path.relpath(dirpath, root)
            if rel_dir != ".":
                state["dirs"].append(rel_dir)

            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root)
                try:
                    with open(full_path, "r") as f:
                        state["files"][rel_path] = f.read()
                except (UnicodeDecodeError, PermissionError):
                    state["files"][rel_path] = "<binary or unreadable>"

        return state

    def resolve_path(self, target, current_cwd):
        """Resolve a cd target path, ensuring it stays within the sandbox.

        Returns the new absolute path, or None if invalid/escaped.
        """
        if not target or target == "~":
            return self.root

        if target.startswith("~"):
            target = os.path.join(self.root, target[2:])

        if os.path.isabs(target):
            resolved = os.path.normpath(target)
        else:
            resolved = os.path.normpath(os.path.join(current_cwd, target))

        # Block escape from sandbox
        if not resolved.startswith(self.root):
            return None

        if os.path.isdir(resolved):
            return resolved

        return None

    def get_relative_path(self, absolute_path):
        """Get the path relative to sandbox root, prefixed with /."""
        if not self.root or not absolute_path:
            return "/"
        rel = os.path.relpath(absolute_path, self.root)
        if rel == ".":
            return "/"
        return "/" + rel
