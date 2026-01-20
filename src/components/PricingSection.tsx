import { motion } from "framer-motion";
import { Check, X, Star, Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useNavigate } from "react-router-dom";
import { plans } from "@/data/plans";
import { useAuth } from "@/contexts/AuthContext";

const PricingSection = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const currentPackage = user?.package_level;

  const handleViewDetails = (planKey: string) => {
    navigate(`/pachete/${planKey}`);
  };

  return (
    <section className="py-20 md:py-28 bg-background">
      <div className="container mx-auto px-4">
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
              <div className="flex items-center justify-between mb-3">
                {plan.popular && (
                  <div className="px-4 py-1.5 rounded-full bg-gradient-accent text-accent-foreground text-sm font-semibold flex items-center gap-1.5 shadow-accent">
                    <Star className="w-4 h-4" fill="currentColor" />
                    Popular
                  </div>
                )}
                {currentPackage === plan.key && (
                  <Badge variant="secondary" className="ml-auto">Pachet curent</Badge>
                )}
              </div>

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
                {currentPackage === plan.key && (
                  <p className="text-xs text-primary font-semibold mt-2">Acesta este pachetul tău activ</p>
                )}
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
                    <span className={feature.included ? "text-foreground" : "text-muted-foreground"}>
                      {feature.text}
                    </span>
                  </li>
                ))}
              </ul>

              <Button
                variant={plan.popular ? "accent" : "outline"}
                className="w-full"
                size="lg"
                onClick={() => handleViewDetails(plan.key)}
              >
                <Info className="w-4 h-4 mr-2" />
                {currentPackage === plan.key ? "Vezi beneficiile (activ)" : "Vezi beneficiile"}
              </Button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default PricingSection;
