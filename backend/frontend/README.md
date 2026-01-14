# 🎓 UniHub - Frontend Integration

Complete FastAPI backend + TypeScript React frontend for your quiz system.

## 📁 Files Created

### Backend (API)
- `api.py` - FastAPI backend with all endpoints
- `api_requirements.txt` - API dependencies
- `test_api.py` - API test script
- `start_api.sh` - Quick start script

### Frontend (TypeScript React)
- `frontend/Quiz.tsx` - Main quiz component
- `frontend/Quiz.css` - Styling
- `frontend/types.ts` - TypeScript definitions
- `frontend/INTEGRATION_EXAMPLES.tsx` - Integration examples

### Documentation
- `INTEGRATION_GUIDE.md` - Complete setup guide

## 🚀 Quick Start

### 1. Start the Backend

```bash
# Option A: Use the quick start script
./start_api.sh

# Option B: Manual start
pip install -r api_requirements.txt
python api.py
```

The API will run at `http://localhost:8000`

### 2. Test the API

```bash
# In a new terminal
python test_api.py
```

### 3. Integrate Frontend

Copy the frontend files to your React TypeScript project:

```bash
# Copy to your React project
cp frontend/Quiz.tsx <your-project>/src/pages/
cp frontend/Quiz.css <your-project>/src/pages/
cp frontend/types.ts <your-project>/src/
```

Update your routing (React Router example):
```typescript
import Quiz from './pages/Quiz';

<Route path="/quiz" element={<Quiz />} />
```

Or for Next.js, create:
```
pages/quiz.tsx  (Pages Router)
or
app/quiz/page.tsx  (App Router)
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/questions/initial` | Get initial quiz (13 questions) |
| POST | `/api/submit/initial` | Submit initial quiz → get university matches |
| GET | `/api/questions/extended?profile_id={id}` | Get extended quiz (12-13 questions) |
| POST | `/api/submit/extended` | Submit extended quiz → get program matches |
| POST | `/api/feedback` | Submit user feedback |
| GET | `/api/stats` | Get database statistics |

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🎨 Frontend Features

✅ **Initial Quiz** (13 questions)
- Personal info, GPA, test scores
- Fields of interest
- Budget, location, language preferences

✅ **University Matches**
- Safety/Target/Reach categorization
- Match scores and reasoning
- Detailed university info

✅ **Extended Quiz** (optional, 12-13 questions)
- Deep dive into interests
- Learning preferences
- Course-level ratings

✅ **Program Matches**
- Specific programs at universities
- Program details (degree, duration, language)
- Enhanced matching algorithm

✅ **Feedback System**
- Star ratings (1-5)
- Helpful yes/no
- Optional comments

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **SQLite** - Database (easily upgradeable to PostgreSQL)
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **TypeScript** - Type safety
- **CSS3** - Styling with modern features
- **Fetch API** - HTTP requests

## 📦 Project Structure

```
UniHub/
├── api.py                    # 🔥 FastAPI backend
├── api_requirements.txt      # Backend dependencies
├── test_api.py              # API tests
├── start_api.sh             # Quick start script
│
├── frontend/                # 🎨 Frontend components
│   ├── Quiz.tsx            # Main quiz component
│   ├── Quiz.css            # Styles
│   ├── types.ts            # TypeScript types + API client
│   └── INTEGRATION_EXAMPLES.tsx
│
├── src/                     # Python source
│   ├── interview_system.py
│   ├── extended_interview_system.py
│   ├── matching_engine.py
│   ├── refined_matching_engine.py
│   ├── database.py
│   └── models.py
│
└── docs/                    # Documentation
    └── INTEGRATION_GUIDE.md
```

## 🔧 Configuration

### Update API URL

In `frontend/Quiz.tsx`:
```typescript
const API_BASE_URL = 'http://localhost:8000';  // Development
// const API_BASE_URL = 'https://api.unihub.com';  // Production
```

### CORS Settings

In `api.py`:
```python
allow_origins=[
    "http://localhost:3000",      # React
    "http://localhost:5173",      # Vite
    "https://yourapp.com"         # Production
]
```

### Database

SQLite by default (`unihub.db`). To use PostgreSQL:

```python
# In src/database.py
DATABASE_URL = "postgresql://user:pass@localhost/unihub"
```

## 🧪 Testing

### Test Backend
```bash
python test_api.py
```

### Test Frontend
Open your browser to `http://localhost:3000/quiz` (or your dev server URL)

## 🚀 Deployment

### Backend Options
- **Heroku**: `Procfile`: `web: uvicorn api:app --host=0.0.0.0 --port=${PORT}`
- **Railway/Render**: Auto-detect FastAPI
- **AWS EC2**: Systemd service with nginx
- **Docker**: `FROM python:3.11-slim`

### Frontend Options
- **Vercel** - Zero config for React/Next.js
- **Netlify** - Static site hosting
- **AWS S3 + CloudFront** - Static hosting
- **Docker** - With nginx

## 📱 Screenshots

The frontend includes:
- 📊 Progress bar
- 🎯 Beautiful match cards
- 🟢🟡🔴 Color-coded categories
- ⭐ Star ratings
- 📱 Responsive design

## 🔐 Security Best Practices

1. **Add rate limiting** to prevent abuse
2. **Use environment variables** for sensitive data
3. **Add authentication** (JWT tokens)
4. **Validate all inputs** (already done with Pydantic)
5. **Use HTTPS** in production
6. **Sanitize user inputs** before database queries

## 💡 Next Steps

1. ✅ **Test the API** - Run `python test_api.py`
2. ✅ **Copy frontend files** to your React project
3. ✅ **Update API URL** in Quiz.tsx
4. ✅ **Test in browser** - Navigate to `/quiz`
5. 🚀 **Deploy** - Choose your hosting platform

## 🆘 Troubleshooting

**API won't start**
```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9
```

**CORS errors**
- Add your frontend URL to `allow_origins` in `api.py`

**Module not found**
```bash
pip install -r api_requirements.txt
pip install -r requirements.txt
```

**Database errors**
```bash
# Reset database
rm unihub.db
python api.py  # Will recreate
```

## 📞 Support

For issues or questions:
1. Check `INTEGRATION_GUIDE.md`
2. Review API docs at `http://localhost:8000/docs`
3. Test with `test_api.py`

## ⭐ Features

- ✅ Two-phase quiz system
- ✅ University matching (40+ scoring factors)
- ✅ Program matching (course-level)
- ✅ Safety/Target/Reach classification
- ✅ Feedback collection
- ✅ Database persistence
- ✅ Beautiful UI/UX
- ✅ TypeScript type safety
- ✅ Responsive design
- ✅ RESTful API
- ✅ Auto-generated API docs

---

**Made with ❤️ for UniHub** - Connecting students with their perfect university programs!
