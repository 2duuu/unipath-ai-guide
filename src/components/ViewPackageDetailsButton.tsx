/**
 * Button component to view package details
 * Shows package information without initiating purchase
 */

import { useState } from 'react';
import { Info } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { PackageTier, PACKAGE_DETAILS } from '@/lib/packages';
import { CheckCircle2 } from 'lucide-react';

interface ViewPackageDetailsButtonProps {
  packageTier: PackageTier;
  packageFeatures: string[];
  className?: string;
  variant?: 'default' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

export function ViewPackageDetailsButton({
  packageTier,
  packageFeatures,
  className,
  variant = 'outline',
  size = 'default',
}: ViewPackageDetailsButtonProps) {
  const [showDetailsDialog, setShowDetailsDialog] = useState(false);
  const packageDetails = PACKAGE_DETAILS[packageTier];

  return (
    <>
      <Button
        onClick={() => setShowDetailsDialog(true)}
        className={className}
        variant={variant}
        size={size}
      >
        <Info className="mr-2 h-4 w-4" />
        View Details
      </Button>

      {/* Package Details Dialog */}
      <Dialog open={showDetailsDialog} onOpenChange={setShowDetailsDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              {packageDetails.displayName}
            </DialogTitle>
            <DialogDescription className="pt-2">
              {packageDetails.description}
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            {/* Price */}
            <div className="mb-6">
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold">
                  €{packageDetails.price}
                </span>
                <span className="text-sm text-muted-foreground">one-time payment</span>
              </div>
              <div className="mt-2">
                <span className="text-green-600 font-semibold text-sm">
                  FREE during testing phase
                </span>
              </div>
            </div>

            {/* Features List */}
            <div className="rounded-lg bg-muted p-4">
              <h4 className="font-semibold mb-3">What's included:</h4>
              <ul className="space-y-2">
                {packageFeatures.map((feature, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Info Box */}
            <div className="mt-4 bg-blue-50 dark:bg-blue-950 p-3 rounded border border-blue-200 dark:border-blue-800">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                ℹ️ <strong>Note:</strong> All packages are currently free during our testing phase. 
                Payment gateway integration coming soon.
              </p>
            </div>
          </div>

          <DialogFooter>
            <Button 
              variant="outline" 
              onClick={() => setShowDetailsDialog(false)}
            >
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
