/**
 * Package Checkout Page
 * Displays package details and allows user to confirm purchase
 */

import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle2, Info, CreditCard, ArrowLeft, Loader2, AlertTriangle, TrendingUp, TrendingDown, X, ArrowRight, BadgeCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { PackageTier, PACKAGE_DETAILS, isDowngrade, isUpgrade } from '@/lib/packages';
import { claimPackage, getPackageInfo } from '@/services/packages';
import { useToast } from '@/hooks/use-toast';

const PACKAGE_FEATURES = {
  [PackageTier.FREE]: [
    'AI-guided initial questionnaire',
    'Basic university recommendations',
    'Access to the university database',
  ],
  [PackageTier.DECISION_CLARITY]: [
    'Everything in Decision & Clarity',
    'Advanced AI comparisons',
    'Ranked recommendations',
    'Trade-off analysis',
    'Admission probability',
    'PDF summary download',
    'Unlimited AI chat',
  ],
  [PackageTier.APPLICATION_PREP]: [
    'Everything in Decision & Clarity',
    'Personalized application strategy',
    'Deadlines and requirements timeline',
    'Motivation letter training',
    'Academic CV training',
    'AI-assisted feedback plus human guidance',
  ],
  [PackageTier.GUIDED_SUPPORT]: [
    'Everything in Application Prep',
    'Video counseling sessions',
    'Human expert guidance',
    'Document checks',
    'Submission preparation',
    'Deadline tracking',
    'Peer insights',
  ],
};

const PACKAGE_BENEFITS = {
  [PackageTier.FREE]: [
    { title: 'AI-guided initial questionnaire', description: 'Discover your priorities' },
    { title: 'Basic university recommendations', description: 'Get initial personalized suggestions' },
    { title: 'Database access', description: 'Explore your options' },
  ],
  [PackageTier.DECISION_CLARITY]: [
    { title: 'Advanced AI comparisons', description: 'Compare programs with detailed insights' },
    { title: 'Ranked recommendations', description: 'See options sorted by compatibility' },
    { title: 'PDF download', description: 'Export your results' },
  ],
  [PackageTier.APPLICATION_PREP]: [
    { title: 'Personalized application strategy', description: 'A custom plan for your applications' },
    { title: 'Deadlines and requirements timeline', description: 'Never miss a date again' },
    { title: 'Motivation letter training', description: 'Craft winning motivation letters' },
    { title: 'Academic CV training', description: 'Create professional CVs' },
    { title: 'AI-assisted feedback + human guidance', description: 'Get actionable improvement tips' },
  ],
  [PackageTier.GUIDED_SUPPORT]: [
    { title: 'Video counseling sessions', description: 'Speak directly with experts' },
    { title: 'Human expert guidance', description: '1:1 personalized support' },
    { title: 'Document checks', description: 'Make sure everything is correct' },
    { title: 'Submission preparation', description: 'Finalize applications perfectly' },
  ],
};

