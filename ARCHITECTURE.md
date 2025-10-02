# Agentice - Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACES                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Web App    │  │  Mobile App  │  │     CLI      │  │   Email    │ │
│  │  (Next.js)   │  │  (React N.)  │  │   Commands   │  │  Triggers  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘ │
└─────────┼──────────────────┼──────────────────┼─────────────────┼────────┘
          │                  │                  │                 │
          └──────────────────┴──────────────────┴─────────────────┘
                                     │
                   ┌─────────────────▼──────────────────┐
                   │    API Gateway (FastAPI)           │
                   │  • Authentication (JWT/OAuth2)     │
                   │  • Rate Limiting                   │
                   │  • Request Validation              │
                   │  • Logging & Monitoring            │
                   └─────────────┬──────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐    ┌──────────────────────┐    ┌──────────────┐
│   REST API    │    │  AutoGen Multi-Agent │    │  Background  │
│   Endpoints   │◄───┤      System          │───►│   Tasks      │
│               │    │  ┌────────────────┐  │    │  (Celery)    │
│ • Jobs        │    │  │ JobResearcher  │  │    │              │
│ • Resumes     │    │  │ ResumeOptimizer│  │    │ • Daily Job  │
│ • Tasks       │    │  │ CoverLetterGen │  │    │   Search     │
│ • Profiles    │    │  │ AppManager     │  │    │ • Email      │
│ • Content     │    │  │ ProfileUpdater │  │    │   Processing │
└───────┬───────┘    │  │ ContentCreator │  │    │ • Reminders  │
        │            │  │ Orchestrator   │  │    └──────┬───────┘
        │            │  └────────────────┘  │           │
        │            └──────────┬───────────┘           │
        │                       │                       │
        └───────────────────────┴───────────────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Services   │    │  LLM Layer  │    │  Database   │
    │              │    │             │    │             │
    │ • JobScraper │    │ • OpenAI    │    │ • Postgres  │
    │ • Resume     │    │ • Anthropic │    │ • pgvector  │
    │ • Application│    │ • Azure     │    │ • Redis     │
    │ • Email      │    │ • Ollama    │    │             │
    │ • Calendar   │    │             │    │ • Vector    │
    │ • Notify     │    │ • Guardrails│    │   Store     │
    └──────┬───────┘    └──────┬──────┘    └──────┬──────┘
           │                   │                   │
           └───────────────────┴───────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐     ┌────────────────┐     ┌──────────────┐
