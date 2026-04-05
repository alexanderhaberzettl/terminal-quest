# Terminal Quest: The Lost Server

A terminal-based educational game where you learn common shell commands by solving riddles and finding hidden files. You play a junior sysadmin who has discovered an ancient, forgotten server full of encrypted secrets left behind by a legendary hacker.

## Features

- **28 levels across 7 chapters** — from basic navigation to complex pipes
- **Real sandboxed filesystem** — use actual shell commands, not a simulation
- **Progressive hint system** — 3 hints per level, from vague nudges to direct answers
- **Save/load progress** between sessions
- **ANSI-colored narrative, riddles, and ASCII art**
- **Pure Python 3** — no external dependencies

## Quick Start

```bash
git clone https://github.com/alexanderhaberzettl/terminal-quest.git
cd terminal-quest
python3 main.py
```

## Commands You'll Learn

| Chapter | Theme | Commands |
|---------|-------|----------|
| 1 | First Steps | `pwd`, `ls`, `ls -a`, `cd`, `cd ..` |
| 2 | Creating & Destroying | `touch`, `mkdir`, `mkdir -p`, `rm`, `rm -r` |
| 3 | Reading & Writing | `cat`, `echo >`, `tail`, `echo >>` |
| 4 | Moving & Copying | `mv`, `cp`, wildcards (`*.log`) |
| 5 | Searching | `grep`, `grep -r`, `find`, `find -type -name` |
| 6 | Pipes & Power | `\|`, `wc`, `sort`, `uniq`, output redirection |
| 7 | Boss Level | Everything combined in a multi-step puzzle |

## Documentation

See [HOW_TO_PLAY.md](HOW_TO_PLAY.md) for a full guide including command-line options, in-game commands, and tips.

## Requirements

- Python 3.6+
- A Unix-like terminal (macOS, Linux, WSL)
- `bash` (used to execute commands in the sandbox)

## License

MIT
