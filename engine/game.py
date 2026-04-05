import os
import subprocess
import shlex

from engine import renderer
from engine.sandbox import Sandbox
from engine.validator import check_goals
from engine.hint_system import HintSystem
from engine.score import ScoreTracker
from engine.level_loader import get_chapter_title


class Game:
    def __init__(self, levels):
        self.levels = levels
        self.sandbox = Sandbox()
        self.score = ScoreTracker()
        self.current_cwd = None
        self.current_level_index = 0
        self.hint_system = None
        self.last_stdout = ""
        self.running = True

    def run(self, resume=False):
        """Main game loop."""
        renderer.print_title()

        if resume and self.score.load():
            # Find the level after the last completed one
            found = False
            for i, level in enumerate(self.levels):
                if level.id == self.score.last_completed_level:
                    self.current_level_index = i + 1
                    found = True
                    break
            if found and self.current_level_index < len(self.levels):
                renderer.info(
                    f"\n  Resuming from level {self.levels[self.current_level_index].id} "
                    f"(Score: {self.score.total_score})\n"
                )
            elif found:
                renderer.success("\n  You've already completed all levels!")
                renderer.print_game_over(
                    self.score.total_score,
                    self.score.levels_completed,
                    len(self.levels),
                )
                return
            else:
                self.current_level_index = 0
        else:
            input(
                renderer.colorize(
                    "\n  Press ENTER to begin your quest...\n", renderer.Color.DIM
                )
            )

        last_chapter = None

        while self.running and self.current_level_index < len(self.levels):
            level = self.levels[self.current_level_index]

            # Show chapter intro on chapter change
            if level.chapter != last_chapter:
                renderer.print_chapter_intro(
                    level.chapter, get_chapter_title(level.chapter)
                )
                last_chapter = level.chapter

            self._play_level(level)

            if not self.running:
                break

            self.current_level_index += 1

        if self.running:
            renderer.print_game_over(
                self.score.total_score,
                self.score.levels_completed,
                len(self.levels),
            )

        self.sandbox.teardown()

    def _play_level(self, level):
        """Play a single level."""
        # Set up sandbox
        self.sandbox.create(level.sandbox)
        self.current_cwd = self.sandbox.root
        self.hint_system = HintSystem(level.hints)
        self.last_stdout = ""
        self.score.start_level()

        # Show level intro
        renderer.print_level_intro(
            level.id, level.title, level.narrative, level.riddle
        )
        renderer.print_score_bar(
            level.id,
            self.score.total_score,
            self.hint_system.get_hints_used(),
            self.hint_system.get_total_hints(),
        )
        renderer.dim(
            "  Type 'help' for commands, 'hint' for a hint, 'goal' to see the riddle again\n"
        )

        while self.running:
            # Check sandbox integrity
            if not self.sandbox.is_intact():
                renderer.error(
                    "\n  You have destroyed the ancient server! Rebuilding from backup...\n"
                )
                self.sandbox.rebuild(level.sandbox)
                self.current_cwd = self.sandbox.root
                continue

            # Get input
            rel_path = self.sandbox.get_relative_path(self.current_cwd)
            try:
                cmd = input(renderer.prompt_string(rel_path))
            except (EOFError, KeyboardInterrupt):
                print()
                self.running = False
                return

            cmd = cmd.strip()
            if not cmd:
                continue

            # Handle meta-commands
            if self._handle_meta_command(cmd, level):
                continue

            # Handle cd specially
            if cmd == "cd" or cmd.startswith("cd "):
                self._handle_cd(cmd)
                continue

            # Execute command in sandbox
            self._execute_command(cmd)

            # Check goals after each command
            all_passed, results = check_goals(
                level.goals, self.sandbox.root, self.current_cwd, self.last_stdout
            )

            if all_passed:
                points, bonus_text = self.score.complete_level(
                    level.points,
                    level.par_time_seconds,
                    self.hint_system.get_hints_used(),
                )
                renderer.print_completion(level.title, points, bonus_text)
                self.score.save(level.id)

                if self.current_level_index < len(self.levels) - 1:
                    try:
                        input(
                            renderer.colorize(
                                "  Press ENTER to continue...\n", renderer.Color.DIM
                            )
                        )
                    except (EOFError, KeyboardInterrupt):
                        self.running = False
                return

    def _handle_meta_command(self, cmd, level):
        """Handle game meta-commands. Returns True if handled."""
        lower = cmd.lower()

        if lower == "hint":
            hint = self.hint_system.get_next_hint()
            if hint:
                renderer.hint_text(f"\n  Hint: {hint}\n")
            else:
                renderer.dim("  No more hints available for this level.\n")
            return True

        elif lower in ("goal", "objective", "riddle"):
            print()
            renderer.riddle(f"  {level.riddle}")
            print()
            return True

        elif lower == "score":
            print()
            renderer.info(f"  Total score: {self.score.total_score}")
            renderer.info(f"  Levels completed: {self.score.levels_completed}")
            print()
            return True

        elif lower == "skip":
            renderer.dim(f"  Skipping level {level.id}...")
            return False  # Let the game loop advance

        elif lower in ("quit", "exit"):
            renderer.dim("  Farewell, adventurer. Your progress has been saved.\n")
            self.running = False
            return True

        elif lower == "help":
            self._print_help()
            return True

        elif lower == "check":
            all_passed, results = check_goals(
                level.goals, self.sandbox.root, self.current_cwd, self.last_stdout
            )
            print()
            for r in results:
                if r["passed"]:
                    renderer.success(f"  ✓ {r['description']}")
                else:
                    renderer.error(f"  ✗ {r['description']}")
            print()
            if all_passed:
                points, bonus_text = self.score.complete_level(
                    level.points,
                    level.par_time_seconds,
                    self.hint_system.get_hints_used(),
                )
                renderer.print_completion(level.title, points, bonus_text)
                self.score.save(level.id)
            return not all_passed  # If passed, return False to exit level loop

        return False

    def _handle_cd(self, cmd):
        """Handle cd command by updating tracked cwd."""
        parts = cmd.split(maxsplit=1)
        target = parts[1] if len(parts) > 1 else None

        new_path = self.sandbox.resolve_path(target, self.current_cwd)
        if new_path is None:
            if target and not os.path.isdir(
                os.path.normpath(os.path.join(self.current_cwd, target))
            ):
                renderer.error(f"  bash: cd: {target}: No such file or directory")
            else:
                renderer.error(
                    "  An invisible barrier blocks your path... "
                    "You cannot leave the server."
                )
        else:
            self.current_cwd = new_path

    def _execute_command(self, cmd):
        """Execute a shell command in the sandbox."""
        env = os.environ.copy()
        env["HOME"] = self.sandbox.root
        # Prevent the command from escaping via HOME
        env["OLDPWD"] = self.current_cwd

        try:
            result = subprocess.run(
                ["bash", "-c", cmd],
                cwd=self.current_cwd,
                capture_output=True,
                text=True,
                timeout=10,
                env=env,
            )
            self.last_stdout = result.stdout
            if result.stdout:
                print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
            if result.stderr:
                print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")
        except subprocess.TimeoutExpired:
            renderer.error("  Command timed out (10s limit).")
            self.last_stdout = ""
        except Exception as e:
            renderer.error(f"  Error: {e}")
            self.last_stdout = ""

    def _print_help(self):
        """Print help for meta-commands."""
        print()
        renderer.box(
            "Game Commands:\n"
            "  hint      - Get a hint (costs points)\n"
            "  goal      - Show the current riddle again\n"
            "  check     - Check your progress on goals\n"
            "  score     - Show your current score\n"
            "  skip      - Skip this level\n"
            "  help      - Show this help\n"
            "  quit      - Save and exit\n"
            "\n"
            "Use real terminal commands to solve puzzles!\n"
            "  ls, cd, cat, touch, mkdir, rm, grep, find, ...",
            renderer.Color.BLUE,
        )
        print()
