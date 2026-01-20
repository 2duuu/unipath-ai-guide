import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check, ArrowLeft, CreditCard, Info, Plus, Minus } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import { plans, type Plan } from "@/data/plans";
import { useMemo, useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { createPayment, confirmPayment } from "@/services/api";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

const planHierarchy = ["choose_confidently", "prepare_to_apply", "apply_with_support"] as const;

type PlanKey = (typeof planHierarchy)[number];

const PlanDetails = () => {
  const { planKey } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, user, refreshUser } = useAuth();
  const [showPaymentConfirm, setShowPaymentConfirm] = useState(false);
  const [loading, setLoading] = useState(false);

  const plan: Plan | undefined = useMemo(
    () => plans.find(p => p.key === planKey),
    [planKey]
  );

  const currentPlanKey = (user?.package_level as PlanKey | undefined) || undefined;
  const currentPlan = useMemo(
    () => plans.find(p => p.key === currentPlanKey),
    [currentPlanKey]
  );

  const planRelationship = useMemo(() => {
    if (!plan) return "new";
    if (!currentPlanKey) return "new";
    if (currentPlanKey === plan.key) return "current";
    const currentIndex = planHierarchy.indexOf(currentPlanKey);
    const targetIndex = planHierarchy.indexOf(plan.key as PlanKey);
    if (currentIndex === -1 || targetIndex === -1) return "new";
    return targetIndex > currentIndex ? "upgrade" : "downgrade";
  }, [currentPlanKey, plan]);

  const alreadyOwned = planRelationship === "current";

  // Calculate differential benefits for upgrade/downgrade
  const benefitsDiff = useMemo(() => {
    if (!plan || !currentPlan || planRelationship === "current" || planRelationship === "new") {
      return { added: [], removed: [] };
    }

    const currentFeatureTexts = currentPlan.features.map(f => f.text);
    const targetFeatureTexts = plan.features.map(f => f.text);

    const added = plan.features.filter(f => !currentFeatureTexts.includes(f.text));
    const removed = currentPlan.features.filter(f => !targetFeatureTexts.includes(f.text));

    return { added, removed };
  }, [plan, currentPlan, planRelationship]);

  // Calculate display price based on relationship
  const displayPrice = useMemo(() => {
    if (!plan) return { value: 0, label: "€0" };
    
    if (planRelationship === "downgrade") {
      // Downgrade is free
      return { value: 0, label: "€0", description: "Gratis" };
    }
    
    if (planRelationship === "upgrade" && currentPlan) {
      // Show price difference for upgrade
      const difference = plan.priceValue - currentPlan.priceValue;
      return { 
        value: difference, 
        label: `€${difference}`,
        description: `Diferență față de pachetul curent`
      };
    }
    
    // New or current package - show full price
    return { value: plan.priceValue, label: plan.price };
  }, [plan, currentPlan, planRelationship]);

  const primaryCtaLabel = useMemo(() => {
    switch (planRelationship) {
      case "current":
        return "Pachet activ";
      case "upgrade":
        return "Upgradează la acest pachet";
      case "downgrade":
        return "Downgradează la acest pachet";
      default:
        return "Confirmă pachetul";
    }
  }, [planRelationship]);

  const secondaryCtaLabel = useMemo(() => {
    if (planRelationship === "current") return "Vezi pachetul următor";
    if (planRelationship === "upgrade") return "Vezi pachetul următor";
    if (planRelationship === "downgrade") return "Vezi pachetul anterior";
    return "Vezi alte pachete";
  }, [planRelationship]);

  const getNextPlanKey = (): string => {
    const currentIndex = planHierarchy.indexOf(plan?.key as PlanKey);
    if (currentIndex === -1) return planHierarchy[0]; // Fallback to first
    
    // For current package or upgrade, go to next
    if (planRelationship === "current" || planRelationship === "upgrade") {
      const nextIndex = (currentIndex + 1) % planHierarchy.length;
      return planHierarchy[nextIndex];
    }
    // For downgrade, go to previous (with loop)
    if (planRelationship === "downgrade") {
      const prevIndex = (currentIndex - 1 + planHierarchy.length) % planHierarchy.length;
      return planHierarchy[prevIndex];
    }
    // Default: go to next
    return planHierarchy[(currentIndex + 1) % planHierarchy.length];
  };

  const handleViewNextPackage = () => {
    const nextKey = getNextPlanKey();
    navigate(`/pachete/${nextKey}`);
  };

  // Scroll to top when plan changes
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [planKey]);

  const handleBuy = () => {
    if (!plan) return;
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }
    if (alreadyOwned) {
      alert("Deja ai acest pachet activ.");
      return;
    }
    setShowPaymentConfirm(true);
  };

  const confirmPurchase = async () => {
    if (!plan) return;
    try {
      setLoading(true);
      const payment = await createPayment({
        package_key: plan.key,
        package_name: plan.name,
        amount_eur: displayPrice.value,
      });
      
      if (!payment?.id) {
        console.error("Payment creation failed - no payment ID returned");
        alert("Eroare la crearea plății. Vă rugăm încercați din nou.");
        return;
      }

      try {
        const confirmedPayment = await confirmPayment(payment.id);
        if (!confirmedPayment) {
          console.error("Payment confirmation failed");
          alert("Eroare la confirmarea plății. Vă rugăm contactați suportul.");
          return;
        }
        
        await refreshUser();
        setShowPaymentConfirm(false);
        navigate("/cont?tab=payments");
      } catch (error) {
        console.error("Failed to confirm payment", error);
        alert("Eroare la confirmarea plății. Vă rugăm încercați din nou.");
      }
    } catch (error) {
      console.error("Failed to create payment", error);
      alert("Eroare la crearea plății. Vă rugăm încercați din nou.");
    } finally {
      setLoading(false);
    }
  };

  if (!plan) {
    navigate("/pachete");
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="pt-28 pb-16">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="flex items-center gap-3 mb-6">
            <Button variant="ghost" size="sm" onClick={() => navigate(-1)}>
              <ArrowLeft className="w-4 h-4 mr-2" /> Înapoi
            </Button>
            <Badge variant="secondary" className="capitalize">
              {plan.subtitle}
            </Badge>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            <Card className="lg:col-span-2">
              <CardContent className="p-6 space-y-6">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                  <div>
                    <p className="text-sm text-muted-foreground">Pachet</p>
                    <h1 className="font-display text-3xl font-bold text-foreground">{plan.name}</h1>
                    <p className="text-primary font-semibold">{plan.subtitle}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-muted-foreground">Preț</p>
                    <div className="flex items-end justify-end gap-1">
                      <span className="text-muted-foreground">€</span>
                      <span className="font-display text-4xl font-bold">{plan.price}</span>
                    </div>
                    {displayPrice.description && (
                      <p className="text-xs text-muted-foreground">{displayPrice.description}</p>
                    )}
                    <p className="text-xs text-muted-foreground">TVA inclus</p>
                  </div>
                </div>

                <p className="text-muted-foreground">{plan.description}</p>

                {/* Show differential benefits for upgrade/downgrade */}
                {(planRelationship === "upgrade" || planRelationship === "downgrade") && (
                  <>
                    {planRelationship === "upgrade" && benefitsDiff.added.length > 0 && (
                      <div className="space-y-3">
                        <h2 className="font-semibold text-lg text-green-600 dark:text-green-400">Beneficii adiționale</h2>
                        <ul className="grid sm:grid-cols-2 gap-3">
                          {benefitsDiff.added.map((feature, idx) => (
                            <li
                              key={idx}
                              className="flex items-start gap-3 rounded-lg border border-green-500/30 bg-green-50/50 dark:bg-green-950/20 p-3 transition-all hover:border-green-500/60 hover:bg-green-100/60 dark:hover:bg-green-900/30 hover:scale-105 hover:shadow-md"
                            >
                              <div className="mt-0.5">
                                <Plus className="w-4 h-4 text-green-600 dark:text-green-400" />
                              </div>
                              <span className="text-foreground text-sm">{feature.text}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {planRelationship === "downgrade" && benefitsDiff.removed.length > 0 && (
                      <div className="space-y-3">
                        <h2 className="font-semibold text-lg text-red-600 dark:text-red-400">Beneficii pe care le vei pierde</h2>
                        <ul className="grid sm:grid-cols-2 gap-3">
                          {benefitsDiff.removed.map((feature, idx) => (
                            <li
                              key={idx}
                              className="flex items-start gap-3 rounded-lg border border-red-500/30 bg-red-50/50 dark:bg-red-950/20 p-3 transition-all hover:border-red-500/60 hover:bg-red-100/60 dark:hover:bg-red-900/30 hover:scale-105 hover:shadow-md"
                            >
                              <div className="mt-0.5">
                                <Minus className="w-4 h-4 text-red-600 dark:text-red-400" />
                              </div>
                              <span className="text-foreground text-sm">{feature.text}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}

                {/* Show all benefits for new or current packages */}
                {(planRelationship === "new" || planRelationship === "current") && (
                  <div className="space-y-3">
                    <h2 className="font-semibold text-lg">Beneficii principale</h2>
                    <ul className="grid sm:grid-cols-2 gap-3">
                      {plan.features.map((feature, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-3 rounded-lg border bg-card p-3"
                        >
                          <div className="mt-0.5">
                            <Check className="w-4 h-4 text-primary" />
                          </div>
                          <span className="text-foreground text-sm">{feature.text}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="space-y-3">
                  <h2 className="font-semibold text-lg">Ce primești concret</h2>
                  <ul className="space-y-2">
                    {plan.detailedInfo.includes.map((item, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-sm text-foreground">
                        <div className="mt-1">
                          <Info className="w-4 h-4 text-primary" />
                        </div>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {plan.detailedInfo.note && (
                  <div className="p-4 rounded-lg border bg-muted/50 text-sm text-muted-foreground italic">
                    {plan.detailedInfo.note}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="sticky top-28">
              <CardContent className="p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-base">Ești gata?</h3>
                    <p className="text-xs text-muted-foreground">
                      Confirmă pachetul și vei fi dus în Plăți & Facturi pentru confirmare imediată.
                    </p>
                  </div>
                  {(planRelationship === "upgrade" || planRelationship === "downgrade") && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleViewNextPackage}
                      className="ml-2"
                    >
                      Poți Face Downgrade
                    </Button>
                  )}
                </div>

                {planRelationship !== "current" && currentPlanKey && (
                  <p className="text-xs text-muted-foreground">
                    Pachet curent: {currentPlan?.name || plans.find(p => p.key === currentPlanKey)?.name}
                  </p>
                )}

                <div className="flex items-center justify-between p-3 rounded-lg border bg-muted/40">
                  <div>
                    <p className="text-xs text-muted-foreground">
                      {planRelationship === "downgrade" ? "Preț" : "Total"}
                    </p>
                    <p className={`font-display text-xl font-bold ${
                      planRelationship === "downgrade" ? "text-green-600 dark:text-green-400" :
                      planRelationship === "upgrade" ? "text-blue-600 dark:text-blue-400" :
                      ""
                    }`}>
                      {displayPrice.label}
                    </p>
                    {displayPrice.description && (
                      <p className="text-[10px] text-muted-foreground mt-0.5">{displayPrice.description}</p>
                    )}
                  </div>
                  <Badge variant="outline" className="text-xs">TVA inclus</Badge>
                </div>

                <Button
                  size="lg"
                  className="w-full"
                  onClick={handleBuy}
                  disabled={alreadyOwned}
                >
                  {primaryCtaLabel}
                </Button>

                {(planRelationship === "upgrade" || planRelationship === "downgrade" || planRelationship === "current") && (
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={handleViewNextPackage}
                  >
                    Vezi pachetul anterior
                  </Button>
                )}

                <Button
                  variant="outline"
                  size="sm"
                  className="w-full"
                  onClick={() => navigate("/pachete")}
                >
                  Mai vezi alte pachete
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <Footer />

      <Dialog
        open={showPaymentConfirm}
        onOpenChange={open => setShowPaymentConfirm(open)}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-foreground">
              <CreditCard className="w-5 h-5" />
              Confirmă plata
            </DialogTitle>
            <DialogDescription>
              Vei fi redirecționat către Plăți & Facturi imediat după confirmare.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-2">
            <div className="flex items-center justify-between p-4 rounded-lg border bg-muted/40">
              <div>
                <p className="text-sm text-muted-foreground">Pachet</p>
                <p className="text-lg font-semibold text-foreground">{plan.name}</p>
                <p className="text-sm text-primary font-medium">{plan.subtitle}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-muted-foreground">
                  {planRelationship === "downgrade" ? "Preț" : "Total"}
                </p>
                <div className="flex items-end gap-1 justify-end">
                  <span className={`text-muted-foreground ${
                    planRelationship === "downgrade" ? "text-green-600 dark:text-green-400" :
                    planRelationship === "upgrade" ? "text-blue-600 dark:text-blue-400" :
                    ""
                  }`}>€</span>
                  <span className={`font-display text-3xl font-bold ${
                    planRelationship === "downgrade" ? "text-green-600 dark:text-green-400" :
                    planRelationship === "upgrade" ? "text-blue-600 dark:text-blue-400" :
                    ""
                  }`}>
                    {displayPrice.value}
                  </span>
                </div>
                {displayPrice.description && (
                  <p className="text-[10px] text-muted-foreground mb-1">{displayPrice.description}</p>
                )}
                <p className="text-xs text-muted-foreground">TVA inclus</p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-muted-foreground">
              {["Plată securizată", "Fără costuri ascunse", "Confirmare rapidă", "Acces în Plăți & Facturi"].map(
                text => (
                  <div key={text} className="flex items-center gap-2 p-3 rounded-lg border bg-card">
                    <Check className="w-4 h-4 text-primary" />
                    <span>{text}</span>
                  </div>
                )
              )}
            </div>
          </div>

          <DialogFooter className="gap-3">
            <Button variant="outline" onClick={() => setShowPaymentConfirm(false)} disabled={loading}>
              Închide
            </Button>
            <Button variant="accent" onClick={confirmPurchase} disabled={loading}>
              {loading ? "Se procesează..." : "Confirmă și plătește"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PlanDetails;
