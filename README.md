# Agentice - Personal AI Assistant 🤖

A Jarvis-like AI assistant that automates your career development and daily tasks using AutoGen multi-agent system.

## 🎯 Features

### Autonomous Job Application System
- **Automated Job Search**: Scrapes multiple job boards (Indeed, LinkedIn, Glassdoor)
- **Smart Matching**: AI-powered fit scoring based on your skills and preferences
- **Resume Customization**: Automatically tailors your resume for each job with ATS optimization
- **Cover Letter Generation**: Creates personalized, compelling cover letters
- **Auto-Apply**: Submits applications with your approval
- **Application Tracking**: Monitors application status and schedules follow-ups

### Task & Email Management
- **Smart Email Triage**: Automatically categorizes and prioritizes emails
- **Email-to-Task**: Converts actionable emails into tasks
- **Daily Summaries**: Morning briefs and end-of-day reports
- **Calendar Integration**: Syncs with Google/Microsoft Calendar
- **Proactive Notifications**: Timely reminders and alerts

### Professional Profile Management
- **Multi-Platform Sync**: Updates LinkedIn, GitHub, and Portfolio automatically
- **Content Generation**: Creates posts, articles, and case studies
- **Brand Consistency**: Maintains consistent personal brand across platforms
- **SEO Optimization**: Improves discoverability with keyword optimization

### AI Multi-Agent System (AutoGen)
- **JobResearcher Agent**: Finds and ranks opportunities
- **ResumeOptimizer Agent**: Customizes resumes with ATS optimization
- **CoverLetterWriter Agent**: Generates personalized cover letters
- **ApplicationManager Agent**: Handles submission and tracking
- **ProfileUpdater Agent**: Keeps professional profiles current
- **ContentCreator Agent**: Generates thought leadership content
- **TaskOrchestrator Agent**: Coordinates all agents

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│           Dashboard | Approvals | Settings | Reports         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AutoGen Multi-Agent System                    │  │
│  │  • Job Researcher  • Resume Optimizer                │  │
│  │  • Cover Letter Writer  • Application Manager        │  │
│  │  • Profile Updater  • Content Creator                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Services: Task | Email | Calendar | Resume | Applications  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              Data Layer                                      │
│  PostgreSQL + pgvector  |  Redis  |  Object Storage         │
└──────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│           External Integrations                              │
│  Gmail | Calendar | GitHub | LinkedIn | Job Boards          │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- OpenAI API Key
- Google OAuth credentials
- GitHub token

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Dakshit06/presonal_Agant-for-me-.git
cd presonal_Agant-for-me-
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Or run locally**
```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run database migrations
alembic upgrade head

# Start the API
uvicorn src.main:app --reload
```

5. **Access the application**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Flower (Celery): http://localhost:5555
- Grafana: http://localhost:3000

## 📚 Usage

### Autonomous Job Search & Apply

```python
from src.pipelines.job_application_pipeline import JobApplicationPipeline

# Initialize pipeline
pipeline = JobApplicationPipeline(user_id="your-user-id")

# Run daily job search
results = await pipeline.run_daily_job_search(
    search_criteria={
        'keywords': 'senior software engineer python',
        'location': 'Remote',
        'remote_only': True,
        'max_applications_per_day': 10
    }
)

# Apply to specific job
application = await pipeline.apply_to_specific_job(
    job_url="https://...",
    company_name="Example Corp",
    job_title="Senior Python Developer",
    job_description="...",
    auto_submit=False  # Requires approval
)
```

### Using AutoGen Agents Directly

```python
from src.agents.autogen_agents import AgentManager

# Get agent system
agent_system = AgentManager.get_agent_system(user_id="your-user-id")

# Optimize resume for a job
optimized_resume = await agent_system.optimize_resume_for_job(
    job_description="...",
    current_resume=my_resume
)

# Generate cover letter
cover_letter = await agent_system.generate_cover_letter(
    job_description="...",
    company_name="Example Corp",
    resume=my_resume
)

# Update professional profiles
profile_updates = await agent_system.update_professional_profiles(
    new_experience={
        'skills': ['Kubernetes', 'Terraform'],
        'project': 'Built scalable microservices platform'
    }
)
```

### API Endpoints

#### Job Applications
```bash
# Start autonomous job search
POST /api/v1/applications/auto-search

# Apply to specific job
POST /api/v1/applications/apply
{
    "job_url": "https://...",
    "company_name": "Example Corp",
    "job_title": "Senior Developer",
    "job_description": "..."
}

# Get application status
GET /api/v1/applications/{application_id}

# Approve/reject application
POST /api/v1/applications/{application_id}/approve
POST /api/v1/applications/{application_id}/reject
```

## ⚙️ Configuration

### Feature Flags (`.env`)

```bash
# Auto-apply to jobs without manual approval (use with caution!)
ENABLE_AUTO_APPLY=false

# Require approval before submitting applications
REQUIRE_APPROVAL_FOR_APPLICATIONS=true

# Maximum applications per day
MAX_APPLICATIONS_PER_DAY=50
```

## 🔐 Security & Privacy

- **Encryption**: All sensitive data encrypted at rest and in transit
- **OAuth 2.0**: Secure authentication with external services
- **User Consent**: Explicit approval required for all actions
- **Audit Logs**: Immutable logs of all applied changes

## 📊 Monitoring

- **Prometheus**: Metrics collection (port 9090)
- **Grafana**: Visualization dashboards (port 3000)
- **Flower**: Celery task monitoring (port 5555)

## 📧 Contact

- GitHub: [@Dakshit06](https://github.com/Dakshit06)

## ⚠️ Disclaimer

This tool automates job applications on your behalf. Always review generated materials and approve applications before submission.

---

**Built with ❤️ using AutoGen and AI agents to help you land your dream job!** 
