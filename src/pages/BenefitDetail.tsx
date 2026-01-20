import { useParams, useNavigate } from "react-router-dom";
import { plans } from "@/data/plans";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, CheckCircle2, Zap, BookOpen, Users } from "lucide-react";
import { useMemo } from "react";

const BenefitDetail = () => {
  const { packageKey, benefitIndex } = useParams();
  const navigate = useNavigate();

  const plan = useMemo(() => {
    return plans.find(p => p.key === packageKey);
  }, [packageKey]);

  const benefit = useMemo(() => {
    if (!plan || !benefitIndex) return null;
    const index = parseInt(benefitIndex);
    return plan.features[index];
  }, [plan, benefitIndex]);

  if (!plan || !benefit) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="pt-28 pb-16">
          <div className="container mx-auto px-4">
            <Button variant="ghost" onClick={() => navigate(-1)} className="mb-6">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <p className="text-muted-foreground">Benefit not found</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  // Enhanced descriptions for each benefit type
  const getBenefitContent = () => {
    const text = benefit.text;

    // Map benefit text to detailed descriptions
    const contentMap: Record<string, { icon: React.ReactNode; description: string; details: string[] }> = {
      "Tot din": {
        icon: <CheckCircle2 className="w-8 h-8 text-primary" />,
        description: "This package includes everything from the previous package, plus additional premium features.",
        details: [
          "All features from the lower tier are included",
          "Build upon existing capabilities",
          "More comprehensive support and guidance",
          "Enhanced AI tools and resources"
        ]
      },
      "Comparații AI avansate": {
        icon: <Zap className="w-8 h-8 text-primary" />,
        description: "Advanced AI-powered comparison tool that analyzes multiple universities side-by-side.",
        details: [
          "Compare A vs B vs C universities at once",
          "AI analyzes academic fit for each option",
          "Visual comparison charts and metrics",
          "Detailed pros and cons breakdown",
          "Cost-benefit analysis included"
        ]
      },
      "Universități & programe clasate": {
        icon: <BookOpen className="w-8 h-8 text-primary" />,
        description: "Personalized ranking of universities and programs based on your profile and goals.",
        details: [
          "Universities ranked by fit percentage",
          "Programs sorted by compatibility",
          "Real-time ranking updates",
          "Filter by location, cost, and specialization",
          "AI-powered recommendation engine"
        ]
      },
      "Consiliere academică video": {
        icon: <Users className="w-8 h-8 text-primary" />,
        description: "One-on-one academic advising sessions conducted via video call with university counselors.",
        details: [
          "Scheduled 1-on-1 video calls with advisors",
          "Personalized guidance for your situation",
          "Real-time answers to all your questions",
          "Career path discussion and planning",
          "Follow-up support after each session"
        ]
      },
      "Chat nelimitat": {
        icon: <Zap className="w-8 h-8 text-primary" />,
        description: "Unlimited conversations with our specialized AI academic advisor.",
        details: [
          "24/7 access to AI academic specialist",
          "No limits on number of conversations",
          "Instant responses to your questions",
          "Multi-language support available",
          "Context-aware personalized responses"
        ]
      },
      "Suport ghidat de om": {
        icon: <Users className="w-8 h-8 text-primary" />,
        description: "Professional human guidance throughout your application process.",
        details: [
          "Expert application strategists assigned",
          "Step-by-step guided application process",
          "Personal feedback on all materials",
          "Regular check-ins and progress tracking",
          "Emergency support when needed"
        ]
      }
    };

    // Find the best matching benefit content
    for (const [key, content] of Object.entries(contentMap)) {
      if (text.includes(key)) {
        return content;
      }
    }

    // Default content
    return {
      icon: <CheckCircle2 className="w-8 h-8 text-primary" />,
      description: benefit.text,
      details: [
        "Premium feature for this package level",
        "Enhances your university selection experience",
        "Supports better decision making",
        "Personalized to your needs"
      ]
    };
  };

  const content = getBenefitContent();

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="pt-28 pb-16">
        <div className="container mx-auto px-4 max-w-3xl">
          {/* Back Button */}
          <Button
            variant="ghost"
            onClick={() => navigate(-1)}
            className="mb-8"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to {plan.name}
          </Button>

          {/* Header Section */}
          <div className="mb-12">
            <div className="flex items-start gap-6 mb-8">
              <div className="mt-2">
                {content.icon}
              </div>
              <div>
                <h1 className="text-4xl font-bold mb-2">{benefit.text}</h1>
                <p className="text-muted-foreground text-lg">{plan.subtitle}</p>
              </div>
            </div>
          </div>

          {/* Description Card */}
          <Card className="mb-8 border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <p className="text-lg leading-relaxed">{content.description}</p>
            </CardContent>
          </Card>

          {/* Details Section */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>What's Included</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-4">
                {content.details.map((detail, idx) => (
                  <li key={idx} className="flex items-start gap-4">
                    <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle2 className="w-4 h-4 text-primary" />
                    </div>
                    <span className="text-foreground">{detail}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Call to Action */}
          <div className="space-y-4">
            <Card className="border-primary/30 bg-gradient-to-r from-primary/5 to-primary/10">
              <CardContent className="pt-8 text-center">
                <h3 className="text-xl font-semibold mb-2">Ready to get started?</h3>
                <p className="text-muted-foreground mb-6">
                  Unlock all the benefits of the {plan.name} package today
                </p>
                <Button onClick={() => navigate(`/pachete/${packageKey}`)}>
                  View {plan.name} Package
                </Button>
              </CardContent>
            </Card>

            <p className="text-xs text-muted-foreground text-center">
              Interested in comparing packages? <Button variant="link" onClick={() => navigate("/pachete")}>See all plans</Button>
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default BenefitDetail;
