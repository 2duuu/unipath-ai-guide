/**
 * Button component for claiming a package
 * Simulates payment flow but claims package for free (testing)
 * Architecture ready for payment gateway integration
 */

import { useState } from 'react';
import { CreditCard, CheckCircle2, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { claimPackage } from '@/services/packages';
import { PackageTier } from '@/lib/packages';
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
  const { toast } = useToast();

  const handlePaymentClick = async () => {
    // Show payment dialog first
    setShowPaymentDialog(true);
  };

  const handleConfirmPurchase = async () => {
    setShowPaymentDialog(false);
    
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

  return (
    <>
      <Button
        onClick={handlePaymentClick}
        disabled={isClaiming}
        className={className}
        variant={variant}
        size={size}
      >
        {isClaiming ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Processing...
          </>
        ) : (
          <>
            <CreditCard className="mr-2 h-4 w-4" />
            Get Package
          </>
        )}
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
    </>
  );
}
