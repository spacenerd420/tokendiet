# Awesome Token Reduction (Comprehensive Edition)

A curated collection of **strategies, tools, workarounds, and best practices** to reduce token consumption and costs across Claude Code, Cursor, Codex CLI, and all major AI development environments.

**Updated:** April 2026 with latest workarounds from Anthropic and community findings.

---

## 📊 Executive Summary

Token optimization can achieve:

- **60-90% reduction** via CLI output compression ([RTK](https://github.com/rtk-ai/rtk))
- **90% reduction** via prompt caching on repeated requests
- **70% reduction** via repository compression ([Repomix](https://github.com/yamadashy/repomix))
- **50% savings** via Batch API on scheduled tasks
- **40-70% reduction** on outputs via structured formats (JSON vs prose)
- **Combined impact: 90%+ reduction** when all techniques stacked

---

## 🏆 Top Tools & Quick Comparison

| Tool | Impact | Setup | Best For |
|------|--------|-------|----------|
| **RTK** | 60-90% | Easy (npm install) | All CLI commands automatically |
| **Repomix** | 70% | Easy (npm install) | Initial repo context, docs |
| **Prompt Caching** | 90% (repeats) | Medium (API config) | API users with repeated context |
| **Batch API** | 50% | Medium (API setup) | Scheduled/batch processing |
| **Tokscale** | Monitor | Easy (npm install) | Token usage tracking & analytics |
| **Files-to-prompt** | 50-70% | Easy (CLI) | Selective file inclusion |
| **.claudeignore** | 40-70% | Trivial (1 file) | Context window management |

---

## 🛠️ Tools Deep Dive

### RTK (Rust Token Killer) — ⭐⭐⭐ Highest Priority

**GitHub:** [rtk-ai/rtk](https://github.com/rtk-ai/rtk)

**What:** CLI proxy that intercepts shell commands and returns compressed, AI-optimized output.

**Installation:**
```bash
npm install -g @rtk-ai/rtk
# or Homebrew:
brew install rtk-ai/tap/rtk
# Verify:
rtk --version
```

**Setup for Claude Code:**
```bash
rtk init -g --claude-code
# Creates ~/.claude/RTK.md with @RTK global reference
```

**Setup for Cursor:**
```bash
rtk init -g --cursor
```

**Setup for Codex CLI:**
```bash
rtk init -g --codex
# Creates ~/.codex/RTK.md + ~/.codex/AGENTS.md
```

**Usage (Transparent Hook):**
```bash
# Just use normally—RTK hook automatically compresses output
git status            # ~70-90% smaller
npm test              # ~60-80% smaller
git log               # ~80-90% smaller
find . -type f        # ~95% smaller
ls -la /large/dir     # ~95% smaller
grep -r "pattern" .   # ~90% smaller
```

**Compression Strategies RTK Uses:**
1. **Progress bars & spinners** → Removed
2. **Repeated headers/footers** → Deduplicated
3. **ANSI color codes** → Stripped
4. **Whitespace normalization** → Collapsed
5. **Redundant metadata** → Removed (timestamps unless critical)
6. **Truncated output** → Summarized with counts
7. **Structured data** → Converted to JSON
8. **Line limiting** → Shows first N + last M with count
9. **Duplicate suppression** → Groups identical results
10. **Semantic summarization** → Verbose outputs condensed
11. **Table formatting** → Optimized for token density
12. **Sort & deduplicate** → Tree structures simplified

**Supported Commands:** 100+ including `git`, `npm`, `yarn`, `pnpm`, `ls`, `find`, `grep`, `cat`, `head`, `tail`, `diff`, `docker`, `kubectl`, `ps`, `curl`, `python`, etc.

**Metrics:**
```bash
rtk gain              # Show token savings analytics
rtk gain --history    # Show command history with savings
rtk discover          # Analyze history for missed opportunities
```

**Setup Cost:** ~5 minutes  
**Payoff:** Every command from day 1  
**Recommended:** YES—this is the single highest-ROI tool

---

### Repomix — Repository Compression

**GitHub:** [yamadashy/repomix](https://github.com/yamadashy/repomix)

**What:** Packs your entire codebase into a single structured file (Markdown, XML, or JSON) using Tree-sitter AST.

**Installation:**
```bash
npm install -g repomix
```

**Basic Usage:**
```bash
# Generate repository snapshot
repomix --output repo.md

# With compression (removes function bodies, keeps signatures)
repomix --output repo.md --compress

# Output as JSON
repomix --output repo.json --style json

# Filter to specific directories
repomix --include src,tests --output focused.md

# Exclude patterns
repomix --exclude node_modules,dist --output clean.md
```

**Output Example:**
```markdown
# Repository Structure

## src/app.js (45 lines)
```javascript
export async function createApp(config) { ... }
export const middleware = { ... }
```

## src/db.js (120 lines)
```javascript
export async function query(sql) { ... }
export class Database { ... }
```
```

**Token Savings:** ~70% on repository context

**Best For:**
- Initial code review or architecture understanding
- Uploading to Claude Projects for persistent reference
- Reducing context when full repo isn't needed
- Sharing with AI assistants

**Pro Tip:** Upload compressed repo to Claude Projects once, reference across unlimited conversations = 20% additional session savings.

---

### Files-to-Prompt — Selective Context Building

**GitHub:** [simonw/files-to-prompt](https://github.com/simonw/files-to-prompt)

**Installation:**
```bash
npm install -g files-to-prompt
# or pip:
pip install files-to-prompt
```

**Usage:**
```bash
# Convert specific files
files-to-prompt src/**/*.js --output context.md

# Include line numbers for references
files-to-prompt src/ --include "*.js" --line-numbers

# For system prompts
files-to-prompt config/ --output config.txt
```

**Advantage over Repomix:** Preserves full implementations (doesn't compress), good for targeted file inclusion.

---

### Tokscale — Token Usage Tracking

**What:** Tracks and visualizes token usage across Gemini, Claude, Cursor, and other agents.

**Installation:**
```bash
npm install -g tokscale
```

**Usage:**
```bash
tokscale report              # View token usage stats
tokscale report --history    # Show historical trends
tokscale compare             # Compare models/tools
```

---

## 📋 Layer 1: CLI & Context (Biggest Impact)

### 1.1 Ignore Files (.claudeignore / .geminiignore)

**Why:** Every file Claude reads consumes context, whether relevant or not.

**Comprehensive .claudeignore template:**

```gitignore
# ========== Dependencies & Package Managers ==========
node_modules/
.venv/
venv/
env/
vendor/
go.sum
Cargo.lock
*.lock
pnpm-lock.yaml
yarn.lock
package-lock.json

# ========== Build Artifacts & Generated Files ==========
dist/
build/
out/
.next/
.nuxt/
.vercel/
.env*
__pycache__/
*.pyc
*.pyo
*.egg-info/
.pytest_cache/
.mypy_cache/
target/
.gradle/
.class

# ========== Large Assets (Typically Not Code) ==========
*.png
*.jpg
*.jpeg
*.gif
*.svg
*.webp
*.ico
*.mp4
*.mov
*.avi
*.wav
*.mp3
*.zip
*.tar
*.gz
*.rar
*.7z

# ========== Logs & Temporary Files ==========
*.log
*.tmp
*.temp
tmp/
logs/
coverage/
.DS_Store
Thumbs.db

# ========== IDE & Editor Config ==========
.vscode/
.idea/
*.swp
*.swo
*~
.sublime-*
*.iml

# ========== Environment & Secrets ==========
.env
.env.local
.env.*.local
.secrets
secrets.json
credentials.json

# ========== Version Control ==========
.git/
.github/
.gitignore

# ========== Docker & Containers ==========
node_modules/.bin/
Dockerfile
.dockerignore

# ========== Analytics & Cache ==========
.cache/
.parcel-cache/
.turbo/
dist-ssr/
.nyc_output/
```

**Expected Savings:** 40-70% context reduction

---

### 1.2 Claude Code-Specific Optimizations

#### 1.2a settings.json Configuration (60-80% Reduction)

**Location:** `~/.claude/settings.json`

```json
{
  "model": "sonnet",
  "env": {
    "MAX_THINKING_TOKENS": "10000",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50",
    "CLAUDE_CODE_SUBAGENT_MODEL": "haiku"
  }
}
```

**What This Does:**
- Defaults to Sonnet (60% cheaper than Opus)
- Caps hidden thinking tokens from 32K → 10K (70% saving)
- Compacts context at 50% instead of 95% (healthier sessions)
- Routes all subagents to Haiku (80% cheaper)

**Impact:** 60-80% total token reduction

#### 1.2b Keep CLAUDE.md Lean (90% Reduction on Startup)

**Problem:** CLAUDE.md loads into every message. A 11,000-token CLAUDE.md = 11K tokens wasted on every prompt.

**Solution:** Split into 4 small files (~2K tokens total):

```
.claude/
├── CLAUDE.md            (~800 tokens, critical items only)
├── ARCHITECTURE.md      (~400 tokens, on-demand)
├── PATTERNS.md          (~400 tokens, on-demand)
└── STYLE.md             (~400 tokens, on-demand)
```

**CLAUDE.md Content (Critical Only):**
```markdown
# Project Rules

- Use Sonnet for implementation, Opus for architecture only
- Prefer .claudeignore patterns over file-level filtering
- Test changes locally before pushing

## Tools
- RTK enabled globally
- Repomix available for repo snapshots
```

**How to Reference Dynamically:**
User can ask: "Read ARCHITECTURE.md and suggest a pattern for..."

**Savings:** ~10,000 tokens/session (90% reduction in startup cost)

#### 1.2c The Read-Once Hook (40-90% Reduction on File Reads)

**Problem:** Claude re-reads files way more than necessary.

**Solution:** Install read-once hook that blocks redundant reads:

```bash
curl -fsSL https://raw.githubusercontent.com/Bande-a-Bonnot/Boucle-framework/main/tools/read-once/install.sh | bash
```

**Measured Impact:** ~38K tokens saved on ~94K total reads in a single session

#### 1.2d /clear, /compact, and Session Breaks (Context Management)

**Strategy:**
- `/clear` between unrelated tasks (use `/rename` first)
- `/compact` at logical breakpoints
- Never exceed 200K context even though 1M is available

**Token Savings:** 20-40% per session by avoiding context bloat

### 1.3 Cursor-Specific Optimizations

**Cursor has longer runtime than Claude Code.** One user reported running 8 hours straight without hitting limits.

**Optimization Strategy for Cursor:**
- Same RTK setup: `rtk init -g --cursor`
- Same .claudeignore patterns
- Cursor's longer runtime = better for iterative tasks

### 1.4 Codex CLI-Specific Optimizations

**Installation & Setup:**
```bash
# Install Codex
npm install -g codex
# or pip:
pip install codex

# Setup RTK integration
rtk init -g --codex
# Creates ~/.codex/RTK.md + ~/.codex/AGENTS.md

# Verify
codex --version
```

**Codex RTK Integration:**
- RTK reads `~/.codex/RTK.md` and `~/.codex/AGENTS.md` as global instructions
- Hook transparently rewrites Bash commands (e.g., `git status` → `rtk git status`)
- Codex never sees the rewrite—just gets compressed output

**Token Impact:** Same 60-90% reduction as Claude Code + Cursor

---

## 💻 Layer 2: Prompt & API Optimization

### 2.1 Prompt Caching (90% on Repeats)

**Supported Models:** Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku, Claude 3.5 Haiku

**Python Implementation:**
```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

# System prompt to cache
SYSTEM = """You are an expert code reviewer..."""

# Data to cache (docs, codebase context)
docs = open("docs.txt").read()

# First request (creates cache, full price)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=[
        {"type": "text", "text": SYSTEM, 
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": f"Docs:\n{docs}",
         "cache_control": {"type": "ephemeral"}}
    ],
    messages=[{"role": "user", "content": "Review: ..."}]
)

# Subsequent requests (90% discount on cached tokens)
response2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=[...],  # Same system blocks
    messages=[{"role": "user", "content": "Review: ..."}]
)
```

**Pricing:**
- First hit: Full price on system tokens
- Cache hits (5min): 10% of cached input token cost
- Cache duration: 5 min (default) or 1 hour
- Minimum: 1024 tokens per cache checkpoint

**Use Cases:** Conversational agents, repeated code review, book/doc analysis

---

### 2.2 Output Optimization (40-70% Reduction)

**Key Insight:** Output tokens = 5x cost per token vs input. Optimizing output is critical.

**Strategy:** Request structured output (JSON) instead of prose.

**Example:**
```python
# Prose response (many tokens)
"Please tell me about this document"

# Optimized (JSON structure)
"""Return as JSON:
{
  "title": "...",
  "key_points": ["...", "..."],
  "author": "...",
  "date": "YYYY-MM-DD"
}"""
```

**Techniques:**
- Format constraints: "Return as JSON with max 5 sentences"
- Stop sequences: Stop at first `}`
- Summarization: "List 3 facts, one sentence each"
- Quantity limits: "Max 10 results"

---

### 2.3 Model Selection (60% Cost Reduction)

**Rule:** Use Sonnet for 80%+ of work, Opus for complex decisions only.

| Task | Model | Reason |
|------|-------|--------|
| Code explanation | Sonnet | Fast, accurate, 60% cheaper |
| Writing tests | Sonnet | Straightforward generation |
| Simple edits | Sonnet | Handles replacements well |
| Architecture | Opus | Complex decisions |
| Multi-file refactor | Opus | Orchestrates large changes |
| Debugging complex | Opus | Deep analysis needed |
| Documentation | Sonnet | Standard writing |

**Cost:** Sonnet = ~60% of Opus

---

### 2.4 Batch API (50% Savings)

**Use For:**
- Document processing pipelines
- Code review batches
- Data classification
- Scheduled analysis

**Implementation:**
```python
import anthropic

client = anthropic.Anthropic()

# Prepare 100 requests
requests = [
    {
        "custom_id": f"req-{i}",
        "params": {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": f"Process doc {i}"}]
        }
    }
    for i in range(100)
]

# Submit
batch = client.beta.messages.batches.create(requests=requests)

# Poll (asynchronous, process within 24 hours)
while True:
    status = client.beta.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    # Check results
```

**Savings:** 50% off all input/output tokens

---

## ⚙️ Layer 3: Advanced Techniques

### 3.1 Extended Thinking Optimization

**Cost Model:**
- Input: Standard rate
- Thinking tokens: Output rate (5x more expensive)
- Output: Output rate (5x more expensive)

**Strategy:** Use only when necessary for complex reasoning.

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=8000,
    thinking={"type": "enabled", "budget_tokens": 5000},
    messages=[...]
)
```

### 3.2 Token Compression Algorithms

**For research/special cases:**
- **LLMLingua:** Rank & preserve key tokens in long contexts (10-80% compression)
- **Hard prompting:** Remove redundant tokens via rules
- **Semantic caching:** Cache similar (not just exact) queries
- **KV cache optimization:** Reduce visual tokens in multimodal models

**Resource:** [A Survey of Token Compression for Efficient Multimodal LLMs](https://arxiv.org/html/2507.20198v5)

---

## 🚨 Claude Usage Limits Workarounds (March 2026)

**Context:** Anthropic introduced peak-hour multipliers (~March 23) that burn session limits faster during US business hours (5am-11am PT). Community workarounds:

### A. Workarounds for All Products

**A1. Switch Opus → Sonnet (Single Biggest Lever)**
- Opus consumes ~5x more tokens than Sonnet
- Sonnet handles ~80% of tasks
- Savings: 60%

**A2. Switch 1M → 200K Context Model**
- Default changed to 1M context (more expensive)
- Switch back to standard 200K
- Savings: 20-30%

**A3. Start New Conversations Frequently**
- Context accumulates with every message
- Start per-task conversations
- Savings: 30-50% on long threads

**A4. Be Surgical with Prompts**
- "Fix JWT validation in src/auth/validate.ts line 42" (cheaper)
- vs "fix the auth bug" (broad, expensive)
- Savings: Up to 10x on specificity

**A5. Batch Requests into Fewer Prompts**
- One detailed prompt with 3 asks < 3 separate prompts
- Saves context overhead
- Savings: 20-40%

**A6. Pre-process Documents Externally**
- Convert PDFs to text before uploading
- Parse through ChatGPT first (more generous)
- Savings: 50-80% on document workflows

**A7. Shift Work to Off-Peak Hours**
- Outside weekdays 5am-11am PT
- Note: Less reliable since ~March 28
- Savings: Variable

**A8. Session Timing Trick**
- 5-hour window starts with first message
- Start 2-3 hours before real work
- Window resets at 11am PT mid-work
- Savings: Extra 2-3 hours per session

### B. Claude Code CLI Specific

**B1. settings.json Block (60-80% Reduction)**
See "1.2a settings.json" above

**B2. .claudeignore File (40-70% Reduction)**
See "1.1 Ignore Files" above

**B3. Keep CLAUDE.md Under 60 Lines (90% Startup Reduction)**
See "1.2b Keep CLAUDE.md Lean" above

**B4. Install Read-Once Hook (40-90% Reduction)**
See "1.2c The Read-Once Hook" above

**B5. /clear and /compact Aggressively**
- `/clear` between unrelated tasks
- `/compact` at logical breakpoints
- Never exceed 200K even with 1M available

**B6. Plan in Opus, Implement in Sonnet**
- Architecture/planning = Opus
- Code generation = Sonnet
- Savings: 40-60%

**B7. Install Monitoring Tools**
```bash
npx ccusage@latest              # Token usage from logs
npm install -g ccburn           # Burn-up charts
npm install -g claude-code-usage-monitor  # Real-time dashboard
npm install -g ccstatusline     # Status bar token display
```

**B8. Save Explanations Locally**
```bash
claude "explain schema" > docs/schema-explanation.md
```
Reference later at minimal cost vs re-analysis.

**B9. Advanced Context Engines** (Max 5x/Max 20x only)
- Local MCP context server with Tree-sitter: -90% tool calls, -58% cost
- LSP + ast-grep: Structured code intelligence
- claude-warden hooks: Read compression, output truncation
- Progressive skill loading: ~15K tokens/session recovered
- Subagent model routing: haiku on exploration, opus on architecture only

---

## 🔄 Alternative Tools & Multi-Provider Strategy

### Codex CLI — GPT-5.3-Codex Alternative

**Status:** Actively developed, available in Cursor and VSCode

**Advantage:** More lenient rate limits than Claude. Users report never hitting session limits.

**Setup:**
```bash
npm install -g codex
# Configure with RTK:
rtk init -g --codex
```

**Caveat:** OpenAI may impose similar limits after their promo ends.

**Reference:** [GitHub - openai/codex](https://github.com/openai/codex) | [Claude Code vs Cursor vs Codex: Which AI Coding Tool Should You Use in 2026?](https://medium.com/@writertripathi/claude-code-vs-cursor-vs-openai-codex-which-ai-coding-tool-should-you-use-in-2026-8f124e43c6fd)

### Cursor IDE

**Advantage:** Reportedly offers much more runtime than Claude Code. One user ran 8 hours straight.

**Setup:** Same RTK + .claudeignore patterns work
```bash
rtk init -g --cursor
```

### Gemini CLI (Free)

**Limits:** 60 req/min, 1,000 req/day, 1M context

**Use For:** Terminal tasks when Claude limits exhausted

### Hybrid Workflow (Most Sustainable)

```
Planning/Architecture → Claude (Opus)
        ↓
Code Implementation → Codex, Cursor, or local models
        ↓
File Exploration/Testing → Haiku subagents or local
        ↓
Document Parsing → ChatGPT (more lenient limits)
        ↓
Research → Gemini free or Perplexity
```

Distributes load across vendors, reduces dependency on single limit source.

### Chinese Open-Weight Models

- **Qwen 3.6 Preview** (OpenRouter): Approaching Opus quality
- **DeepSeek:** Improving fast
- **Local inference:** Increasing viability

---

## 📊 Monitoring & Measurement

### Track Usage

```bash
# RTK analytics
rtk gain              # Token savings
rtk gain --history    # Usage history
rtk discover          # Optimization opportunities

# Claude Code specific
npx ccusage@latest    # Token usage from logs
ccburn --compact      # Visual burn-up charts
```

### Expected Baseline Improvements

After implementing all strategies:
- **Tokens per session:** 50-70% reduction
- **Cost per task:** 60-80% reduction
- **Response latency:** Improves (smaller context)
- **Rate limit hits:** Dramatically reduced

---

## 🎯 Implementation Checklist

**Phase 1 (Day 1): Quick Wins**
- [ ] Create .claudeignore / .geminiignore
- [ ] Install RTK: `npm install -g @rtk-ai/rtk`
- [ ] Setup for your tool: `rtk init -g --[claude-code|cursor|codex]`

**Phase 2 (Week 1): Medium Wins**
- [ ] Configure settings.json
- [ ] Lean down CLAUDE.md
- [ ] Install read-once hook
- [ ] Generate Repomix snapshot

**Phase 3 (Week 2-4): Long-term**
- [ ] Audit commands with `rtk discover`
- [ ] Enable prompt caching (API users)
- [ ] Set up batch processing
- [ ] Install monitoring (tokscale, ccusage)

---

## 📚 References

### Official Documentation
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Prompt Caching - Claude API](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Prompting Best Practices - Claude API](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

### Token Optimization Guides
- [6 Ways I Cut My Claude Token Usage in Half!](https://www.sabrina.dev/p/6-ways-i-cut-my-claude-token-usage)
- [Stop Burning Tokens: A Developer's Guide to Claude AI Token Optimization](https://levelup.gitconnected.com/stop-burning-tokens-a-developers-guide-to-claude-ai-token-optimization-4c70c7c52ffb)
- [18 Claude Code Token Management Hacks](https://www.mindstudio.ai/blog/claude-code-token-management-hacks)
- [How to Save 90% on Claude API Costs: 3 Official Techniques](https://dev.to/stklen/how-to-save-90-on-claude-api-costs-3-official-techniques-3d4n)
- [How I Reduced LLM Token Costs by 90%](https://medium.com/@ravityuval/how-i-reduced-llm-token-costs-by-90-using-prompt-rag-and-ai-agent-optimization-f64bd1b56d9f)

### Tools & Integration
- [RTK (Rust Token Killer) GitHub](https://github.com/rtk-ai/rtk)
- [Repomix - Repository Compression](https://github.com/yamadashy/repomix)
- [Files-to-Prompt](https://github.com/simonw/files-to-prompt)
- [Codex CLI - OpenAI](https://github.com/openai/codex)
- [RTK Saves 60% of Tokens. I Made It Save 90%.](https://dev.to/ji_ai/rtk-saves-60-of-tokens-i-made-it-save-90-3ib1)

### Advanced Resources
- [LLM Token Optimization: Cut Costs & Latency in 2026](https://redis.io/blog/llm-token-optimization-speed-up-apps/)
- [A Survey of Token Compression for Efficient Multimodal LLMs](https://arxiv.org/html/2507.20198v5)
- [Context Compression Techniques: Reduce LLM Costs by 50%](https://www.sitepoint.com/optimizing-token-usage-context-compression-techniques/)
- [Token Efficiency and Compression Techniques in LLMs](https://medium.com/@anicomanesh/token-efficiency-and-compression-techniques-in-large-language-models-navigating-context-length-05a61283412b)

### Community Insights
- [Claude Code Best Practices: 15 Tips from 6 Projects](https://aiorg.dev/blog/claude-code-best-practices)
- [50 Claude Code Tips and Best Practices](https://www.builder.io/blog/claude-code-tips-best-practices)
- [5 Patterns That Make Claude Code Follow Your Rules](https://dev.to/docat0209/5-patterns-that-make-claude-code-actually-follow-your-rules-44dh)
- [Claude Code Efficiency Tricks](https://medium.com/@mehedipy/claude-code-efficiency-tricks-de09a72d9019)
- [CLI Coding Agent Extensions Tier List 2026](https://claudelab.net/en/articles/claude-code/cli-coding-agent-extensions-tier-list-2026)

---

## 💡 Pro Tips

1. **Combine strategies:** RTK + .claudeignore + prompt caching = 90%+ total
2. **Start with RTK:** Highest ROI—install once, save on everything automatically
3. **Monitor continuously:** Track with `rtk gain` and `ccusage`
4. **Use Claude Projects:** Upload docs once, reference infinitely
5. **Batch expensive work:** Use Batch API for document processing
6. **Audit regularly:** Use `rtk discover` for new opportunities
7. **Multi-provider:** Distribute load across tools to avoid hitting limits

---

**Last Updated:** April 2026  
**Maintained by:** Token Optimizer Community  
**Contributions Welcome:** Submit PRs for new tools, techniques, or updated metrics
