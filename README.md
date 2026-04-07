# tokendiet

Put your AI tokens on a diet. Save 60-90% across Claude Code, Cursor, Codex CLI, and Gemini CLI.

## Quick Start

```bash
python3 optimizer.py
```

The wizard walks you through 6 phases:
1. **Ignore files** -- create `.claudeignore` / `.geminiignore` / `.codexignore` (40-70% savings)
2. **Claude Code settings** -- tune `~/.claude/settings.json` per-setting (60-80% savings)
3. **Install tools** -- RTK, Repomix, Tokscale, ccusage, files-to-prompt
4. **CLAUDE.md check** -- flag oversized instruction files
5. **Best practices** -- quick reference table
6. **Monitoring** -- commands to track your savings

Each phase clears the screen and shows a progress log of completed steps.

## What It Installs

| Tool | What It Does | Savings |
|------|-------------|---------|
| [RTK](https://github.com/rtk-ai/rtk) | Compresses CLI output (git, npm, ls...) before AI sees it | 60-90% |
| [Repomix](https://github.com/yamadashy/repomix) | Packs your codebase into one AI-friendly file | ~70% |
| [Tokscale](https://www.npmjs.com/package/tokscale) | Tracks token usage across tools | monitor |
| [ccusage](https://www.npmjs.com/package/ccusage) | Shows Claude Code token usage from logs | monitor |
| [files-to-prompt](https://github.com/simonw/files-to-prompt) | Cherry-picks files into prompt-friendly format | 50-70% |

All installs are opt-in (y/n for each tool). npm permission issues are handled with sudo fallback.

## Copy-Paste Prompt

Don't want to run the script? Paste this into Claude Code, Cursor, Codex, or any LLM to optimize manually:

```
I want to reduce my AI token consumption by 60-90%. Help me do the following:

1. CREATE IGNORE FILES
   Create a .claudeignore (or .geminiignore / .codexignore) in my project root that excludes:
   node_modules, .venv, vendor, lock files, dist, build, __pycache__, images, videos,
   archives, logs, tmp files, .vscode, .idea, .env, .git, .cache directories.

2. OPTIMIZE CLAUDE CODE SETTINGS
   Update ~/.claude/settings.json with these values (merge, don't overwrite):
   - "model": "sonnet" (60% cheaper than Opus, handles 80% of tasks)
   - env.MAX_THINKING_TOKENS: "10000" (caps hidden reasoning, default is ~32K)
   - env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "50" (compact context at 50%, default is 95%)
   - env.CLAUDE_CODE_SUBAGENT_MODEL: "haiku" (cheaper model for file search/grep tasks)

3. INSTALL TOOLS
   - npm install -g @rtk-ai/rtk && rtk init -g --claude-code
   - npm install -g repomix
   - npm install -g tokscale
   - npm install -g ccusage

4. CHECK MY CLAUDE.md
   If my CLAUDE.md is over 60 lines, suggest splitting it into:
   - CLAUDE.md (critical rules only, always loaded)
   - ARCHITECTURE.md, PATTERNS.md, STYLE.md (loaded on-demand with @filename)

5. SHOW ME HOW TO MONITOR
   After setup, I should run: rtk gain, rtk discover, tokscale report, npx ccusage@latest
```

## Requirements

- Python 3.7+
- npm, pip, or Homebrew (for tool installs)

## Settings Reference

| Setting | What | Recommended | Why |
|---------|------|-------------|-----|
| `model` | Default Claude model | `sonnet` | 60% cheaper than Opus for most tasks |
| `MAX_THINKING_TOKENS` | Hidden reasoning cap | `10000` | Default ~32K, billed at 5x input rate |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | When to compress context | `50` | Default 95% means context rarely compacts |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for background tasks | `haiku` | Search/grep don't need expensive models |

## Monitoring

```bash
rtk gain              # Token savings analytics
rtk discover          # Find missed optimizations
tokscale report       # Usage across tools
npx ccusage@latest    # Claude Code usage from logs
```

## License

MIT
