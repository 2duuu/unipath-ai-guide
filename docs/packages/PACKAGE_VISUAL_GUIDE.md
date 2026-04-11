# Package Access Control Flow

## User Journey: Downloading PDF

```
┌─────────────────────────────────────────────────────────────┐
│                    USER CLICKS DOWNLOAD                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  DownloadPDFButton.tsx      │
        │  (Frontend Component)       │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  packages.ts service         │
        │  triggerPDFDownload()       │
        └─────────────┬───────────────┘
                      │
                      │ GET /api/download/recommendations-pdf
                      │ Authorization: Bearer {token}
                      │
                      ▼
        ┌─────────────────────────────┐
        │    Backend API (api.py)     │
        │  @app.get("/api/download/   │
        │    recommendations-pdf")    │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  get_current_user_id()      │
        │  (JWT token validation)     │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Query user from database   │
        │  Check user.package_tier    │
        └─────────────┬───────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
  package_tier                package_tier
  = "free"                    = "decision_clarity"
          │                       │
          ▼                       ▼
  ┌───────────────┐      ┌──────────────────┐
  │ Return 403    │      │ Generate PDF     │
  │ "Requires     │      │ (pdf_generator)  │
  │  premium      │      └────────┬─────────┘
  │  package"     │               │
  └───────┬───────┘               ▼
          │              ┌──────────────────┐
          │              │ Return PDF blob  │
          │              │ Content-Type:    │
          │              │ application/pdf  │
          │              └────────┬─────────┘
          │                       │
          ▼                       ▼
  ┌───────────────┐      ┌──────────────────┐
  │ Show upgrade  │      │ Browser downloads│
  │ dialog with   │      │ PDF file         │
  │ package info  │      │ "recommendations │
  │               │      │  _2026-01-20.pdf"│
  └───────────────┘      └──────────────────┘
       FREE USER           PREMIUM USER
```

## Package Feature Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FEATURE AVAILABILITY                          │
├──────────────────────┬──────┬──────────┬──────────┬────────────────┤
│ Feature              │ FREE │ DECISION │   APP    │    GUIDED      │
│                      │      │ CLARITY  │   PREP   │    SUPPORT     │
├──────────────────────┼──────┼──────────┼──────────┼────────────────┤
│ Basic Quiz           │  ✅  │    ✅    │    ✅    │      ✅        │
│ Uni Recommendations  │  ✅  │    ✅    │    ✅    │      ✅        │
│ Advanced AI Compare  │  ❌  │    ✅    │    ✅    │      ✅        │
│ Ranked Recommends    │  ❌  │    ✅    │    ✅    │      ✅        │
│ Trade-off Analysis   │  ❌  │    ✅    │    ✅    │      ✅        │
│ Admission Prob.      │  ❌  │    ✅    │    ✅    │      ✅        │
│ 📄 PDF DOWNLOAD      │  ❌  │    ✅    │    ✅    │      ✅        │
│ Unlimited AI Chat    │  ❌  │    ✅    │    ✅    │      ✅        │
│ Application Strategy │  ❌  │    ❌    │    ✅    │      ✅        │
│ Deadline Timeline    │  ❌  │    ❌    │    ✅    │      ✅        │
│ Letter Training      │  ❌  │    ❌    │    ✅    │      ✅        │
│ CV Training          │  ❌  │    ❌    │    ✅    │      ✅        │
│ AI Feedback          │  ❌  │    ❌    │    ✅    │      ✅        │
│ Video Counseling     │  ❌  │    ❌    │    ❌    │      ✅        │
│ Human Guidance       │  ❌  │    ❌    │    ❌    │      ✅        │
│ Document Checks      │  ❌  │    ❌    │    ❌    │      ✅        │
│ Submission Prep      │  ❌  │    ❌    │    ❌    │      ✅        │
│ Deadline Tracking    │  ❌  │    ❌    │    ❌    │      ✅        │
│ Peer Insights        │  ❌  │    ❌    │    ❌    │      ✅        │
├──────────────────────┼──────┼──────────┼──────────┼────────────────┤
│ PRICE                │  €0  │  €36.30  │   €121   │     €484       │
└──────────────────────┴──────┴──────────┴──────────┴────────────────┘
```

## Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                    student_profiles                          │
├─────────────────────────────────────────────────────────────┤
│ id                    INTEGER PRIMARY KEY                    │
│ name                  VARCHAR                                │
│ email                 VARCHAR UNIQUE                         │
│ username              VARCHAR UNIQUE                         │
│ password_hash         VARCHAR                                │
│ ...                   (other profile fields)                 │
│                                                               │
│ 📦 package_tier       VARCHAR(50) DEFAULT 'free'            │
│ 📦 package_purchased_at  DATETIME                            │
│ 📦 package_expires_at    DATETIME                            │
│                                                               │
│ created_at            DATETIME                               │
│ updated_at            DATETIME                               │
└─────────────────────────────────────────────────────────────┘
```

