"""Package, entitlement and invoice endpoints for the signed-in user."""
from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas import ClaimPackageRequest, UpgradePackageRequest
from app.core.security import get_current_user_id
from app.db.database import SessionLocal, StudentProfileDB

router = APIRouter()


@router.post("/api/user/claim-package")
async def claim_package(
    request: ClaimPackageRequest,
    user_id: int = Depends(get_current_user_id)
):
    """
    Claim a package. Currently free for testing, but structured for future payment gateway.
    In production, this endpoint would:
    1. Receive payment confirmation from payment gateway
    2. Verify payment status
    3. Then assign package to user
    """
    from datetime import datetime

    from app.core.packages import PackageTier

    # Validate package tier
    try:
        tier = PackageTier(request.package_tier)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid package tier")
    
    db = SessionLocal()
    try:
        profile = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user already has this package
        current_tier = PackageTier(profile.package_tier) if profile.package_tier else PackageTier.FREE
        if current_tier == tier:
            raise HTTPException(
                status_code=400, 
                detail="You already have this package"
            )
        
        # TODO: Payment gateway integration here
        # payment_confirmed = await verify_payment_with_gateway(payment_id)
        # if not payment_confirmed:
        #     raise HTTPException(status_code=402, detail="Payment not confirmed")
        
        # For now, simulate successful payment and assign package
        profile.package_tier = tier.value
        purchase_time = datetime.utcnow().isoformat()
        profile.package_purchased_at = purchase_time
        profile.updated_at = purchase_time
        # In production, also set expiration date if applicable
        # profile.package_expires_at = calculate_expiration_date(tier)
        
        # Get package details
        package_names = {
            PackageTier.DECISION_CLARITY: "Decision & Clarity",
            PackageTier.APPLICATION_PREP: "Application Prep",
            PackageTier.GUIDED_SUPPORT: "Guided Support"
        }
        package_prices = {
            PackageTier.DECISION_CLARITY: 36.30,
            PackageTier.APPLICATION_PREP: 121.00,
            PackageTier.GUIDED_SUPPORT: 484.00
        }
        
        # Create invoice
        import random

        from app.db.database import InvoiceDB

        # Generate invoice number
        invoice_number = f"INV-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        invoice = InvoiceDB(
            student_profile_id=user_id,
            invoice_number=invoice_number,
            package_tier=tier.value,
            package_name=package_names.get(tier, "Premium Package"),
            amount=package_prices.get(tier, 0),
            currency="EUR",
            status="paid",
            created_at=purchase_time
        )
        db.add(invoice)
        db.commit()
        
        return {
            "message": "Package activated successfully!",
            "package_tier": tier.value,
            "package_name": package_names.get(tier, "Premium Package"),
            "purchased_at": profile.package_purchased_at,
            "invoice_number": invoice_number,
            "payment_simulated": True  # Remove this field in production
        }
    finally:
        db.close()


@router.get("/api/user/invoices")
async def get_user_invoices(
    user_id: int = Depends(get_current_user_id)
):
    """
    Get all invoices for the current user.
    """
    from app.db.database import InvoiceDB
    
    db = SessionLocal()
    try:
        invoices = db.query(InvoiceDB).filter(
            InvoiceDB.student_profile_id == user_id
        ).order_by(InvoiceDB.created_at.desc()).all()
        
        return {
            "invoices": [
                {
                    "id": inv.invoice_number,
                    "invoice_number": inv.invoice_number,
                    "date": inv.created_at,
                    "package": inv.package_name,
                    "package_tier": inv.package_tier,
                    "amount": inv.amount,
                    "currency": inv.currency,
                    "status": inv.status
                }
                for inv in invoices
            ]
        }
    finally:
        db.close()


@router.post("/api/user/upgrade-package")
async def upgrade_package(
    request: UpgradePackageRequest,
    user_id: int = Depends(get_current_user_id)
):
    """
    Upgrade user's package tier.
    In production, this would integrate with payment processing.
    """
    from datetime import datetime

    from app.core.packages import PackageTier

    # Validate package tier
    try:
        tier = PackageTier(request.package_tier)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid package tier")
    
    db = SessionLocal()
    try:
        profile = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update package
        profile.package_tier = tier.value
        profile.package_purchased_at = datetime.utcnow().isoformat()
        profile.updated_at = datetime.utcnow().isoformat()
        
        db.commit()
        
        return {
            "message": "Package upgraded successfully",
            "package_tier": tier.value,
            "purchased_at": profile.package_purchased_at
        }
    finally:
        db.close()


@router.get("/api/user/package-info")
async def get_package_info(user_id: int = Depends(get_current_user_id)):
    """Get current user's package information and available features."""
    from app.core.packages import PackageTier, get_package_features
    
    db = SessionLocal()
    try:
        profile = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        package_tier = PackageTier(profile.package_tier) if profile.package_tier else PackageTier.FREE
        features = [f.value for f in get_package_features(package_tier)]
        
        return {
            "package_tier": package_tier.value,
            "purchased_at": profile.package_purchased_at,
            "expires_at": profile.package_expires_at,
            "features": features
        }
    finally:
        db.close()
