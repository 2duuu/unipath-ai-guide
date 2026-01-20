/**
 * Packages page - Shows available packages and allows claiming
 */

import { useState, useEffect } from 'react';
import { PackageInfoCard } from '@/components/PackageInfoCard';
import { ClaimPackageButton } from '@/components/ClaimPackageButton';
import { PackageTier, PACKAGE_DETAILS } from '@/lib/packages';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2 } from 'lucide-react';

const PACKAGE_FEATURES = {
  [PackageTier.FREE]: [
    'Basic Academic Quiz',
    'University Recommendations',
  ],
  [PackageTier.DECISION_CLARITY]: [
    'Everything in Free',
    'Advanced AI Comparisons',
    'Ranked Recommendations',
    'Trade-off Analysis',
    'Admission Probability',
    'PDF Summary Download',
    'Unlimited AI Chat',
  ],
  [PackageTier.APPLICATION_PREP]: [
    'Everything in Choose Confidently',
    'Application Strategy Guide',
    'Deadline Timeline',
    'Motivation Letter Training',
    'CV Training',
    'AI Document Feedback',
  ],
  [PackageTier.GUIDED_SUPPORT]: [
    'Everything in Prepare to Apply',
    'Video Counseling Sessions',
    'Human Expert Guidance',
    'Document Checks',
    'Submission Preparation',
    'Deadline Tracking',
    'Peer Insights',
  ],
};

export default function PackagesPage() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleClaimSuccess = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Choose Your Package</h1>
          <p className="text-xl text-muted-foreground">
            Unlock premium features to make the best decision for your academic future
          </p>
        </div>

        {/* Current Package */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-4">Your Current Package</h2>
          <PackageInfoCard key={refreshKey} />
        </div>

        {/* Available Packages */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-6">Available Packages</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.values(PackageTier).map((tier) => {
              const details = PACKAGE_DETAILS[tier];
              const features = PACKAGE_FEATURES[tier];
              const isFree = tier === PackageTier.FREE;
              const isClaimable = tier === PackageTier.DECISION_CLARITY;

              return (
                <Card 
                  key={tier} 
                  className={`flex flex-col ${isClaimable ? 'border-primary shadow-lg' : ''}`}
                >
                  <CardHeader>
                    <div className="flex items-center justify-between mb-2">
                      <CardTitle className="text-lg">{details.displayName}</CardTitle>
                      {isClaimable && (
                        <Badge variant="default" className="bg-green-600">
                          FREE
                        </Badge>
                      )}
                    </div>
                    <CardDescription>{details.description}</CardDescription>
                    <div className="mt-4">
                      <span className="text-3xl font-bold">
                        {details.price === '0' ? 'Free' : `€${details.price}`}
                      </span>
                      {details.price !== '0' && !isClaimable && (
                        <span className="text-sm text-muted-foreground ml-1">one-time</span>
                      )}
                    </div>
                  </CardHeader>
                  
                  <CardContent className="flex-1">
                    <ul className="space-y-2">
                      {features.map((feature, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                  
                  <CardFooter>
                    {isFree ? (
                      <Badge variant="outline" className="w-full justify-center py-2">
                        Current Plan
                      </Badge>
                    ) : (
                      <ClaimPackageButton
                        packageTier={tier}
                        packageName={details.displayName}
                        className="w-full"
                        onSuccess={handleClaimSuccess}
                      />
                    )}
                  </CardFooter>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-12 p-6 rounded-lg bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800">
          <h3 className="font-semibold text-lg mb-2 text-blue-900 dark:text-blue-100">
            🎉 Special Offer: Choose Confidently Package FREE!
          </h3>
          <p className="text-blue-800 dark:text-blue-200">
            For a limited time, claim the "Choose Confidently" package for free! Get access to advanced AI comparisons, 
            PDF downloads, and more premium features to help you make the best academic decision.
          </p>
        </div>
      </div>
    </div>
  );
}
