# Package-Based Access Control System

## Overview

UniPath AI Guide now has a complete package-based access control system that gates premium features behind different pricing tiers. Users start with a FREE package and can upgrade to access more features.

## Package Tiers

### 1. **FREE** (Academic Orientation)
- Basic Quiz
- University Recommendations

### 2. **DECISION_CLARITY** (Choose Confidently - €36.30)
- All FREE features +
- Advanced AI Comparisons
- Ranked Recommendations
- Trade-off Analysis
- Admission Probability
- **PDF Summary Download** ⭐
- Unlimited AI Chat

### 3. **APPLICATION_PREP** (Prepare to Apply - €121)
- All DECISION_CLARITY features +
- Application Strategy Guide
- Deadline Timeline
- Motivation Letter Training
- CV Training
- AI Document Feedback

### 4. **GUIDED_SUPPORT** (Apply with Support - €484)
- All APPLICATION_PREP features +
- Video Counseling Sessions
- Human Expert Guidance
- Document Checks
- Submission Preparation
- Deadline Tracking
- Peer Insights

## Backend Implementation

### Database Schema

The `student_profiles` table now includes:

```sql
package_tier VARCHAR(50) DEFAULT 'free'
package_purchased_at DATETIME
package_expires_at DATETIME
```

### Core Modules

#### 1. **backend/src/packages.py**
Defines the package system:
- `PackageTier` enum (FREE, DECISION_CLARITY, APPLICATION_PREP, GUIDED_SUPPORT)
- `PackageFeature` enum (19 features)
- `PACKAGE_FEATURES` mapping (which features are in which packages)
- Helper functions:
  - `can_download_pdf(user)` - Check if user can download PDF
  - `get_package_tier(tier_str)` - Convert string to enum
  - `get_user_features(user)` - Get all features for a user

#### 2. **backend/src/pdf_generator.py**
Generates PDF summaries:
- `generate_recommendation_pdf(user, recommendations)` - Creates formatted PDF
- Returns BytesIO buffer with PDF content
- Uses reportlab for PDF generation

### API Endpoints

#### GET `/api/user/package-info`
Get current user's package information.

**Auth**: Required (Bearer token)

**Response**:
```json
{
  "package_tier": "decision_clarity",
  "purchased_at": "2026-01-20T10:30:00",
  "expires_at": null,
  "features": [
    "basic_quiz",
    "university_recommendations",
    "advanced_ai_comparisons",
    "ranked_recommendations",
    "tradeoff_analysis",
    "admission_probability",
    "pdf_summary",
    "unlimited_ai_chat"
  ]
}
```

#### POST `/api/user/upgrade-package`
Upgrade user's package tier.

**Auth**: Required (Bearer token)

**Request Body**:
```json
{
  "package_tier": "decision_clarity"
}
```

**Response**:
```json
{
  "message": "Package upgraded successfully",
  "new_tier": "decision_clarity"
}
```

#### GET `/api/download/recommendations-pdf`
Download PDF summary of recommendations.

**Auth**: Required (Bearer token)

**Package Required**: DECISION_CLARITY or higher

**Response**: PDF file (application/pdf)

**Error Response** (403 if insufficient package):
```json
{
  "detail": "PDF download requires 'Choose Confidently' package or higher. Please upgrade your package."
}
```

## Frontend Implementation

### Core Modules

#### 1. **src/lib/packages.ts**
Frontend package types and utilities:
- `PackageTier` enum (mirrors backend)
- `PackageFeature` enum (mirrors backend)
- `PACKAGE_DETAILS` - Display names, prices, descriptions
- Helper functions:
  - `hasFeature(packageInfo, feature)` - Check if user has feature
  - `canDownloadPDF(packageInfo)` - Check PDF access
  - `getPackageDisplayName(tier)` - Get display name

#### 2. **src/services/packages.ts**
API service for package operations:
- `getPackageInfo()` - Fetch user's package info
- `upgradePackage(tier)` - Upgrade to new tier
- `downloadRecommendationsPDF()` - Download PDF blob
- `triggerPDFDownload()` - Trigger browser download

### UI Components

#### 1. **src/components/PackageInfoCard.tsx**
Displays user's current package:
- Package name and price
- Purchase date
- List of available features with checkmarks
- Auto-loads on mount

**Usage**:
```tsx
import { PackageInfoCard } from '@/components/PackageInfoCard';

<PackageInfoCard />
```

#### 2. **src/components/DownloadPDFButton.tsx**
Button to download PDF with access control:
- Shows download button
- Checks package access on click
- Shows upgrade dialog if insufficient package
- Handles download and error states

**Usage**:
```tsx
import { DownloadPDFButton } from '@/components/DownloadPDFButton';

<DownloadPDFButton 
  variant="default" 
  size="default" 
/>
```

## Database Migration

A migration script was created to add package columns to existing databases:

