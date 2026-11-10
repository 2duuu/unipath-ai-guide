"""Package tiers and features: no admission-prediction feature, deterministic output."""
import pytest

from app.core.packages import (
    PACKAGE_FEATURES,
    PackageFeature,
    PackageTier,
    get_package_features,
    has_feature_access,
)

PAID_TIERS = [
    PackageTier.DECISION_CLARITY,
    PackageTier.APPLICATION_PREP,
    PackageTier.GUIDED_SUPPORT,
]


def test_no_feature_promises_admission_probability():
    values = {f.value for f in PackageFeature}
    assert not any("admission" in v or "probability" in v for v in values)
    assert not hasattr(PackageFeature, "ADMISSION_PROBABILITY")


def test_requirements_fit_check_replaces_it_in_every_paid_tier():
    assert PackageFeature.REQUIREMENTS_FIT_CHECK.value == "requirements_fit_check"
    for tier in PAID_TIERS:
        assert has_feature_access(tier, PackageFeature.REQUIREMENTS_FIT_CHECK)
    assert not has_feature_access(PackageTier.FREE, PackageFeature.REQUIREMENTS_FIT_CHECK)


@pytest.mark.parametrize("tier", list(PackageTier))
def test_get_package_features_is_deterministic_and_sorted(tier):
    features = [f.value for f in get_package_features(tier)]
    assert features == sorted(features)
    assert set(features) == {f.value for f in PACKAGE_FEATURES[tier]}
