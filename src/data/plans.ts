export type Plan = {
  key: "choose_confidently" | "prepare_to_apply" | "apply_with_support";
  name: string;
  subtitle: string;
  price: string;
  priceValue: number;
  description: string;
  features: { text: string; included: boolean }[];
  popular: boolean;
  detailedInfo: {
    title: string;
    subtitle: string;
    includes: string[];
    note: string | null;
  };
};

export const plans: Plan[] = [
  {
    key: "choose_confidently",
    name: "Choose Confidently",
    subtitle: "Decision & Clarity",
    price: "36.30",
    priceValue: 36.3,
    description: "Ia decizii informate cu claritate completă",
    features: [
      { text: "Tot din Academic Orientation", included: true },
      { text: "Comparații AI avansate (A vs B vs C)", included: true },
      { text: "Universități & programe clasate după potrivire", included: true },
      { text: "Analiză trade-off-uri (cost, competitivitate)", included: true },
      { text: "Estimări probabilitate admitere (intervale)", included: true },
      { text: "Rezumat PDF pentru părinți", included: true },
      { text: "Chat nelimitat cu AI specializat", included: true },
    ],
    popular: false,
    detailedInfo: {
      title: "Package 1 — Decision & Clarity",
      subtitle: "Choose Confidently",
      includes: [
        "Full UniHub Quiz (core + extended)",
        "University recommendations",
        "Program recommendations",
        "AI explanations of academic fit",
        "High-level difficulty indicators",
        "Advanced AI comparisons (A vs B vs C)",
        "Ranked best-fit universities & programs",
        "Trade-off analysis (cost, competitiveness, outcomes)",
        "Risk & uncertainty overview",
        "AI-based admission probability estimates (ranges)",
        "Parent-friendly written summary (PDF)",
        "Unlimited chat with Trained AI model in academic advising"
      ],
      note: "Ethical note: Admission probabilities are estimates, not guarantees."
    }
  },
  {
    key: "prepare_to_apply",
    name: "Prepare to Apply",
    subtitle: "Application Preparation",
    price: "121",
    priceValue: 121,
    description: "Pregătește aplicația perfectă cu îndrumări personalizate",
    features: [
      { text: "Tot din Decision & Clarity", included: true },
      { text: "Strategie personalizată de aplicare", included: true },
      { text: "Timeline deadline-uri și cerințe", included: true },
      { text: "Training pentru scrisoare de motivație", included: true },
      { text: "Training pentru CV academic", included: true },
      { text: "Feedback asistat de AI + ghidare umană", included: true },
    ],
    popular: true,
    detailedInfo: {
      title: "Package 2 — Application Preparation",
      subtitle: "Prepare to Apply",
      includes: [
        "Everything from Decision & Clarity package",
        "Personalized application strategy",
        "Deadline & requirement timeline",
        "Motivation letter training",
        "Academic CV training",
        "AI-assisted feedback + human guidance"
      ],
      note: "Boundary: UniHub provides guidance and training. All application materials are written by the student."
    }
  },
  {
    key: "apply_with_support",
    name: "Apply with Support",
    subtitle: "Guided Application Support",
    price: "484",
    priceValue: 484,
    description: "Suport complet ghidat pentru aplicare",
    features: [
      { text: "Tot din Application Preparation", included: true },
      { text: "Consiliere academică video call 1-on-1", included: true },
      { text: "Suport ghidat de om pentru aplicare", included: true },
      { text: "Verificări completitudine documente", included: true },
      { text: "Pregătire pentru trimitere", included: true },
      { text: "Tracking deadline-uri & reminder-e", included: true },
      { text: "Sesiuni Peer Insight (Bonus)", included: true },
    ],
    popular: false,
    detailedInfo: {
      title: "Package 3 — Guided Application Support",
      subtitle: "Apply with Support",
      includes: [
        "Everything from Application Preparation package",
        "1-on-1 academic advising video call",
        "Human-guided application support",
        "Document completeness & readiness checks",
        "Submission preparation (no automated applying)",
        "Deadline tracking & reminders",
        "Peer Insight Sessions (Bonus)"
      ],
      note: null
    }
  },
];
