#!/usr/bin/env python3
"""
tokendiet - AI Token Optimization Wizard
"""

import os
import subprocess
import sys
import json
import shutil
import platform
import argparse
from pathlib import Path


# ─────────────────────────────────────────────────────────────
# Visual Engine
# ─────────────────────────────────────────────────────────────

class Colors:
    def __init__(self):
        self.enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
        self._width = shutil.get_terminal_size((80, 24)).columns

    def _c(self, code, text):
        return f"\033[{code}m{text}\033[0m" if self.enabled else text

    @property
    def width(self):
        return min(self._width, 72)

    def bold(self, t):    return self._c("1", t)
    def dim(self, t):     return self._c("2", t)
    def red(self, t):     return self._c("91", t)
    def green(self, t):   return self._c("92", t)
    def yellow(self, t):  return self._c("93", t)
    def blue(self, t):    return self._c("94", t)
    def cyan(self, t):    return self._c("96", t)
    def white(self, t):   return self._c("97", t)

    def gradient(self, text):
        if not self.enabled:
            return text
        codes = [
            "38;5;201", "38;5;200", "38;5;199", "38;5;198",
            "38;5;163", "38;5;128", "38;5;93",  "38;5;63",
            "38;5;33",  "38;5;39",  "38;5;45",  "38;5;51",
            "38;5;50",  "38;5;49",  "38;5;48",  "38;5;47",
        ]
        result = []
        for i, line in enumerate(text.split("\n")):
            result.append(f"\033[{codes[min(i, len(codes)-1)]}m{line}\033[0m")
        return "\n".join(result)


C = Colors()

BANNER = r"""
  _        _                  _ _      _
 | |_ ___ | | _____ _ __   __| (_) ___| |_
 | __/ _ \| |/ / _ \ '_ \ / _` | |/ _ \ __|
 | || (_) |   <  __/ | | | (_| | |  __/ |_
  \__\___/|_|\_\___|_| |_|\__,_|_|\___|\__|
"""

PHASE_NAMES = {
    1: "Ignore Files",
    2: "Claude Code Settings",
    3: "Install Tools",
    4: "CLAUDE.md Check",
    5: "Best Practices",
    6: "Monitoring",
}


# ─────────────────────────────────────────────────────────────
# State: tracks completed phases for the progress log
# ─────────────────────────────────────────────────────────────

completed_phases = []  # list of (phase_num, title)