│ External APIs │     │  Job Boards    │     │  User Data   │
│               │     │                │     │              │
│ • Gmail API   │     │ • Indeed       │     │ • Profiles   │
│ • Calendar    │     │ • LinkedIn     │     │ • Resumes    │
│ • GitHub API  │     │ • Glassdoor    │     │ • History    │
│ • LinkedIn    │     │ • RemoteOK     │     │ • Prefs      │
└───────────────┘     └────────────────┘     └──────────────┘
```

## Autonomous Job Application Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    DAILY JOB SEARCH TRIGGER                      │
│              (Celery Beat - Scheduled @ 9:00 AM)                 │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │  1. Fetch User Preferences  │
         │  • Keywords                 │
         │  • Location                 │
         │  • Salary Range             │
         │  • Max Applications/Day     │
         └─────────────┬───────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │  2. JobResearcher Agent     │
         │  ┌─────────────────────┐    │
         │  │ Search Job Boards   │    │
         │  │ • Indeed            │    │
         │  │ • LinkedIn          │    │
         │  │ • Glassdoor         │    │
         │  └─────────┬───────────┘    │
         │            │                │
         │  ┌─────────▼───────────┐    │
         │  │ Extract Requirements│    │
         │  │ • Skills            │    │
         │  │ • Experience        │    │
         │  │ • Education         │    │
         │  └─────────┬───────────┘    │
         │            │                │
         │  ┌─────────▼───────────┐    │
         │  │ Calculate Fit Score │    │
         │  │ • Skill Match: 0.8  │    │
         │  │ • Exp Match: 0.9    │    │
         │  │ • Location: 1.0     │    │
         │  └─────────┬───────────┘    │
         └────────────┬────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  3. Rank & Filter          │
         │  Top 10 Opportunities      │
         │  Sorted by Fit Score       │
         └────────────┬───────────────┘
                      │
       ┌──────────────┴──────────────┐
       │  FOR EACH OPPORTUNITY       │
       └──────────────┬──────────────┘
                      │
      ┌───────────────▼───────────────┐
      │  4. ResumeOptimizer Agent     │
      │  ┌─────────────────────┐      │
      │  │ Analyze JD          │      │
      │  │ • Key Requirements  │      │
      │  │ • Keywords          │      │
      │  └─────────┬───────────┘      │
      │            │                  │
      │  ┌─────────▼───────────┐      │
      │  │ Customize Resume    │      │
      │  │ • Reorder Skills    │      │
      │  │ • Rewrite Bullets   │      │
      │  │ • Add Keywords      │      │
      │  └─────────┬───────────┘      │
      │            │                  │
      │  ┌─────────▼───────────┐      │
      │  │ ATS Optimization    │      │
      │  │ • Format Check      │      │
      │  │ • Keyword Density   │      │
      │  │ • Readability       │      │
      │  └─────────┬───────────┘      │
      └────────────┬──────────────────┘
                   │
                   ▼
      ┌────────────────────────────┐
      │  5. CoverLetterWriter      │
      │  ┌─────────────────────┐   │
      │  │ Research Company    │   │
      │  │ • Culture          │   │
      │  │ • Recent News      │   │
      │  └─────────┬───────────┘   │
      │            │               │
      │  ┌─────────▼───────────┐   │
      │  │ Generate Letter     │   │
      │  │ • Hook             │   │
      │  │ • Match Skills     │   │
      │  │ • Enthusiasm       │   │
      │  │ • Call to Action   │   │
      │  └─────────┬───────────┘   │
      └────────────┬───────────────┘
                   │
                   ▼
      ┌────────────────────────────┐
      │  6. Create Draft           │
      │  Application Record        │
      │  • Resume Variant          │
      │  • Cover Letter            │
      │  • Status: DRAFT           │
      └────────────┬───────────────┘
                   │
                   ▼
      ┌────────────────────────────┐
      │  7. User Approval Required │
      │  ┌─────────────────────┐   │
      │  │ Send Notification   │   │
      │  │ • Email             │   │
      │  │ • Push              │   │
      │  │ • Web Dashboard     │   │
      │  └─────────┬───────────┘   │
      │            │               │
      │  ┌─────────▼───────────┐   │
      │  │ Show Diff Viewer    │   │
      │  │ • Original Resume   │   │
      │  │ • Customized Resume │   │
      │  │ • Cover Letter      │   │
      │  │ • Job Details       │   │
      │  └─────────┬───────────┘   │
      │            │               │
      │  ┌─────────▼───────────┐   │
      │  │ Wait for Response   │   │
      │  │ Timeout: 24 hours   │   │
      │  └─────────┬───────────┘   │
      └────────────┬───────────────┘
                   │
          ┌────────┴────────┐
          │                 │
      APPROVED          REJECTED
          │                 │
          ▼                 ▼
┌─────────────────┐   ┌──────────────┐
│ 8. Submit App   │   │ Mark Rejected│
│ ┌─────────────┐ │   │ Store Reason │
│ │ Fill Form   │ │   └──────────────┘
│ │ Upload Docs │ │
│ │ Submit      │ │
│ └──────┬──────┘ │
│        │        │
│ ┌──────▼──────┐ │
│ │ Get Confirm │ │
│ │ Number      │ │
│ └──────┬──────┘ │
└────────┬────────┘
         │
         ▼
┌────────────────────┐
│ 9. Update Status   │
│ • SUBMITTED        │
│ • Log Confirmation │
│ • Store Timestamp  │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ 10. Schedule       │
│ Follow-ups         │
│ • Day 7: Reminder  │
│ • Day 14: Reminder │
│ • Day 21: Reminder │
└────────────────────┘
```

