import { motion } from "framer-motion";
import { Target, BarChart3, Brain, Lightbulb, Users, Award } from "lucide-react";

const features = [
  {
    icon: Target,
    title: "We analyze your interests",
    description: "Advanced psychometric tests to uncover what motivates you and what you enjoy doing.",
  },
  {
    icon: BarChart3,
    title: "We compare universities",
    description: "A database of 150+ universities in Romania, kept up to date.",
  },
  {
    icon: Brain,
    title: "AI-powered recommendations",
    description: "Machine-learning algorithms that find the perfect match for your profile.",
  },
  {
    icon: Lightbulb,
    title: "Personalized insights",
    description: "Detailed reports with strengths, gaps, and development directions.",
  },
  {
    icon: Users,
    title: "1:1 mentorship",
    description: "Educational counselors available for questions and extra guidance.",
  },
  {
    icon: Award,
    title: "Proven results",
    description: "95% of our users are satisfied with their university choice.",
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
            What we do for you
          </h2>
          <p className="text-lg text-muted-foreground">
            A complete approach to help you make the best decision for your academic future.
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
