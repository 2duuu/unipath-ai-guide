# UniHub Frontend-Backend Integration

This document describes how the UniHub frontend is connected to the backend API.

## Architecture Overview

The application follows a client-server architecture:
- **Frontend**: React + TypeScript + Vite (port 8080)
- **Backend**: FastAPI + Python (port 8000)
- **Database**: SQLite (unihub.db)

## Directory Structure

```
src/
├── services/
│   └── api.ts              # API service layer for backend communication
├── types/
│   └── quiz.ts            # TypeScript interfaces for API data
├── pages/
│   ├── Quiz.tsx           # Main quiz component
│   └── Quiz.css           # Quiz styling
└── ...

UniHub/
├── api.py                 # FastAPI backend server
├── src/                   # Backend source code
│   ├── interview_system.py
│   ├── extended_interview_system.py
│   ├── matching_engine.py
│   └── ...
└── ...
```

## Setup Instructions

### 1. Backend Setup

First, install Python dependencies:

```bash
cd UniHub
pip install -r api_requirements.txt
```

Initialize the database (done automatically on first start):

```bash
python api.py
```

Or use uvicorn:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Frontend Setup

Install Node.js dependencies (if not already done):

```bash
npm install
```

The following has already been configured:
- ✅ Axios for HTTP requests
- ✅ API service layer (`src/services/api.ts`)
- ✅ TypeScript types (`src/types/quiz.ts`)
- ✅ Environment variables (`.env`)
- ✅ Vite proxy configuration

Start the frontend development server:

```bash
npm run dev
```

The frontend will be available at: http://localhost:8080

## API Endpoints

### Quiz Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/questions/initial` | Get initial quiz questions (13 questions) |
| POST | `/api/submit/initial` | Submit initial quiz and get university matches |
| GET | `/api/questions/extended?profile_id={id}` | Get extended quiz questions |
| POST | `/api/submit/extended` | Submit extended quiz and get program matches |
| POST | `/api/feedback` | Submit user feedback |
| GET | `/api/stats` | Get database statistics |

### Request/Response Examples

**Get Initial Questions:**
```bash
curl http://localhost:8000/api/questions/initial
```

**Submit Initial Quiz:**
```bash
curl -X POST http://localhost:8000/api/submit/initial \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"question_id": "name", "answer": "John"},
      {"question_id": "age", "answer": 18},
      ...
    ]
  }'
```

## Frontend-Backend Communication

### API Service Layer

The `src/services/api.ts` file provides typed functions for all API endpoints:

```typescript
import { getInitialQuestions, submitInitialQuiz } from '@/services/api';

// Fetch questions
const data = await getInitialQuestions();

// Submit quiz
const result = await submitInitialQuiz({ answers: [...] });
```

### Environment Configuration

The API base URL is configured in `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

For production, update this to your production API URL.

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (Create React App)
- `http://localhost:5173` (Vite default)
- `http://localhost:8080` (Current Vite config)

To add more origins, update `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://yourapp.com"],
    ...
)
```

## Quiz Flow

1. **Initial Quiz** (13 questions)
   - User answers demographic and preference questions
   - System generates university matches
   - Profile saved to database with unique `profile_id`

2. **University Results**
   - Display matched universities categorized as:
     - 🟢 Safety Schools
     - 🟡 Target Schools
     - 🔴 Reach Schools

3. **Extended Quiz** (12-13 questions)
   - Optional deeper dive based on initial profile
   - More specific questions about interests and goals

4. **Program Results**
   - Display matched programs with detailed information
   - Categorized by match type

5. **Feedback**
   - User can rate recommendations (1-5 stars)
   - Indicate if helpful (yes/no)
   - Provide optional comments

## Features

### Frontend
- ✅ Dynamic question rendering (choice, multiple choice, text, number, range)
- ✅ Progress tracking
- ✅ Real-time validation
- ✅ Match visualization with scores
- ✅ Feedback collection
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states

### Backend
- ✅ RESTful API with FastAPI
- ✅ SQLite database for persistence
- ✅ LLM-powered matching engine
- ✅ Profile storage and retrieval
- ✅ Feedback collection
- ✅ Statistics tracking

## Development Workflow

### Running Both Servers

**Terminal 1 - Backend:**
```bash
cd UniHub
python api.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

### Testing the Integration

1. Navigate to http://localhost:8080
2. Click on "Quiz" in the navigation
3. Answer the initial quiz questions
4. View university matches
5. Optionally take the extended quiz
6. View program matches
7. Provide feedback

## Troubleshooting

### Backend not responding
- Check if Python server is running: `curl http://localhost:8000/`
- Verify dependencies: `pip install -r api_requirements.txt`
- Check for port conflicts

### Frontend can't connect to backend
- Verify `.env` has correct `VITE_API_BASE_URL`
- Check browser console for CORS errors
- Ensure backend CORS middleware includes frontend port

### Database errors
- Delete `unihub.db` and restart backend to reinitialize
- Check file permissions

## Production Deployment

### Backend
1. Update CORS origins in `api.py`
2. Use production WSGI server (Gunicorn)
3. Set up proper database (PostgreSQL)
4. Configure environment variables

### Frontend
1. Update `.env` with production API URL
2. Build: `npm run build`
3. Deploy `dist/` folder to hosting service
4. Configure reverse proxy if needed

## API Documentation

Full interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Support

For issues or questions:
1. Check the console for error messages
2. Review API documentation at `/docs`
3. Check backend logs for API errors
4. Verify network requests in browser DevTools
