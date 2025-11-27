# YugNex Technology v1.0 - Complete Blueprint

**Document Version:** 1.0  
**Date:** November 26, 2025  
**Status:** Ready for Development  
**Timeline:** 2-3 weeks (with AI assistance)

---

## Part 1: The Vision

### What is YugNex?

> **YugNex is an AI software company - not a chatbot, but a team of specialized AI agents that operates like a real development agency.**

### The Problem We Solve:

| Current AI Pain | YugNex Solution |
|-----------------|-----------------|
| AI gives buggy code, breaks other things | Agents review each other's work before delivery |
| AI forgets everything when chat ends | Persistent memory - never forgets |
| AI says "yes" to everything (sugar-coated lies) | Honest assessment - "this takes 2 weeks, here's why" |
| Switching between AIs = start over | One system, consistent context |
| AI doesn't act like real developers | Team collaboration, proper handoffs |

### The Full Vision (v1 → v5):

| Version | Focus | Key Features |
|---------|-------|--------------|
| **v1** | Foundation | Chat + Agent modes, 5 core agents, memory, web app |
| **v2** | Execution | Browser automation, terminal, auto-deploy |
| **v3** | Full Company | Social media, email, more specialists |
| **v4** | Personal AI | Jarvis mode, calendar, daily assistant |
| **v5** | Commercial | Multi-user, billing, public launch |

### Primary Use:

- **First:** In-house use for your agency (serve clients faster)
- **Future:** Commercial product for market

---

## Part 2: v1 Scope

### What v1 INCLUDES:

| Feature | Description |
|---------|-------------|
| **2 Modes** | Chat Mode (quick Q&A) + Agent Mode (collaboration) |
| **5 Agents** | Tilotma, Advait, Saanvi, Shubham, Navya |
| **Memory System** | Projects, conversations, preferences - persistent |
| **Web App** | Responsive (works on laptop + mobile) |
| **AI Integration** | Claude (primary) + Gemini (fallback) |
| **Project System** | Create, manage, switch between projects |
| **Honest AI** | Realistic estimates, says "I don't know" when appropriate |

### What v1 EXCLUDES (Save for v2+):

| Feature | Version |
|---------|---------|
| Browser automation | v2 |
| Terminal execution | v2 |
| Auto-deploy | v2 |
| Social media management | v3 |
| Email handling | v3 |
| Jarvis/personal assistant | v4 |
| IDE integration | v3 |
| Multi-user / billing | v5 |

---

## Part 3: Architecture

### The 4 Pillars:

```
┌─────────────────────────────────────────────────────────────────┐
│                         YUGNEX v1                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │   PILLAR 1  │  │   PILLAR 2  │  │   PILLAR 3  │            │
│   │   MEMORY    │  │    BRAIN    │  │   AGENTS    │            │
│   │   SYSTEM    │  │  (Tilotma)  │  │   (Team)    │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
│   ┌─────────────────────────────────────────────────┐          │
│   │                   PILLAR 4                       │          │
│   │            INTERFACE (Web App)                   │          │
│   └─────────────────────────────────────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Hierarchy:

```
                    ┌─────────────┐
                    │    USER     │
                    │   (CEO)     │
                    └──────┬──────┘
                           │
                           │ Direct line
                           ▼
                    ┌─────────────┐
                    │  TILOTMA    │
                    │ Chief AI    │
                    │  Officer    │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │  ADVAIT   │   │  SAANVI   │   │   NAVYA   │
    │ Tech Lead │   │ Analyst   │   │ Reviewer  │
    └─────┬─────┘   └───────────┘   └───────────┘
          │
          ▼
    ┌───────────┐
    │  SHUBHAM  │
    │ Developer │
    └───────────┘
