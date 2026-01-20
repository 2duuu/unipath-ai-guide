import Navbar from "@/components/Navbar";
import PricingSection from "@/components/PricingSection";
import CTASection from "@/components/CTASection";
import Footer from "@/components/Footer";
import { ClaimPackageButton } from "@/components/ClaimPackageButton";
import { PackageTier, PACKAGE_DETAILS } from "@/lib/packages";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { CheckCircle2, Sparkles } from "lucide-react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const PACKAGE_FEATURES = {
  [PackageTier.DECISION_CLARITY]: [
    'Basic Quiz & Recommendations',
    'Advanced AI Comparisons',
    'Ranked Recommendations',
    'Trade-off Analysis',
    'Admission Probability',
    'PDF Summary Download',
    'Unlimited AI Chat',
  ],
  [PackageTier.APPLICATION_PREP]: [
    'Everything in Choose Confidently',
    'Application Strategy Guide',
    'Deadline Timeline',
    'Motivation Letter Training',
    'CV Training',
    'AI Document Feedback',
  ],
  [PackageTier.GUIDED_SUPPORT]: [
    'Everything in Prepare to Apply',
    'Video Counseling Sessions',
    'Human Expert Guidance',
    'Document Checks',
    'Submission Preparation',
    'Deadline Tracking',
    'Peer Insights',
  ],
};

const Packages = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, []);

  const handleClaimSuccess = () => {
    // Package claimed successfully - user can check it in their profile
  };

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

      {/* Special Offer Banner */}
      <section className="py-8">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="p-6 rounded-lg bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950 dark:to-emerald-950 border-2 border-green-200 dark:border-green-800 shadow-lg"
            >
              <div className="flex items-center gap-3 mb-3">
                <Sparkles className="h-6 w-6 text-green-600" />
                <h3 className="font-semibold text-xl text-green-900 dark:text-green-100">
                  🎉 Free During Testing Phase!
                </h3>
              </div>
              <p className="text-green-800 dark:text-green-200 mb-4">
                All packages are currently <strong>FREE</strong> during our testing phase! Get full access to premium features 
                and help us improve the platform. Payment gateway will be integrated soon.
              </p>
              {isLoggedIn ? (
                <ClaimPackageButton
                  packageTier={PackageTier.DECISION_CLARITY}
                  packageName="Choose Confidently"
                  variant="default"
                  className="bg-green-600 hover:bg-green-700"
                  onSuccess={handleClaimSuccess}
                />
              ) : (
                <a href="/login" className="inline-block">
                  <button className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold">
                    Login to Get Started
                  </button>
                </a>
              )}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Package Cards */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">All Packages</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {Object.values(PackageTier)
                .filter(tier => tier !== PackageTier.FREE)
                .map((tier) => {
                const details = PACKAGE_DETAILS[tier];
                const features = PACKAGE_FEATURES[tier];
                const isRecommended = tier === PackageTier.DECISION_CLARITY;

                return (
                  <motion.div
                    key={tier}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                  >
                    <Card 
                      className={`flex flex-col h-full ${isRecommended ? 'border-primary shadow-xl relative' : ''}`}
                    >
                      {isRecommended && (
                        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                          <Badge className="bg-primary text-white px-4 py-1">
                            MOST POPULAR
                          </Badge>
                        </div>
                      )}
                      
                      <CardHeader>
                        <CardTitle className="text-xl">{details.displayName}</CardTitle>
                        <CardDescription>{details.description}</CardDescription>
                        <div className="mt-4">
                          <div className="flex items-baseline gap-2">
                            <span className="text-4xl font-bold">
                              €{details.price}
                            </span>
                            <span className="text-sm text-muted-foreground line-through">
                              Regular Price
                            </span>
                          </div>
                          <div className="mt-1">
                            <span className="text-green-600 font-semibold">
                              FREE during testing
                            </span>
                          </div>
                        </div>
                      </CardHeader>
                      
                      <CardContent className="flex-1">
                        <ul className="space-y-3">
                          {features.map((feature, index) => (
                            <li key={index} className="flex items-start gap-2">
                              <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                              <span className="text-sm">{feature}</span>
                            </li>
                          ))}
                        </ul>
                      </CardContent>
                      
                      <CardFooter>
                        {isLoggedIn ? (
                          <ClaimPackageButton
                            packageTier={tier}
                            packageName={details.displayName}
                            className="w-full"
                            onSuccess={handleClaimSuccess}
                          />
                        ) : (
                          <a href="/login" className="w-full">
                            <button className="w-full bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded-lg font-semibold">
                              Login to Get Package
                            </button>
                          </a>
                        )}
                      </CardFooter>
                    </Card>
                  </motion.div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      <CTASection />
      <Footer />
    </div>
  );
};

export default Packages;
