<p align="center">
  <h1 align="center">tokendiet</h1>
  <p align="center">
    <strong>Put your AI tokens on a diet. Save 60-90%.</strong>
  </p>
  <p align="center">
    <a href="https://github.com/spacenerd420/tokendiet"><img src="https://img.shields.io/github/stars/spacenerd420/tokendiet?style=social" alt="Stars"></a>
    <a href="https://github.com/spacenerd420/tokendiet/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
    <img src="https://img.shields.io/badge/python-3.7+-blue" alt="Python">
    <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
    <a href="https://github.com/spacenerd420/tokendiet/issues"><img src="https://img.shields.io/github/issues/spacenerd420/tokendiet" alt="Issues"></a>
  </p>
</p>

---

Interactive wizard + copy-paste prompt for reducing token consumption across **Claude Code**, **Cursor**, **Codex CLI**, **Gemini CLI**, and any LLM-powered dev tool.

> **Real-world impact:** 500K tokens/month &rarr; 50-200K/month with these techniques.

---

## Quick Start

### Option A: Run the wizard

```bash
git clone https://github.com/spacenerd420/tokendiet.git
cd tokendiet
python3 wizard.py
```

The wizard walks you through 6 phases with a clean, step-by-step UI. Already-installed tools are auto-detected and skipped.

| Phase | What | Savings |
|-------|------|---------|
| 1. Ignore files | Create `.claudeignore` / `.geminiignore` / `.codexignore` | 40-70% |
| 2. Settings | Tune `~/.claude/settings.json` per-setting | 60-80% |
| 3. Tools | Install RTK, Repomix, ccusage, etc. (auto-detects existing) | 60-90% |
| 4. CLAUDE.md | Flag oversized instruction files | up to 90% |
| 5. Best practices | Quick reference cheat sheet | -- |
| 6. Monitoring | Commands to track savings | -- |

### Option B: Just tell your AI

Paste this into any AI coding assistant (Claude Code, Cursor, Codex, Gemini, Copilot, Windsurf, etc.):

```
Read https://github.com/spacenerd420/tokendiet/blob/main/README.md and follow it to
optimize my token usage and reduce costs. Set up ignore files for whichever AI tool
I'm using, configure my settings for cost reduction, install the recommended CLI tools
(RTK, Repomix, ccusage), check if my project instruction files are too large, and show
me how to monitor my savings going forward.
```

### Option C: Full manual prompt

<details>
<summary>Click to expand -- paste into any LLM</summary>

```
I want to reduce my AI coding assistant's token consumption by 60-90%. Do the following:

1. CREATE IGNORE FILES
   Create ignore files in my project root (use whichever applies to my tools):
   - .claudeignore (for Claude Code)
   - .geminiignore (for Gemini CLI)
   - .codexignore (for Codex CLI)
   - .cursorignore (for Cursor)
   Exclude: node_modules, .venv, vendor, lock files, dist, build, __pycache__,
   images, videos, archives, logs, tmp files, .vscode, .idea, .env, .git, .cache dirs.

2. OPTIMIZE SETTINGS (Claude Code users)
   Update ~/.claude/settings.json (merge with existing, don't overwrite):
   - "model": "sonnet" (60% cheaper than Opus, handles 80% of tasks)
   - env.MAX_THINKING_TOKENS: "10000" (caps hidden reasoning tokens, default ~32K)
   - env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "50" (compact at 50%, default 95%)
   - env.CLAUDE_CODE_SUBAGENT_MODEL: "haiku" (cheaper model for file search/grep)

3. INSTALL TOOLS (check if already installed first)
   npm install -g @rtk-ai/rtk   # CLI output compression
   rtk init -g --claude-code     # (or --cursor, --codex, --gemini)
   npm install -g repomix        # repo compression
   npm install -g ccusage        # usage monitoring

4. CHECK MY INSTRUCTION FILES
   If my CLAUDE.md / .cursorrules / codex instructions are over 60 lines, suggest
   splitting into a main file (critical rules only, always loaded) plus separate
   on-demand files (architecture, patterns, style) loaded via @filename references.

5. MONITOR
   Show me how to run: rtk gain, rtk discover, npx ccusage@latest
```

