import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, ArrowLeft, CheckCircle, Brain, BookOpen, Briefcase, MapPin, Star } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

const questions = [
  {
    id: 1,
    question: "Ce materii îți plac cel mai mult?",
    icon: BookOpen,
    options: [
      "Matematică și Fizică",
      "Informatică și Tehnologie",
      "Literatură și Limbi străine",
      "Biologie și Chimie",
      "Economie și Antreprenoriat",
    ],
  },
  {
    id: 2,
    question: "Care sunt notele tale medii?",
    icon: Star,
    options: [
      "Sub 7",
      "Între 7 și 8",
      "Între 8 și 9",
      "Între 9 și 10",
      "10 sau foarte aproape",
    ],
  },
  {
    id: 3,
    question: "Preferi lucrul teoretic sau practic?",
    icon: Brain,
    options: [
      "Teoretic - îmi place să analizez și să cercetez",
      "Practic - îmi place să creez și să construiesc",
      "O combinație echilibrată",
      "Prefer lucrul cu oamenii",
      "Nu sunt sigur încă",
    ],
  },
  {
    id: 4,
    question: "Ce tip de carieră te atrage?",
    icon: Briefcase,
    options: [
      "Job stabil și sigur",
      "Carieră creativă și dinamică",
      "Antreprenoriat",
      "Cercetare și inovație",
      "Muncă cu impact social",
    ],
  },
  {
    id: 5,
    question: "În ce oraș ai vrea să studiezi?",
    icon: MapPin,
    options: [
      "București",
      "Cluj-Napoca",
      "Iași",
      "Timișoara",
      "Altul sau nu contează",
    ],
  },
];

const results = {
  profile: "Analitic – Creativ",
  recommendations: [
    { name: "Informatică", university: "Universitatea București", score: 92 },
    { name: "Automatică și Calculatoare", university: "UPB", score: 87 },
    { name: "Economie și IT", university: "ASE", score: 84 },
  ],
};

const Quiz = () => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [showResults, setShowResults] = useState(false);

  const progress = ((currentQuestion + 1) / questions.length) * 100;

  const handleAnswer = (answer: string) => {
    setAnswers({ ...answers, [questions[currentQuestion].id]: answer });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResults(true);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const currentQuestionData = questions[currentQuestion];
  const selectedAnswer = answers[currentQuestionData.id];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <section className="pt-28 pb-16 min-h-[calc(100vh-80px)]">
        <div className="container mx-auto px-4">
          <AnimatePresence mode="wait">
            {!showResults ? (
              <motion.div
                key="quiz"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="max-w-2xl mx-auto"
              >
                {/* Progress */}
                <div className="mb-8">
                  <div className="flex justify-between text-sm text-muted-foreground mb-2">
                    <span>Întrebarea {currentQuestion + 1} din {questions.length}</span>
                    <span>{Math.round(progress)}% completat</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>

                {/* Question */}
                <motion.div
                  key={currentQuestion}
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -50 }}
                  transition={{ duration: 0.3 }}
                  className="bg-card rounded-2xl border border-border p-8 shadow-lg"
                >
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center">
                      <currentQuestionData.icon className="w-7 h-7 text-primary" />
                    </div>
                    <h2 className="font-display text-xl md:text-2xl font-bold text-foreground">
                      {currentQuestionData.question}
                    </h2>
                  </div>

                  <div className="space-y-3">
                    {currentQuestionData.options.map((option, index) => (
                      <button
                        key={index}
                        onClick={() => handleAnswer(option)}
                        className={`w-full p-4 rounded-xl border-2 text-left transition-all duration-200 ${
                          selectedAnswer === option
                            ? "border-primary bg-primary/5"
                            : "border-border hover:border-primary/50 hover:bg-secondary/50"
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div
                            className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors ${
                              selectedAnswer === option
                                ? "border-primary bg-primary"
                                : "border-muted-foreground"
                            }`}
                          >
                            {selectedAnswer === option && (
                              <CheckCircle className="w-3 h-3 text-primary-foreground" />
                            )}
                          </div>
                          <span className="text-foreground">{option}</span>
                        </div>
                      </button>
                    ))}
                  </div>

                  {/* Navigation */}
                  <div className="flex justify-between mt-8 pt-6 border-t border-border">
                    <Button
                      variant="ghost"
                      onClick={handlePrevious}
                      disabled={currentQuestion === 0}
                      className="gap-2"
                    >
                      <ArrowLeft className="w-4 h-4" />
                      Înapoi
                    </Button>
                    <Button
                      variant="default"
                      onClick={handleNext}
                      disabled={!selectedAnswer}
                      className="gap-2"
                    >
                      {currentQuestion === questions.length - 1 ? "Vezi rezultatele" : "Continuă"}
                      <ArrowRight className="w-4 h-4" />
                    </Button>
                  </div>
                </motion.div>
              </motion.div>
            ) : (
              <motion.div
                key="results"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="max-w-3xl mx-auto"
              >
                {/* Results Header */}
                <div className="text-center mb-10">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.2, type: "spring" }}
                    className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6"
                  >
                    <CheckCircle className="w-10 h-10 text-primary" />
                  </motion.div>
                  <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
                    Rezultatele tale
                  </h1>
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/20 text-accent-foreground">
                    <Brain className="w-4 h-4 text-accent" />
                    <span className="font-medium">Profil: {results.profile}</span>
                  </div>
                </div>

                {/* Recommendations */}
                <div className="space-y-4">
                  <h2 className="font-display text-xl font-semibold text-foreground mb-4">
                    Facultăți recomandate
                  </h2>
                  {results.recommendations.map((rec, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 + index * 0.1 }}
                      className="p-6 rounded-2xl bg-card border border-border hover:shadow-lg transition-shadow"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-display text-lg font-semibold text-foreground">
                            {rec.name}
                          </h3>
                          <p className="text-sm text-muted-foreground">{rec.university}</p>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-primary">{rec.score}%</div>
                          <div className="text-xs text-muted-foreground">compatibilitate</div>
                        </div>
                      </div>
                      <div className="mt-4">
                        <Progress value={rec.score} className="h-2" />
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* CTA */}
                <div className="flex flex-col sm:flex-row gap-4 justify-center mt-10">
                  <Button variant="accent" size="lg">
                    Primește raportul complet
                  </Button>
                  <Button variant="outline" size="lg" onClick={() => {
                    setShowResults(false);
                    setCurrentQuestion(0);
                    setAnswers({});
                  }}>
                    Reia testul
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Quiz;
