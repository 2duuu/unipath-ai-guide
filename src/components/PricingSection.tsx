import { motion } from "framer-motion";
import { Check, Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { PackageTier } from "@/lib/packages";
import { getPackageInfo } from "@/services/packages";

const plans = [
  {
    name: "Choose Confidently",
    subtitle: "Decision & Clarity",
    price: "36.30",
    description: "Make informed decisions with complete clarity",
    features: [
      { text: "Everything from Academic Orientation", included: true },
      { text: "Advanced AI comparisons (A vs B vs C)", included: true },
      { text: "Universities & programs ranked by fit", included: true },
      { text: "Trade-off analysis (cost, competitiveness)", included: true },
      { text: "Admission probability estimates (ranges)", included: true },
      { text: "Parent-ready PDF summary", included: true },
      { text: "Unlimited chat with specialized AI", included: true },
    ],
    popular: true,
    detailedInfo: {
      title: "Package 1 — Decision & Clarity",
      subtitle: "Choose Confidently",
      includes: [
        "Full UniHub Quiz (core + extended)",
        "University recommendations",
        "Program recommendations",
        "AI explanations of academic fit",
        "High-level difficulty indicators",
        "Advanced AI comparisons (A vs B vs C)",
        "Ranked best-fit universities & programs",
        "Trade-off analysis (cost, competitiveness, outcomes)",
        "Risk & uncertainty overview",
        "AI-based admission probability estimates (ranges)",
        "Parent-friendly written summary (PDF)",
        "Unlimited chat with Trained AI model in academic advising"
      ],
      note: "Ethical note: Admission probabilities are estimates, not guarantees."
    }
  },
  {
    name: "Prepare to Apply",
    subtitle: "Application Preparation",
    price: "121",
    description: "Craft the perfect application with personalized guidance",
    features: [
      { text: "Everything from Decision & Clarity", included: true },
      { text: "Personalized application strategy", included: true },
      { text: "Deadline and requirements timeline", included: true },
      { text: "Motivation letter training", included: true },
      { text: "Academic CV training", included: true },
      { text: "AI-assisted feedback + human guidance", included: true },
    ],
    popular: false,
    detailedInfo: {
      title: "Package 2 — Application Preparation",
      subtitle: "Prepare to Apply",
      includes: [
        "Everything from Decision & Clarity package",
        "Personalized application strategy",
        "Deadline & requirement timeline",
        "Motivation letter training",
        "Academic CV training",
        "AI-assisted feedback + human guidance"
      ],
      note: "Boundary: UniHub provides guidance and training. All application materials are written by the student."
    }
  },
  {
    name: "Apply with Support",
    subtitle: "Guided Application Support",
    price: "484",
    description: "Fully guided support for your application",
    features: [
      { text: "Everything from Application Preparation", included: true },
      { text: "1-on-1 academic advising video call", included: true },
      { text: "Human-guided application support", included: true },
      { text: "Document completeness checks", included: true },
      { text: "Submission readiness prep", included: true },
      { text: "Deadline tracking & reminders", included: true },
      { text: "Peer Insight Sessions (Bonus)", included: true },
    ],
    popular: false,
    detailedInfo: {
      title: "Package 3 — Guided Application Support",
      subtitle: "Apply with Support",
      includes: [
        "Everything from Application Preparation package",
        "1-on-1 academic advising video call",
        "Human-guided application support",
        "Document completeness & readiness checks",
        "Submission preparation (no automated applying)",
        "Deadline tracking & reminders",
        "Peer Insight Sessions (Bonus)"
      ],
      note: null
    }
  },
];

// Map plan names to package tiers
const planToTier: Record<string, PackageTier> = {
  "Choose Confidently": PackageTier.DECISION_CLARITY,
  "Prepare to Apply": PackageTier.APPLICATION_PREP,
  "Apply with Support": PackageTier.GUIDED_SUPPORT,
};

const PricingSection = () => {
  const navigate = useNavigate();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<typeof plans[0] | null>(null);
  const [currentPackage, setCurrentPackage] = useState<PackageTier | null>(null);

  useEffect(() => {
    loadCurrentPackage();
  }, []);

  const loadCurrentPackage = async () => {
    try {
      const info = await getPackageInfo();
      setCurrentPackage(info.package_tier);
    } catch (error) {
      setCurrentPackage(PackageTier.FREE);
    }
  };

  const handleViewDetails = (plan: typeof plans[0]) => {
    setSelectedPlan(plan);
    setIsDialogOpen(true);
  };

  const handleChoosePlan = () => {
    if (!selectedPlan) return;
    
    const targetTier = planToTier[selectedPlan.name];
    const fromTier = currentPackage || PackageTier.FREE;
    
    // Navigate to checkout page with from parameter
    navigate(`/pachete/checkout?package=${targetTier}&from=${fromTier}`);
  };

  return (
    <section className="py-20 md:py-28 bg-background" id="pricing">
      <div className="container mx-auto px-4">
        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-6 md:gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative"
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 z-10">
                  <Badge className="bg-[#F59E0B] hover:bg-[#F59E0B] text-white px-4 py-1 text-sm font-semibold">
                    ⭐ Popular
                  </Badge>
                </div>
              )}

              <Card 
                className={`flex flex-col h-full ${
                  plan.popular ? 'border-[#3B82F6] border-2 shadow-lg' : 'border-border'
                }`}
              >
                <CardHeader className="text-center pb-4">
                  <CardTitle className="text-2xl font-bold mb-2">{plan.name}</CardTitle>
                  <div className="text-[#3B82F6] font-semibold mb-3">{plan.subtitle}</div>
                  <p className="text-sm text-muted-foreground mb-4">
                    {plan.description}
                  </p>
                  <div className="space-y-1">
                    <div className="flex items-baseline justify-center gap-1">
                      <span className="text-sm text-muted-foreground">€</span>
                      <span className="text-5xl font-bold">
                        {plan.price}
                      </span>
                    </div>
                    <div className="text-sm text-muted-foreground">VAT included</div>
                  </div>
                </CardHeader>

                <CardContent className="flex-1 pt-6">
                  <ul className="space-y-3">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-3">
                        <Check className="w-5 h-5 text-[#3B82F6] mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-left">{feature.text}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>

                <CardFooter className="pt-6">
                  <Button
                    variant={plan.name === "Choose Confidently" ? "accent" : "outline"}
                    className="w-full"
                    onClick={() => handleViewDetails(plan)}
                  >
                    <Info className="w-4 h-4 mr-2" />
                    View Details
                  </Button>
                </CardFooter>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Detailed Package Dialog */}
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="text-2xl font-display">
                {selectedPlan?.detailedInfo.title}
              </DialogTitle>
              <DialogDescription className="text-lg font-semibold text-primary">
                {selectedPlan?.detailedInfo.subtitle}
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-6">
              <div>
                <h4 className="font-semibold text-lg mb-3">Includes:</h4>
                <ul className="space-y-2">
                  {selectedPlan?.detailedInfo.includes.map((item, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <div className="w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center mt-0.5">
                        <Check className="w-3.5 h-3.5 text-primary" />
                      </div>
                      <span className="text-foreground flex-1">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {selectedPlan?.detailedInfo.note && (
                <div className="p-4 rounded-lg bg-muted/50 border border-border">
                  <p className="text-sm text-muted-foreground italic">
                    {selectedPlan.detailedInfo.note}
                  </p>
                </div>
              )}

              <div className="pt-4 border-t">
                <div className="flex items-end justify-between mb-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Price</p>
                    <div className="flex items-end gap-1">
                      <span className="text-muted-foreground">€</span>
                      <span className="font-display text-3xl font-bold text-foreground">
                        {selectedPlan?.price}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground">VAT included • No hidden fees</p>
                  </div>
                  <Button variant="accent" size="lg" onClick={handleChoosePlan}>
                    Choose {selectedPlan?.name}
                  </Button>
                </div>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </section>
  );
};

export default PricingSection;
