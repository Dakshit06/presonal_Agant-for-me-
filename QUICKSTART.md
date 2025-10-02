# 🤖 Agentice - Your Personal AI Assistant

**Jarvis-like AI Assistant for Autonomous Job Applications & Career Management**

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)

---

## ✅ Project Status: FULLY OPERATIONAL

Your Agentice application is **running successfully** and ready to use!

### 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Dashboard** | http://localhost:8000 | Web UI for control & monitoring |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | System status |
| **OpenAPI Spec** | http://localhost:8000/openapi.json | API specification |

---

## 🚀 Quick Start

### Start the Application

```bash
# Simple start
./start.sh

# Or manually
source .venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the Dashboard

1. Open your browser
2. Navigate to: **http://localhost:8000**
3. You'll see the Agentice Dashboard with:
   - Control Panel (Auto-apply toggle)
   - Job Search Configuration
   - Application Tracking
   - Settings & API Configuration

---

## 🎯 Core Features

### 1. **Autonomous Job Applications** 🤖
- Automatically searches job boards daily
- Analyzes job compatibility with your resume
- Generates tailored cover letters
- Optimizes resume for each position
- Applies to jobs autonomously (when enabled)

### 2. **AI-Powered Multi-Agent System** 🧠
- **8 Specialized Agents**:
  - JobResearcher: Finds opportunities
  - ResumeOptimizer: Tailors your resume
  - CoverLetterWriter: Creates custom letters
  - ApplicationManager: Handles submissions
  - ProfileUpdater: Keeps profiles current
  - ContentCreator: Generates content
  - TaskOrchestrator: Manages workflows
  - UserProxy: Human approval loop

### 3. **Smart Task Management** 📋
- Extracts tasks from emails
- Creates calendar events
- Sends automated reminders
- Priority-based scheduling

### 4. **Career Tracking** 📊
- Application status monitoring
- Interview scheduling
- Follow-up automation
- Success metrics & analytics

---

## 📱 Using the Dashboard

### Control Panel

**Auto-Apply Toggle**
- `ON`: Automatically applies to matching jobs
- `OFF`: Requires manual approval for each application

**Daily Application Limit**
- Set max applications per day (1-50)
- Prevents overwhelming yourself

### Job Search Configuration

Fill in your preferences:
- **Keywords**: e.g., "Python Developer", "AI Engineer"
- **Location**: "Remote", "San Francisco", etc.
- **Min Salary**: Your minimum acceptable salary
- **Experience Level**: Entry, Mid, Senior, Lead
- **Job Type**: Full-time, Contract, Part-time

Click **"Search Jobs"** to start!

### Application Tracking

View all your applications with:
- Company name
- Position title
- Application status
- Match score (AI-calculated)
- Applied date
- Quick actions (View, Follow-up, Withdraw)

---

## ⚙️ Configuration

### 1. Add OpenAI API Key (Required)

The AI features need an OpenAI API key:

```bash
# Edit .env file
nano .env

# Add your key
OPENAI_API_KEY=sk-your-actual-key-here
```

### 2. Configure via Dashboard

Click **"Configure Settings"** in the dashboard:

**Profile Tab**
- Full name, email, phone
- LinkedIn URL
- GitHub profile

**Resume Tab**
- Upload your resume (PDF/DOCX)
- Manage multiple versions
- Set active resume

**API Keys Tab**
- OpenAI API key
- LinkedIn credentials (optional)
- Indeed API key (optional)

**Notifications Tab**
- Email alerts
- Interview notifications
- Daily summaries

---

## 🔌 API Usage

### Authentication

```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "you@example.com",
    "name": "Your Name"
  }'
```

### Start Automated Job Search

```bash
curl -X POST "http://localhost:8000/api/v1/applications/auto-search" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Python Developer",
    "location": "Remote",
    "max_applications": 10,
    "auto_apply": true
  }'
```

### Upload Resume

```bash
curl -X POST "http://localhost:8000/api/v1/resumes" \
  -F "file=@/path/to/resume.pdf" \
  -F "title=Senior Developer Resume"