const PackageCheckout = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const packageTierParam = searchParams.get('package') as PackageTier | null;
  const fromTierParam = searchParams.get('from') as PackageTier | null;
  const [isProcessing, setIsProcessing] = useState(false);
  const [showPaymentDialog, setShowPaymentDialog] = useState(false);
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);
  const [currentPackage, setCurrentPackage] = useState<PackageTier | null>(null);
  
  const isOwnedPackage = currentPackage && packageTierParam && currentPackage === packageTierParam;
  const isDowngradeFlow = fromTierParam && packageTierParam && isDowngrade(fromTierParam, packageTierParam);
  const isUpgradeFlow = fromTierParam && packageTierParam && isUpgrade(fromTierParam, packageTierParam) && !isOwnedPackage;

  useEffect(() => {
    if (!packageTierParam || !Object.values(PackageTier).includes(packageTierParam)) {
      navigate('/pachete');
      return;
    }
    
    loadCurrentPackage();
  }, [packageTierParam, navigate]);

  const loadCurrentPackage = async () => {
    try {
      const info = await getPackageInfo();
      setCurrentPackage(info.package_tier);
    } catch (error) {
      setCurrentPackage(PackageTier.FREE);
    }
  };

  if (!packageTierParam) return null;

  const packageDetails = PACKAGE_DETAILS[packageTierParam];
  const features = PACKAGE_FEATURES[packageTierParam] || [];
  const benefits = PACKAGE_BENEFITS[packageTierParam] || [];

  // Calculate upgrade price (difference between packages)
  const getUpgradePrice = (): number => {
    if (isDowngradeFlow || packageTierParam === PackageTier.FREE) {
      return 0;
    }
    
    if (isUpgradeFlow && fromTierParam) {
      const currentPrice = parseFloat(PACKAGE_DETAILS[fromTierParam].price);
      const newPrice = parseFloat(packageDetails.price);
      return Math.max(0, newPrice - currentPrice);
    }
    
    // New purchase (from FREE or no package)
    return parseFloat(packageDetails.price);
  };

  const upgradePrice = getUpgradePrice();
  const displayPrice = upgradePrice.toFixed(2);

  // Get next package in circular loop (includes FREE)
  const getNextPackage = (): PackageTier => {
    const allPackages = [
      PackageTier.FREE,
      PackageTier.DECISION_CLARITY,
      PackageTier.APPLICATION_PREP,
      PackageTier.GUIDED_SUPPORT,
    ];
    const currentIndex = allPackages.indexOf(packageTierParam);
    const nextIndex = (currentIndex + 1) % allPackages.length;
    return allPackages[nextIndex];
  };

  const handleViewNextPackage = () => {
    const nextPackage = getNextPackage();
    // Use the user's actual current package (not the viewed package) to determine upgrade/downgrade
    const fromPackage = currentPackage || PackageTier.FREE;
    navigate(`/pachete/checkout?package=${nextPackage}&from=${fromPackage}`);
  };

  const handleConfirmPurchase = () => {
    setShowPaymentDialog(true);
  };

  const handlePaymentConfirm = async () => {
    setShowPaymentDialog(false);
    setIsProcessing(true);

    try {
      // Simulate payment gateway processing
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Claim package
      const result = await claimPackage(packageTierParam);

      // Dispatch event to update navbar
      window.dispatchEvent(new CustomEvent('packageUpdated'));

      setShowSuccessDialog(true);

      toast({
        title: 'Payment successful!',
        description: result.message,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error while processing payment';
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8 pt-24">
        <div className="max-w-6xl mx-auto">
          {/* Back Button */}
          <Button
            variant="ghost"
            onClick={() => navigate('/pachete')}
            className="mb-6"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            See other packages
          </Button>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Package Details */}
            <div className="lg:col-span-2 space-y-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <Card className={isDowngradeFlow ? 'border-orange-500 border-2' : isUpgradeFlow ? 'border-green-600 border-2' : isOwnedPackage ? 'border-blue-500 border-2' : ''}>
                  <CardHeader>
                    <div className="flex items-center gap-2 mb-2">
                      {isDowngradeFlow ? (
                        <>
                          <AlertTriangle className="h-5 w-5 text-orange-500" />
                          <span className="text-sm font-semibold text-orange-500">Downgrade</span>
                        </>
                      ) : isOwnedPackage ? (
                        <>
                          <BadgeCheck className="h-5 w-5 text-blue-500" />
                          <span className="text-sm font-semibold text-blue-500">Your Current Plan</span>
                        </>
                      ) : (
                        <>
                          <TrendingUp className="h-5 w-5 text-green-600" />
                          <span className="text-sm font-semibold text-green-600">Upgrade</span>
                        </>
                      )}
                    </div>
                    <CardTitle className="text-3xl">{packageDetails.displayName}</CardTitle>
                    <div className="text-lg text-muted-foreground mt-2">
                      {packageDetails.description}
                    </div>
                    {isDowngradeFlow && fromTierParam && (
                      <div className="mt-4 p-3 bg-orange-50 dark:bg-orange-950 rounded-lg border border-orange-200 dark:border-orange-800">
                        <p className="text-sm text-orange-800 dark:text-orange-200">
                          <strong>Heads up:</strong> You are switching from <strong>{PACKAGE_DETAILS[fromTierParam].displayName}</strong> to <strong>{packageDetails.displayName}</strong>.
                          You will lose access to premium features.
                        </p>
                      </div>
                    )}
                    {isUpgradeFlow && fromTierParam && (
                      <div className="mt-4 p-3 bg-green-50 dark:bg-green-950 rounded-lg border border-green-200 dark:border-green-800">
                        <p className="text-sm text-green-800 dark:text-green-200">
                          <strong>Upgrade:</strong> You're moving from <strong>{PACKAGE_DETAILS[fromTierParam].displayName}</strong> to <strong>{packageDetails.displayName}</strong>.
                          You'll gain additional premium features.
                        </p>
                      </div>
                    )}
                    {isOwnedPackage && (
                      <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
                        <p className="text-sm text-blue-800 dark:text-blue-200">
                          <strong>Active:</strong> This plan is already active on your account.
                          You already have access to all included features.
                        </p>
                      </div>
                    )}
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* New Features Highlight for Upgrade */}
                    {isUpgradeFlow && fromTierParam && (
                      <div className="bg-green-50 dark:bg-green-950 p-4 rounded-lg border border-green-200 dark:border-green-800">
                        <div className="flex items-start gap-3 mb-3">
                          <TrendingUp className="h-5 w-5 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <h3 className="font-semibold text-lg text-green-900 dark:text-green-100 mb-2">
                              New features you'll gain
                            </h3>
                            <p className="text-sm text-green-800 dark:text-green-200 mb-3">
                              By switching to {packageDetails.displayName}, you'll get access to:
                            </p>
                          </div>
                        </div>
                        <ul className="space-y-2 ml-8">
                          {PACKAGE_FEATURES[packageTierParam]
                            ?.filter(feature => !PACKAGE_FEATURES[fromTierParam]?.includes(feature))
                            .map((feature, i) => (
                              <li key={i} className="flex items-start gap-2 text-sm text-green-800 dark:text-green-200">
                                <CheckCircle2 className="w-4 h-4 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
                                <span>{feature}</span>
                              </li>
                            ))
                          }
                        </ul>
                      </div>
                    )}
                    
                    {/* Lost Features Warning for Downgrade */}
                    {isDowngradeFlow && fromTierParam && (
                      <div className="bg-orange-50 dark:bg-orange-950 p-4 rounded-lg border border-orange-200 dark:border-orange-800">
                        <div className="flex items-start gap-3 mb-3">
                          <AlertTriangle className="h-5 w-5 text-orange-600 dark:text-orange-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <h3 className="font-semibold text-lg text-orange-900 dark:text-orange-100 mb-2">
                              Features you'll lose
                            </h3>
                            <p className="text-sm text-orange-800 dark:text-orange-200 mb-3">
                              By switching to {packageDetails.displayName}, you will no longer have access to:
                            </p>
                          </div>
                        </div>
                        <ul className="space-y-2 ml-8">
                          {PACKAGE_FEATURES[fromTierParam]
                            ?.filter(feature => !PACKAGE_FEATURES[packageTierParam]?.includes(feature))
                            .map((feature, i) => (
                              <li key={i} className="flex items-start gap-2 text-sm text-orange-800 dark:text-orange-200">
                                <X className="w-4 h-4 text-orange-600 dark:text-orange-400 mt-0.5 flex-shrink-0" />
                                <span>{feature}</span>
                              </li>
                            ))
                          }
                        </ul>
                      </div>
                    )}
                    
                    {/* Main Benefits Grid */}
                    <div>
                      <h3 className="font-semibold text-lg mb-4">
                        {isDowngradeFlow ? 'What you keep' : isUpgradeFlow ? 'What you keep + new features' : isOwnedPackage ? 'Your current benefits' : 'Key benefits'}
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {benefits.slice(0, 6).map((benefit, index) => (
                          <div key={index} className="p-4 rounded-lg bg-muted">
                            <div className="flex items-start gap-2">
                              <CheckCircle2 className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                              <div>
                                <div className="font-medium text-sm">{benefit.title}</div>
                                <div className="text-xs text-muted-foreground mt-1">
                                  {benefit.description}
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* What You Get */}
                    <div>
                      <h3 className="font-semibold text-lg mb-4">What you get</h3>
                      <div className="space-y-2">
                        {features.map((feature, index) => (
                          <div key={index} className="flex items-start gap-2">
                            <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                            <span className="text-sm">{feature}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Disclaimer */}
                    <div className="mt-6 p-4 rounded-lg bg-muted text-sm text-muted-foreground italic">
                      Boundary: UniHub provides guidance and training. All application materials are
                      written by the student.
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>

            {/* Right Column - Payment Summary */}
            <div className="lg:col-span-1">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="sticky top-24"
              >
                <Card className={isDowngradeFlow ? 'border-orange-500 border-2' : isUpgradeFlow ? 'border-green-600 border-2' : isOwnedPackage ? 'border-blue-500 border-2' : ''}>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      {isDowngradeFlow ? (
                        <>
                          <TrendingDown className="h-5 w-5 text-orange-500" />
                          <span>Confirm downgrade?</span>
                        </>
                      ) : isUpgradeFlow ? (
                        <>
                          <TrendingUp className="h-5 w-5 text-green-600" />
                          <span>Confirm upgrade?</span>
                        </>
                      ) : isOwnedPackage ? (
                        <>
                          <BadgeCheck className="h-5 w-5 text-blue-500" />
                          <span>Your Plan</span>
                        </>
                      ) : (
                        <>
                          <TrendingUp className="h-5 w-5 text-green-600" />
                          <span>Ready?</span>
                        </>
                      )}
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {isDowngradeFlow
                        ? 'You will lose premium features but your data will remain.'
                        : isUpgradeFlow
                        ? 'You will gain additional premium features immediately.'
                        : isOwnedPackage
                        ? 'This plan is already active. Explore other plans using the button below.'
                        : 'Confirm the plan and you will be taken to Payments & Invoices for instant confirmation.'}
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <div className="text-sm text-muted-foreground mb-1">Total</div>
                      <div className="flex items-baseline gap-2">
                        <span className="text-4xl font-bold">€{displayPrice}</span>
                      </div>
                      {isUpgradeFlow && fromTierParam && upgradePrice !== parseFloat(packageDetails.price) && (
                        <div className="text-xs text-muted-foreground mt-1">
                          Package price: €{packageDetails.price} - Previous package price: €{PACKAGE_DETAILS[fromTierParam].price}
                        </div>
                      )}
                      <div className="text-sm text-muted-foreground">{packageTierParam === PackageTier.FREE || isDowngradeFlow ? 'Free' : 'VAT included'}</div>
                      <div className="mt-2">
                        {isDowngradeFlow ? (
                          <span className="text-orange-600 font-semibold text-sm">
                            Downgrading is free
                          </span>
                        ) : packageTierParam === PackageTier.FREE ? (
                          <span className="text-blue-600 font-semibold text-sm">
                            Permanent free plan
                          </span>
                        ) : isUpgradeFlow && upgradePrice < parseFloat(packageDetails.price) ? (
                          <span className="text-green-600 font-semibold text-sm">
                            Pay only the price difference
                          </span>
                        ) : (
                          <span className="text-green-600 font-semibold text-sm">
                            FREE during the trial period
                          </span>
                        )}
                      </div>
                    </div>

                    {!isOwnedPackage && (
                      <Button
                        onClick={handleConfirmPurchase}
                        disabled={isProcessing}
                        className="w-full"
                        size="lg"
                        variant={isDowngradeFlow ? 'destructive' : 'default'}
                      >
                        {isProcessing ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Processing...
                          </>
                        ) : isDowngradeFlow ? (
                          <>
                            <TrendingDown className="mr-2 h-4 w-4" />
                            Confirm downgrade
                          </>
                        ) : isUpgradeFlow ? (
                          <>
                            <TrendingUp className="mr-2 h-4 w-4" />
                            Confirm upgrade
                          </>
                        ) : packageTierParam === PackageTier.FREE ? (
                          <>
                            <CheckCircle2 className="mr-2 h-4 w-4" />
                            Activate free plan
                          </>
                        ) : (
                          <>
                            <CreditCard className="mr-2 h-4 w-4" />
                            Confirm plan
                          </>
                        )}
                      </Button>
                    )}

                    <Button
                      variant="outline"
                      onClick={handleViewNextPackage}
                      className="w-full"
                    >
                      View next plan
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Payment Gateway Dialog */}
      <Dialog open={showPaymentDialog} onOpenChange={setShowPaymentDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              {isDowngradeFlow ? (
                <>
                  <AlertTriangle className="h-5 w-5 text-orange-500" />
                  <span>Downgrade Confirmation</span>
                </>
              ) : isUpgradeFlow ? (
                <>
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span>Upgrade Confirmation</span>
                </>
              ) : (
                <>
                  <CreditCard className="h-5 w-5 text-primary" />
                  <span>Payment Gateway</span>
                </>
              )}
            </DialogTitle>
            <DialogDescription className="pt-4">
              {isDowngradeFlow
                ? `Confirm switch to ${packageDetails.displayName}?`
                : isUpgradeFlow
                ? `Confirm upgrade to ${packageDetails.displayName}?`
                : `Processing payment for ${packageDetails.displayName}`}
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="rounded-lg bg-muted p-4">
              <h4 className="font-semibold mb-2">Payment details</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Plan:</span>
                  <span className="font-medium">{packageDetails.displayName}</span>
                </div>
                {isUpgradeFlow && fromTierParam && upgradePrice !== parseFloat(packageDetails.price) && (
                  <>
                    <div className="flex justify-between">
                      <span>New plan price:</span>
                      <span className="font-medium">€{packageDetails.price}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Current plan price:</span>
                      <span className="font-medium">-€{PACKAGE_DETAILS[fromTierParam].price}</span>
                    </div>
                    <div className="border-t pt-2 mt-2"></div>
                  </>
                )}
                <div className="flex justify-between">
                  <span>{isUpgradeFlow && upgradePrice !== parseFloat(packageDetails.price) ? 'Amount due (difference):' : 'Price:'}</span>
                  <span className="font-medium">€{displayPrice}</span>
                </div>
                <div className="flex justify-between">
                  <span>VAT:</span>
                  <span className="font-medium">{isDowngradeFlow || packageTierParam === PackageTier.FREE ? 'N/A' : 'Included'}</span>
                </div>
              </div>
              <div className="mt-4 bg-green-50 dark:bg-green-950 p-3 rounded border border-green-200 dark:border-green-800">
                <p className="text-sm text-green-800 dark:text-green-200">
                  {isDowngradeFlow ? (
                    <>
                      🎉 <strong>Free downgrade:</strong> You will not be charged to move to a lower plan.
                    </>
                  ) : packageTierParam === PackageTier.FREE ? (
                    <>
                      🎉 <strong>Free plan:</strong> This plan is and will remain free permanently.
                    </>
                  ) : (
                    <>
                      🎉 <strong>Testing:</strong> The payment will be marked as successful automatically.
                      A real payment gateway will be integrated soon.
                    </>
                  )}
                </p>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button 
              variant="outline" 
              onClick={() => setShowPaymentDialog(false)}
            >
              Cancel
            </Button>
            <Button onClick={handlePaymentConfirm}>
              Confirm payment
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Success Dialog */}
      <Dialog open={showSuccessDialog} onOpenChange={setShowSuccessDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-green-600" />
              {isDowngradeFlow ? 'Downgrade complete!' : isUpgradeFlow ? 'Upgrade complete!' : 'Payment successful!'}
            </DialogTitle>
            <DialogDescription className="pt-4">
              {isDowngradeFlow
                ? `You successfully moved to ${packageDetails.displayName}.`
                : isUpgradeFlow
                ? `You upgraded successfully to ${packageDetails.displayName}!`
                : `You successfully purchased ${packageDetails.displayName}!`}
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className={`rounded-lg p-4 ${
              isDowngradeFlow 
                ? 'bg-orange-50 dark:bg-orange-950'
                : isUpgradeFlow
                ? 'bg-green-50 dark:bg-green-950'
                : 'bg-green-50 dark:bg-green-950'
            }`}>
              <h4 className={`font-semibold mb-2 ${
                isDowngradeFlow
                  ? 'text-orange-900 dark:text-orange-100'
                  : isUpgradeFlow
                  ? 'text-green-900 dark:text-green-100'
                  : 'text-green-900 dark:text-green-100'
              }`}>
                {isDowngradeFlow ? 'Plan updated' : isUpgradeFlow ? 'New features unlocked!' : 'Features unlocked!'}
              </h4>
              <p className={`text-sm ${
                isDowngradeFlow
                  ? 'text-orange-800 dark:text-orange-200'
                  : isUpgradeFlow
                  ? 'text-green-800 dark:text-green-200'
                  : 'text-green-800 dark:text-green-200'
              }`}>
                {isDowngradeFlow
                  ? 'Your data is safe. You can upgrade again anytime.'
                  : isUpgradeFlow
                  ? 'You can see all your new features in the "My Plan" section of your profile.'
                  : 'You can see all your new features in the "My Plan" section of your profile.'}
              </p>
            </div>
          </div>

          <DialogFooter>
            <Button 
              variant="outline"
              onClick={() => navigate('/pachete')}
            >
              View other plans
            </Button>
            <Button onClick={() => navigate('/cont')}>
              Go to profile
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Footer />
    </div>
  );
};

export default PackageCheckout;
