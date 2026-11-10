"""System endpoints: health checks and stats."""
from fastapi import APIRouter, HTTPException

from app.db.database import FeedbackDB, SessionLocal, StudentProfileDB

router = APIRouter()


@router.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "UniHub API",
        "version": "1.0.0"
    }


@router.get("/api/health")
async def api_health():
    """Explicit /api/health endpoint for frontend checks."""
    return {
        "status": "ok",
        "service": "UniHub API",
        "version": "1.0.0"
    }


@router.get("/api/stats")
async def get_stats():
    """Get database statistics (number of profiles and feedback entries)."""
    try:
        db = SessionLocal()
        try:
            student_count = db.query(StudentProfileDB).count()
            feedback_count = db.query(FeedbackDB).count()
            
            return {
                "total_profiles": student_count,
                "total_feedback": feedback_count
            }
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
