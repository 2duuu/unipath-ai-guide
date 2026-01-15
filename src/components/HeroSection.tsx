import { motion } from "framer-motion";
import { ArrowRight, Sparkles, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import heroIllustration from "@/assets/copil turcoaz.png";

const HeroSection = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [hasStartedQuiz, setHasStartedQuiz] = useState(false);

  useEffect(() => {
    // Check if user has started the quiz
    const quizStarted = localStorage.getItem('quizStarted');
    setHasStartedQuiz(quizStarted === 'true');
  }, []);

  const handleQuizClick = () => {
    if (hasStartedQuiz) {
      // Clear quiz progress and restart
      localStorage.removeItem('quizStarted');
      localStorage.removeItem('quizProgress');
      setHasStartedQuiz(false);
    }
    if (location.pathname === "/quiz") {
      window.location.reload();
    } else {
      navigate("/quiz");
    }
  };

  return (
    <section className="relative min-h-screen bg-hero-gradient overflow-hidden pt-20">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full blur-3xl" />
        <div className="absolute top-1/2 -left-20 w-60 h-60 bg-accent/20 rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-1/4 w-40 h-40 bg-primary/15 rounded-full blur-2xl" />
      </div>

      <div className="container mx-auto px-4 py-16 md:py-24 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
            className="text-center lg:text-left"
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/20 text-accent-foreground mb-6"
            >
              <Sparkles className="w-4 h-4 text-accent" />
              <span className="text-sm font-medium">Ghidare bazată pe AI</span>
            </motion.div>

            <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-bold text-foreground leading-tight mb-6">
              Alege{" "}
              <span className="text-primary relative">
                facultatea
                <svg className="absolute -bottom-2 left-0 w-full" viewBox="0 0 200 12" fill="none">
                  <path d="M2 8C50 2 150 2 198 8" stroke="hsl(var(--accent))" strokeWidth="4" strokeLinecap="round" />
                </svg>
              </span>{" "}
              potrivită pentru tine
            </h1>

            <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-xl mx-auto lg:mx-0">
              Ghidare personalizată pentru viitorul tău academic. AI-ul nostru analizează 
              interesele, abilitățile și aspirațiile tale pentru a-ți recomanda cele mai 
              bune opțiuni.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button variant="accent" size="xl" className="group" onClick={handleQuizClick}>
                {hasStartedQuiz ? 'Reîncepe Quizul' : 'Începe Quizul Carierei'}
                {hasStartedQuiz ? (
                  <RefreshCw className="w-5 h-5 group-hover:rotate-180 transition-transform" />
                ) : (
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                )}
              </Button>
              <Button variant="outline" size="xl">
                Vezi pachetele
              </Button>
            </div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="grid grid-cols-3 gap-6 mt-12 pt-8 border-t border-border/50"
            >
              {[
                { value: "5000+", label: "Studenți ghidați" },
                { value: "150+", label: "Facultăți analizate" },
                { value: "95%", label: "Satisfacție" },
              ].map((stat, i) => (
                <div key={i} className="text-center lg:text-left">
                  <div className="font-display text-2xl md:text-3xl font-bold text-primary">
                    {stat.value}
                  </div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </motion.div>

          {/* Illustration */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.3, ease: "easeOut" }}
            className="relative"
          >
            <div className="relative z-10">
              <img
                src={heroIllustration}
                alt="UniHub AI Education Platform"
                className="w-full max-w-lg mx-auto lg:max-w-none drop-shadow-2xl"
              />
            </div>
            {/* Floating elements */}
            <motion.div
              animate={{ y: [0, -15, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              className="absolute top-10 right-10 w-16 h-16 bg-accent/30 rounded-2xl blur-sm"
            />
            <motion.div
              animate={{ y: [0, 15, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              className="absolute bottom-20 left-10 w-12 h-12 bg-primary/30 rounded-full blur-sm"
            />
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
