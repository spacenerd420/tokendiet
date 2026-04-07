# Token Optimizer: A Complete Guide to Reducing AI Token Consumption

[![GitHub](https://img.shields.io/badge/github-token--optimizer-blue?logo=github)](https://github.com/yourusername/token-optimizer)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7+-blue)

> **Token Optimization = Faster responses + Lower costs + Reduced API limits pressure.** This guide covers strategies, tools, and best practices for reducing token consumption in AI-powered development environments like Claude Code, Gemini CLI, Cursor, Windsurf, and Cline by 60-90%.

---

## 📊 Impact & Results

Token optimization can deliver dramatic results:

- **60-90% reduction** in daily token consumption with tool-based approaches ([rtk](https://github.com/rtk-ai/rtk))
- **50% cost savings** on API calls via Batch API processing
- **90% reduction** on repeated requests via prompt caching
- **70% reduction** on repository context via intelligent compression (repomix)
- **10-80% savings** on documentation/classification tasks via output optimization

**Real-world example:** A developer averaging 500K tokens/month can reduce to ~50-200K/month with these techniques, saving hundreds of dollars while improving response speed.

---

## 🎯 Quick Start

### 1. Install Tools

```bash
# Run the optimizer wizard (creates .claudeignore / .geminiignore and installs tools)
python3 optimizer.py

# Or manually install
npm install -g @rtk-ai/rtk repomix
```

### 2. Create Ignore Files

```bash
# Create .claudeignore and .geminiignore with recommended defaults
cat > .claudeignore << 'EOF'
node_modules/
.venv/
vendor/
dist/
build/
.next/
__pycache__/
*.lock
*.min.js
*.map
coverage/
*.log
.env*
*.png
*.jpg
*.jpeg
*.gif
*.pdf
*.mp4
EOF
```

### 3. Start Using RTK

```bash
# RTK automatically intercepts your commands and compresses output
# No config needed—just install and use normally
git status         # Automatically optimized via rtk hook
npm test           # 60-90% token reduction
ls -la             # Compressed, AI-friendly output
```

### 4. Enable Prompt Caching (API Users)

For Anthropic API users, enable prompt caching in your requests:

```python
import anthropic

client = anthropic.Anthropic()

# Automatic caching: add cache_control at request level
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    extra_headers={"cache-control": "ephemeral"}  # Enable caching
)
```

---

## 🏗️ Architecture & Strategy

Token consumption flows through three layers:

```
┌─────────────────────────────────────────┐
│ LAYER 1: CLI & Context (Biggest Impact) │
│  • Ignore files (.claudeignore)         │
│  • Output compression (rtk, repomix)    │
│  • Selective file reading               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 2: Prompt & API (Medium Impact)   │
│  • Prompt caching (90% on repeats)      │
│  • Output optimization                  │
│  • Model selection (Sonnet vs Opus)     │
│  • Batch API (50% discount)             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 3: Advanced (Specialized)         │
│  • Extended thinking optimization       │
│  • Token compression algorithms         │
│  • Context window management            │
│  • Tool routing                         │
└─────────────────────────────────────────┘
```

---

## 🛠️ Core Tools & Installation

### RTK (Rust Token Killer) — ⭐ Highest Impact

**What:** A CLI proxy that intercepts shell commands and returns compressed, AI-friendly output.

**Impact:** 60-90% reduction on `git`, `npm`, `ls`, `grep`, `find`, and 100+ other commands.

**Installation:**
```bash
npm install -g @rtk-ai/rtk
# or via Homebrew:
brew install rtk-ai/tap/rtk
```

**Usage (Automatic):**
```bash
# Just use CLI normally—RTK hooks automatically compress output
git log                    # 70-90% smaller
npm test                   # 60-80% smaller
git status                 # 50-60% smaller
find . -type f -name "*.js" # 80%+ smaller
```

**How it Works:**
- Intercepts command execution via Claude Code/Cursor hooks
- Filters redundant lines, progress bars, and noise
- Returns structured, dense output optimized for LLM consumption
- <10ms overhead per command

**Supported Commands:** `git`, `npm`, `yarn`, `pnpm`, `ls`, `find`, `grep`, `cat`, `head`, `tail`, `diff`, `log`, `ps`, `curl`, `docker`, `kubectl`, `python`, and 100+ more.

### Repomix — Repository Compression

**What:** Packs your entire codebase into a single structured file (Markdown, XML, or JSON).

**Impact:** 70% reduction on repository context via Tree-sitter AST extraction.

**Installation:**
```bash
npm install -g repomix
```

**Usage:**
```bash
# Generate compressed repository snapshot
repomix --output repo.md

# With compression (removes function bodies, keeps signatures)
repomix --output repo.md --compress

# Output as JSON for processing
repomix --output repo.json --style json

# Filter to specific directories
repomix --include src,tests --output focused.md
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

**Best For:**
- Uploading to Claude Projects for persistent reference
- Initial code review or architecture understanding
- Reducing context when full repo isn't needed
- Sharing with AI assistants

### Files-to-Prompt — Selective Context Building

**What:** Converts files matching patterns into a prompt-friendly format.

**Installation:**
```bash
npm install -g files-to-prompt
# or via pip:
pip install files-to-prompt
```

**Usage:**
```bash
# Convert specific files
files-to-prompt src/**/*.js --output context.md

# Include line numbers
files-to-prompt src/ --include "*.js" --line-numbers

# For system prompts
files-to-prompt config/ --output config.txt
```

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
tokscale compare             # Compare models
```

---

## 📋 Layer 1: CLI & Context Optimization (Biggest Impact)

### 1.1 Ignore Files (.claudeignore / .geminiignore)

**Why:** Every file Claude reads consumes context, whether relevant or not. Smaller context = faster responses + better output + lower costs.

**Recommended .claudeignore / .geminiignore:**

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

# ========== Documentation (Rarely Needed) ==========
# Uncomment only if not actively editing docs
# docs/
# **/*.md

# ========== Analytics & Large Config ==========
.cache/
.parcel-cache/
.turbo/
dist-ssr/
coverage/
.nyc_output/
```

**Size Impact:**
- Average reduction: **40-70%** of context
- Example: Next.js project without `.claudeignore` = 15MB context, with = 3-5MB

### 1.2 RTK Command Output Compression

**Compression Strategies (RTK's 12 Core Filters):**

| Command | Without RTK | With RTK | Savings |
|---------|------------|----------|---------|
| `git log` | 50KB | 3KB | 94% |
| `npm test` | 100KB | 15KB | 85% |
| `git status` | 8KB | 1.5KB | 81% |
| `find . -type f` | 40KB | 2KB | 95% |
| `grep -r "foo"` | 60KB | 4KB | 93% |
| `ls -la /large/dir` | 35KB | 1.8KB | 95% |

**How RTK Filters Work:**
1. **Progress bars & spinners** → Removed entirely
2. **Repeated header/footer lines** → Deduplicated
3. **Whitespace normalization** → Collapsed empty lines
4. **ANSI color codes** → Stripped
5. **Truncated output** → Summarized counts
6. **Metadata filtering** → Remove timestamps, IDs (unless critical)
7. **Structured data** → Converted to JSON when applicable
8. **Line limiting** → Shows first N + last M lines with count
9. **Duplicate suppression** → Groups identical results
10. **Semantic summarization** → For verbose outputs (docker ps, ps aux)
11. **Table formatting** → Optimizes for readability + tokens
12. **Sort & deduplicate** → Tree structures simplified

### 1.3 Selective File Reading

**Instead of:**
```bash
# Reads entire 10MB file into context
read_file("package.json")
```

**Use:**
```bash
# Read only specific section
grep_search('dependencies' in package.json)

# Or use RTK with grep
rtk grep "name\|version\|main" package.json
```

**Token Savings:** 90% on large files with narrow queries.

---

## 💻 Layer 2: Prompt & API Optimization (Medium Impact)

### 2.1 Prompt Caching (90% Reduction on Repeats)

**What:** Cache system prompts and uploaded documents so repeated requests only pay 10% of cached token costs.

**Supported Models:** Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku, Claude 3.5 Haiku

**Implementation:**

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

# System prompt that will be cached
SYSTEM_PROMPT = """You are an expert code reviewer...
[long stable instructions]
"""

# Upload large documentation once
with open("docs.txt", "r") as f:
    docs = f.read()

# First request (creates cache)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}  # Cache for 5 min
        },
        {
            "type": "text",
            "text": f"Documentation:\n{docs}",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "Review this code: ..."}
    ]
)

# Subsequent requests hit cache (90% cheaper)
response2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": f"Documentation:\n{docs}",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "Review another code: ..."}
    ]
)
```

**Cache Pricing:**
- First request: Full price on cached content
- Subsequent hits (within 5 min): 10% of cached input token cost
- Cache duration options: 5 minutes (default) or 1 hour (at additional cost)
- Minimum cached tokens: 1024 per cache checkpoint

**Best Use Cases:**
- Conversational agents with long system instructions
- Uploading books, papers, or documentation
- Repeated code review tasks
- Multi-turn conversations with context

### 2.2 Output Optimization (40-70% Reduction)

**Key Insight:** Output tokens cost 5x more per token than input tokens. Optimizing output length is critical.

**Strategy:** Request structured output (JSON) instead of prose.

**Example:**

```python
# Verbose response (many tokens)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": "Extract key information from this document"
        }
    ]
)

# Optimized response (40-70% fewer tokens)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": """Extract key information and return as JSON:
{
  "title": "...",
  "author": "...",
  "key_points": ["...", "..."],
  "date": "YYYY-MM-DD"
}"""
        }
    ]
)
```

**Token Reduction Techniques:**
1. **Format constraints** → "Return as JSON with max 5 sentences"
2. **Stop sequences** → Stop at first `}` in JSON extraction
3. **Summarization prompts** → "List 3 key facts, one sentence each"
4. **Structured schemas** → Define exact output format
5. **Quantity limits** → "Max 10 results", "3-5 bullet points"

### 2.3 Model Selection (60% Cost Reduction)

**Rule:** Use Sonnet for 80%+ of work, Opus for complex tasks only.

| Task | Recommended | Reasoning |
|------|-------------|-----------|
| Code explanation | Sonnet | Fast, accurate, 60% cheaper |
| Writing tests | Sonnet | Straightforward generation |
| Simple edits | Sonnet | Handles replacements well |
| Architecture design | Opus | Complex decisions need depth |
| Multi-file refactor | Opus | Orchestrates large changes |
| Debugging complex issues | Opus | Deep analysis needed |
| Documentation | Sonnet | Straightforward writing |

**Cost Impact:** Sonnet is ~60% cheaper than Opus for equivalent quality on routine tasks.

### 2.4 Batch API (50% Cost Savings)

**What:** Submit up to 100,000 requests at once, process asynchronously within 24 hours, pay 50% price.

**Use Cases:**
- Document processing pipelines
- Code review batches
- Data classification
- Scheduled analysis tasks

**Implementation:**

```python
import anthropic
import json

client = anthropic.Anthropic(api_key="your-key")

# Prepare batch requests
requests = [
    {
        "custom_id": f"request-{i}",
        "params": {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": f"Process document {i}"}
            ]
        }
    }
    for i in range(100)
]

# Submit batch
batch = client.beta.messages.batches.create(
    requests=requests
)

print(f"Batch created: {batch.id}")

# Poll for results (or check later)
while True:
    batch_status = client.beta.messages.batches.retrieve(batch.id)
    if batch_status.processing_status == "ended":
        break
    print(f"Status: {batch_status.processing_status}")
    # Wait before polling again
    import time
    time.sleep(5)

# Get results
results = client.beta.messages.batches.results(batch.id)
for result in results:
    print(f"Request {result.custom_id}: {result.result.message.content}")
```

**Savings:** 50% off all input and output tokens vs. standard API.

---

## 🎓 Layer 3: Advanced Techniques (Specialized)

### 3.1 Extended Thinking Optimization

**What:** Extended thinking generates invisible reasoning tokens (billed at output rate) before producing final response.

**Cost Model:**
- Input tokens: Standard rate
- Thinking tokens: Output rate (5x more expensive)
- Output tokens: Output rate (5x more expensive)

**Strategy:** Use extended thinking only when necessary for complex reasoning.

```python
# Extended thinking (reserve for truly complex problems)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=8000,
    thinking={
        "type": "enabled",
        "budget_tokens": 5000  # Limit thinking to reduce cost
    },
    messages=[
        {"role": "user", "content": "Solve this complex architectural problem..."}
    ]
)
```

### 3.2 Token Compression Algorithms

**Advanced techniques for research/special cases:**

- **LLMLingua:** Leverages smaller LMs to rank and preserve key tokens in long contexts. Effective for RAG systems with 10-80% compression ratios.
- **Hard prompting:** Removes redundant tokens from natural language prompts using rule-based methods.
- **Semantic caching:** Cache similar queries (not just exact matches) via embeddings.
- **KV cache optimization:** Reduce visual tokens in multimodal models.

**Resource:** [A Survey of Token Compression for Efficient Multimodal LLMs](https://arxiv.org/html/2507.20198v5)

### 3.3 Tool Routing & Lazy Loading

**What:** Only pay for tools Claude actually uses.

**Implementation:**
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[
        # Define 100+ tools—only used ones are charged
        {"name": "search", "description": "...", "input_schema": {}},
        {"name": "execute", "description": "...", "input_schema": {}},
        # ...
    ],
    messages=[{"role": "user", "content": "..."}]
)
```

---

## 📊 Monitoring & Analytics

### Track Token Usage

```bash
# Using rtk
rtk gain              # Show token savings analytics
rtk gain --history    # Show command history with savings
rtk discover          # Analyze history for missed opportunities

# Using tokscale
tokscale report
tokscale report --history
```

### Expected Metrics

After implementing these strategies, track:

1. **Tokens per session** — Should drop 50-70%
2. **Cost per task** — Expected 60-80% reduction
3. **Response latency** — Should improve with smaller context
4. **Rate limit hits** — Should dramatically decrease

---

## 🚀 Implementation Roadmap

**Phase 1 (Day 1):** Quick Wins
- [ ] Create `.claudeignore` file
- [ ] Install rtk
- [ ] Start using RTK hook

**Phase 2 (Week 1):** Medium Wins
- [ ] Set up Batch API for scheduled tasks
- [ ] Enable prompt caching (if using API)
- [ ] Generate repomix snapshot for documentation

**Phase 3 (Week 2-4):** Long-term
- [ ] Audit all commands for optimization opportunities
- [ ] Implement token tracking (tokscale)
- [ ] Measure and document baseline improvements

---

## 📚 Resources & References

### Official Documentation
- [Best Practices for Claude Code - Claude Code Docs](https://code.claude.com/docs/en/best-practices)
- [Prompt caching - Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Prompting best practices - Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

### Token Optimization Guides
- [6 Ways I Cut My Claude Token Usage in Half!](https://www.sabrina.dev/p/6-ways-i-cut-my-claude-token-usage)
- [Stop Burning Tokens: A Developer's Guide to Claude AI Token Optimization](https://levelup.gitconnected.com/stop-burning-tokens-a-developers-guide-to-claude-ai-token-optimization-4c70c7c52ffb)
- [18 Claude Code Token Management Hacks](https://www.mindstudio.ai/blog/claude-code-token-management-hacks)
- [How to Save 90% on Claude API Costs: 3 Official Techniques](https://dev.to/stklen/how-to-save-90-on-claude-api-costs-3-official-techniques-3d4n)
- [How I Reduced LLM Token Costs by 90% Building AI Agents](https://medium.com/@ravityuval/how-i-reduced-llm-token-costs-by-90-using-prompt-rag-and-ai-agent-optimization-f64bd1b56d9f)

### Tools & Integration
- [RTK (Rust Token Killer) GitHub](https://github.com/rtk-ai/rtk)
- [Repomix - Repository Compression](https://github.com/yamadashy/repomix)
- [Files-to-Prompt - Selective Context Building](https://github.com/simonw/files-to-prompt)
- [RTK Saves 60% of Tokens. I Made It Save 90%.](https://dev.to/ji_ai/rtk-saves-60-of-tokens-i-made-it-save-90-3ib1)

### Advanced Resources
- [LLM Token Optimization: Cut Costs & Latency in 2026](https://redis.io/blog/llm-token-optimization-speed-up-apps/)
- [A Survey of Token Compression for Efficient Multimodal LLMs](https://arxiv.org/html/2507.20198v5)
- [Context Compression Techniques: Reduce LLM Costs by 50%](https://www.sitepoint.com/optimizing-token-usage-context-compression-techniques/)
- [Token Efficiency and Compression Techniques in LLMs](https://medium.com/@anicomanesh/token-efficiency-and-compression-techniques-in-large-language-models-navigating-context-length-05a61283412b)

### Community Insights
- [Claude Code Best Practices: 15 Tips from 6 Projects](https://aiorg.dev/blog/claude-code-best-practices)
- [50 Claude Code Tips and Best Practices For Daily Use](https://www.builder.io/blog/claude-code-tips-best-practices)
- [5 Patterns That Make Claude Code Actually Follow Your Rules](https://dev.to/docat0209/5-patterns-that-make-claude-code-actually-follow-your-rules-44dh)
- [Claude Code Efficiency Tricks](https://medium.com/@mehedipy/claude-code-efficiency-tricks-de09a72d9019)

---

## 💡 Pro Tips

1. **Combine strategies:** RTK + .claudeignore + prompt caching = 90%+ total reduction
2. **Start with RTK:** Highest ROI—install once, save on everything automatically
3. **Monitor savings:** Track with `rtk gain` to validate improvements
4. **Use Claude Projects:** Upload docs once, reference across unlimited conversations
5. **Batch expensive tasks:** Use Batch API for document processing, classification
6. **Audit regularly:** Use `rtk discover` to find new optimization opportunities

---

## 📝 Contributing

Suggestions? Spot an outdated tool? Open an issue or PR with:
- New tool/technique
- Benchmark improvements
- Better patterns

---

## 📄 License

MIT License — See LICENSE file for details

---

**Last Updated:** April 2026
**Maintained by:** Token Optimizer Contributors