```

---

## Part 4: Folder Structure

```
yugnex/
│
├── backend/
│   │
│   ├── core/                       # Pillar 2: The Brain
│   │   ├── __init__.py
│   │   ├── tilotma.py             # Chief AI Officer - central command
│   │   ├── mode_handler.py        # Chat vs Agent mode detection
│   │   ├── task_analyzer.py       # Understands what user wants
│   │   └── model_manager.py       # Claude/Gemini switching
│   │
│   ├── memory/                     # Pillar 1: Memory System
│   │   ├── __init__.py
│   │   ├── persistent.py          # Never-forget storage
│   │   ├── project_memory.py      # Project-specific context
│   │   ├── conversation.py        # Chat history
│   │   └── user_preferences.py    # User settings & preferences
│   │
│   ├── agents/                     # Pillar 3: Agent Framework
│   │   ├── __init__.py
│   │   ├── base.py                # Base agent class
│   │   ├── registry.py            # Loads & manages all agents
│   │   ├── leadership.py          # Tilotma, Advait
│   │   ├── analysts.py            # Saanvi (+ Dhruv, Ananya in v2)
│   │   ├── developers.py          # Shubham (+ Myra, Riaan in v2)
│   │   ├── reviewers.py           # Navya (+ Tanish, Daksh in v2)
│   │   └── collaboration/
│   │       ├── __init__.py
│   │       ├── handoff.py         # Agent-to-agent task passing
│   │       └── workflow.py        # Task pipelines
│   │
│   ├── api/                        # REST API
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app entry
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py            # Chat endpoints
│   │   │   ├── projects.py        # Project management
│   │   │   ├── agents.py          # Agent status & control
│   │   │   └── auth.py            # Authentication
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── auth_middleware.py # JWT validation
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── chat.py            # Request/Response models
│   │       ├── project.py
│   │       └── user.py
│   │
│   ├── database/                   # Data Layer
│   │   ├── __init__.py
│   │   ├── connection.py          # DB connection
│   │   ├── models.py              # SQLAlchemy models
│   │   └── migrations/            # Alembic migrations
│   │
│   ├── services/                   # Business Logic
│   │   ├── __init__.py
│   │   ├── ai_router.py           # Claude/Gemini integration
│   │   ├── auth_service.py        # Auth logic
│   │   └── project_service.py     # Project logic
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Environment config
│   │   └── prompts/               # Agent system prompts
│   │       ├── tilotma.txt
│   │       ├── advait.txt
│   │       ├── saanvi.txt
│   │       ├── shubham.txt
│   │       └── navya.txt
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_agents.py
│   │   ├── test_memory.py
│   │   └── test_api.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── MessageBubble.tsx
│   │   │   │   ├── TypingIndicator.tsx
│   │   │   │   └── AgentBadge.tsx
│   │   │   ├── Projects/
│   │   │   │   ├── ProjectList.tsx
│   │   │   │   └── ProjectCard.tsx
│   │   │   ├── Agents/
│   │   │   │   ├── AgentStatus.tsx
│   │   │   │   └── AgentSelector.tsx
│   │   │   ├── Layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── MainLayout.tsx
│   │   │   └── Common/
│   │   │       ├── Button.tsx
│   │   │       ├── Input.tsx
│   │   │       ├── Modal.tsx
│   │   │       └── Loading.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Chat.tsx
│   │   │   ├── Projects.tsx
│   │   │   ├── Login.tsx
│   │   │   └── Settings.tsx
│   │   │
│   │   ├── store/
│   │   │   ├── useStore.ts        # Zustand store
│   │   │   ├── chatSlice.ts
│   │   │   ├── projectSlice.ts
│   │   │   └── userSlice.ts
│   │   │
│   │   ├── services/
│   │   │   └── api.ts             # API client
│   │   │
│   │   ├── hooks/
│   │   │   ├── useChat.ts
│   │   │   ├── useProjects.ts
│   │   │   └── useAuth.ts
│   │   │
│   │   ├── types/
│   │   │   └── index.ts           # TypeScript types
│   │   │
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

**Total: ~50 files (organized, purposeful, extensible)**

---

## Part 5: Database Schema

### Tables:

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    role VARCHAR(50) DEFAULT 'user',  -- 'user', 'admin'
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    tech_stack VARCHAR(100),          -- 'python', 'react', 'flutter', etc.
    status VARCHAR(50) DEFAULT 'active',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Conversations (Chat History)
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200),
    mode VARCHAR(50) DEFAULT 'chat',  -- 'chat', 'agent'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL,        -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    agent_key VARCHAR(50),            -- Which agent responded
    model_used VARCHAR(50),           -- 'claude-sonnet-4.5', etc.
    tokens_used INTEGER,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Project Memory (Persistent Context)
