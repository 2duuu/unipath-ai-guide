/**
 * Button component for claiming a package
 * Simulates payment flow but claims package for free (testing)
 * Architecture ready for payment gateway integration
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CreditCard, CheckCircle2, Loader2, TrendingUp, TrendingDown, AlertTriangle, BadgeCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { claimPackage, getPackageInfo } from '@/services/packages';
import { PackageTier, isUpgrade, isDowngrade, getNextTierUp, PACKAGE_DETAILS } from '@/lib/packages';
import { useToast } from '@/hooks/use-toast';

interface ClaimPackageButtonProps {
  packageTier: PackageTier;
  packageName: string;
  className?: string;
  variant?: 'default' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  onSuccess?: () => void;
}

export function ClaimPackageButton({
  packageTier,
  packageName,
  className,
  variant = 'default',
  size = 'default',
  onSuccess,
}: ClaimPackageButtonProps) {
  const [isClaiming, setIsClaiming] = useState(false);
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);
  const [showPaymentDialog, setShowPaymentDialog] = useState(false);
  const [showDowngradeWarning, setShowDowngradeWarning] = useState(false);
  const [showUpgradeRecommendation, setShowUpgradeRecommendation] = useState(false);
  const [currentPackageTier, setCurrentPackageTier] = useState<PackageTier | null>(null);
  const [recommendedTier, setRecommendedTier] = useState<PackageTier | null>(null);
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    loadCurrentPackage();
  }, []);

  const loadCurrentPackage = async () => {
    try {
      const packageInfo = await getPackageInfo();
      setCurrentPackageTier(packageInfo.package_tier);
    } catch (error) {
      // User might not be logged in or no package info
      setCurrentPackageTier(PackageTier.FREE);
    }
  };

  const handlePaymentClick = async () => {
    // Check if user already has a package
    if (!currentPackageTier || currentPackageTier === PackageTier.FREE) {
      // User has FREE tier - navigate to checkout page to show upgrade
      navigate(`/pachete/checkout?package=${packageTier}&from=${currentPackageTier || PackageTier.FREE}`);
      return;
    }

    // User already has a package - check if upgrade or downgrade
    if (isDowngrade(currentPackageTier, packageTier)) {
      // Navigate to checkout page for downgrades
      navigate(`/pachete/checkout?package=${packageTier}&from=${currentPackageTier}`);
      return;
    } else if (isUpgrade(currentPackageTier, packageTier)) {
      // Navigate to checkout page for upgrades
      navigate(`/pachete/checkout?package=${packageTier}&from=${currentPackageTier}`);
      return;
    } else {
      // Same package
      toast({
        title: 'Already Purchased',
        description: 'You already have this package!',
      });
    }
  };

  const handleConfirmPurchase = async () => {
    setShowPaymentDialog(false);
    
    // Check if we should recommend upgrade before purchase
    if (currentPackageTier === PackageTier.FREE && packageTier !== PackageTier.GUIDED_SUPPORT) {
      const nextTier = getNextTierUp(packageTier);
      if (nextTier) {
        setRecommendedTier(nextTier);
        setShowUpgradeRecommendation(true);
        return;
      }
    }
    
    // Simulate payment processing
    try {
      setIsClaiming(true);
      
      // TODO: In production, integrate with payment gateway here
      // const paymentResult = await processPayment(packageTier, amount);
      // if (!paymentResult.success) throw new Error(paymentResult.error);
      
      // Simulate payment delay (remove in production)
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Claim package after "payment" success
      const result = await claimPackage(packageTier);
      
      setShowSuccessDialog(true);
      
      toast({
        title: 'Payment Successful!',
        description: result.message,
      });

      // Refresh current package
      await loadCurrentPackage();

      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to process purchase';
      
      if (errorMessage.includes('already have')) {
        toast({
          title: 'Already Purchased',
          description: 'You already have this package!',
          variant: 'default',
        });
      } else {
        toast({
          title: 'Error',
          description: errorMessage,
          variant: 'destructive',
        });
      }
    } finally {
      setIsClaiming(false);
    }
  };

  // Check if user already owns this package
  const isOwnedPackage = currentPackageTier === packageTier;

  // Determine button text and icon
  const getButtonContent = () => {
    if (isClaiming) {
      return (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Processing...
        </>
      );
    }

    // If user already owns this package
    if (isOwnedPackage) {
      return (
        <>
          <BadgeCheck className="mr-2 h-4 w-4" />
          Current Package
        </>
      );
    }

    if (!currentPackageTier || currentPackageTier === PackageTier.FREE) {
      return (
        <>
          <TrendingUp className="mr-2 h-4 w-4" />
          Upgrade
        </>
      );
    }

    if (isUpgrade(currentPackageTier, packageTier)) {
      return (
        <>
          <TrendingUp className="mr-2 h-4 w-4" />
          Upgrade
        </>
      );
    }

    if (isDowngrade(currentPackageTier, packageTier)) {
      return (
        <>
          <TrendingDown className="mr-2 h-4 w-4" />
          Downgrade
        </>
      );
    }

    return (
      <>
        <CreditCard className="mr-2 h-4 w-4" />
        Get Package
      </>
    );
  };

  return (
    <>
      <Button
        onClick={handlePaymentClick}
        disabled={isClaiming || isOwnedPackage}
        className={className}
        variant={isOwnedPackage ? 'secondary' : variant}
        size={size}
      >
        {getButtonContent()}
      </Button>

      {/* Success Dialog */}
      <Dialog open={showSuccessDialog} onOpenChange={setShowSuccessDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-green-600" />
              Package Claimed Successfully!
            </DialogTitle>
            <DialogDescription className="pt-4">
              You now have access to the <strong>{packageName}</strong> package and all its premium features!
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="rounded-lg bg-green-50 dark:bg-green-950 p-4">
              <h4 className="font-semibold mb-2 text-green-900 dark:text-green-100">
                New Features Unlocked:
              </h4>
              <ul className="space-y-1 text-sm text-green-800 dark:text-green-200">
                <li>✓ Advanced AI Comparisons</li>
                <li>✓ Ranked Recommendations</li>
                <li>✓ Trade-off Analysis</li>
                <li>✓ Admission Probability</li>
                <li>✓ PDF Summary Download</li>
                <li>✓ Unlimited AI Chat</li>
              </ul>
            </div>
          </div>

          <DialogFooter>
            <Button onClick={() => {
              setShowSuccessDialog(false);
              // Refresh the page to update package info
              window.location.reload();
            }}>
              Start Using Features
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Payment Confirmation Dialog */}
      <Dialog open={showPaymentDialog} onOpenChange={setShowPaymentDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <CreditCard className="h-5 w-5 text-primary" />
              Confirm Package Purchase
            </DialogTitle>
            <DialogDescription className="pt-4">
              You're about to purchase the <strong>{packageName}</strong> package.
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="rounded-lg bg-muted p-4">
              <h4 className="font-semibold mb-2">{packageName}</h4>
              <p className="text-sm text-muted-foreground mb-4">
                This package includes all premium features to help you make the best academic decision.
              </p>
              <div className="bg-blue-50 dark:bg-blue-950 p-3 rounded border border-blue-200 dark:border-blue-800">
                <p className="text-sm text-blue-800 dark:text-blue-200">
                  ℹ️ <strong>Test Mode:</strong> Payment gateway integration coming soon. 
                  For now, packages are available for free testing.
                </p>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button 
              variant="outline" 
              onClick={() => setShowPaymentDialog(false)}
              disabled={isClaiming}
            >
              Cancel
            </Button>
            <Button 
              onClick={handleConfirmPurchase}
              disabled={isClaiming}
            >
              {isClaiming ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processing...
                </>
              ) : (
                'Confirm Purchase'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Downgrade Warning Dialog */}
      <Dialog open={showDowngradeWarning} onOpenChange={setShowDowngradeWarning}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <TrendingDown className="h-5 w-5 text-orange-600" />
              Confirm Downgrade
            </DialogTitle>
            <DialogDescription className="pt-4">
              You're about to downgrade from <strong>{currentPackageTier && PACKAGE_DETAILS[currentPackageTier]?.displayName}</strong> to <strong>{packageName}</strong>.
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="rounded-lg bg-orange-50 dark:bg-orange-950 p-4 border border-orange-200 dark:border-orange-800">
              <h4 className="font-semibold mb-2 text-orange-900 dark:text-orange-100 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4" />
                Warning: You will lose access to:
              </h4>
              <ul className="space-y-1 text-sm text-orange-800 dark:text-orange-200">
                <li>• Advanced features from your current package</li>
                <li>• Premium AI comparisons and insights</li>
                <li>• Some tools and resources</li>
                <li>• Higher tier support options</li>
              </ul>
              <p className="mt-3 text-sm font-medium text-orange-900 dark:text-orange-100">
                Are you sure you want to continue?
              </p>
            </div>
          </div>

          <DialogFooter>
            <Button 
              variant="outline" 
              onClick={() => setShowDowngradeWarning(false)}
            >
              Cancel
            </Button>
            <Button 
              variant="destructive"
              onClick={() => {
                setShowDowngradeWarning(false);
                setShowPaymentDialog(true);
              }}
            >
              Yes, Downgrade
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Upgrade Recommendation Dialog */}
      <Dialog open={showUpgradeRecommendation} onOpenChange={setShowUpgradeRecommendation}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-blue-600" />
              Consider Upgrading!
            </DialogTitle>
            <DialogDescription className="pt-4">
              We noticed you're purchasing <strong>{packageName}</strong>. 
              {recommendedTier && (
                <> Have you considered <strong>{PACKAGE_DETAILS[recommendedTier]?.displayName}</strong>?</>
              )}
            </DialogDescription>
          </DialogHeader>
          
          {recommendedTier && (
            <div className="py-4">
              <div className="rounded-lg bg-blue-50 dark:bg-blue-950 p-4 border border-blue-200 dark:border-blue-800">
                <h4 className="font-semibold mb-2 text-blue-900 dark:text-blue-100">
                  {PACKAGE_DETAILS[recommendedTier]?.displayName} - €{PACKAGE_DETAILS[recommendedTier]?.price}
                </h4>
                <p className="text-sm text-blue-800 dark:text-blue-200 mb-3">
                  {PACKAGE_DETAILS[recommendedTier]?.description}
                </p>
                <div className="bg-white dark:bg-gray-900 p-3 rounded">
                  <p className="text-sm font-medium mb-2">Additional benefits:</p>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    {recommendedTier === PackageTier.APPLICATION_PREP && (
                      <>
                        <li>✓ Application Strategy Guide</li>
                        <li>✓ Deadline Timeline</li>
                        <li>✓ Motivation Letter Training</li>
                        <li>✓ CV Training & AI Feedback</li>
                      </>
                    )}
                    {recommendedTier === PackageTier.GUIDED_SUPPORT && (
                      <>
                        <li>✓ Video Counseling Sessions</li>
                        <li>✓ Human Expert Guidance</li>
                        <li>✓ Document Checks</li>
                        <li>✓ Submission Preparation</li>
                      </>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          )}

          <DialogFooter className="flex-col sm:flex-row gap-2">
            <Button 
              variant="outline" 
              onClick={async () => {
                setShowUpgradeRecommendation(false);
                // Continue with original purchase
                try {
                  setIsClaiming(true);
                  await new Promise(resolve => setTimeout(resolve, 1500));
                  const result = await claimPackage(packageTier);
                  setShowSuccessDialog(true);
                  toast({
                    title: 'Payment Successful!',
                    description: result.message,
                  });
                  await loadCurrentPackage();
                  if (onSuccess) onSuccess();
                } catch (error) {
                  const errorMessage = error instanceof Error ? error.message : 'Failed to process purchase';
                  toast({
                    title: 'Error',
                    description: errorMessage,
                    variant: 'destructive',
                  });
                } finally {
                  setIsClaiming(false);
                }
              }}
              className="w-full sm:w-auto"
            >
              No, Keep {packageName}
            </Button>
            <Button 
              onClick={() => {
                setShowUpgradeRecommendation(false);
                // Switch to recommended tier
                if (recommendedTier) {
                  // The parent component should handle showing this package's button
                  toast({
                    title: 'Great Choice!',
                    description: `Please select the ${PACKAGE_DETAILS[recommendedTier]?.displayName} package below.`,
                  });
                }
              }}
              className="w-full sm:w-auto"
            >
              Yes, Upgrade to Better Package
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
