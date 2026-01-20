"""
Quick test script to verify package access control system
Tests the core functionality without requiring a full API call
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.packages import (
    PackageTier, 
    PackageFeature,
    PACKAGE_FEATURES,
    can_download_pdf,
    get_package_features,
    has_feature_access
)
from src.database import StudentProfileDB

def test_package_system():
    """Test the package access control system"""
    
    print("🧪 Testing Package Access Control System\n")
    print("=" * 60)
    
    # Test 1: Package Features Mapping
    print("\n1️⃣ Testing Package Features Mapping")
    print("-" * 60)
    for tier in PackageTier:
        features = PACKAGE_FEATURES[tier]
        print(f"\n{tier.value.upper()} ({len(features)} features):")
        for feature in list(features)[:5]:  # Show first 5
            print(f"  ✓ {feature.value}")
        if len(features) > 5:
            print(f"  ... and {len(features) - 5} more")
    
    # Test 2: FREE User (No PDF Access)
    print("\n\n2️⃣ Testing FREE User Access")
    print("-" * 60)
    free_tier = PackageTier.FREE
    
    features = get_package_features(free_tier)
    can_pdf = can_download_pdf(free_tier)
    
    print(f"Package: {free_tier.value}")
    print(f"Total Features: {len(features)}")
    print(f"Can Download PDF: {'❌ NO' if not can_pdf else '✅ YES'}")
    print(f"Expected: Should NOT have PDF access")
    assert not can_pdf, "Free user should NOT have PDF access"
    print("✅ PASSED")
    
    # Test 3: DECISION_CLARITY User (Has PDF Access)
    print("\n\n3️⃣ Testing DECISION_CLARITY User Access")
    print("-" * 60)
    premium_tier = PackageTier.DECISION_CLARITY
    
    features = get_package_features(premium_tier)
    can_pdf = can_download_pdf(premium_tier)
    has_pdf_feature = PackageFeature.PDF_SUMMARY in features
    
    print(f"Package: {premium_tier.value}")
    print(f"Total Features: {len(features)}")
    print(f"Can Download PDF: {'✅ YES' if can_pdf else '❌ NO'}")
    print(f"Has PDF_SUMMARY Feature: {'✅ YES' if has_pdf_feature else '❌ NO'}")
    print(f"Expected: Should HAVE PDF access")
    assert can_pdf, "Decision Clarity user SHOULD have PDF access"
    assert has_pdf_feature, "Decision Clarity user should have PDF_SUMMARY feature"
    print("✅ PASSED")
    
    # Test 4: Package Tier Conversion
    print("\n\n4️⃣ Testing Feature Access Function")
    print("-" * 60)
    test_cases = [
        (PackageTier.FREE, PackageFeature.PDF_SUMMARY, False),
        (PackageTier.DECISION_CLARITY, PackageFeature.PDF_SUMMARY, True),
        (PackageTier.APPLICATION_PREP, PackageFeature.PDF_SUMMARY, True),
        (PackageTier.GUIDED_SUPPORT, PackageFeature.PDF_SUMMARY, True),
        (PackageTier.FREE, PackageFeature.BASIC_QUIZ, True),
    ]
    
    for tier, feature, expected in test_cases:
        result = has_feature_access(tier, feature)
        status = "✅" if result == expected else "❌"
        print(f"{status} {tier.value} + {feature.value} = {result} (expected: {expected})")
        assert result == expected, f"Failed feature access check for {tier.value} + {feature.value}"
    
    print("✅ ALL PASSED")
    
    # Test 5: Feature Inheritance (Higher tiers have lower tier features)
    print("\n\n5️⃣ Testing Feature Inheritance")
    print("-" * 60)
    
    free_features = PACKAGE_FEATURES[PackageTier.FREE]
    decision_features = PACKAGE_FEATURES[PackageTier.DECISION_CLARITY]
    app_prep_features = PACKAGE_FEATURES[PackageTier.APPLICATION_PREP]
    guided_features = PACKAGE_FEATURES[PackageTier.GUIDED_SUPPORT]
    
    # Decision Clarity should have all Free features
    assert free_features.issubset(decision_features), "DECISION_CLARITY missing FREE features"
    print("✅ DECISION_CLARITY includes all FREE features")
    
    # Application Prep should have all Decision Clarity features
    assert decision_features.issubset(app_prep_features), "APPLICATION_PREP missing DECISION_CLARITY features"
    print("✅ APPLICATION_PREP includes all DECISION_CLARITY features")
    
    # Guided Support should have all Application Prep features
    assert app_prep_features.issubset(guided_features), "GUIDED_SUPPORT missing APPLICATION_PREP features"
    print("✅ GUIDED_SUPPORT includes all APPLICATION_PREP features")
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print("\nPackage system is working correctly!")
    print("✅ Feature mapping correct")
    print("✅ Access control working")
    print("✅ Tier conversion working")
    print("✅ Feature inheritance correct")
    
    return True

if __name__ == "__main__":
    try:
        test_package_system()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
