import { motion } from "framer-motion";
import { Target, BarChart3, Brain, Lightbulb, Users, Award } from "lucide-react";

const features = [
  {
    icon: Target,
    title: "Analizăm interesele tale",
    description: "Teste psihometrice avansate pentru a descoperi ce te motivează și ce ți-ar plăcea să faci.",
  },
  {
    icon: BarChart3,
    title: "Comparăm facultăți",
    description: "Bază de date cu peste 150 de facultăți din România, actualizată constant.",
  },
  {
    icon: Brain,
    title: "Recomandări cu AI",
    description: "Algoritmi de machine learning care găsesc matchul perfect pentru profilul tău.",
  },
  {
    icon: Lightbulb,
    title: "Insight-uri personalizate",
    description: "Rapoarte detaliate cu puncte forte, puncte slabe și direcții de dezvoltare.",
  },
  {
    icon: Users,
    title: "Mentorat 1:1",
    description: "Consilieri educaționali disponibili pentru întrebări și ghidare suplimentară.",
  },
  {
    icon: Award,
    title: "Rezultate dovedite",
    description: "95% dintre utilizatorii noștri sunt mulțumiți de alegerea facultății.",
  },
];

const FeaturesSection = () => {
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
            Ce facem pentru tine?
          </h2>
          <p className="text-lg text-muted-foreground">
            O abordare completă pentru a te ajuta să iei cea mai bună decizie pentru viitorul tău academic.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group p-6 md:p-8 rounded-2xl bg-card border border-border/50 hover:border-primary/30 hover:shadow-glow transition-all duration-300"
            >
              <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mb-5 group-hover:bg-primary/20 transition-colors">
                <feature.icon className="w-7 h-7 text-primary" />
              </div>
              <h3 className="font-display text-xl font-semibold text-foreground mb-3">
                {feature.title}
              </h3>
              <p className="text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
