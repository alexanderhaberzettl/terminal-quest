#!/usr/bin/env python3
"""Terminal Quest: The Lost Server - Learn terminal commands through puzzles."""

import argparse
import os
import sys

from engine.game import Game
from engine.level_loader import load_levels
from engine.score import ScoreTracker


def main():
    parser = argparse.ArgumentParser(
        description="Terminal Quest: The Lost Server - Learn terminal commands by solving puzzles"
    )
    parser.add_argument(
        "--reset", action="store_true", help="Reset saved progress and start fresh"
    )
    parser.add_argument(
        "--level", type=str, help="Start from a specific level (e.g., '2-1')"
    )
    args = parser.parse_args()

    if args.reset:
        ScoreTracker.reset_save()
        print("Progress reset. Starting fresh!")

    # Load levels
    levels_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levels")
    levels = load_levels(levels_dir)

    if not levels:
        print("Error: No levels found. Check the 'levels/' directory.")
        sys.exit(1)

    game = Game(levels)

    # Handle --level flag
    if args.level:
        for i, level in enumerate(levels):
            if level.id == args.level:
                game.current_level_index = i
                break
        else:
            print(f"Error: Level '{args.level}' not found.")
            print("Available levels:", ", ".join(l.id for l in levels))
            sys.exit(1)
        game.run(resume=False)
    else:
        # Check for saved progress
        score = ScoreTracker()
        has_save = score.load()
        game.run(resume=has_save)


if __name__ == "__main__":
    main()
