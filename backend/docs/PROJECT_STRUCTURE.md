# UniHub Project Structure

## 📁 Folder Organization

```
UniHub/
├── src/                    # Core application modules
│   ├── __init__.py
│   ├── database.py         # SQLAlchemy models and database config
│   ├── db_query.py         # Database query interface
│   ├── models.py           # Pydantic data models
│   ├── interview_system.py # Student questionnaire system
│   ├── matching_engine.py  # University matching algorithm
│   └── llm_interface.py    # LLM integration (optional)
│
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_mvp.py         # MVP system tests
│
├── scripts/                # Utility scripts
│   ├── __init__.py
│   ├── seed_romanian_universities.py  # Database seeding
│   ├── application_assistant.py       # Application help
│   ├── examples.py                    # Usage examples
│   └── university_database.py         # Legacy database
│
├── docs/                   # Documentation
│   ├── README.md           # Main documentation
│   ├── MVP_README.md       # MVP user guide
│   └── DATABASE_README.md  # Database documentation
│
├── data/                   # Data files
│   └── unihub.db          # SQLite database
│
├── .venv/                  # Virtual environment
│
├── unihub.py              # Main application entry point
├── run_mvp.py             # MVP runner
├── requirements.txt       # Python dependencies
└── .gitignore            # Git ignore rules
```

## 🚀 Quick Start

### Running the MVP
```bash
python run_mvp.py
```

### Running Tests
```bash
python tests/test_mvp.py
```

### Seeding Database
```bash
python scripts/seed_romanian_universities.py
```

## 📦 Core Modules

### src/database.py
- SQLAlchemy ORM models
- Database connection configuration
- Tables: universities, programs, admission_criteria, student_profiles, feedback

### src/matching_engine.py
- Deterministic matching algorithm
- 100-point scoring system
- Balance recommendations (safety/target/reach)

### src/interview_system.py
- Interactive student questionnaire
- Profile creation
- Data validation

### src/db_query.py
- Database query layer
- Search and filter methods
- Pydantic model conversion

## 🧪 Testing

All tests are located in `tests/` folder:
- **test_mvp.py**: Complete MVP system validation
  - Profile creation ✅
  - University matching ✅
  - Database persistence ✅
  - Algorithm verification ✅

## 📊 Database

- **Location**: `data/unihub.db`
- **Type**: SQLite
- **Tables**: 5 (universities, programs, admission_criteria, student_profiles, feedback)
- **Current Data**: 11 Romanian universities, 36 academic programs

## 🔧 Scripts

- **seed_romanian_universities.py**: Populate database with initial data
- **examples.py**: Usage examples and demos
- **application_assistant.py**: Application guidance helper

## 📖 Documentation

- **README.md**: Main project documentation
- **MVP_README.md**: MVP user guide and features
- **DATABASE_README.md**: Database schema and query guide
- **PROJECT_STRUCTURE.md**: This file!

## 🛠️ Development

### Adding New Universities
1. Edit `scripts/seed_romanian_universities.py`
2. Add university data to the `universities_data` list
3. Run: `python scripts/seed_romanian_universities.py`

### Running Interactive MVP
```bash
python run_mvp.py
```

### Testing Changes
```bash
python tests/test_mvp.py
```

## 📝 Import Guidelines

### From Root Level (unihub.py, run_mvp.py)
```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models import UserProfile
from src.matching_engine import MatchingEngine
```

### From src/ Package (internal)
```python
from .models import UserProfile
from .database import SessionLocal
```

### From tests/ Folder
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import UserProfile
from src.matching_engine import MatchingEngine
```

### From scripts/ Folder
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal
from src.models import FieldOfInterest
```

## ✨ Features

✅ Organized modular structure  
✅ Clean separation of concerns  
✅ Easy to test and maintain  
✅ Scalable architecture  
✅ Comprehensive documentation  
✅ All imports properly configured  

## 🔄 Migration Notes

- Database path updated to `data/unihub.db`
- All imports use proper package references
- Path setup included in entry point files
- Backward compatibility maintained

---

**Last Updated**: December 25, 2025  
**Version**: 1.0 (MVP Complete with Organized Structure)
