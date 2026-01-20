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
    'Chestionar inițial ghidat de AI',
    'Recomandări de bază universități',
    'Acces la baza de date universități',
  ],
  [PackageTier.DECISION_CLARITY]: [
    'Tot din Decision & Clarity',
    'Comparări avansate cu AI',
    'Recomandări clasate',
    'Analiză tradeoff-uri',
    'Probabilitate de admitere',
    'Descărcare rezumat PDF',
    'Chat AI nelimitat',
  ],
  [PackageTier.APPLICATION_PREP]: [
    'Tot din Decision & Clarity',
    'Strategie personalizată de aplicare',
    'Timeline deadline-uri și cerințe',
    'Training pentru scrisoare de motivație',
    'Training pentru CV academic',
    'Feedback asistat de AI + ghidare umană',
  ],
  [PackageTier.GUIDED_SUPPORT]: [
    'Tot din Application Prep',
    'Sesiuni de consiliere video',
    'Ghidare expert umană',
    'Verificări documente',
    'Pregătire submission',
    'Tracking deadline-uri',
    'Insight-uri de la colegi',
  ],
};

const PACKAGE_BENEFITS = {
  [PackageTier.FREE]: [
    { title: 'Chestionar inițial ghidat de AI', description: 'Descoperă-ți prioritățile' },
    { title: 'Recomandări de bază universități', description: 'Prime sugestii personalizate' },
    { title: 'Acces la baza de date', description: 'Explorează opțiunile tale' },
  ],
  [PackageTier.DECISION_CLARITY]: [
    { title: 'Comparări avansate cu AI', description: 'Compară programe cu detalii aprofundate' },
    { title: 'Recomandări clasate', description: 'Vezi opțiunile sortate după compatibilitate' },
    { title: 'Descărcare PDF', description: 'Exportă rezultatele tale' },
  ],
  [PackageTier.APPLICATION_PREP]: [
    { title: 'Strategie personalizată de aplicare', description: 'Plan customizat pentru aplicații' },
    { title: 'Timeline deadline-uri și cerințe', description: 'Nu mai rata nicio dată' },
    { title: 'Training pentru scrisoare de motivație', description: 'Scrie scrisori de motivație câștigătoare' },
    { title: 'Training pentru CV academic', description: 'Creează CV-uri profesionale' },
    { title: 'Feedback asistat de AI + ghidare umană', description: 'Primește sugestii de îmbunătățire' },
  ],
  [PackageTier.GUIDED_SUPPORT]: [
    { title: 'Sesiuni de consiliere video', description: 'Vorbește direct cu experți' },
    { title: 'Ghidare expert umană', description: 'Suport personalizat 1-la-1' },
    { title: 'Verificări documente', description: 'Asigură-te că totul e corect' },
    { title: 'Pregătire submission', description: 'Finalizează aplicațiile perfect' },
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

      setShowSuccessDialog(true);

      toast({
        title: 'Plată reușită!',
        description: result.message,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Eroare la procesarea plății';
      toast({
        title: 'Eroare',
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
            Mai vezi alte pachete
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
                          <span className="text-sm font-semibold text-blue-500">Pachetul Tău Actual</span>
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
                          <strong>Atenție:</strong> Treci de la <strong>{PACKAGE_DETAILS[fromTierParam].displayName}</strong> la <strong>{packageDetails.displayName}</strong>.
                          Vei pierde accesul la funcționalități premium.
                        </p>
                      </div>
                    )}
                    {isUpgradeFlow && fromTierParam && (
                      <div className="mt-4 p-3 bg-green-50 dark:bg-green-950 rounded-lg border border-green-200 dark:border-green-800">
                        <p className="text-sm text-green-800 dark:text-green-200">
                          <strong>Upgrade:</strong> Treci de la <strong>{PACKAGE_DETAILS[fromTierParam].displayName}</strong> la <strong>{packageDetails.displayName}</strong>.
                          Vei avea acces la funcționalități premium suplimentare.
                        </p>
                      </div>
                    )}
                    {isOwnedPackage && (
                      <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
                        <p className="text-sm text-blue-800 dark:text-blue-200">
                          <strong>Activ:</strong> Acest pachet este deja activ pentru contul tău. 
                          Te bucuri deja de toate funcționalitățile incluse.
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
                              Funcționalități noi pe care le vei câștiga
                            </h3>
                            <p className="text-sm text-green-800 dark:text-green-200 mb-3">
                              Prin trecerea la {packageDetails.displayName}, vei avea acces la:
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
                              Funcționalități pe care le vei pierde
                            </h3>
                            <p className="text-sm text-orange-800 dark:text-orange-200 mb-3">
                              Prin trecerea la {packageDetails.displayName}, nu vei mai avea acces la:
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
                        {isDowngradeFlow ? 'Ce vei păstra' : isUpgradeFlow ? 'Ce vei păstra + funcționalități noi' : isOwnedPackage ? 'Beneficiile tale actuale' : 'Beneficii principale'}
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
                      <h3 className="font-semibold text-lg mb-4">Ce primești concret</h3>
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
                          <span>Confirmi downgrade?</span>
                        </>
                      ) : isUpgradeFlow ? (
                        <>
                          <TrendingUp className="h-5 w-5 text-green-600" />
                          <span>Confirmi upgrade?</span>
                        </>
                      ) : isOwnedPackage ? (
                        <>
                          <BadgeCheck className="h-5 w-5 text-blue-500" />
                          <span>Pachetul Tău</span>
                        </>
                      ) : (
                        <>
                          <TrendingUp className="h-5 w-5 text-green-600" />
                          <span>Ești gata?</span>
                        </>
                      )}
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {isDowngradeFlow
                        ? 'Vei pierde accesul la funcționalități premium, dar vei păstra datele tale.'
                        : isUpgradeFlow
                        ? 'Vei avea acces la funcționalități premium suplimentare imediat.'
                        : isOwnedPackage
                        ? 'Acest pachet este deja activ. Explorează alte pachete folosind butonul de mai jos.'
                        : 'Confirmă pachetul și vei fi dus în Plăți & Facturi pentru confirmare imediată.'}
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
                          Preț pachet: €{packageDetails.price} - Preț pachet anterior: €{PACKAGE_DETAILS[fromTierParam].price}
                        </div>
                      )}
                      <div className="text-sm text-muted-foreground">{packageTierParam === PackageTier.FREE || isDowngradeFlow ? 'Gratuit' : 'TVA inclus'}</div>
                      <div className="mt-2">
                        {isDowngradeFlow ? (
                          <span className="text-orange-600 font-semibold text-sm">
                            Downgrade-ul este gratuit
                          </span>
                        ) : packageTierParam === PackageTier.FREE ? (
                          <span className="text-blue-600 font-semibold text-sm">
                            Pachet gratuit permanent
                          </span>
                        ) : isUpgradeFlow && upgradePrice < parseFloat(packageDetails.price) ? (
                          <span className="text-green-600 font-semibold text-sm">
                            Plătești doar diferența de preț
                          </span>
                        ) : (
                          <span className="text-green-600 font-semibold text-sm">
                            GRATUIT în perioada de testare
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
                            Se procesează...
                          </>
                        ) : isDowngradeFlow ? (
                          <>
                            <TrendingDown className="mr-2 h-4 w-4" />
                            Confirmă downgrade
                          </>
                        ) : isUpgradeFlow ? (
                          <>
                            <TrendingUp className="mr-2 h-4 w-4" />
                            Confirmă upgrade
                          </>
                        ) : packageTierParam === PackageTier.FREE ? (
                          <>
                            <CheckCircle2 className="mr-2 h-4 w-4" />
                            Activează pachetul gratuit
                          </>
                        ) : (
                          <>
                            <CreditCard className="mr-2 h-4 w-4" />
                            Confirmă pachetul
                          </>
                        )}
                      </Button>
                    )}

                    <Button
                      variant="outline"
                      onClick={handleViewNextPackage}
                      className="w-full"
                    >
                      Vezi pachetul următor
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
                  <span>Confirmare Downgrade</span>
                </>
              ) : isUpgradeFlow ? (
                <>
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span>Confirmare Upgrade</span>
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
                ? `Confirmi trecerea la ${packageDetails.displayName}?`
                : isUpgradeFlow
                ? `Confirmi upgrade la ${packageDetails.displayName}?`
                : `Procesare plată pentru ${packageDetails.displayName}`}
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="rounded-lg bg-muted p-4">
              <h4 className="font-semibold mb-2">Detalii plată</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Pachet:</span>
                  <span className="font-medium">{packageDetails.displayName}</span>
                </div>
                {isUpgradeFlow && fromTierParam && upgradePrice !== parseFloat(packageDetails.price) && (
                  <>
                    <div className="flex justify-between">
                      <span>Preț pachet nou:</span>
                      <span className="font-medium">€{packageDetails.price}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Preț pachet actual:</span>
                      <span className="font-medium">-€{PACKAGE_DETAILS[fromTierParam].price}</span>
                    </div>
                    <div className="border-t pt-2 mt-2"></div>
                  </>
                )}
                <div className="flex justify-between">
                  <span>{isUpgradeFlow && upgradePrice !== parseFloat(packageDetails.price) ? 'De plată (diferență):' : 'Preț:'}</span>
                  <span className="font-medium">€{displayPrice}</span>
                </div>
                <div className="flex justify-between">
                  <span>TVA:</span>
                  <span className="font-medium">{isDowngradeFlow || packageTierParam === PackageTier.FREE ? 'N/A' : 'Inclus'}</span>
                </div>
              </div>
              <div className="mt-4 bg-green-50 dark:bg-green-950 p-3 rounded border border-green-200 dark:border-green-800">
                <p className="text-sm text-green-800 dark:text-green-200">
                  {isDowngradeFlow ? (
                    <>
                      🎉 <strong>Downgrade gratuit:</strong> Nu vei fi taxat pentru a trece la un pachet mai mic.
                    </>
                  ) : packageTierParam === PackageTier.FREE ? (
                    <>
                      🎉 <strong>Pachet gratuit:</strong> Acest pachet este și va rămâne gratuit permanent.
                    </>
                  ) : (
                    <>
                      🎉 <strong>Testare:</strong> Plata va fi marcată ca reușită automat. 
                      Gateway real de plată va fi integrat în curând.
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
              Anulează
            </Button>
            <Button onClick={handlePaymentConfirm}>
              Confirmă plata
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
              {isDowngradeFlow ? 'Downgrade realizat!' : isUpgradeFlow ? 'Upgrade realizat!' : 'Plată reușită!'}
            </DialogTitle>
            <DialogDescription className="pt-4">
              {isDowngradeFlow
                ? `Ai trecut cu succes la pachetul ${packageDetails.displayName}.`
                : isUpgradeFlow
                ? `Ai făcut upgrade cu succes la ${packageDetails.displayName}!`
                : `Ai achiziționat cu succes pachetul ${packageDetails.displayName}!`}
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
                {isDowngradeFlow ? 'Pachet actualizat' : isUpgradeFlow ? 'Funcționalități noi deblocate!' : 'Funcționalități deblocate!'}
              </h4>
              <p className={`text-sm ${
                isDowngradeFlow
                  ? 'text-orange-800 dark:text-orange-200'
                  : isUpgradeFlow
                  ? 'text-green-800 dark:text-green-200'
                  : 'text-green-800 dark:text-green-200'
              }`}>
                {isDowngradeFlow
                  ? 'Datele tale sunt în siguranță. Poți re-upgrade oricând dorești.'
                  : isUpgradeFlow
                  ? 'Poți vedea toate funcționalitățile tale noi în secțiunea "Pachetul Meu" din profilul tău.'
                  : 'Poți vedea toate funcționalitățile tale noi în secțiunea "Pachetul Meu" din profilul tău.'}
              </p>
            </div>
          </div>

          <DialogFooter>
            <Button 
              variant="outline"
              onClick={() => navigate('/pachete')}
            >
              Vezi alte pachete
            </Button>
            <Button onClick={() => navigate('/cont')}>
              Mergi la profil
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Footer />
    </div>
  );
};

export default PackageCheckout;
