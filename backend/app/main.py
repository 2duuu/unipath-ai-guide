"""
FastAPI application entry point for the UniHub backend.

Run with:  uvicorn app.main:app --port 8084   (from the backend/ directory)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, packages, quiz, system, universities
from app.db.database import init_db

app = FastAPI(title="UniHub API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080", "http://localhost:8081", "http://localhost:8082", "http://localhost:8083", "http://localhost:8084"],  # React/Vite defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(system.router)
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(universities.router)
app.include_router(packages.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
