import Navbar from "@/components/Navbar";
import PricingSection from "@/components/PricingSection";
import CTASection from "@/components/CTASection";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";

const Packages = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero */}
      <section className="pt-32 pb-8 bg-hero-gradient">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center max-w-3xl mx-auto"
          >
            <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-6">
              Alege pachetul <span className="text-primary">potrivit</span> pentru tine
            </h1>
            <p className="text-lg text-muted-foreground">
              Fiecare pachet include acces la AI-ul nostru. Diferența constă în 
              nivelul de suport și personalizare pe care îl primești.
            </p>
          </motion.div>
        </div>
      </section>

      <PricingSection />
      <CTASection />
      <Footer />
    </div>
  );
};

export default Packages;