## AutoGen Agent Collaboration

```
┌──────────────────────────────────────────────────────┐
│              USER REQUEST                            │
│  "Find and apply to 5 remote Python developer jobs"  │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  TaskOrchestrator      │
         │  "I'll coordinate this"│
         └────────────┬───────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│JobResear-│   │Resume    │   │CoverLett-│
│cher      │──►│Optimizer │──►│erWriter  │
│          │   │          │   │          │
│ Searches │   │ Tailors  │   │ Writes   │
│ 50 jobs  │   │ Resume   │   │ Letter   │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     │              │              │
     └──────────────┼──────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  UserProxy       │
         │  "Approve this?" │◄─────┐
         └──────┬───────────┘      │
                │                  │
         User Reviews & Approves   │
                │                  │
                ▼                  │
         ┌──────────────────┐      │
         │ AppManager       │      │
         │ "Submitting..."  │──────┘
         └──────────────────┘
                │
                ▼
         Application Submitted ✓
```

## Data Flow Diagram

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Gmail   │────►│  Email   │────►│  Task    │
│  Inbox   │     │  Triage  │     │  Created │
└──────────┘     └──────────┘     └──────────┘
                                        │
                                        ▼
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Job     │────►│  Vector  │────►│ Matching │
│  Board   │     │  Search  │     │ Score    │
└──────────┘     └──────────┘     └──────────┘
     │                                  │
     │                                  ▼
     │                            ┌──────────┐
     │                            │  Resume  │
     └───────────────────────────►│ Optimize │
                                  └────┬─────┘
                                       │
                                       ▼
                                 ┌──────────┐
                                 │ Approval │
                                 │  Queue   │
                                 └────┬─────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  Submit  │
                                │  & Track │
                                └──────────┘
```

## Security & Privacy Flow

```
┌─────────────┐
│  User Data  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Encryption     │
│  at Rest        │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│  OAuth Tokens   │─────►│  Encrypted   │
│  & Credentials  │      │  Vault       │
└─────────────────┘      └──────────────┘
       │
       ▼
┌─────────────────┐
│  Scoped Access  │
│  • Read-only    │
│  • Write with   │
│    approval     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Audit Logs     │
│  Immutable      │
│  Record         │
└─────────────────┘
```

## Monitoring Dashboard Layout

```
┌────────────────────────────────────────────────────┐
│                AGENTICE DASHBOARD                  │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │Applications │  │  Opportunities│  │ Approvals │ │
│  │ Today: 5    │  │  Found: 47   │  │ Pending:3 │ │
│  └─────────────┘  └─────────────┘  └───────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │          Application Success Rate             │ │
│  │  █████████████████░░░░░░  75%                │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │       Recent Applications                     │ │
│  │  • Tech Corp - Pending                       │ │
│  │  • StartupXYZ - Interview Scheduled          │ │
│  │  • BigCo - Rejected                          │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │       Agent Activity                          │ │
│  │  JobResearcher:  ████░░ Active               │ │
│  │  ResumeOptimizer: ██░░░░ Active              │ │
│  │  AppManager:     ░░░░░░ Idle                 │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

---

## Key Architectural Decisions

### 1. **AutoGen for Multi-Agent System**
- **Why**: Native support for agent collaboration and human-in-the-loop
- **Benefit**: Easier to build complex workflows with approval gates

### 2. **FastAPI for Backend**
- **Why**: Async support, auto-generated docs, type safety
- **Benefit**: High performance and developer experience

### 3. **PostgreSQL + pgvector**
- **Why**: Relational data + vector similarity search
- **Benefit**: Single database for all needs

### 4. **Celery for Background Tasks**
- **Why**: Mature, reliable, supports scheduling
- **Benefit**: Async job processing without blocking API

### 5. **Docker Compose**
- **Why**: Easy local development and deployment
- **Benefit**: One command to start entire stack

---

This architecture provides a scalable, maintainable, and secure foundation for the Agentice Personal AI Assistant! 🚀
