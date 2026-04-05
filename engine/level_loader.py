import json
import os


class Level:
    def __init__(self, data):
        self.id = data["id"]
        self.chapter = data["chapter"]
        self.title = data["title"]
        self.narrative = data["narrative"]
        self.riddle = data["riddle"]
        self.commands_taught = data.get("commands_taught", [])
        self.sandbox = data["sandbox"]
        self.goals = data["goals"]
        self.hints = data.get("hints", [])
        self.points = data.get("points", 10)
        self.par_time_seconds = data.get("par_time_seconds", 120)


def load_levels(levels_dir):
    """Load all levels from JSON files in the levels directory.

    Returns a list of Level objects sorted by id.
    """
    levels = []

    for filename in sorted(os.listdir(levels_dir)):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(levels_dir, filename)
        with open(filepath, "r") as f:
            data = json.load(f)

        for level_data in data.get("levels", []):
            levels.append(Level(level_data))

    levels.sort(key=lambda l: (l.chapter, l.id))
    return levels


def get_chapter_title(chapter_num):
    """Return the chapter title for a given chapter number."""
    titles = {
        1: "First Steps — Learning to See",
        2: "Creating & Destroying — Shaping the World",
        3: "Reading & Writing — The Power of Words",
        4: "Moving & Copying — Rearranging Reality",
        5: "Searching — Finding the Unfindable",
        6: "Pipes & Power — Chaining Commands",
        7: "The Final Challenge — The Master's Test",
    }
    return titles.get(chapter_num, f"Chapter {chapter_num}")