CREATE TABLE project_memory (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    memory_type VARCHAR(50),          -- 'requirement', 'decision', 'code', 'note'
    content TEXT NOT NULL,
    importance INTEGER DEFAULT 5,     -- 1-10 scale
    embedding VECTOR(1536),           -- For semantic search (optional v1)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Agent Activity Log
CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    agent_key VARCHAR(50) NOT NULL,
    action VARCHAR(100),              -- 'started', 'completed', 'handoff', 'error'
    input_summary TEXT,
    output_summary TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Key Relationships:

```
User (1) ──────< (Many) Projects
Project (1) ────< (Many) Conversations
Conversation (1) < (Many) Messages
Project (1) ────< (Many) Project Memory
Conversation (1) < (Many) Agent Logs
```

---

## Part 6: v1 Agents Specification

### Agent 1: Tilotma (Chief AI Officer)

| Property | Value |
|----------|-------|
| **Key** | `tilotma` |
| **Role** | Chief AI Officer - Central Command |
| **Reports To** | User (CEO) |
| **Manages** | Advait, Saanvi, Navya |

**Responsibilities:**
- Receives all user commands
- Understands intent and context
- Delegates tasks to appropriate agents
- Monitors progress across team
- Reports summaries to user
- Makes decisions when agents disagree
- Holds full project context

**System Prompt (core):**
```
You are Tilotma, the Chief AI Officer at YugNex Technology.

YOUR ROLE:
- You are the user's direct contact. All requests come through you.
- You understand what the user needs and delegate to your team.
- You never lie or sugar-coat. If something takes 2 weeks, say 2 weeks.
- You ask clarifying questions before starting complex work.

YOUR TEAM:
- Advait (Tech Lead): Manages technical decisions
- Saanvi (Analyst): Gathers and clarifies requirements
- Shubham (Developer): Writes code
- Navya (Reviewer): Reviews code quality

HOW YOU WORK:
1. Receive user request
2. Analyze: Is this a quick question (chat) or a task (agent mode)?
3. For tasks: Delegate to appropriate team member(s)
4. Monitor progress, coordinate handoffs
5. Report results to user

CRITICAL RULES:
- Never guess. If unsure, ask.
- Never promise what team can't deliver.
- Always summarize what you understood before starting work.
- If user is frustrated, acknowledge and clarify.
```

---

### Agent 2: Advait (Tech Lead)

| Property | Value |
|----------|-------|
| **Key** | `advait` |
| **Role** | Tech Lead - Technical Decisions |
| **Reports To** | Tilotma |
| **Manages** | Shubham |

**Responsibilities:**
- Makes architecture decisions
- Reviews technical feasibility
- Guides development approach
- Resolves technical conflicts

**System Prompt (core):**
```
You are Advait, the Tech Lead at YugNex Technology.

YOUR ROLE:
- You make technical architecture decisions
- You ensure code quality and best practices
- You guide Shubham (Developer) on implementation

HOW YOU WORK:
1. Receive technical task from Tilotma
2. Analyze feasibility and approach
3. If complex: Break down into subtasks
4. Assign to Shubham with clear specifications
5. Review output before passing back

CRITICAL RULES:
- Be specific about requirements. No vague instructions.
- Consider scalability, security, maintainability.
- If something is technically risky, flag it.
```

---

### Agent 3: Saanvi (Product Analyst)

| Property | Value |
|----------|-------|
| **Key** | `saanvi` |
| **Role** | Product Analyst - Requirements |
| **Reports To** | Tilotma |

**Responsibilities:**
- Gathers requirements from vague requests
- Asks clarifying questions
- Creates clear specifications
- Identifies edge cases

**System Prompt (core):**
```
You are Saanvi, the Product Analyst at YugNex Technology.

YOUR ROLE:
- You transform vague requests into clear requirements
- You ask the RIGHT questions to understand what user really needs
- You think about edge cases and potential issues

HOW YOU WORK:
1. Receive request from Tilotma
2. Analyze: What is clear? What is ambiguous?
3. Ask 2-4 targeted clarifying questions (not 10)
4. Create clear requirements document
5. Pass to Advait/Shubham for implementation

CRITICAL RULES:
- Never assume. If unclear, ask.
- Ask questions in order of importance.
- Think about: Who uses this? What can go wrong?
```

---

### Agent 4: Shubham (Developer)

| Property | Value |
|----------|-------|
| **Key** | `shubham` |
| **Role** | Senior Developer - Code Implementation |
| **Reports To** | Advait |

**Responsibilities:**
- Writes clean, working code
- Follows specifications from Advait
- Implements best practices
- Self-reviews before submitting

**System Prompt (core):**
```
You are Shubham, a Senior Developer at YugNex Technology.

YOUR ROLE:
- You write production-quality code
- You follow specifications from Advait exactly
- You write code that is clean, readable, maintainable

HOW YOU WORK:
1. Receive specification from Advait
2. Plan implementation approach
3. Write code following best practices
4. Self-review: Does it meet requirements?
5. Pass to Navya for review

CRITICAL RULES:
- Write complete code, not snippets with "// TODO"
- Include error handling
- Add comments for complex logic
- If spec is unclear, ask Advait (don't guess)
```

---

### Agent 5: Navya (Code Reviewer)

| Property | Value |
|----------|-------|
| **Key** | `navya` |
| **Role** | Code Reviewer - Quality Gate |
| **Reports To** | Tilotma |

**Responsibilities:**
- Reviews code for bugs, security, quality
- Provides constructive feedback
- Approves or requests changes
- Final quality gate before delivery

**System Prompt (core):**
```
You are Navya, the Code Reviewer at YugNex Technology.

YOUR ROLE:
- You are the quality gate. No code reaches user without your review.
- You check for bugs, security issues, best practices
- You provide clear, actionable feedback

HOW YOU WORK:
1. Receive code from Shubham
2. Review for:
   - Correctness: Does it work?
   - Security: Any vulnerabilities?
   - Quality: Clean, readable, maintainable?
   - Edge cases: What could break?
3. Decision: APPROVE or REQUEST CHANGES
4. If approved: Pass to Tilotma for delivery
5. If changes needed: Send back to Shubham with specific feedback

CRITICAL RULES:
- Be constructive, not harsh
- Be specific: "Line 45: SQL injection risk" not "has issues"
- Don't nitpick style if logic is sound
```

---

## Part 7: API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create new account |
| POST | `/api/auth/login` | Login, get JWT |
| POST | `/api/auth/refresh` | Refresh token |
| GET | `/api/auth/me` | Get current user |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | List user's projects |
| POST | `/api/projects` | Create project |
| GET | `/api/projects/:id` | Get project details |
| PUT | `/api/projects/:id` | Update project |
| DELETE | `/api/projects/:id` | Delete project |

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/:id/conversations` | List conversations |
| POST | `/api/projects/:id/conversations` | Start new conversation |
| GET | `/api/conversations/:id/messages` | Get messages |
| POST | `/api/conversations/:id/messages` | Send message |
| POST | `/api/conversations/:id/stream` | Send message (SSE streaming) |

### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents` | List all agents |
| GET | `/api/agents/:key/status` | Get agent status |

---

## Part 8: Frontend Pages

### Page 1: Dashboard
- Welcome message
- Recent projects list
- Quick stats (conversations, agents used)
- "New Project" button

### Page 2: Chat (Main Interface)
- Left sidebar: Project list, conversation history
- Center: Chat interface
- Right panel (optional): Agent activity, artifacts
- Mode toggle: Chat / Agent
- Input area with send button

### Page 3: Projects
- Project cards with stats
- Create new project
- Project settings

### Page 4: Settings
- User preferences
- Default AI model
- Notification settings

### Page 5: Login/Register
- Simple auth forms

---

## Part 9: Development Strategy & Rules

### CRITICAL DEVELOPMENT RULES:

| Rule | Why |
|------|-----|
| **Backend first, UI later** | Get agents working before building UI. Test via API first. |
| **Test each agent INDIVIDUALLY** | Make sure Tilotma works alone before adding other agents |
| **Build memory system EARLY** | This prevents "forgetting" problem. Do it on Day 3, not later. |
| **Add confidence scores** | Every agent response includes: "I'm 90% sure" or "I'm unsure, please confirm" |
| **Log EVERYTHING** | Every agent action saved to database - helps debug issues |
| **No hallucination** | If agent is unsure, it ASKS instead of guessing |
| **Validate before proceeding** | Agent confirms understanding before starting work |

### Agent Behavior Rules (Built into base.py):

```python
# Every agent MUST follow these rules:

class AgentBehavior:
    RULES = {
        "no_hallucination": "If unsure, ask. Never make up information.",
        "confirm_understanding": "Before starting, confirm: 'You want me to [X], correct?'",
        "honest_estimates": "If task takes 2 weeks, say 2 weeks. No sugar-coating.",
        "ask_clarification": "When request is vague, ask 1-2 specific questions.",
        "admit_mistakes": "If wrong, say 'I made an error, let me fix it.'",
        "confidence_score": "Include confidence: 'I'm [X]% confident about this.'",
    }
```

### Test Conversations (Create These):

Before v1 is "done", test these 10 scenarios:

| # | Test Scenario | Expected Behavior |
|---|---------------|-------------------|
| 1 | "Hi" | Tilotma greets, asks how to help |
| 2 | "Build me an app" (vague) | Saanvi asks clarifying questions |
| 3 | "Create login API in Python" | Shubham writes code, Navya reviews |
| 4 | "What's 2+2?" (simple) | Chat mode, quick answer |
| 5 | "Build WhatsApp clone" (unrealistic) | Honest response about complexity |
| 6 | "Continue our previous project" (no context) | Asks which project, doesn't assume |
| 7 | Complex multi-file task | Agents collaborate with handoffs |
| 8 | User gives wrong info | Agent asks for clarification |
| 9 | User changes requirement mid-way | Agent confirms new direction |
| 10 | "I don't like this code" | Navya asks what to change specifically |

---

## Part 10: Development Phases

### Phase 1: Foundation (Days 1-4)

| Day | Tasks | Validation |
|-----|-------|------------|
| 1 | Database setup, models, migrations | ✓ Can create tables |
| 1 | Backend project structure | ✓ Folder structure matches blueprint |
| 2 | Auth service (register, login, JWT) | ✓ Can register & login via API |
| 2 | Basic API routes (auth, health check) | ✓ Health endpoint returns OK |
| 3 | Memory system (persistent.py, project_memory.py) | ✓ Data persists after restart |
| 4 | AI router (Claude + Gemini integration) | ✓ Both models respond correctly |

**Day 4 Checkpoint:** Can call Claude and Gemini, data saves to DB, auth works.

### Phase 2: Agents (Days 5-8)

| Day | Tasks | Validation |
|-----|-------|------------|
| 5 | base.py - Agent base class with behavior rules | ✓ Base class includes all rules |
| 5 | Tilotma - core logic (TEST ALONE FIRST) | ✓ Tilotma responds correctly |
| 6 | Advait, Saanvi agents (test individually) | ✓ Each agent works alone |
| 7 | Shubham, Navya agents (test individually) | ✓ Each agent works alone |
| 8 | Collaboration - handoff.py, workflow.py | ✓ Agents pass context correctly |

**Day 8 Checkpoint:** All 5 agents work individually AND together. Handoffs work.

### Phase 3: API (Days 9-11)

| Day | Tasks | Validation |
|-----|-------|------------|
| 9 | Project endpoints | ✓ CRUD projects via API |
| 10 | Chat endpoints + streaming | ✓ Messages stream in real-time |
| 11 | Agent endpoints, integration testing | ✓ Can see agent status via API |

**Day 11 Checkpoint:** Full API working. Test all 10 scenarios via API (no UI yet).

### Phase 4: Frontend (Days 12-16)

| Day | Tasks | Validation |
|-----|-------|------------|
| 12 | Project setup, routing, layout | ✓ App loads, routes work |
| 13 | Auth pages (login, register) | ✓ Can login via UI |
| 14 | Dashboard, project list | ✓ Projects display |
| 15 | Chat interface | ✓ Can send messages, see responses |
| 16 | Agent status, polish | ✓ See which agent is working |

**Day 16 Checkpoint:** UI connected to backend. Can do full flow via browser.

### Phase 5: Integration & Testing (Days 17-20)

| Day | Tasks | Validation |
|-----|-------|------------|
| 17 | Connect frontend to backend | ✓ No API errors |
| 18 | End-to-end testing (all 10 scenarios) | ✓ All scenarios pass |
| 19 | Bug fixes, edge cases | ✓ No critical bugs |
| 20 | Final polish, documentation | ✓ README complete |

**Day 20 Checkpoint:** v1 DONE. All success criteria met.

---

## Part 11: AI Model Usage (IMPORTANT)

### Claude and Gemini are EQUAL PARTNERS (Not Fallback)

| Task Type | Use This Model | Why |
|-----------|----------------|-----|
| Complex reasoning | Claude | Better at deep analysis |
| Architecture decisions | Claude | Stronger logical thinking |
| Code review | Claude | Catches more issues |
| Fast responses | Gemini | Faster response time |
| Simple Q&A | Gemini | Quick and efficient |
| Code generation | Either | Both are capable |
| Bulk processing | Gemini | Higher rate limits |

### How Model Selection Works:

```python
# In model_manager.py

def select_model(task_type: str, complexity: str) -> str:
    """
    Auto-select best model for task.
    User can override by specifying model.
    """
    
    # Complex tasks → Claude
    if complexity == "high" or task_type in ["architecture", "review", "analysis"]:
        return "claude"
    
    # Simple/fast tasks → Gemini
    if complexity == "low" or task_type in ["quick_answer", "simple_code"]:
        return "gemini"
    
    # Default for medium complexity
    return "claude"  # Prefer Claude for safety
```

### Rate Limit Handling:

- If Claude hits rate limit → Switch to Gemini temporarily
- If Gemini hits rate limit → Switch to Claude temporarily
- Log all switches for monitoring
- Notify user if both models unavailable

---

## Part 12: Tech Stack (Final)

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **AI:** LangChain + Anthropic SDK + Google Vertex AI
- **Auth:** JWT (python-jose)
- **Async:** Uvicorn

### Frontend
- **Language:** TypeScript
- **Framework:** React 18
- **Build:** Vite
- **Styling:** Tailwind CSS
- **State:** Zustand
- **HTTP:** Axios
- **Routing:** React Router

### Infrastructure
- **Deployment:** GCP (Cloud Run or GKE)
- **Database:** Cloud SQL (PostgreSQL)
- **Container:** Docker
- **CI/CD:** GitHub Actions (later)

---

## Part 13: Success Criteria for v1

### v1 is DONE when:

- [ ] User can register and login
- [ ] User can create projects
- [ ] User can chat with Tilotma
- [ ] Tilotma delegates to other agents correctly
- [ ] Agents pass context to each other
- [ ] Code goes through Navya review before delivery
- [ ] Memory persists across sessions
- [ ] Works on desktop and mobile browser
- [ ] Claude and Gemini both work with auto-fallback
- [ ] Honest responses (no "sure, I can build WhatsApp in 1 hour")

---

## Part 14: What NOT to Build in v1

Explicitly out of scope:

- ❌ Browser automation (v2)
- ❌ Terminal execution (v2)
- ❌ Auto-deployment (v2)
- ❌ Social media management (v3)
- ❌ Email handling (v3)
- ❌ More than 5 agents
- ❌ Voice input/output
- ❌ IDE integration
- ❌ Multi-user teams
- ❌ Billing/payments

---

## Ready to Build

This blueprint contains everything needed to start v1 development.

**Next steps:**
1. Create new project (clean)
2. Upload this blueprint to project knowledge
3. Start with Phase 1, Day 1

---

**Built with clarity. Built to last. Built to extend.**

*YugNex Technology v1.0*
