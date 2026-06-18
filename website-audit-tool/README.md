# AI Website Audit Tool

Modern SaaS-style website audit platform built with FastAPI, SQLAlchemy, Jinja2, Bootstrap 5.3, Chart.js, AOS, Requests, BeautifulSoup4, and ReportLab.

## Features

- SEO, performance, mobile, accessibility, and security audits
- JWT authentication with registration and login
- Dashboard with charts, recent audits, and score breakdowns
- Professional PDF report generation
- Responsive glassmorphism UI

## Project Structure

- `backend/` FastAPI application, models, schemas, services, and report generation
- `frontend/` Jinja2 templates and static assets

## Setup

1. Create and activate a Python 3.12+ virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`.
4. Start the app:

   ```bash
   uvicorn backend.main:app --reload
   ```

## Environment Variables

```env
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/website_audit_tool
BACKEND_CORS_ORIGINS=http://localhost:8000
APP_NAME=AI Website Audit Tool
APP_BASE_URL=http://localhost:8000
```

If MySQL is not available, you can point `DATABASE_URL` to SQLite for local development.
