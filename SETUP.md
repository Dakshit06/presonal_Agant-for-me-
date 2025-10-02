# Agentice - Quick Setup Guide

## Prerequisites
- Python 3.11+
- Docker & Docker Compose (recommended)
- OpenAI API key
- Google Cloud credentials (for Gmail/Calendar)
- GitHub personal access token

## Quick Setup (Docker)

1. **Clone and configure**:
```bash
git clone https://github.com/Dakshit06/presonal_Agant-for-me-.git
cd presonal_Agant-for-me-
cp .env.example .env
```

2. **Edit `.env` file** with your API keys:
   - `OPENAI_API_KEY=your-key`
   - `GOOGLE_CLIENT_ID=your-id`
   - `GOOGLE_CLIENT_SECRET=your-secret`
   - `GITHUB_TOKEN=your-token`

3. **Start services**:
```bash
docker-compose up -d
```

4. **Access the application**:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Flower: http://localhost:5555

## Manual Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Set up database**:
```bash
# Start PostgreSQL (with docker)
docker run -d --name agentice-postgres \
  -e POSTGRES_USER=agentice \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=agentice \
  -p 5432:5432 \
  ankane/pgvector

# Start Redis
docker run -d --name agentice-redis \
  -p 6379:6379 \
  redis:7-alpine
```

4. **Run the application**:
```bash
uvicorn src.main:app --reload
```

5. **In another terminal, start Celery worker**:
```bash
celery -A src.worker.celery_app worker --loglevel=info
```

6. **In another terminal, start Celery beat**:
```bash
celery -A src.worker.celery_app beat --loglevel=info
```

## Usage Examples

### Apply to a Specific Job
```bash
curl -X POST "http://localhost:8000/api/v1/applications/apply" \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://...",
    "company_name": "Example Corp",
    "job_title": "Senior Python Developer",
    "job_description": "We are looking for...",
    "auto_submit": false
  }'
```

### Start Autonomous Job Search
```bash
curl -X POST "http://localhost:8000/api/v1/applications/auto-search" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "python developer remote",
    "location": "Remote",
    "remote_only": true,
    "max_applications_per_day": 5
  }'
```

## Next Steps

1. Set up OAuth integrations (Gmail, LinkedIn, GitHub)
2. Upload your resume
3. Configure job search preferences
4. Enable auto-apply (optional)
5. Review and approve applications

## Troubleshooting

**Database connection error**: Make sure PostgreSQL is running
**Redis connection error**: Make sure Redis is running
**Import errors**: Run `pip install -r requirements.txt` again

For more help, see the full documentation in `/docs` or visit http://localhost:8000/docs
