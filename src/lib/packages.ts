/**
 * Package utilities and types for frontend
 */

export enum PackageTier {
  FREE = 'free',
  DECISION_CLARITY = 'decision_clarity',
  APPLICATION_PREP = 'application_prep',
  GUIDED_SUPPORT = 'guided_support',
}

export enum PackageFeature {
  BASIC_QUIZ = 'basic_quiz',
  UNIVERSITY_RECOMMENDATIONS = 'university_recommendations',
  ADVANCED_AI_COMPARISONS = 'advanced_ai_comparisons',
  RANKED_RECOMMENDATIONS = 'ranked_recommendations',
  TRADEOFF_ANALYSIS = 'tradeoff_analysis',
  ADMISSION_PROBABILITY = 'admission_probability',
  PDF_SUMMARY = 'pdf_summary',
  UNLIMITED_AI_CHAT = 'unlimited_ai_chat',
  APPLICATION_STRATEGY = 'application_strategy',
  DEADLINE_TIMELINE = 'deadline_timeline',
  MOTIVATION_LETTER_TRAINING = 'motivation_letter_training',
  CV_TRAINING = 'cv_training',
  AI_FEEDBACK = 'ai_feedback',
  VIDEO_COUNSELING = 'video_counseling',
  HUMAN_GUIDANCE = 'human_guidance',
  DOCUMENT_CHECKS = 'document_checks',
  SUBMISSION_PREP = 'submission_prep',
  DEADLINE_TRACKING = 'deadline_tracking',
  PEER_INSIGHTS = 'peer_insights',
}

export interface PackageInfo {
  package_tier: PackageTier;
  purchased_at: string | null;
  expires_at: string | null;
  features: PackageFeature[];
}

export interface PackageDetails {
  name: string;
  displayName: string;
  price: string;
  description: string;
  tier: PackageTier;
}

export const PACKAGE_DETAILS: Record<PackageTier, PackageDetails> = {
  [PackageTier.FREE]: {
    name: 'Free',
    displayName: 'Academic Orientation',
    price: '0',
    description: 'Basic quiz and university recommendations',
    tier: PackageTier.FREE,
  },
  [PackageTier.DECISION_CLARITY]: {
    name: 'Choose Confidently',
    displayName: 'Decision & Clarity',
    price: '36.30',
    description: 'Advanced AI comparisons and PDF summaries',
    tier: PackageTier.DECISION_CLARITY,
  },
  [PackageTier.APPLICATION_PREP]: {
    name: 'Prepare to Apply',
    displayName: 'Application Preparation',
    price: '121',
    description: 'Complete application guidance and training',
    tier: PackageTier.APPLICATION_PREP,
  },
  [PackageTier.GUIDED_SUPPORT]: {
    name: 'Apply with Support',
    displayName: 'Guided Application Support',
    price: '484',
    description: 'Full 1-on-1 support throughout application process',
    tier: PackageTier.GUIDED_SUPPORT,
  },
};

export function hasFeature(packageInfo: PackageInfo, feature: PackageFeature): boolean {
  return packageInfo.features.includes(feature);
}

export function canDownloadPDF(packageInfo: PackageInfo): boolean {
  return hasFeature(packageInfo, PackageFeature.PDF_SUMMARY);
}

export function getPackageDisplayName(tier: PackageTier): string {
  return PACKAGE_DETAILS[tier]?.displayName || 'Unknown';
}
