import { motion } from "framer-motion";
import { Check, X, Star, Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useState } from "react";

const plans = [
  {
    name: "Choose Confidently",
    subtitle: "Decision & Clarity",
    price: "36.30",
    description: "Ia decizii informate cu claritate completă",
    features: [
      { text: "Tot din Academic Orientation", included: true },
      { text: "Comparații AI avansate (A vs B vs C)", included: true },
      { text: "Universități & programe clasate după potrivire", included: true },
      { text: "Analiză trade-off-uri (cost, competitivitate)", included: true },
      { text: "Estimări probabilitate admitere (intervale)", included: true },
      { text: "Rezumat PDF pentru părinți", included: true },
      { text: "Chat nelimitat cu AI specializat", included: true },
    ],
    popular: false,
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
    description: "Pregătește aplicația perfectă cu îndrumări personalizate",
    features: [
      { text: "Tot din Decision & Clarity", included: true },
      { text: "Strategie personalizată de aplicare", included: true },
      { text: "Timeline deadline-uri și cerințe", included: true },
      { text: "Training pentru scrisoare de motivație", included: true },
      { text: "Training pentru CV academic", included: true },
      { text: "Feedback asistat de AI + ghidare umană", included: true },
    ],
    popular: true,
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
    description: "Suport complet ghidat pentru aplicare",
    features: [
      { text: "Tot din Application Preparation", included: true },
      { text: "Consiliere academică video call 1-on-1", included: true },
      { text: "Suport ghidat de om pentru aplicare", included: true },
      { text: "Verificări completitudine documente", included: true },
      { text: "Pregătire pentru trimitere", included: true },
      { text: "Tracking deadline-uri & reminder-e", included: true },
      { text: "Sesiuni Peer Insight (Bonus)", included: true },
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

const PricingSection = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<typeof plans[0] | null>(null);

  const handleViewDetails = (plan: typeof plans[0]) => {
    setSelectedPlan(plan);
    setIsDialogOpen(true);
  };

  return (
    <section className="py-20 md:py-28 bg-background">
      <div className="container mx-auto px-4">
        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-6 md:gap-8 max-w-5xl mx-auto">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className={`relative p-6 md:p-8 rounded-2xl border-2 transition-all duration-300 ${
                plan.popular
                  ? "border-primary bg-card shadow-glow scale-105"
                  : "border-border bg-card hover:border-primary/30 hover:shadow-lg"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1.5 rounded-full bg-gradient-accent text-accent-foreground text-sm font-semibold flex items-center gap-1.5 shadow-accent">
                  <Star className="w-4 h-4" fill="currentColor" />
                  Popular
                </div>
              )}

              <div className="text-center mb-8">
                <h3 className="font-display text-xl font-bold text-foreground mb-1">
                  {plan.name}
                </h3>
                <p className="text-sm font-semibold text-primary mb-2">
                  {plan.subtitle}
                </p>
                <p className="text-sm text-muted-foreground mb-4">
                  {plan.description}
                </p>
                <div className="flex items-end justify-center gap-1">
                  <span className="text-muted-foreground mb-1.5">€</span>
                  <span className="font-display text-4xl md:text-5xl font-bold text-foreground">
                    {plan.price}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">VAT included</p>
              </div>

              <ul className="space-y-4 mb-8">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-3">
                    {feature.included ? (
                      <div className="w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center">
                        <Check className="w-3.5 h-3.5 text-primary" />
                      </div>
                    ) : (
                      <div className="w-5 h-5 rounded-full bg-muted flex items-center justify-center">
                        <X className="w-3.5 h-3.5 text-muted-foreground" />
                      </div>
                    )}
                    <span
                      className={
                        feature.included ? "text-foreground" : "text-muted-foreground"
                      }
                    >
                      {feature.text}
                    </span>
                  </li>
                ))}
              </ul>

              <Button
                variant={plan.popular ? "accent" : "outline"}
                className="w-full"
                size="lg"
                onClick={() => handleViewDetails(plan)}
              >
                <Info className="w-4 h-4 mr-2" />
                View Details
              </Button>
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
                  <Button variant="accent" size="lg">
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
