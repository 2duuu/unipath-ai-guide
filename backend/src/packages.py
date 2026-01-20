"""
Package-based access control system for UniHub.
Defines package tiers and their associated features.
"""

from enum import Enum
from typing import List, Set


class PackageTier(str, Enum):
    """Available package tiers."""
    FREE = "free"  # Basic quiz access
    DECISION_CLARITY = "decision_clarity"  # Package 1 - Choose Confidently
    APPLICATION_PREP = "application_prep"  # Package 2 - Prepare to Apply
    GUIDED_SUPPORT = "guided_support"  # Package 3 - Apply with Support


class PackageFeature(str, Enum):
    """Features available across different packages."""
    # Free features
    BASIC_QUIZ = "basic_quiz"
    UNIVERSITY_RECOMMENDATIONS = "university_recommendations"
    
    # Package 1 - Decision & Clarity
    ADVANCED_AI_COMPARISONS = "advanced_ai_comparisons"
    RANKED_RECOMMENDATIONS = "ranked_recommendations"
    TRADEOFF_ANALYSIS = "tradeoff_analysis"
    ADMISSION_PROBABILITY = "admission_probability"
    PDF_SUMMARY = "pdf_summary"  # THIS IS THE KEY FEATURE
    UNLIMITED_AI_CHAT = "unlimited_ai_chat"
    
    # Package 2 - Application Preparation
    APPLICATION_STRATEGY = "application_strategy"
    DEADLINE_TIMELINE = "deadline_timeline"
    MOTIVATION_LETTER_TRAINING = "motivation_letter_training"
    CV_TRAINING = "cv_training"
    AI_FEEDBACK = "ai_feedback"
    
    # Package 3 - Guided Application Support
    VIDEO_COUNSELING = "video_counseling"
    HUMAN_GUIDANCE = "human_guidance"
    DOCUMENT_CHECKS = "document_checks"
    SUBMISSION_PREP = "submission_prep"
    DEADLINE_TRACKING = "deadline_tracking"
    PEER_INSIGHTS = "peer_insights"


# Define which features are included in each package
PACKAGE_FEATURES: dict[PackageTier, Set[PackageFeature]] = {
    PackageTier.FREE: {
        PackageFeature.BASIC_QUIZ,
        PackageFeature.UNIVERSITY_RECOMMENDATIONS,
    },
    PackageTier.DECISION_CLARITY: {
        # All free features
        PackageFeature.BASIC_QUIZ,
        PackageFeature.UNIVERSITY_RECOMMENDATIONS,
        # Plus package 1 features
        PackageFeature.ADVANCED_AI_COMPARISONS,
        PackageFeature.RANKED_RECOMMENDATIONS,
        PackageFeature.TRADEOFF_ANALYSIS,
        PackageFeature.ADMISSION_PROBABILITY,
        PackageFeature.PDF_SUMMARY,
        PackageFeature.UNLIMITED_AI_CHAT,
    },
    PackageTier.APPLICATION_PREP: {
        # All Decision & Clarity features
        PackageFeature.BASIC_QUIZ,
        PackageFeature.UNIVERSITY_RECOMMENDATIONS,
        PackageFeature.ADVANCED_AI_COMPARISONS,
        PackageFeature.RANKED_RECOMMENDATIONS,
        PackageFeature.TRADEOFF_ANALYSIS,
        PackageFeature.ADMISSION_PROBABILITY,
        PackageFeature.PDF_SUMMARY,
        PackageFeature.UNLIMITED_AI_CHAT,
        # Plus package 2 features
        PackageFeature.APPLICATION_STRATEGY,
        PackageFeature.DEADLINE_TIMELINE,
        PackageFeature.MOTIVATION_LETTER_TRAINING,
        PackageFeature.CV_TRAINING,
        PackageFeature.AI_FEEDBACK,
    },
    PackageTier.GUIDED_SUPPORT: {
        # All Application Prep features
        PackageFeature.BASIC_QUIZ,
        PackageFeature.UNIVERSITY_RECOMMENDATIONS,
        PackageFeature.ADVANCED_AI_COMPARISONS,
        PackageFeature.RANKED_RECOMMENDATIONS,
        PackageFeature.TRADEOFF_ANALYSIS,
        PackageFeature.ADMISSION_PROBABILITY,
        PackageFeature.PDF_SUMMARY,
        PackageFeature.UNLIMITED_AI_CHAT,
        PackageFeature.APPLICATION_STRATEGY,
        PackageFeature.DEADLINE_TIMELINE,
        PackageFeature.MOTIVATION_LETTER_TRAINING,
        PackageFeature.CV_TRAINING,
        PackageFeature.AI_FEEDBACK,
        # Plus package 3 features
        PackageFeature.VIDEO_COUNSELING,
        PackageFeature.HUMAN_GUIDANCE,
        PackageFeature.DOCUMENT_CHECKS,
        PackageFeature.SUBMISSION_PREP,
        PackageFeature.DEADLINE_TRACKING,
        PackageFeature.PEER_INSIGHTS,
    },
}


def has_feature_access(package: PackageTier, feature: PackageFeature) -> bool:
    """Check if a package tier includes access to a specific feature."""
    return feature in PACKAGE_FEATURES.get(package, set())


def get_package_features(package: PackageTier) -> List[PackageFeature]:
    """Get all features available for a package tier."""
    return list(PACKAGE_FEATURES.get(package, set()))


def can_download_pdf(package: PackageTier) -> bool:
    """
    Check if user with given package can download PDF summaries.
    This is a helper for the specific feature you mentioned.
    """
    return has_feature_access(package, PackageFeature.PDF_SUMMARY)
