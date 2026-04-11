# 🚀 Quick Reference: Package System

## API Endpoints

### Get Package Info
```bash
GET /api/user/package-info
Headers: Authorization: Bearer {token}
```

### Upgrade Package
```bash
POST /api/user/upgrade-package
Headers: Authorization: Bearer {token}, Content-Type: application/json
Body: {"package_tier": "decision_clarity"}
```

### Download PDF
```bash
GET /api/download/recommendations-pdf
Headers: Authorization: Bearer {token}
Returns: PDF file (if user has DECISION_CLARITY+ package)
```

## Frontend Components

### PDF Download Button
```tsx
import { DownloadPDFButton } from '@/components/DownloadPDFButton';
<DownloadPDFButton />
```

### Package Info Card
```tsx
import { PackageInfoCard } from '@/components/PackageInfoCard';
<PackageInfoCard />
```

## Backend Functions

```python
from src.packages import can_download_pdf, PackageTier, PackageFeature, has_feature_access

# Check PDF access
tier = PackageTier(user.package_tier)
if can_download_pdf(tier):
    # User can download

# Check any feature
if has_feature_access(tier, PackageFeature.UNLIMITED_AI_CHAT):
    # User has feature
```

## Package Tiers

| Tier | Value | Price |
|------|-------|-------|
| FREE | `"free"` | €0 |
| DECISION_CLARITY | `"decision_clarity"` | €36.30 |
| APPLICATION_PREP | `"application_prep"` | €121 |
| GUIDED_SUPPORT | `"guided_support"` | €484 |

## Key Features

- ✅ `PDF_SUMMARY` - Available in DECISION_CLARITY+
- ✅ `BASIC_QUIZ` - Available in FREE+
- ✅ `ADVANCED_AI_COMPARISONS` - Available in DECISION_CLARITY+
- ✅ `UNLIMITED_AI_CHAT` - Available in DECISION_CLARITY+
- ✅ `VIDEO_COUNSELING` - Available in GUIDED_SUPPORT only

## Database Fields

```sql
package_tier VARCHAR(50) DEFAULT 'free'
package_purchased_at DATETIME
package_expires_at DATETIME
```

## Testing

```bash
# Run tests
python backend/test_package_system.py

# All tests should pass:
✅ Feature mapping correct
✅ Access control working
✅ Feature inheritance correct
```

## Common Tasks

### Upgrade a user manually (for testing)
```python
from src.database import StudentProfileDB, get_db
from datetime import datetime

db = next(get_db())
user = db.query(StudentProfileDB).filter(StudentProfileDB.id == 1).first()
user.package_tier = "decision_clarity"
user.package_purchased_at = datetime.now()
db.commit()
```

### Add a new feature
1. Add to `PackageFeature` enum in `backend/src/packages.py`
2. Add to appropriate `PACKAGE_FEATURES` sets
3. Add to `PackageFeature` enum in `src/lib/packages.ts`
4. Create access check function if needed

### Gate a new endpoint
```python
from src.packages import has_feature_access, PackageFeature, PackageTier

@app.get("/api/some-premium-endpoint")
async def premium(user_id: int = Depends(get_current_user_id)):
    user = db.query(StudentProfileDB).filter_by(id=user_id).first()
    tier = PackageTier(user.package_tier)
    
    if not has_feature_access(tier, PackageFeature.YOUR_FEATURE):
        raise HTTPException(
            status_code=403,
            detail="This requires a premium package"
        )
    
    # Your code here
```

## Restart Backend
```powershell
# Stop backend
Get-Process | Where-Object {$_.ProcessName -like '*python*'} | Stop-Process -Force

# Start backend
cd backend
& ..\.venv\Scripts\python.exe api.py
```

---
**Status**: ✅ Production Ready  
**Last Updated**: January 20, 2026  
**Migration**: ✅ Complete