</details>

---

## Settings Reference

| Setting | What | Recommended | Why |
|---------|------|-------------|-----|
| `model` | Default Claude model | `sonnet` | 60% cheaper than Opus for most tasks |
| `MAX_THINKING_TOKENS` | Hidden reasoning cap | `10000` | Default ~32K, billed at 5x input rate |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | When to compress context | `50` | Default 95% = context rarely compacts |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for background tasks | `haiku` | Search/grep don't need expensive models |

---

## Awesome Token Optimization Tools

A curated list of tools for reducing AI token consumption, monitoring costs, and optimizing context.

### Context Compression

| Tool | Description |
|------|-------------|
| [RTK](https://github.com/rtk-ai/rtk) | CLI proxy that compresses shell output by 60-90%. Hooks into Claude Code, Cursor, Codex, Gemini. |
| [Repomix](https://github.com/yamadashy/repomix) | Packs entire repos into one structured file via Tree-sitter AST. |
| [files-to-prompt](https://github.com/simonw/files-to-prompt) | Cherry-picks specific files into prompt-friendly format. |
| [Code2Prompt](https://github.com/mufeedvh/code2prompt) | Converts codebases into structured LLM prompts with token counting. |
| [Headroom](https://github.com/chopratejas/headroom) | Context optimization layer with 70-90% token savings on tool outputs. |
| [gptree](https://github.com/travisvn/gptree) | Combines project files into single text with directory tree structure. |
| [llmd](https://github.com/akatz-ai/llmd) | Converts git repos into LLM-friendly context markdown. |
| [ttok](https://github.com/simonw/ttok) | Count and truncate text based on tokens. |

### Usage Monitoring

| Tool | Description |
|------|-------------|
| [ccusage](https://github.com/ryoppippi/ccusage) | Analyzes Claude Code usage from local JSONL log files. |
| [Tokscale](https://github.com/junhoyeo/tokscale) | Tracks token usage across Claude Code, OpenCode, and other AI tools. |
| [toktrack](https://github.com/mag123c/toktrack) | Ultra-fast Rust-based token and cost tracker. |
| [Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | Real-time Claude Code usage monitor with predictions. |
| [Helicone](https://github.com/Helicone/helicone) | Open-source LLM observability platform for costs, latency, and quality. |
| [tokencost](https://github.com/AgentOps-AI/tokencost) | Token price estimates for 400+ LLMs. |

### Prompt Caching & Optimization

| Tool | Description |
|------|-------------|
| [GPTCache](https://github.com/zilliztech/GPTCache) | Semantic cache for LLM responses. Integrates with LangChain. |
| [LiteLLM](https://github.com/BerriAI/litellm) | Unified LLM proxy with caching, spend tracking, and 100+ provider support. |
| [Semantic Cache](https://github.com/upstash/semantic-cache) | Fuzzy key-value store based on semantic similarity for LLM caching. |

### Context Window Management

| Tool | Description |
|------|-------------|
| [Context Engine](https://github.com/Context-Engine-AI/Context-Engine) | MCP-based agentic context compression suite. |
| [llm-context](https://github.com/cyberchitta/llm-context.py) | Share code with LLMs via MCP with rule-based task customization. |
| [context-llemur](https://github.com/jerpint/context-llemur) | Persistent, version-controlled memory for LLM context via MCP. |

---

## Monitoring Cheat Sheet

```bash
rtk gain              # Token savings analytics
rtk discover          # Find missed optimizations
tokscale report       # Usage across tools
npx ccusage@latest    # Claude Code usage from logs
```

---

## Requirements

- Python 3.7+
- npm, pip, or Homebrew (for tool installs)

## Contributing

Found a tool that should be on the list? [Open an issue](https://github.com/spacenerd420/tokendiet/issues) or submit a PR.

## License

MIT