```

### Get Applications

```bash
curl "http://localhost:8000/api/v1/applications?status=pending"
```

---

## 📊 Database

Your data is stored in SQLite at: `./agentice.db`

**11 Tables:**
- `users` - User profiles
- `integrations` - OAuth tokens
- `tasks` - Task management
- `events` - Calendar events
- `emails` - Email triage
- `opportunities` - Job postings
- `resumes` - Resume versions
- `applications` - Application tracking
- `changesets` - Pending changes
- `content_drafts` - Generated content
- `feedback` - Learning data

---

## 🛠️ Troubleshooting

### Issue: "Cannot GET /"
**Solution**: Application is now fixed! The frontend is properly configured.

### Issue: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Database error"
```bash
# Reset database
rm agentice.db
# Restart application - it will recreate tables
./start.sh
```

### Issue: "OpenAI API error"
- Check your API key in `.env`
- Ensure you have credits in your OpenAI account
- Verify the key starts with `sk-`

---

## 📈 How It Works

### Autonomous Application Workflow

```
1. Daily Search (8 AM)
   ↓
2. AI Analysis (Match Score)
   ↓
3. Resume Optimization
   ↓
4. Cover Letter Generation
   ↓
5. Auto-Apply (if enabled)
   ↓
6. Track Response
   ↓
7. Schedule Interview
   ↓
8. Follow-up (7, 14, 21 days)
```

### Example Scenario

**You set criteria:**
```json
{
  "keywords": ["Senior Python Developer", "Tech Lead"],
  "location": "Remote",
  "min_salary": 150000,
  "auto_apply": true,
  "daily_limit": 5
}
```

**Agentice automatically:**
1. Searches job boards at 8 AM daily
2. Finds ~30 matching jobs
3. Filters to top 5 (60%+ match)
4. Optimizes your resume for each
5. Generates custom cover letters
6. Applies while you sleep 😴
7. Tracks all responses
8. Schedules interviews
9. Sends follow-ups

**You wake up to interview invites!** ☕

---

## 🎓 Technology Stack

- **Backend**: FastAPI, Python 3.12
- **Frontend**: HTML, CSS, JavaScript (Bootstrap 5)
- **Database**: SQLite (dev), PostgreSQL (prod)
- **AI**: OpenAI GPT-4, AutoGen Multi-Agent
- **Queue**: Celery + Redis
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker, Docker Compose

---

## 📝 API Endpoints

### Applications
- `POST /api/v1/applications/auto-search` - Start job search
- `POST /api/v1/applications/apply` - Apply to specific job
- `GET /api/v1/applications` - List applications
- `GET /api/v1/applications/{id}` - Get application details
- `POST /api/v1/applications/{id}/approve` - Approve application

### Opportunities
- `GET /api/v1/opportunities` - List opportunities
- `POST /api/v1/opportunities/search` - Search jobs
- `GET /api/v1/opportunities/{id}` - Get opportunity

### Resumes
- `POST /api/v1/resumes` - Upload resume
- `GET /api/v1/resumes` - List resumes
- `PUT /api/v1/resumes/{id}` - Update resume
- `DELETE /api/v1/resumes/{id}` - Delete resume

### Tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks` - List tasks
- `PUT /api/v1/tasks/{id}` - Update task

### Events
- `POST /api/v1/events` - Create event
- `GET /api/v1/events` - List events
- `PUT /api/v1/events/{id}` - Update event

**Full API docs**: http://localhost:8000/docs

---

## 🔒 Security

- OAuth 2.0 authentication
- Encrypted token storage
- HTTPS in production
- Rate limiting enabled
- CORS configured
- SQL injection protection

---

## 🚢 Deployment

### Docker (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production

```bash
# Set environment
export ENVIRONMENT=production
export DATABASE_URL=postgresql://user:pass@host/db

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

---

## 📚 Documentation

- **Architecture**: See `ARCHITECTURE.md`
- **Setup Guide**: See `SETUP.md`
- **Use Cases**: See `USE_CASES.md`
- **Project Summary**: See `PROJECT_SUMMARY.md`

---

## 🤝 Support

**The application is running successfully!**

For issues or questions:
1. Check the logs in the terminal
2. Visit http://localhost:8000/docs for API reference
3. Review the troubleshooting section above

---

## 🎯 Next Steps

1. ✅ Application is running
2. ✅ Dashboard is accessible
3. ⏭️ Add your OpenAI API key
4. ⏭️ Upload your resume
5. ⏭️ Configure job search preferences
6. ⏭️ Enable auto-apply
7. ⏭️ Let Agentice find your dream job!

---

## 📄 License

This is your personal AI assistant project.

---

## 🎉 Success!

**Your Agentice Personal AI Assistant is fully operational!**

Open http://localhost:8000 in your browser to get started! 🚀
