# 🚀 UniHub Setup & Installation Guide

Complete instructions for setting up and running the UniHub platform locally.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Deployment](#deployment)

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Node.js** (v18 or higher)
   ```bash
   # Check version
   node --version
   
   # Install with nvm (recommended)
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   nvm install 18
   nvm use 18
   ```

2. **npm** (comes with Node.js)
   ```bash
   # Check version
   npm --version
   ```

3. **Python** (3.10 or higher)
   ```bash
   # Check version
   python3 --version
   # or
   python --version
   ```

4. **pip** (Python package manager)
   ```bash
   # Check version
   pip3 --version
   # or
   pip --version
   ```

### Optional but Recommended

- **Git** for version control
- **VS Code** or your preferred IDE
- **Python virtual environment** (venv or conda)

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
# Clone the repo
git clone <YOUR_GIT_URL>

# Navigate to project directory
cd unipath-ai-guide
```

### Step 2: Install Frontend Dependencies

```bash
# Install all npm packages
npm install

# This will install:
# - React, React Router, TypeScript
# - Vite build tools
# - shadcn/ui components
# - Tailwind CSS
# - Axios, Framer Motion, etc.
```

### Step 3: Install Backend Dependencies

```bash
# Navigate to backend folder
cd backend

# Create a Python virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install core dependencies
pip install -r requirements.txt

# Install API dependencies
pip install -r api_requirements.txt
```

**Backend dependencies include:**
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- OpenAI/Anthropic (for future LLM features)
- pytest (testing)
- ReportLab (PDF generation)

---

## 🏃 Running the Application

### Option 1: Run Frontend & Backend Separately (Recommended for Development)

#### Terminal 1 - Frontend
```bash
# From project root
npm run dev

# Output:
# ➜  Local:   http://localhost:3001/
# ➜  Network: http://192.168.x.x:3001/
```

#### Terminal 2 - Backend API
```bash
# From project root
cd backend

# Activate virtual environment if not already active
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start FastAPI server with auto-reload
python -m uvicorn src.api:app --reload --port 8000

# Output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Access Points:**
- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs (Swagger UI)
- Alternative API Docs: http://localhost:8000/redoc (ReDoc)

### Option 2: Using the Backend Startup Script

```bash
cd backend
./start_api.sh
```

---

## 🗄 Database Setup

UniHub uses SQLite for data storage. The database is automatically created on first run.

### Initial Database Setup

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Seed the database with Romanian universities
python scripts/seed_anosr_universities_final.py

# This will populate:
# - 11 major Romanian universities
# - 36+ academic programs
# - Admission criteria
# - University metadata
```

### Database Location
- **Path**: `backend/data/unihub.db`
- **Type**: SQLite
- **Backup**: `backend/data/unihub.db.backup`

### Database Tables
- `users` - User accounts and authentication
- `universities` - University information
- `programs` - Academic programs
- `admission_criteria` - Admission requirements
- `student_profiles` - Quiz results and preferences
- `quiz_results` - Saved quiz data
- `packages` - User package/subscription info
- `feedback` - User feedback

### Inspecting the Database

```bash
# Install SQLite browser (optional)
brew install sqlite  # macOS
apt-get install sqlite3  # Ubuntu/Debian

# Open database
sqlite3 backend/data/unihub.db

# View tables
.tables

# View schema
.schema universities

# Run queries
SELECT * FROM universities LIMIT 5;

# Exit
.quit
```

---

## ⚙️ Environment Configuration

### Frontend Environment Variables

Create `.env` file in project root (optional):

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000

# Other configs (if needed)
VITE_APP_NAME=UniHub
VITE_APP_VERSION=1.0.0
```

### Backend Environment Variables

Create `.env` file in `backend/` folder (if needed for API keys):

```env
# Database (auto-configured for SQLite)
DATABASE_URL=sqlite:///./data/unihub.db

# JWT Secret (for authentication)
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM API Keys (for future use)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Email (for future notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Note**: The `.env` file is git-ignored for security.

---

## 🛠 Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Problem**: Port 3001 or 8000 is already in use

**Solution**:
```bash
# Kill process on port 3001 (macOS/Linux)
lsof -ti:3001 | xargs kill -9

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
npm run dev -- --port 3002
python -m uvicorn src.api:app --reload --port 8001
```

#### 2. Module Not Found Errors (Python)

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated
cd backend
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
pip install -r api_requirements.txt
```

#### 3. CORS Errors

**Problem**: Frontend can't connect to backend

**Solution**: Backend is configured to allow `localhost:3000-3010`. If you're using a different port, update `backend/src/api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:YOUR_PORT"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. Database Locked Error

**Problem**: `sqlite3.OperationalError: database is locked`

**Solution**:
```bash
# Close all connections to the database
# Stop backend server
# Wait a few seconds
# Restart backend server
```

#### 5. npm Install Fails

**Problem**: Installation errors during `npm install`

**Solution**:
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and lock file
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

## 💻 Development Workflow

### Frontend Development

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Run tests
npm run test
```

### Backend Development

```bash
cd backend

# Start with auto-reload
python -m uvicorn src.api:app --reload

# Run specific test file
pytest tests/test_api.py

# Run all tests with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_api.py::test_login -v
```

### Code Structure

**Frontend** (`src/`):
- `pages/` - Full page components (Quiz, Account, etc.)
- `components/` - Reusable UI components
- `contexts/` - React context providers (Auth)
- `services/` - API client functions
- `lib/` - Utilities and helpers
- `types/` - TypeScript type definitions

**Backend** (`backend/src/`):
- `api.py` - FastAPI routes and endpoints
- `database.py` - SQLAlchemy models
- `auth.py` - Authentication logic
- `models.py` - Pydantic request/response models
- `matching_engine.py` - University matching algorithm
- `interview_system.py` - Quiz logic

---

## 🧪 Testing

### Frontend Tests

```bash
# Run all tests
npm run test

# Run in watch mode
npm run test:watch

# Test specific file
npm run test -- Quiz.test.tsx
```

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test module
pytest tests/test_api.py

# Run with verbose output
pytest -v

# Run and stop at first failure
pytest -x
```

### Manual Testing

1. **Authentication**:
   - Register new user at `/signup`
   - Login at `/login`
   - Check token in browser localStorage

2. **Quiz System**:
   - Start quiz at `/quiz`
   - Complete all questions
   - View results on `/cont` (Account page)

3. **Package System**:
   - Browse packages at `/pachete`
   - "Purchase" a package (testing mode)
   - Verify features unlock on `/cont`

4. **University Browse**:
   - Visit `/facultati`
   - Use search and filters
   - View university details

---

## 🚀 Deployment

### Frontend Deployment (Vercel/Netlify)

```bash
# Build for production
npm run build

# Output in dist/ folder

# Deploy to Vercel (if configured)
vercel deploy

# Deploy to Netlify
netlify deploy --prod
```

### Backend Deployment (Heroku/Railway/Render)

```bash
# Install Gunicorn for production
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api:app
```

**Environment variables to set in production:**
- `DATABASE_URL` - Production database URL
- `SECRET_KEY` - Strong random secret key
- `ALLOWED_ORIGINS` - Frontend URL(s)
- API keys for LLM services (when integrated)

---

## 📞 Support

If you encounter issues not covered here:

1. Check existing [GitHub Issues](https://github.com/your-repo/issues)
2. Review [backend/docs/](./backend/docs/) for detailed documentation
3. Contact the development team

---

## 📝 Quick Reference

### Start Everything (2 Terminals)

**Terminal 1**:
```bash
npm run dev
```

**Terminal 2**:
```bash
cd backend
source venv/bin/activate
python -m uvicorn src.api:app --reload
```

### Reset Database

```bash
cd backend
rm data/unihub.db
python scripts/seed_anosr_universities_final.py
```

### Update Dependencies

**Frontend**:
```bash
npm update
```

**Backend**:
```bash
cd backend
pip install --upgrade -r requirements.txt
```

---

**Happy coding! 🎉**

*Last Updated: January 23, 2026*
