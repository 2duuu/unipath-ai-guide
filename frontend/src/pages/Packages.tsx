import Navbar from "@/components/Navbar";
import PricingSection from "@/components/PricingSection";
import CTASection from "@/components/CTASection";
import Footer from "@/components/Footer";
import { ClaimPackageButton } from "@/components/ClaimPackageButton";
import { ViewPackageDetailsButton } from "@/components/ViewPackageDetailsButton";
import { PackageTier, PACKAGE_DETAILS } from "@/lib/packages";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { CheckCircle2, Sparkles } from "lucide-react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

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
                const isPopular = tier === PackageTier.DECISION_CLARITY;

                return (
                  <motion.div
                    key={tier}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="relative"
                  >
                    {isPopular && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 z-10">
                        <Badge className="bg-[#F59E0B] hover:bg-[#F59E0B] text-white px-4 py-1 text-sm font-semibold">
                          ⭐ Popular
                        </Badge>
                      </div>
                    )}
                    
                    <Card 
                      className={`flex flex-col h-full ${isPopular ? 'border-[#3B82F6] border-2 shadow-lg' : 'border-border'}`}
                    >
                      <CardHeader className="text-center pb-4">
                        <CardTitle className="text-2xl font-bold mb-2">{details.name}</CardTitle>
                        <div className="text-[#3B82F6] font-semibold mb-3">{details.displayName}</div>
                        <p className="text-sm text-muted-foreground mb-4">{details.description}</p>
                        <div className="space-y-1">
                          <div className="flex items-baseline justify-center gap-1">
                            <span className="text-sm text-muted-foreground">€</span>
                            <span className="text-5xl font-bold">
                              {details.price}
                            </span>
                          </div>
                          <div className="text-sm text-muted-foreground">VAT included</div>
                        </div>
                      </CardHeader>
                      
                      <CardContent className="flex-1 pt-6">
                        <ul className="space-y-3">
                          {features.map((feature, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <CheckCircle2 className="h-5 w-5 text-[#3B82F6] mt-0.5 flex-shrink-0" />
                              <span className="text-sm text-left">{feature}</span>
                            </li>
                          ))}
                        </ul>
                      </CardContent>
                      
                      <CardFooter className="flex flex-col gap-3 pt-6">
                        {isLoggedIn ? (
                          <ClaimPackageButton
                            packageTier={tier}
                            packageName={details.displayName}
                            className="w-full"
                            onSuccess={handleClaimSuccess}
                          />
                        ) : (
                          <a href="/login" className="w-full">
                            <Button className="w-full">
                              Login to Get Package
                            </Button>
                          </a>
                        )}
                        <ViewPackageDetailsButton
                          packageTier={tier}
                          packageFeatures={features}
                          className="w-full"
                          variant="outline"
                        />
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
