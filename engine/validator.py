import os
import re


def check_goals(goals, sandbox_root, cwd, last_stdout=""):
    """Check all goals for a level. Returns (all_passed, results).

    Each result is a dict with 'type', 'passed', and 'description'.
    """
    results = []
    all_passed = True

    for goal in goals:
        goal_type = goal["type"]
        passed = False
        description = ""

        if goal_type == "file_exists":
            path = os.path.join(sandbox_root, goal["path"])
            passed = os.path.isfile(path)
            description = f"File exists: {goal['path']}"

        elif goal_type == "file_absent":
            path = os.path.join(sandbox_root, goal["path"])
            passed = not os.path.exists(path)
            description = f"File removed: {goal['path']}"

        elif goal_type == "file_contains":
            path = os.path.join(sandbox_root, goal["path"])
            target = goal["value"]
            if os.path.isfile(path):
                with open(path, "r") as f:
                    content = f.read()
                if goal.get("regex"):
                    passed = bool(re.search(target, content))
                else:
                    passed = target in content
            description = f"File contains expected content: {goal['path']}"

        elif goal_type == "file_moved":
            old_path = os.path.join(sandbox_root, goal["from"])
            new_path = os.path.join(sandbox_root, goal["to"])
            passed = not os.path.exists(old_path) and os.path.isfile(new_path)
            description = f"File moved from {goal['from']} to {goal['to']}"

        elif goal_type == "dir_exists":
            path = os.path.join(sandbox_root, goal["path"])
            passed = os.path.isdir(path)
            description = f"Directory exists: {goal['path']}"

        elif goal_type == "output_contains":
            target = goal["value"]
            if goal.get("regex"):
                passed = bool(re.search(target, last_stdout))
            else:
                passed = target in last_stdout
            description = f"Command output contains: {goal['value']}"

        elif goal_type == "file_count":
            path = os.path.join(sandbox_root, goal["path"])
            if os.path.isdir(path):
                count = len(os.listdir(path))
                passed = count == goal["count"]
            description = f"Directory {goal['path']} has {goal['count']} items"

        if not passed:
            all_passed = False

        results.append({
            "type": goal_type,
            "passed": passed,
            "description": description,
        })

    return all_passed, results