def redraw(current_phase=None):
    """Clear screen, print logo, print completed phase log, print current header."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")

    # Always show logo
    print(C.gradient(BANNER))
    print(C.dim("  Put your tokens on a diet. Save 60-90%."))
    print()

    # Show completed phases
    for num, title in completed_phases:
        print(f"  {C.green('+')} Phase {num}: {title}")

    # Show current phase header
    if current_phase:
        title = PHASE_NAMES.get(current_phase, "")
        if completed_phases:
            print()
        print(f"  {C.bold(C.cyan(f'Phase {current_phase}/6: {title}'))}")
        print(f"  {'─' * C.width}\n")


def finish_phase(num):
    """Mark a phase as done."""
    completed_phases.append((num, PHASE_NAMES[num]))


def ok(text):    print(f"  {C.green('+')} {text}")
def info(text):  print(f"  {C.blue('*')} {text}")
def warn(text):  print(f"  {C.yellow('!')} {text}")
def err(text):   print(f"  {C.red('x')} {text}")


def ask(prompt, default="n"):
    suffix = "(Y/n)" if default == "y" else "(y/N)"
    try:
        r = input(f"  {C.cyan('?')} {prompt} {C.dim(suffix)}: ").strip().lower()
    except EOFError:
        return default == "y"
    if not r:
        return default == "y"
    return r.startswith("y")


def pick(prompt, options, allow_all=False):
    """Returns list of selected indices."""
    for i, opt in enumerate(options, 1):
        print(f"    {C.cyan(str(i))}. {opt}")
    if allow_all:
        print(f"    {C.cyan('a')}. All")
    try:
        raw = input(f"\n  {C.cyan('?')} {prompt}: ").strip().lower()
    except EOFError:
        return []
    if allow_all and raw in ("a", "all"):
        return list(range(len(options)))
    try:
        return [int(x.strip()) - 1 for x in raw.split(",")
                if 0 <= int(x.strip()) - 1 < len(options)]
    except (ValueError, IndexError):
        return []


# ─────────────────────────────────────────────────────────────
# System Detection
# ─────────────────────────────────────────────────────────────

class System:
    def __init__(self):
        self.home = Path.home()
        self.platform = platform.system()
        self._npm = self._pip = self._brew = None

    @property
    def has_npm(self):
        if self._npm is None: self._npm = self._exists("npm")
        return self._npm

    @property
    def has_pip(self):
        if self._pip is None: self._pip = self._exists("pip3") or self._exists("pip")
        return self._pip

    @property
    def pip_cmd(self):
        return "pip3" if self._exists("pip3") else "pip"

    @property
    def has_brew(self):
        if self._brew is None: self._brew = self.platform == "Darwin" and self._exists("brew")
        return self._brew

    @property
    def is_root(self):
        return hasattr(os, "geteuid") and os.geteuid() == 0

    @property
    def is_windows(self):
        return self.platform == "Windows"

    def _exists(self, cmd):
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def npm_writable(self):
        try:
            prefix = subprocess.run(
                ["npm", "config", "get", "prefix"],
                capture_output=True, text=True, check=True
            ).stdout.strip()
            return os.access(prefix, os.W_OK)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def run(self, cmd):
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


SYS = System()


# ─────────────────────────────────────────────────────────────
# Install helpers
# ─────────────────────────────────────────────────────────────

def npm_install(name, pkg):
    cmd = ["npm", "install", "-g", pkg]
    if SYS.run(cmd):
        ok(f"Installed {name}")
        return True
    if not SYS.is_windows and not SYS.is_root:
        if ask("Permission denied. Retry with sudo?"):
            if SYS.run(["sudo"] + cmd):
                ok(f"Installed {name}")
                return True
    info(f"You can still use: npx {pkg}")
    return False


def pip_install(name, pkg):
    if SYS.run([SYS.pip_cmd, "install", "--user", pkg]):
        ok(f"Installed {name}")
        return True
    err(f"Failed to install {name}")
    return False


def brew_install(name, tap):
    if SYS.run(["brew", "install", tap]):
        ok(f"Installed {name}")
        return True
    err(f"Failed to install {name}")
    return False


# ─────────────────────────────────────────────────────────────
# Phase 1: Ignore Files
# ─────────────────────────────────────────────────────────────

IGNORE_CATEGORIES = [
    ("Dependencies",  "node_modules, .venv, vendor, lock files -- large, auto-generated",
     ["node_modules/", ".venv/", "venv/", "env/", "vendor/", "go.sum",
      "Cargo.lock", "*.lock", "pnpm-lock.yaml", "yarn.lock", "package-lock.json"]),
    ("Build output",  "dist, build, __pycache__ -- compiled artifacts, not source",
     ["dist/", "build/", "out/", ".next/", ".nuxt/", ".vercel/",
      "__pycache__/", "*.pyc", "*.pyo", "*.egg-info/", ".pytest_cache/",
      ".mypy_cache/", "target/", ".gradle/", "*.class"]),
    ("Media/binary",  "images, video, archives -- AI can't read these",
     ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.webp", "*.ico",
      "*.mp4", "*.mov", "*.avi", "*.wav", "*.mp3",
      "*.zip", "*.tar", "*.gz", "*.rar", "*.7z"]),
    ("Logs & temp",   "*.log, *.tmp, coverage/ -- ephemeral, changes every run",
     ["*.log", "*.tmp", "*.temp", "tmp/", "logs/", "coverage/", ".DS_Store", "Thumbs.db"]),
    ("IDE config",    ".vscode, .idea -- editor-specific, not code",
     [".vscode/", ".idea/", "*.swp", "*.swo", "*~"]),
    ("Secrets",       ".env, credentials.json -- sensitive, AI should never see",
     [".env", ".env.local", ".env.*.local", ".secrets", "secrets.json", "credentials.json"]),
    ("Git internals", ".git/, .github/ -- version control metadata",
     [".git/", ".github/", ".gitignore"]),
    ("Caches",        ".cache, .turbo, .parcel-cache -- build caches",
     [".cache/", ".parcel-cache/", ".turbo/", "dist-ssr/", ".nyc_output/"]),
]


def phase_ignore_files():
    redraw(1)
    info("Like .gitignore but for AI -- blocks irrelevant files from context. Saves 40-70%.\n")

    targets = [(".claudeignore", "Claude Code"), (".geminiignore", "Gemini CLI"), (".codexignore", "Codex CLI")]
    to_create = []
    for fname, tool in targets:
        if Path(fname).exists():
            info(f"{fname} exists, skipping.")
        elif ask(f"Create {fname} for {tool}?"):
            to_create.append(fname)

    if not to_create:
        finish_phase(1)
        return

    print(f"\n  {C.bold('Categories to exclude:')}\n")
    sel = pick(
        "Pick categories (comma-separated, or 'a' for all)",
        [f"{C.bold(n):24s} {C.dim(d)}" for n, d, _ in IGNORE_CATEGORIES],
        allow_all=True,
    )
    if not sel:
        warn("Nothing selected.")
        finish_phase(1)
        return

    lines = []
    for i in sel:
        name, desc, patterns = IGNORE_CATEGORIES[i]
        lines.append(f"# {name} -- {desc}")
        lines.extend(patterns)
        lines.append("")

    content = "\n".join(lines)
    n = sum(1 for l in lines if l and not l.startswith("#"))
    for fname in to_create:
        Path(fname).write_text(content)
        ok(f"{fname} ({n} patterns)")

    finish_phase(1)


# ─────────────────────────────────────────────────────────────
# Phase 2: Claude Code Settings
# ─────────────────────────────────────────────────────────────

SETTINGS = [
    {
        "key": "model",
        "name": "Default model",
        "why": "Which model Claude Code uses. Sonnet is ~60% cheaper than Opus for ~80% of tasks.",
        "rec": "sonnet",
        "opts": [
            ("sonnet", "Good quality, 60% cheaper than Opus"),
            ("opus",   "Best quality, most expensive"),
            ("haiku",  "Cheapest, good for simple tasks"),
        ],
    },
    {
        "key": "env.MAX_THINKING_TOKENS",
        "name": "Thinking token cap",
        "why": "Hidden reasoning tokens billed at 5x input rate. Default ~32K. Lower = cheaper.",
        "rec": "10000",
        "opts": [
            ("5000",  "Aggressive -- may hurt complex reasoning"),
            ("10000", "Balanced -- 70% savings, handles most tasks"),
            ("20000", "Conservative -- slight savings"),
            ("32000", "No change -- full budget"),
        ],
    },
    {
        "key": "env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE",
        "name": "Auto-compact at %",
        "why": "When context hits this %, old messages get summarized. Default 95% (almost never).",
        "rec": "50",
        "opts": [
            ("30", "Aggressive -- compacts early, leaner context"),
            ("50", "Balanced -- compacts at half-full"),
            ("70", "Moderate"),
            ("95", "No change -- default, rarely compacts"),
        ],
    },
    {
        "key": "env.CLAUDE_CODE_SUBAGENT_MODEL",
        "name": "Subagent model",
        "why": "Model for background tasks (file search, grep). Simpler tasks, cheaper model.",
        "rec": "haiku",
        "opts": [
            ("haiku",  "Cheapest -- handles search/grep fine"),
            ("sonnet", "Mid-range"),
            ("opus",   "Most expensive -- usually overkill"),
        ],
    },
]


def phase_settings():
    redraw(2)
    info("Configures ~/.claude/settings.json. Pick each setting individually.")
    info("Existing settings (permissions, hooks) are preserved.\n")

    if not ask("Configure settings?"):
        finish_phase(2)
        return

    claude_dir = SYS.home / ".claude"
    settings_file = claude_dir / "settings.json"
    existing = {}
    if settings_file.exists():
        try:
            existing = json.loads(settings_file.read_text())
        except (json.JSONDecodeError, OSError):
            pass

    claude_dir.mkdir(exist_ok=True)
    result = dict(existing)
    changes = []

    for s in SETTINGS:
        if s["key"].startswith("env."):
            env_key = s["key"].split(".", 1)[1]
            cur = existing.get("env", {}).get(env_key, "default")
        else:
            cur = existing.get(s["key"], "default")

        print(f"\n  {C.bold(s['name'])}  {C.dim('(current: ' + str(cur) + ')')}")
        print(f"  {s['why']}\n")

        for i, (val, desc) in enumerate(s["opts"], 1):
            star = C.green(" *") if val == s["rec"] else ""
            print(f"    {C.cyan(str(i))}. {val:8s} {C.dim(desc)}{star}")
        print(f"    {C.cyan('s')}. Skip")

        try:
            raw = input(f"\n  {C.cyan('?')} Choice: ").strip().lower()
        except EOFError:
            raw = "s"

        if raw == "s" or not raw:
            continue

        try:
            idx = int(raw) - 1
            if not (0 <= idx < len(s["opts"])):
                continue
        except ValueError:
            continue

        chosen = s["opts"][idx][0]
        if s["key"].startswith("env."):
            env_key = s["key"].split(".", 1)[1]
            result.setdefault("env", {})[env_key] = chosen
        else:
            result[s["key"]] = chosen
        changes.append((s["name"], chosen))
        ok(f"{s['name']} = {chosen}")

    if changes:
        settings_file.write_text(json.dumps(result, indent=2) + "\n")
        print()
        ok(f"Wrote {len(changes)} setting(s) to ~/.claude/settings.json")

    finish_phase(2)


# ─────────────────────────────────────────────────────────────
# Phase 3: Install Tools (linear, one at a time)
# ─────────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "RTK",
        "savings": "60-90%",
        "oneliner": "Compresses CLI output (git, npm, ls, grep...) before AI sees it.",
        "how": "Installs as a hook -- your commands run normally, output gets auto-compressed.",
        "example": "git log: 50KB -> 3KB (94% smaller)",
        "installer": "install_rtk",
    },
    {
        "name": "Repomix",
        "savings": "~70%",
        "oneliner": "Packs your entire codebase into one AI-friendly file.",
        "how": "Uses Tree-sitter to extract function signatures, skip bodies.",
        "example": "repomix --output repo.md --compress",
        "installer": "install_repomix",
    },
    {
        "name": "Tokscale",
        "savings": "monitor",
        "oneliner": "Tracks token usage across Claude, Gemini, Cursor, Codex.",
        "how": "Aggregates usage data and shows trends so you know what to optimize.",
        "example": "tokscale report --history",
        "installer": "install_tokscale",
    },
    {
        "name": "ccusage",
        "savings": "monitor",
        "oneliner": "Shows token usage from Claude Code's local log files.",
        "how": "Reads ~/.claude/logs and breaks down input/output/thinking per session.",
        "example": "npx ccusage@latest",
        "installer": "install_ccusage",
    },
    {
        "name": "files-to-prompt",
        "savings": "50-70%",
        "oneliner": "Cherry-picks specific files into a prompt-friendly format.",
        "how": "Unlike Repomix (whole repo), this targets individual files you choose.",
        "example": "files-to-prompt src/**/*.js --output context.md",
        "installer": "install_files_to_prompt",
    },
]

# Map string names to actual functions (defined below)
TOOL_INSTALLERS = {}


def phase_install_tools():
    redraw(3)

    if not SYS.has_npm and not SYS.has_pip and not SYS.has_brew:
        err("No package manager found (npm, pip, or brew).")
        finish_phase(3)
        return []

    mgrs = ", ".join(filter(None, [
        "npm" if SYS.has_npm else None,
        SYS.pip_cmd if SYS.has_pip else None,
        "brew" if SYS.has_brew else None,
    ]))
    info(f"Package managers: {mgrs}\n")

    installed = []
    for t in TOOLS:
        sav = t["savings"]
        tag = C.green(f"[{sav}]") if sav != "monitor" else C.blue("[monitor]")
        print(f"  {C.bold(t['name'])} {tag}  {t['oneliner']}")
        print(f"  {C.dim(t['how'])}")
        print(f"  {C.dim('e.g. ' + t['example'])}")

        if ask(f"Install {t['name']}?"):
            fn = TOOL_INSTALLERS[t["installer"]]
            if fn():
                installed.append(t["name"])
        print()

    finish_phase(3)
    return installed


def install_rtk():
    if SYS.has_npm and npm_install("RTK", "@rtk-ai/rtk"):
        setup_rtk()
        return True
    if SYS.has_brew and brew_install("RTK", "rtk-ai/tap/rtk"):
        setup_rtk()
        return True
    err("Could not install RTK.")
    return False


def setup_rtk():
    tools = [("claude-code", "Claude Code"), ("cursor", "Cursor"), ("codex", "Codex CLI"), ("gemini", "Gemini CLI")]
    info("Which AI tools should RTK hook into?\n")
    sel = pick("Tools (comma-separated or 'a')", [n for _, n in tools], allow_all=True)
    for i in sel:
        tid, name = tools[i]
        if SYS.run(["rtk", "init", "-g", f"--{tid}"]):
            ok(f"RTK hooked into {name}")
        else:
            err(f"Failed for {name}")


def install_repomix():
    if SYS.has_npm: return npm_install("Repomix", "repomix")
    err("Needs npm.")
    return False


def install_tokscale():
    if SYS.has_npm: return npm_install("Tokscale", "tokscale")
    err("Needs npm.")
    return False


def install_ccusage():
    if SYS.has_npm: return npm_install("ccusage", "ccusage")
    err("Needs npm.")
    return False


def install_files_to_prompt():
    if SYS.has_npm and npm_install("files-to-prompt", "files-to-prompt"):
        return True
    if SYS.has_pip:
        return pip_install("files-to-prompt", "files-to-prompt")
    err("Needs npm or pip.")
    return False


# Register installers
TOOL_INSTALLERS = {
    "install_rtk": install_rtk,
    "install_repomix": install_repomix,
    "install_tokscale": install_tokscale,
    "install_ccusage": install_ccusage,
    "install_files_to_prompt": install_files_to_prompt,
}


# ─────────────────────────────────────────────────────────────
# Phase 4: CLAUDE.md
# ─────────────────────────────────────────────────────────────

def phase_claude_md():
    redraw(4)
    info("CLAUDE.md loads into every message. Bigger file = more tokens per prompt.\n")

    p = Path("CLAUDE.md")
    if not p.exists():
        info("No CLAUDE.md in current directory.")
        finish_phase(4)
        return

    content = p.read_text()
    lines = len(content.splitlines())
    toks = len(content) // 4

    if lines <= 60:
        ok(f"{lines} lines (~{toks:,} tok/msg) -- good size.")
    elif lines <= 150:
        warn(f"{lines} lines (~{toks:,} tok/msg) -- consider trimming.")
        info("Split into CLAUDE.md (critical rules) + @ARCHITECTURE.md (on-demand).")
    else:
        err(f"{lines} lines (~{toks:,} tok/msg) -- too large.")
        info("Over a 50-msg session: ~{:,} tokens on instructions alone.".format(toks * 50))
        info("Split into smaller files, reference with @filename in prompts.")

    finish_phase(4)


# ─────────────────────────────────────────────────────────────
# Phase 5: Best Practices
# ─────────────────────────────────────────────────────────────

def phase_best_practices():
    redraw(5)

    tips = [
        ("Use Sonnet by default",    "60%",    "cheaper than Opus for most tasks"),
        ("Enable .claudeignore",     "40-70%", "auto-exclude irrelevant files"),
        ("Use RTK hooks",            "60-90%", "compress all CLI output"),
        ("/clear between tasks",     "30-50%", "prevent context bloat"),
        ("Batch requests",           "20-40%", "fewer prompts = less overhead"),
        ("Use repomix",              "70%",    "compress repo context"),
        ("Prompt caching (API)",     "90%",    "on repeated system prompts"),
        ("Batch API",                "50%",    "for scheduled workloads"),
    ]

    for i, (tip, sav, why) in enumerate(tips, 1):
        print(f"  {i:2}. {tip:28s} {C.green(f'{sav:>6}')}  {C.dim(why)}")

    print(f"\n  {C.dim('Details: awesome-token-reduction.md')}")
    finish_phase(5)


# ─────────────────────────────────────────────────────────────
# Phase 6: Monitoring
# ─────────────────────────────────────────────────────────────

def phase_monitoring():
    redraw(6)

    cmds = [
        ("rtk gain",           "Token savings analytics"),
        ("rtk discover",       "Find missed optimizations"),
        ("tokscale report",    "Usage across tools"),
        ("npx ccusage@latest", "Claude Code usage from logs"),
    ]
    for cmd, desc in cmds:
        print(f"    {C.cyan(f'{cmd:24s}')} {C.dim(desc)}")

    finish_phase(6)


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="tokendiet - AI Token Optimization Wizard")
    parser.add_argument("--version", action="version", version="tokendiet 1.0.0")
    parser.add_argument("--skip", type=str, default="", help="Skip phases (e.g. --skip 1,2)")
    args = parser.parse_args()

    skip = set()
    if args.skip:
        try:
            skip = {int(x) for x in args.skip.split(",")}
        except ValueError:
            print("--skip: use comma-separated numbers (1-6)")
            sys.exit(1)

    # Opening screen
    redraw()
    input(f"  {C.dim('Press Enter to start...')}")

    installed = []
    if 1 not in skip: phase_ignore_files()
    if 2 not in skip: phase_settings()
    if 3 not in skip: installed = phase_install_tools()
    if 4 not in skip: phase_claude_md()
    if 5 not in skip: phase_best_practices()
    if 6 not in skip: phase_monitoring()

    # Final screen
    redraw()
    print()
    if installed:
        ok(f"Installed: {', '.join(installed)}")
    print(f"""
  {C.bold('Next steps:')}
    1. Start a new Claude Code session
    2. Use tools normally (RTK hooks are automatic)
    3. Track savings: {C.bold('rtk gain')} / {C.bold('npx ccusage@latest')}
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n  {C.yellow('Cancelled.')}")
        sys.exit(0)
