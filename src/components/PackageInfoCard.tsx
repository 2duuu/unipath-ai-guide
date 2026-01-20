/**
 * Component to display user's package info and feature access
 */

import { useState, useEffect } from 'react';
import { getPackageInfo } from '@/services/packages';
import { PackageInfo, PACKAGE_DETAILS, PackageFeature } from '@/lib/packages';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2 } from 'lucide-react';

const FEATURE_LABELS: Record<PackageFeature, string> = {
  [PackageFeature.BASIC_QUIZ]: 'Basic Academic Quiz',
  [PackageFeature.UNIVERSITY_RECOMMENDATIONS]: 'University Recommendations',
  [PackageFeature.ADVANCED_AI_COMPARISONS]: 'Advanced AI Comparisons',
  [PackageFeature.RANKED_RECOMMENDATIONS]: 'Ranked Recommendations',
  [PackageFeature.TRADEOFF_ANALYSIS]: 'Trade-off Analysis',
  [PackageFeature.ADMISSION_PROBABILITY]: 'Admission Probability',
  [PackageFeature.PDF_SUMMARY]: 'PDF Summary Download',
  [PackageFeature.UNLIMITED_AI_CHAT]: 'Unlimited AI Chat',
  [PackageFeature.APPLICATION_STRATEGY]: 'Application Strategy Guide',
  [PackageFeature.DEADLINE_TIMELINE]: 'Deadline Timeline',
  [PackageFeature.MOTIVATION_LETTER_TRAINING]: 'Motivation Letter Training',
  [PackageFeature.CV_TRAINING]: 'CV Training',
  [PackageFeature.AI_FEEDBACK]: 'AI Document Feedback',
  [PackageFeature.VIDEO_COUNSELING]: 'Video Counseling Sessions',
  [PackageFeature.HUMAN_GUIDANCE]: 'Human Expert Guidance',
  [PackageFeature.DOCUMENT_CHECKS]: 'Document Checks',
  [PackageFeature.SUBMISSION_PREP]: 'Submission Preparation',
  [PackageFeature.DEADLINE_TRACKING]: 'Deadline Tracking',
  [PackageFeature.PEER_INSIGHTS]: 'Peer Insights',
};

export function PackageInfoCard() {
  const [packageInfo, setPackageInfo] = useState<PackageInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPackageInfo();
  }, []);

  const loadPackageInfo = async () => {
    try {
      setLoading(true);
      setError(null);
      const info = await getPackageInfo();
      setPackageInfo(info);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load package info');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Package</CardTitle>
          <CardDescription>Loading...</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Package</CardTitle>
          <CardDescription className="text-destructive">{error}</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  if (!packageInfo) {
    return null;
  }

  const packageDetails = PACKAGE_DETAILS[packageInfo.package_tier];

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>{packageDetails.displayName}</CardTitle>
            <CardDescription>{packageDetails.description}</CardDescription>
          </div>
          <Badge variant="default" className="text-lg">
            {packageDetails.price === '0' ? 'Free' : `€${packageDetails.price}`}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {packageInfo.purchased_at && (
            <div className="text-sm text-muted-foreground">
              Purchased: {new Date(packageInfo.purchased_at).toLocaleDateString()}
            </div>
          )}
          
          <div>
            <h4 className="font-semibold mb-2">Available Features</h4>
            <ul className="space-y-2">
              {packageInfo.features.map((feature) => (
                <li key={feature} className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  <span className="text-sm">{FEATURE_LABELS[feature]}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
