import json
import os
import time


SAVE_FILE = os.path.expanduser("~/.terminal_quest_save.json")
HINT_PENALTY = 10


class ScoreTracker:
    def __init__(self):
        self.total_score = 0
        self.level_start_time = None
        self.levels_completed = 0
        self.last_completed_level = None

    def start_level(self):
        self.level_start_time = time.time()

    def complete_level(self, base_points, par_time, hints_used):
        """Calculate and add points for completing a level."""
        elapsed = time.time() - self.level_start_time if self.level_start_time else 0

        points = base_points
        bonus_text = None

        # Time bonus
        if elapsed < par_time:
            time_bonus = int(base_points * 0.5)
            points += time_bonus
            bonus_text = f"Speed bonus: +{time_bonus}"

        # Hint penalty
        penalty = hints_used * HINT_PENALTY
        points = max(0, points - penalty)

        self.total_score += points
        self.levels_completed += 1

        return points, bonus_text

    def save(self, last_level_id):
        """Save progress to disk."""
        self.last_completed_level = last_level_id
        data = {
            "total_score": self.total_score,
            "levels_completed": self.levels_completed,
            "last_completed_level": last_level_id,
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load(self):
        """Load progress from disk. Returns True if save exists."""
        if not os.path.isfile(SAVE_FILE):
            return False
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            self.total_score = data.get("total_score", 0)
            self.levels_completed = data.get("levels_completed", 0)
            self.last_completed_level = data.get("last_completed_level")
            return True
        except (json.JSONDecodeError, KeyError):
            return False

    @staticmethod
    def reset_save():
        """Delete the save file."""
        if os.path.isfile(SAVE_FILE):
            os.remove(SAVE_FILE)
