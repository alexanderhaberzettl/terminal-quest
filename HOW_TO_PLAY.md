# Terminal Quest: The Lost Server

A terminal-based game where you learn common shell commands by solving riddles and finding hidden files.

## Getting Started

Make sure you have Python 3 installed, then run:

```bash
python3 main.py
```

No external dependencies required — the game uses only the Python standard library.

## Command Line Options

| Command | Description |
|---------|-------------|
| `python3 main.py` | Start the game (resumes from last save if available) |
| `python3 main.py --reset` | Delete saved progress and start fresh |
| `python3 main.py --level 3-1` | Jump directly to a specific level |

## In-Game Commands

While playing, you can use these special commands alongside regular terminal commands:

| Command | Description |
|---------|-------------|
| `hint` | Get a hint for the current level (costs points) |
| `goal` | Re-display the current riddle |
| `check` | Check your progress on the current level's goals |
| `score` | Show your current score and levels completed |
| `skip` | Skip the current level |
| `help` | Show available game commands |
| `quit` | Save progress and exit |

## How It Works

- Each level creates a **sandboxed directory** with files and folders for you to explore.
- You solve puzzles using **real terminal commands** (`ls`, `cd`, `cat`, `grep`, etc.).
- The game checks whether you've achieved the level's goals after each command.
- You earn points for completing levels, with bonuses for speed and penalties for using hints.
- Progress is saved automatically to `~/.terminal_quest_save.json`.

## Chapters

1. **First Steps** — `pwd`, `ls`, `ls -a`, `cd`, `cd ..`
2. **Creating & Destroying** — `touch`, `mkdir`, `mkdir -p`, `rm`, `rm -r`
3. **Reading & Writing** — `cat`, `echo >`, `tail`, `echo >>`
4. **Moving & Copying** — `mv`, `cp`, wildcards (`*.log`)
5. **Searching** — `grep`, `grep -r`, `find`, `find -type -name`
6. **Pipes & Power** — `|`, `wc`, `sort`, `uniq`, output redirection
7. **The Final Challenge** — A boss level combining everything

## Tips

- Hidden files start with a dot (`.`) — use `ls -a` to see them.
- Use `hint` if you're stuck — hints go from vague to specific.
- The game uses `bash` to run your commands, even if your default shell is different.
- If you accidentally destroy the sandbox (`rm -rf *`), the game will rebuild it for you.
- You can always type `goal` to re-read the current riddle.
