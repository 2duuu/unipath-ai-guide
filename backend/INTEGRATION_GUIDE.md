# UniHub Frontend & Backend Integration Guide

## 🚀 Quick Start

### 1. Backend Setup (API)

Install API dependencies:
```bash
pip install -r api_requirements.txt
```

Start the FastAPI server:
```bash
python api.py
```

Or with uvicorn:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend Setup (React/TypeScript)

Copy the files to your React TypeScript project:
- `frontend/Quiz.tsx` → Your React components folder (e.g., `src/pages/Quiz.tsx`)
- `frontend/Quiz.css` → Same folder as Quiz.tsx

Update the API URL if needed (in Quiz.tsx):
```typescript
const API_BASE_URL = 'http://localhost:8000'; // or your production URL
```

Import and use in your app:
```typescript
import Quiz from './pages/Quiz';

function App() {
  return <Quiz />;
}
```

## 📋 API Endpoints

### GET `/api/questions/initial`
Get initial quiz questions (13 questions)
- **Response**: `{ questions: Question[] }`

### POST `/api/submit/initial`
Submit initial quiz and get university matches
- **Body**: `{ answers: Answer[] }`
- **Response**: `{ profile_id: number, match_type: "university", matches: UniversityMatch[] }`

### GET `/api/questions/extended?profile_id={id}`
Get extended quiz questions (12-13 questions)
- **Query**: `profile_id` (integer)
- **Response**: `{ questions: Question[] }`

### POST `/api/submit/extended`
Submit extended quiz and get program matches
- **Body**: `{ profile_id: number, answers: Answer[] }`
- **Response**: `{ profile_id: number, match_type: "program", matches: ProgramMatch[] }`

### POST `/api/feedback`
Submit user feedback
- **Body**: `{ profile_id: number, rating: number, helpful: boolean, comments?: string }`
- **Response**: `{ status: "success", message: string }`

### GET `/api/stats`
Get database statistics
- **Response**: `{ total_profiles: number, total_feedback: number }`

## 🎨 Frontend Features

- ✅ Progress bar showing quiz completion
- ✅ Multiple question types (choice, multiple choice, number, text, range)
- ✅ Beautiful match cards with scores
- ✅ Safety/Target/Reach categorization
- ✅ Feedback collection system
- ✅ Responsive design for mobile/tablet
- ✅ Loading states and error handling

## 🔧 Configuration

### CORS Settings
The API allows connections from:
- `http://localhost:3000` (Create React App default)
- `http://localhost:5173` (Vite default)

Add more origins in `api.py`:
```python
allow_origins=["http://localhost:3000", "https://yourapp.com"]
```

### Database
Uses SQLite by default (`unihub.db`). Initialized automatically on API startup.

## 📦 Project Structure

```
UniHub/
├── api.py                    # FastAPI backend
├── api_requirements.txt      # API dependencies
├── src/                      # Python source code
│   ├── interview_system.py
│   ├── matching_engine.py
│   ├── database.py
│   └── models.py
├── frontend/                 # TypeScript React components
│   ├── Quiz.tsx             # Main quiz component
│   └── Quiz.css             # Styles
└── docs/                    # Documentation
```

## 🧪 Testing

Test the API endpoints:
```bash
# Health check
curl http://localhost:8000/

# Get questions
curl http://localhost:8000/api/questions/initial

# Get stats
curl http://localhost:8000/api/stats
```

## 🌐 Deployment

### Backend (API)
Deploy to:
- **Heroku**: Use `Procfile` with `web: uvicorn api:app --host=0.0.0.0 --port=${PORT}`
- **AWS EC2**: Run with systemd service
- **Railway/Render**: Auto-detect FastAPI

### Frontend
Deploy to:
- **Vercel**: Upload React build
- **Netlify**: Upload React build
- **AWS S3 + CloudFront**: Static hosting

Remember to update `API_BASE_URL` in Quiz.tsx to your production API URL!

## 🔒 Environment Variables (Production)

Create `.env` file:
```
DATABASE_URL=postgresql://...  # For production database
ALLOWED_ORIGINS=https://yourapp.com
```

Update api.py to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

## 💡 Tips

1. **Development**: Use `--reload` flag for hot reloading
2. **Production**: Use `--workers 4` for multiple workers
3. **HTTPS**: Use nginx or Caddy as reverse proxy
4. **Monitoring**: Add logging middleware to FastAPI
5. **Rate Limiting**: Add rate limiting to prevent abuse

## 🐛 Common Issues

**CORS Error**: Make sure frontend origin is in `allow_origins` list
**Port in use**: Change port with `--port 8001`
**Module not found**: Install dependencies with `pip install -r api_requirements.txt`
**Database locked**: Close other connections to unihub.db

## 📚 Next Steps

1. Add user authentication (JWT tokens)
2. Add payment integration
3. Add email notifications
4. Add admin dashboard
5. Add application tracking system
6. Add university comparison tool
