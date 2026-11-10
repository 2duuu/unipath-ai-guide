"""University catalog endpoints."""
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal

router = APIRouter()


@router.get("/api/universities")
async def get_universities(
    city: Optional[str] = None,
    field: Optional[str] = None,
    search: Optional[str] = None
):
    """Get list of universities with optional filtering."""
    try:
        from app.db.database import ProgramDB, UniversityDB
        db = SessionLocal()
        try:
            query = db.query(UniversityDB)
            
            # Filter by city if provided
            if city:
                query = query.filter(UniversityDB.city == city)
            
            # Filter by search term in university name
            if search:
                query = query.filter(UniversityDB.name.ilike(f"%{search}%"))
            
            universities = query.all()
            
            # If field filter is provided, filter by programs
            if field:
                filtered_unis = []
                for uni in universities:
                    programs = db.query(ProgramDB).filter(
                        ProgramDB.university_id == uni.id,
                        ProgramDB.field == field
                    ).count()
                    if programs > 0:
                        filtered_unis.append(uni)
                universities = filtered_unis
            
            result = []
            for uni in universities:
                # Count programs
                programs_count = db.query(ProgramDB).filter(
                    ProgramDB.university_id == uni.id
                ).count()
                
                # Get program fields
                programs = db.query(ProgramDB).filter(
                    ProgramDB.university_id == uni.id
                ).all()
                program_fields = list(set([p.field for p in programs if p.field]))
                
                result.append({
                    "id": uni.id,
                    "name": uni.name,
                    "name_en": uni.name_en or uni.name,
                    "city": uni.city,
                    "country": uni.country,
                    "description": uni.description_en or uni.description or "",
                    "tuition_annual_eur": uni.tuition_annual_eur,
                    "tuition_annual_ron": getattr(uni, "tuition_annual_ron", None),
                    "acceptance_rate": uni.acceptance_rate,
                    "student_count": uni.student_count,
                    "type": uni.type,
                    "programs_count": programs_count,
                    "program_fields": program_fields,
                    "website": uni.website,
                    "national_rank": uni.national_rank
                })
            
            return {"universities": result, "total": len(result)}
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
