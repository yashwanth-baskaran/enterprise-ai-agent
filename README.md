# enterprise-ai-agent

> A natural language interface layer for enterprise business systems.  
> You describe what you want. The agent figures out how to do it. Deterministic tools execute it reliably.

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yashwanth-baskaran/enterprise-ai-agent.git
cd enterprise-ai-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your credentials
cp .env.example .env
# Open .env and fill in your business system details

# 4. Test your connection
python tools/connect.py
```

**Using with Claude:**
- Go to [claude.ai](https://claude.ai) → Create a Project
- Upload `CLAUDE.md` as the project instruction
- Start giving instructions in plain English:

> *"Show me all open opportunities created this month"*  
> *"Which salesperson has the most deals stuck in the first stage?"*  
> *"Build a report showing email performance by send time"*

The agent reads the workflow, calls the right tool, and delivers the result.

---

## The problem this solves

Most attempts at AI-powered business automation fail the same way: they let the AI handle both the *reasoning* and the *execution*. When each step is 90% accurate, five steps gives you 59% success. That's not automation — that's gambling.

This framework solves that by separating concerns:

- **AI handles reasoning** — interpreting intent, choosing the right workflow, deciding on inputs, recovering from ambiguity
- **Deterministic scripts handle execution** — API calls, data transformations, file operations, database queries

The result is a system where complex, multi-step business tasks can be triggered by a plain English instruction and run reliably — without hallucination risk.

---

## Architecture: WAT (Workflows · Agents · Tools)

```
You (plain English instruction)
        │
        ▼
┌───────────────────┐
│   Layer 1         │  WORKFLOWS  — Markdown SOPs in workflows/
│   The Instructions│  Define: objective, inputs, which tools,
│                   │  expected outputs, edge case handling
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   Layer 2         │  AGENT  — Claude (or any capable LLM)
│   The Coordinator │  Reads workflows, sequences tool calls,
│                   │  handles failures, asks when unclear
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   Layer 3         │  TOOLS  — Python scripts in tools/
│   The Executor    │  Deterministic. Testable. Fast.
│                   │  Credentials in .env only
└───────────────────┘
         │
         ▼
Business System API (ERP, CRM, Marketing platform, etc.)
```

**Why this matters:** The agent never calls APIs directly — it calls scripts that call APIs. Scripts are testable, versionable, and predictable. The AI stays in its lane.

---

## What was built with this

This framework was used to build two production modules on a live ERP deployment:

| Module | What it does |
|--------|-------------|
| [crm-live-dashboard](../crm-live-dashboard) | Real-time sales pipeline dashboard — live ORM polling, Chart.js visualisations, team performance breakdown, clickable funnel |
| [adv-marketing-reports](../adv-marketing-reports) | 15 SQL-backed read-only analytics views — campaign rankings, engagement scoring, list health, send-time analysis, A/B test results |

Both were built by giving the agent plain English instructions. The agent read the relevant workflow, called the right tools, and produced working code — iterating on failures until the output was correct.

---

## Repository structure

```
enterprise-ai-agent/
├── workflows/              # Markdown SOPs — one file per task type
│   ├── create_module.md    # How to scaffold a new ERP module
│   ├── query_data.md       # How to read from the business system
│   ├── update_records.md   # How to write/update records safely
│   └── generate_report.md  # How to build a report or dashboard
│
├── tools/                  # Python scripts — deterministic execution
│   ├── connect.py          # Establish and test API connection
│   ├── read_records.py     # Read/search/filter records
│   ├── write_records.py    # Create/update records
│   └── run_query.py        # Execute raw queries safely
│
├── .env.example            # Required environment variables (copy to .env)
├── .gitignore              # Excludes .env, credentials, tmp files
├── CLAUDE.md               # Agent instructions — loaded at session start
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## How to use this

### 1. Clone and configure

```bash
git clone https://github.com/YOUR_USERNAME/enterprise-ai-agent.git
cd enterprise-ai-agent
cp .env.example .env
# Fill in your business system credentials in .env
pip install -r requirements.txt
```

### 2. Point your agent at CLAUDE.md

If using Claude via the API or Claude.ai Projects, load `CLAUDE.md` as your system prompt or project instruction. It tells the agent how to operate — read workflows first, call tools for execution, update workflows when things break.

### 3. Give it a task

```
"Find all open opportunities created this month and export a summary to Google Sheets"
"Build a report showing email campaign performance by send time"
"Show me which salesperson has the most deals stuck in the first stage"
```

The agent reads the relevant workflow, identifies the required tools, executes them in sequence, and delivers the output.

### 4. Extend it

To add a new capability:
1. Write a workflow in `workflows/` describing what to do and how
2. Write a tool in `tools/` that handles the deterministic part
3. Test the tool standalone first — it should work without the agent
4. Add the workflow to your agent's context

---

## Adapting to your business system

The framework is API-agnostic. The reference implementation uses a JSON-RPC ERP API. To point it at a different system:

1. Update `tools/connect.py` with your system's auth method
2. Update `tools/read_records.py` and `tools/write_records.py` with your API's read/write pattern
3. Update `.env.example` with the required credentials for your system
4. Workflows stay the same — they describe *intent*, not implementation

Any system with a REST or RPC API works: Salesforce, SAP, HubSpot, NetSuite, Dynamics, custom backends.

---

## Environment variables

Copy `.env.example` to `.env` and fill in your values:

```
BUSINESS_SYSTEM_URL=https://your-instance.example.com
BUSINESS_SYSTEM_DB=your_database
BUSINESS_SYSTEM_USER=your@email.com
BUSINESS_SYSTEM_API_KEY=your_api_key
```

**Never commit `.env`.** It is in `.gitignore`. Use `.env.example` for documentation.

---

## The self-improvement loop

This system gets better over time through a deliberate loop:

1. Agent hits an error
2. Agent reads the full trace, fixes the tool
3. Agent verifies the fix works
4. Agent updates the workflow with what it learned
5. Next run uses the improved approach

Rate limits, API quirks, edge cases — everything gets documented in the workflow so it never breaks the same way twice.

---

## Tech stack

- **Agent**: Claude (claude-sonnet or equivalent capable LLM)
- **Tools**: Python 3.10+
- **Credentials**: python-dotenv
- **API pattern**: JSON-RPC / REST (adaptable)

---

## License

MIT — use it, adapt it, build on it.
