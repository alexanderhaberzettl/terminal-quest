class HintSystem:
    def __init__(self, hints):
        self.hints = hints
        self.hints_used = 0

    def has_hints(self):
        return self.hints_used < len(self.hints)

    def get_next_hint(self):
        """Return the next hint, or None if all used."""
        if not self.has_hints():
            return None
        hint = self.hints[self.hints_used]
        self.hints_used += 1
        return hint

    def get_hints_used(self):
        return self.hints_used

    def get_total_hints(self):
        return len(self.hints)

    def reset(self):
        self.hints_used = 0
