/**
 * Button component for downloading PDF recommendations
 * Includes package access check and upgrade prompt
 */

import { useState } from 'react';
import { Download, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { triggerPDFDownload } from '@/services/packages';
import { useToast } from '@/hooks/use-toast';

interface DownloadPDFButtonProps {
  className?: string;
  variant?: 'default' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

export function DownloadPDFButton({
  className,
  variant = 'default',
  size = 'default',
}: DownloadPDFButtonProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [showUpgradeDialog, setShowUpgradeDialog] = useState(false);
  const { toast } = useToast();

  const handleDownload = async () => {
    try {
      setIsDownloading(true);
      await triggerPDFDownload();
      toast({
        title: 'Success',
        description: 'PDF downloaded successfully!',
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to download PDF';
      
      // Check if error is due to package restriction
      if (errorMessage.includes('Choose Confidently') || errorMessage.includes('package')) {
        setShowUpgradeDialog(true);
      } else {
        toast({
          title: 'Error',
          description: errorMessage,
          variant: 'destructive',
        });
      }
    } finally {
      setIsDownloading(false);
    }
  };

  const handleUpgradeClick = () => {
    setShowUpgradeDialog(false);
    // Navigate to pricing section
    const pricingSection = document.getElementById('pricing');
    if (pricingSection) {
      pricingSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <>
      <Button
        onClick={handleDownload}
        disabled={isDownloading}
        className={className}
        variant={variant}
        size={size}
      >
        {isDownloading ? (
          <>
            <Download className="mr-2 h-4 w-4 animate-pulse" />
            Downloading...
          </>
        ) : (
          <>
            <Download className="mr-2 h-4 w-4" />
            Download PDF Summary
          </>
        )}
      </Button>

      <Dialog open={showUpgradeDialog} onOpenChange={setShowUpgradeDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Lock className="h-5 w-5 text-amber-600" />
              Upgrade Required
            </DialogTitle>
            <DialogDescription className="pt-4">
              PDF download is a premium feature available with the{' '}
              <strong>Choose Confidently</strong> package or higher.
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="rounded-lg bg-muted p-4">
              <h4 className="font-semibold mb-2">Choose Confidently Package - €36.30</h4>
              <ul className="space-y-1 text-sm">
                <li>✓ Advanced AI Comparisons</li>
                <li>✓ Ranked Recommendations</li>
                <li>✓ Trade-off Analysis</li>
                <li>✓ PDF Summary Download</li>
                <li>✓ And more...</li>
              </ul>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowUpgradeDialog(false)}>
              Maybe Later
            </Button>
            <Button onClick={handleUpgradeClick}>
              View Packages
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
