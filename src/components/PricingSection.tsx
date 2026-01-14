import { motion } from "framer-motion";
import { Check, X, Star } from "lucide-react";
import { Button } from "@/components/ui/button";

const plans = [
  {
    name: "Basic",
    price: "99",
    description: "Perfect pentru o primă evaluare",
    features: [
      { text: "Test AI complet", included: true },
      { text: "1 raport personalizat", included: true },
      { text: "Ședință cu consilier", included: false },
      { text: "Suport Zoom", included: false },
    ],
    popular: false,
  },
  {
    name: "Standard",
    price: "249",
    description: "Alegerea populară pentru elevi",
    features: [
      { text: "Test AI complet", included: true },
      { text: "2 rapoarte personalizate", included: true },
      { text: "1 ședință cu consilier", included: true },
      { text: "Suport Zoom", included: false },
    ],
    popular: true,
  },
  {
    name: "Premium",
    price: "499",
    description: "Ghidare completă și personalizată",
    features: [
      { text: "Test AI complet", included: true },
      { text: "Rapoarte nelimitate", included: true },
      { text: "3 ședințe cu consilier", included: true },
      { text: "Suport Zoom prioritar", included: true },
    ],
    popular: false,
  },
];

const PricingSection = () => {
  return (
    <section className="py-20 md:py-28 bg-background">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-2xl mx-auto mb-16"
        >
          <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
            Pachete de consultanță
          </h2>
          <p className="text-lg text-muted-foreground">
            Alege pachetul care se potrivește cel mai bine nevoilor tale. Toate includ acces la AI-ul nostru.
          </p>
        </motion.div>

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
                <h3 className="font-display text-xl font-bold text-foreground mb-2">
                  {plan.name}
                </h3>
                <p className="text-sm text-muted-foreground mb-4">
                  {plan.description}
                </p>
                <div className="flex items-end justify-center gap-1">
                  <span className="font-display text-4xl md:text-5xl font-bold text-foreground">
                    {plan.price}
                  </span>
                  <span className="text-muted-foreground mb-1.5">lei</span>
                </div>
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
              >
                Alege {plan.name}
              </Button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default PricingSection;
