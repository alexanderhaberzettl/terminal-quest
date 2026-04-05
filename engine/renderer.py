import os
import shutil


# ANSI color codes
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def get_terminal_width():
    return shutil.get_terminal_size((80, 24)).columns


def colorize(text, color):
    return f"{color}{text}{Color.RESET}"


def bold(text):
    return colorize(text, Color.BOLD)


def narrative(text):
    """Print story/narrative text in green."""
    print(colorize(text, Color.GREEN))


def riddle(text):
    """Print riddle text in yellow italic."""
    print(colorize(text, Color.YELLOW + Color.ITALIC))


def hint_text(text):
    """Print hint text in cyan."""
    print(colorize(text, Color.CYAN))


def error(text):
    """Print error text in red."""
    print(colorize(text, Color.RED))


def success(text):
    """Print success text in bold green."""
    print(colorize(text, Color.BOLD + Color.GREEN))


def info(text):
    """Print info text in blue."""
    print(colorize(text, Color.BLUE))


def dim(text):
    """Print dimmed text."""
    print(colorize(text, Color.DIM))


def box(text, color=Color.CYAN):
    """Draw a box around text."""
    width = get_terminal_width() - 2
    lines = text.split("\n")
    max_len = min(max(len(line) for line in lines), width - 4)

    top = f"╔{'═' * (max_len + 2)}╗"
    bottom = f"╚{'═' * (max_len + 2)}╝"

    print(colorize(top, color))
    for line in lines:
        padded = line.ljust(max_len)
        print(colorize(f"║ {padded} ║", color))
    print(colorize(bottom, color))


def header(text):
    """Print a centered header."""
    width = get_terminal_width()
    padded = f" {text} "
    centered = padded.center(width, "━")
    print(colorize(centered, Color.BOLD + Color.MAGENTA))


def separator():
    """Print a horizontal separator."""
    width = get_terminal_width()
    print(colorize("─" * width, Color.DIM))


def clear_screen():
    """Clear the terminal screen."""
    os.system("clear" if os.name != "nt" else "cls")


def print_title():
    """Print the game title screen."""
    clear_screen()
    title = r"""
  ╔════════════════════════════════════════════════════════╗
  ║                                                        ║
  ║   _____ _____ ____  __  __ ___ _   _    _    _         ║
  ║  |_   _| ____|  _ \|  \/  |_ _| \ | |  / \  | |       ║
  ║    | | |  _| | |_) | |\/| || ||  \| | / _ \ | |       ║
  ║    | | | |___|  _ <| |  | || || |\  |/ ___ \| |___    ║
  ║    |_| |_____|_| \_\_|  |_|___|_| \_/_/   \_\_____|   ║
  ║                                                        ║
  ║              ___  _   _ _____ ____ _____               ║
  ║             / _ \| | | | ____/ ___|_   _|              ║
  ║            | | | | | | |  _| \___ \ | |                ║
  ║            | |_| | |_| | |___ ___) || |                ║
  ║             \__\_\\___/|_____|____/ |_|                ║
  ║                                                        ║
  ║            ~ The Lost Server ~                         ║
  ║                                                        ║
  ╚════════════════════════════════════════════════════════╝
"""
    print(colorize(title, Color.CYAN + Color.BOLD))
    narrative(
        "  You are a junior sysadmin who has discovered an ancient,\n"
        "  forgotten server in the basement of your company.\n"
        "  The server contains encrypted secrets left behind by\n"
        "  a legendary hacker. Use your terminal skills to uncover them.\n"
    )


def print_chapter_intro(chapter_num, chapter_title):
    """Print chapter transition screen."""
    separator()
    print()
    header(f"CHAPTER {chapter_num}")
    print()
    box(chapter_title, Color.MAGENTA)
    print()
    separator()


def print_level_intro(level_id, title, narrative_text, riddle_text):
    """Print level introduction."""
    print()
    header(f"Level {level_id}: {title}")
    print()
    narrative(narrative_text)
    print()
    box(riddle_text, Color.YELLOW)
    print()


def print_score_bar(level_id, score, hints_used, hints_total):
    """Print a compact status bar."""
    hints_remaining = hints_total - hints_used
    bar = (
        f"{colorize('Level:', Color.DIM)} {colorize(level_id, Color.WHITE + Color.BOLD)}  "
        f"{colorize('Score:', Color.DIM)} {colorize(str(score), Color.YELLOW + Color.BOLD)}  "
        f"{colorize('Hints:', Color.DIM)} {colorize(str(hints_remaining), Color.CYAN + Color.BOLD)}/{hints_total}"
    )
    print(bar)
    separator()


def print_completion(level_title, points_earned, bonus_text=None):
    """Print level completion message."""
    print()
    success("  ✓ LEVEL COMPLETE!")
    print()
    box(f"  {level_title}\n  Points earned: {points_earned}" +
        (f"\n  {bonus_text}" if bonus_text else ""), Color.GREEN)
    print()


def print_game_over(total_score, levels_completed, total_levels):
    """Print game completion screen."""
    clear_screen()
    print()
    header("CONGRATULATIONS!")
    print()
    box(
        f"You have conquered The Lost Server!\n\n"
        f"  Levels completed: {levels_completed}/{total_levels}\n"
        f"  Final score: {total_score}\n\n"
        f"  The legendary hacker's secrets are yours.\n"
        f"  You are now a Terminal Master.",
        Color.YELLOW
    )
    print()


def prompt_string(rel_path):
    """Generate the game prompt string."""
    return f"{colorize('[Terminal Quest]', Color.MAGENTA)} {colorize('~' + rel_path, Color.BLUE + Color.BOLD)} $ "
