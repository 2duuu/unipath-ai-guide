import { motion } from "framer-motion";
import { Check, Cpu, TrendingUp, UserCheck } from "lucide-react";
import aiRobot from "@/assets/robot albastru.png";

const aiFeatures = [
  {
    icon: Cpu,
    title: "Teste inteligente",
    description: "Întrebări adaptive care se ajustează în funcție de răspunsurile tale.",
  },
  {
    icon: UserCheck,
    title: "Analiză profil elev",
    description: "Profilare completă bazată pe interese, abilități și aspirații.",
  },
  {
    icon: TrendingUp,
    title: "Predicție compatibilitate",
    description: "Scor de potrivire pentru fiecare facultate din baza noastră de date.",
  },
];

const AISection = () => {
  return (
    <section className="py-20 md:py-28 bg-secondary/30 overflow-hidden">
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Image Side */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="relative order-2 lg:order-1"
          >
            <div className="relative z-10 max-w-md mx-auto lg:max-w-none">
              <img
                src={aiRobot}
                alt="UniHub AI Assistant"
                className="w-full rounded-2xl shadow-2xl"
              />
            </div>
            {/* Decorations */}
            <div className="absolute -top-10 -left-10 w-40 h-40 bg-primary/20 rounded-full blur-3xl" />
            <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-accent/30 rounded-full blur-2xl" />
          </motion.div>

          {/* Content Side */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="order-1 lg:order-2"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary mb-6">
              <Cpu className="w-4 h-4" />
              <span className="text-sm font-medium">Tehnologie AI</span>
            </div>

            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-6">
              AI-ul nostru te cunoaște mai bine decât crezi
            </h2>

            <p className="text-lg text-muted-foreground mb-8">
              Folosim algoritmi de machine learning antrenați pe date de la mii de 
              studenți pentru a-ți oferi cele mai precise recomandări.
            </p>

            <div className="space-y-6">
              {aiFeatures.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="flex gap-4"
                >
                  <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                    <feature.icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-display font-semibold text-foreground mb-1">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground text-sm">
                      {feature.description}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Trust badges */}
            <div className="flex items-center gap-6 mt-10 pt-8 border-t border-border/50">
              {["Securitate datelor", "GDPR Compliant", "Fără date vândute"].map((badge) => (
                <div key={badge} className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Check className="w-4 h-4 text-primary" />
                  {badge}
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default AISection;