## Code Architecture

```
Backend (Python)
├── src/
│   ├── packages.py          🔑 Package definitions & access control
│   │   ├── PackageTier enum
│   │   ├── PackageFeature enum
│   │   ├── PACKAGE_FEATURES mapping
│   │   └── can_download_pdf()
│   │
│   ├── pdf_generator.py     📄 PDF creation
│   │   └── generate_recommendation_pdf()
│   │
│   ├── auth.py              🔐 JWT & authentication
│   ├── database.py          💾 SQLAlchemy models
│   └── ...
│
└── api.py                   🌐 FastAPI endpoints
    ├── GET /api/user/package-info
    ├── POST /api/user/upgrade-package
    └── GET /api/download/recommendations-pdf

Frontend (React + TypeScript)
├── src/
│   ├── lib/
│   │   └── packages.ts      📦 Package types & utilities
│   │
│   ├── services/
│   │   └── packages.ts      🔌 API service layer
│   │       ├── getPackageInfo()
│   │       ├── upgradePackage()
│   │       └── triggerPDFDownload()
│   │
│   └── components/
│       ├── PackageInfoCard.tsx      📊 Display user package
│       └── DownloadPDFButton.tsx    ⬇️ PDF download + gate
```

## Access Control Logic

```python
# Backend: packages.py

PACKAGE_FEATURES = {
    PackageTier.FREE: {
        PackageFeature.BASIC_QUIZ,
        PackageFeature.UNIVERSITY_RECOMMENDATIONS,
    },
    PackageTier.DECISION_CLARITY: {
        # All FREE features +
        PackageFeature.BASIC_QUIZ,
        PackageFeature.UNIVERSITY_RECOMMENDATIONS,
        # New features:
        PackageFeature.PDF_SUMMARY,  # ← THE KEY FEATURE
        PackageFeature.ADVANCED_AI_COMPARISONS,
        # ...
    },
    # ...
}

def can_download_pdf(package: PackageTier) -> bool:
    return PackageFeature.PDF_SUMMARY in PACKAGE_FEATURES[package]
```

## Error Handling Flow

```
User clicks Download
        │
        ▼
Frontend sends request
        │
        ▼
Backend checks package
        │
        ├─ Has premium? ─────────┐
        │                        ▼
        │                   Generate PDF
        │                        │
        │                        ▼
        │                   Return 200 + PDF
        │                        │
        │                        ▼
        │                   Browser downloads
        │
        └─ Free user? ───────────┐
                                 ▼
                            Return 403
                     "Requires premium package"
                                 │
                                 ▼
                    Frontend catches error
                                 │
                                 ▼
                      Show upgrade dialog
                        with package info
                                 │
                                 ▼
                    User clicks "View Packages"
                                 │
                                 ▼
                      Scroll to pricing section
```

## Testing Results

```
🧪 Package System Tests

✅ Test 1: Feature Mapping
   - FREE: 2 features
   - DECISION_CLARITY: 8 features
   - APPLICATION_PREP: 13 features
   - GUIDED_SUPPORT: 19 features

✅ Test 2: FREE User Access
   - Can download PDF: ❌ NO ✓

✅ Test 3: DECISION_CLARITY User Access
   - Can download PDF: ✅ YES ✓
   - Has PDF_SUMMARY feature: ✅ YES ✓

✅ Test 4: Feature Access Function
   - All access checks working correctly ✓

✅ Test 5: Feature Inheritance
   - Higher tiers include lower tier features ✓

🎉 ALL TESTS PASSED
```

## Migration Status

```
┌────────────────────────────────────────────┐
│        DATABASE MIGRATION STATUS           │
├────────────────────────────────────────────┤
│                                            │
│  ✅ Migration script created               │
│  ✅ Migration executed successfully        │
│  ✅ 3 columns added to student_profiles    │
│     - package_tier (DEFAULT 'free')        │
│     - package_purchased_at                 │
│     - package_expires_at                   │
│                                            │
│  ✅ All existing users set to FREE         │
│  ✅ No data lost                           │
│                                            │
│  Database: backend/data/unihub.db          │
│  Date: 2026-01-20                          │
│                                            │
└────────────────────────────────────────────┘
```

## Quick Commands

```bash
# Test package system
python backend/test_package_system.py

# Run migration (if needed)
python backend/migrate_add_packages.py

# Start backend
cd backend
python api.py

# Test PDF download (premium user)
curl -X GET "http://localhost:8084/api/download/recommendations-pdf" \
  -H "Authorization: Bearer TOKEN" \
  -o recommendations.pdf

# Upgrade user to premium
curl -X POST "http://localhost:8084/api/user/upgrade-package" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"package_tier": "decision_clarity"}'
```

---

**System Status**: ✅ PRODUCTION READY  
**Tests**: ✅ ALL PASSING  
**Migration**: ✅ COMPLETE  
**Dependencies**: ✅ INSTALLED
