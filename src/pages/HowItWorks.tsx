import { motion } from "framer-motion";
import { FileText, Brain, Database, Target, Gift, ArrowRight } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";

const steps = [
  {
    number: "01",
    icon: FileText,
    title: "Complete the quiz",
    description: "Answer questions about your interests, grades, and skills.",
    color: "primary",
  },
  {
    number: "02",
    icon: Brain,
    title: "AI analyzes your data",
    description: "Our algorithms process your answers and build a full psychometric profile.",
    color: "accent",
  },
  {
    number: "03",
    icon: Database,
    title: "We compare with the database",
    description: "We check your compatibility with over 150 universities in Romania.",
    color: "primary",
  },
  {
    number: "04",
    icon: Target,
    title: "We calculate your score",
    description: "Get a compatibility score for every recommended university.",
    color: "accent",
  },
  {
    number: "05",
    icon: Gift,
    title: "Personalized recommendations",
    description: "Receive a detailed report with the right universities and tailored advice.",
    color: "primary",
  },
];

const HowItWorks = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero */}
      <section className="pt-32 pb-16 bg-hero-gradient">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center max-w-3xl mx-auto"
          >
            <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-6">
              How does our <span className="text-primary">AI</span> work?
            </h1>
            <p className="text-lg text-muted-foreground">
              A simple 5-step process that helps you find the perfect university,
              powered by science and technology.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Steps */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="relative flex gap-6 md:gap-10 mb-12 last:mb-0"
              >
                {/* Timeline line */}
                {index < steps.length - 1 && (
                  <div className="absolute left-6 md:left-10 top-20 w-0.5 h-full bg-border" />
                )}

                {/* Icon */}
                <div
                  className={`flex-shrink-0 w-12 h-12 md:w-20 md:h-20 rounded-2xl flex items-center justify-center ${
                    step.color === "primary"
                      ? "bg-primary/10"
                      : "bg-accent/20"
                  }`}
                >
                  <step.icon
                    className={`w-6 h-6 md:w-10 md:h-10 ${
                      step.color === "primary" ? "text-primary" : "text-accent"
                    }`}
                  />
                </div>

                {/* Content */}
                <div className="flex-1 pt-1">
                  <div className="text-sm font-bold text-muted-foreground mb-1">
                    Step {step.number}
                  </div>
                  <h3 className="font-display text-xl md:text-2xl font-bold text-foreground mb-3">
                    {step.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mt-16"
          >
            <Button variant="accent" size="xl" className="group">
              Start the free test
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </motion.div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default HowItWorks;