**File**: `backend/migrate_add_packages.py`

**Run**:
```bash
cd backend
python migrate_add_packages.py
```

The script:
- ✅ Checks if columns already exist
- ✅ Adds missing columns only
- ✅ Sets default value for package_tier ('free')
- ✅ Preserves all existing data
- ✅ Shows current schema after migration

## Setup Instructions

### 1. Install Dependencies

```bash
# Backend (in virtual environment)
pip install reportlab>=4.0.0

# Or install all requirements
pip install -r backend/requirements.txt
```

### 2. Run Database Migration

```bash
cd backend
python migrate_add_packages.py
```

### 3. Restart Backend

```bash
cd backend
python api.py
```

The backend will now run with package access control enabled.

### 4. Frontend (No additional setup needed)

The frontend components are ready to use. Just import and place them where needed.

## Integration Examples

### Example 1: Add PDF Download to Results Page

```tsx
// In your results/recommendations page
import { DownloadPDFButton } from '@/components/DownloadPDFButton';
import { PackageInfoCard } from '@/components/PackageInfoCard';

function ResultsPage() {
  return (
    <div>
      <h1>Your Recommendations</h1>
      
      {/* Show user's package */}
      <PackageInfoCard />
      
      {/* PDF download button with access control */}
      <DownloadPDFButton />
      
      {/* Rest of your results */}
    </div>
  );
}
```

### Example 2: Check Feature Access

```tsx
import { useState, useEffect } from 'react';
import { getPackageInfo } from '@/services/packages';
import { canDownloadPDF } from '@/lib/packages';

function FeatureGate() {
  const [canDownload, setCanDownload] = useState(false);
  
  useEffect(() => {
    async function checkAccess() {
      const info = await getPackageInfo();
      setCanDownload(canDownloadPDF(info));
    }
    checkAccess();
  }, []);
  
  return canDownload ? (
    <PremiumFeature />
  ) : (
    <UpgradePrompt />
  );
}
```

### Example 3: Backend Feature Check

```python
from src.packages import can_download_pdf, get_user_features

# Check specific feature
@app.get("/api/some-premium-feature")
async def premium_feature(user_id: int = Depends(get_current_user_id)):
    user = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
    
    if not can_download_pdf(user):
        raise HTTPException(
            status_code=403,
            detail="This feature requires 'Choose Confidently' package or higher"
        )
    
    # Proceed with feature...
    
# Get all user features
@app.get("/api/check-access")
async def check_access(user_id: int = Depends(get_current_user_id)):
    user = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
    features = get_user_features(user)
    return {"features": [f.value for f in features]}
```

## Testing

### Test PDF Download

1. **As FREE user**:
```bash
curl -X GET "http://localhost:8084/api/download/recommendations-pdf" \
  -H "Authorization: Bearer <token>"
# Expected: 403 error with upgrade message
```

2. **As DECISION_CLARITY user**:
```bash
curl -X GET "http://localhost:8084/api/download/recommendations-pdf" \
  -H "Authorization: Bearer <token>" \
  -o recommendations.pdf
# Expected: PDF file downloaded
```

### Test Package Info

```bash
curl -X GET "http://localhost:8084/api/user/package-info" \
  -H "Authorization: Bearer <token>"
# Expected: Package info JSON
```

### Test Package Upgrade

```bash
curl -X POST "http://localhost:8084/api/user/upgrade-package" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"package_tier": "decision_clarity"}'
# Expected: Success message
```

## Future Enhancements

### Payment Integration
Currently, package upgrades are direct database updates. Future implementation should:
1. Integrate with Stripe/PayPal
2. Add payment verification
3. Handle subscriptions vs one-time purchases
4. Add package expiration logic

### Additional Features to Gate
- Advanced matching algorithm
- Priority support
- Extended university database
- Application checklist
- Interview preparation
- Scholarship finder

### Analytics
- Track feature usage by package tier
- Measure upgrade conversion rates
- A/B test pricing
- Monitor which features drive upgrades

## Troubleshooting

### "Package_tier column doesn't exist"
Run the migration script:
```bash
cd backend
python migrate_add_packages.py
```

### "Module 'reportlab' not found"
Install reportlab:
```bash
pip install reportlab
```

### "PDF download returns 404"
Check that:
1. User is authenticated (token in Authorization header)
2. User has recommendations data
3. Backend has reportlab installed

### Frontend shows "Failed to fetch package info"
Check that:
1. Backend is running on port 8084
2. User is logged in (token in localStorage)
3. CORS is properly configured

## Summary

✅ **Backend**: Complete package access control system with 3 API endpoints
✅ **Database**: Migration script ready, columns added
✅ **Frontend**: UI components for package display and PDF download
✅ **PDF Generation**: Full reportlab implementation
✅ **Documentation**: Comprehensive guide for integration

The system is production-ready pending payment integration!
