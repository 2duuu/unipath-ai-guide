import { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, GraduationCap, User, Package, Crown, Lock, Check, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { getPackageInfo } from "@/services/packages";
import { PackageInfo, PackageTier, PACKAGE_DETAILS, PackageFeature, hasFeature } from "@/lib/packages";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const navLinks = [
  { href: "/", label: "Acasă" },
  { href: "/cum-functioneaza", label: "Cum funcționează AI" },
  { href: "/pachete", label: "Pachete" },
  { href: "/facultati", label: "Facultăți" },
  { href: "/contact", label: "Contact" },
];

const FEATURE_LABELS: Record<PackageFeature, string> = {
  [PackageFeature.BASIC_QUIZ]: 'Chestionar Academic de Bază',
  [PackageFeature.UNIVERSITY_RECOMMENDATIONS]: 'Recomandări Universități',
  [PackageFeature.ADVANCED_AI_COMPARISONS]: 'Comparații AI Avansate',
  [PackageFeature.RANKED_RECOMMENDATIONS]: 'Recomandări Clasificate',
  [PackageFeature.TRADEOFF_ANALYSIS]: 'Analiză Compromisuri',
  [PackageFeature.ADMISSION_PROBABILITY]: 'Probabilitate Admitere',
  [PackageFeature.PDF_SUMMARY]: 'Descărcare Raport PDF',
  [PackageFeature.UNLIMITED_AI_CHAT]: 'Chat AI Nelimitat',
  [PackageFeature.APPLICATION_STRATEGY]: 'Ghid Strategie Aplicare',
  [PackageFeature.DEADLINE_TIMELINE]: 'Calendar Termene Limită',
  [PackageFeature.MOTIVATION_LETTER_TRAINING]: 'Training Scrisoare Motivație',
  [PackageFeature.CV_TRAINING]: 'Training CV',
  [PackageFeature.AI_FEEDBACK]: 'Feedback AI Documente',
  [PackageFeature.VIDEO_COUNSELING]: 'Sesiuni Consiliere Video',
  [PackageFeature.HUMAN_GUIDANCE]: 'Îndrumare Expert Uman',
  [PackageFeature.DOCUMENT_CHECKS]: 'Verificare Documente',
  [PackageFeature.SUBMISSION_PREP]: 'Pregătire Trimitere',
  [PackageFeature.DEADLINE_TRACKING]: 'Urmărire Termene',
  [PackageFeature.PEER_INSIGHTS]: 'Perspective Colegi',
};

const ALL_FEATURES = Object.values(PackageFeature);

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated, user } = useAuth();
  const [packageInfo, setPackageInfo] = useState<PackageInfo | null>(null);

  const handleNavClick = (href: string, e: React.MouseEvent<HTMLAnchorElement>) => {
    if (location.pathname === href) {
      e.preventDefault();
      window.scrollTo(0, 0);
      window.location.reload();
    }
  };

  useEffect(() => {
    const fetchPackageInfo = async () => {
      if (isAuthenticated) {
        try {
          const info = await getPackageInfo();
          setPackageInfo(info);
        } catch (err) {
          console.error('Error fetching package info:', err);
          // Set free tier as default
          setPackageInfo({
            package_tier: PackageTier.FREE,
            purchased_at: null,
            expires_at: null,
            features: []
          });
        }
      }
    };

    fetchPackageInfo();

    // Listen for package update events
    const handlePackageUpdate = () => {
      fetchPackageInfo();
    };

    window.addEventListener('packageUpdated', handlePackageUpdate);

    return () => {
      window.removeEventListener('packageUpdated', handlePackageUpdate);
    };
  }, [isAuthenticated]);

  const getPackageIcon = (tier: PackageTier) => {
    if (tier === PackageTier.FREE) return <Package className="w-4 h-4" />;
    return <Crown className="w-4 h-4" />;
  };

  const getPackageColor = (tier: PackageTier) => {
    switch (tier) {
      case PackageTier.FREE:
        return "bg-gray-500/10 text-gray-600 hover:bg-gray-500/20";
      case PackageTier.DECISION_CLARITY:
        return "bg-blue-500/10 text-blue-600 hover:bg-blue-500/20";
      case PackageTier.APPLICATION_PREP:
        return "bg-purple-500/10 text-purple-600 hover:bg-purple-500/20";
      case PackageTier.GUIDED_SUPPORT:
        return "bg-amber-500/10 text-amber-600 hover:bg-amber-500/20";
      default:
        return "bg-gray-500/10 text-gray-600 hover:bg-gray-500/20";
    }
  };

  const handleFeatureClick = (feature: PackageFeature, isLocked: boolean) => {
    if (isLocked) {
      navigate('/pachete');
    } else {
      // Navigate to specific feature pages when unlocked
      switch (feature) {
        case PackageFeature.BASIC_QUIZ:
          navigate('/quiz');
          break;
        case PackageFeature.UNIVERSITY_RECOMMENDATIONS:
          navigate('/facultati');
          break;
        default:
          navigate('/pachete');
      }
    }
  };

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-50 glass border-b border-border/50"
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <motion.div 
              className="w-10 h-10 rounded-xl bg-gradient-primary flex items-center justify-center shadow-md group-hover:shadow-glow transition-shadow duration-300"
              whileHover={{ rotate: [0, -5, 5, -5, 5, 0] }}
              transition={{ duration: 0.5 }}
            >
              <GraduationCap className="w-6 h-6 text-primary-foreground" />
            </motion.div>
            <span className="font-display font-bold text-xl text-foreground">
              Uni<span className="text-primary">Hub</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                onClick={(e) => handleNavClick(link.href, e)}
                className="px-4 py-2 text-sm font-medium text-foreground/80 hover:text-primary transition-colors rounded-lg hover:bg-primary/5"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <>
                {packageInfo && (
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className={`gap-2 ${getPackageColor(packageInfo.package_tier)}`}
                      >
                        {getPackageIcon(packageInfo.package_tier)}
                        {PACKAGE_DETAILS[packageInfo.package_tier]?.name || 'Free'}
                        <ChevronDown className="w-4 h-4 ml-1" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-80">
                      <DropdownMenuLabel className="flex items-center justify-between">
                        <span>Beneficiile Pachetului Tău</span>
                        {packageInfo.package_tier === PackageTier.FREE && (
                          <span className="text-xs font-normal text-muted-foreground">Free Plan</span>
                        )}
                      </DropdownMenuLabel>
                      <DropdownMenuSeparator />
                      <div className="max-h-[400px] overflow-y-auto">
                        {ALL_FEATURES.map((feature) => {
                          const isUnlocked = hasFeature(packageInfo, feature);
                          return (
                            <DropdownMenuItem
                              key={feature}
                              onClick={() => handleFeatureClick(feature, !isUnlocked)}
                              className="flex items-start gap-3 py-3 cursor-pointer"
                            >
                              <div className="mt-0.5">
                                {isUnlocked ? (
                                  <Check className="w-4 h-4 text-green-600" />
                                ) : (
                                  <Lock className="w-4 h-4 text-muted-foreground" />
                                )}
                              </div>
                              <span className={`text-sm flex-1 ${!isUnlocked ? 'text-muted-foreground' : ''}`}>
                                {FEATURE_LABELS[feature]}
                              </span>
                            </DropdownMenuItem>
                          );
                        })}
                      </div>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem asChild>
                        <Link to="/pachete" className="w-full cursor-pointer text-primary font-medium">
                          {packageInfo.package_tier === PackageTier.FREE ? 'Upgrade la Premium' : 'Vezi Toate Pachetele'}
                        </Link>
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                )}
                <Link to="/cont">
                  <Button variant="ghost" size="sm" className="gap-2">
                    <User className="w-4 h-4" />
                    {user?.username || 'Contul meu'}
                  </Button>
                </Link>
                <Link to="/quiz">
                  <Button variant="default" size="sm">
                    Începe Quiz
                  </Button>
                </Link>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="outline" size="sm">
                    Autentificare
                  </Button>
                </Link>
                <Link to="/quiz">
                  <Button variant="default" size="sm">
                    Începe Quiz
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-foreground hover:bg-primary/5 rounded-lg transition-colors"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="md:hidden glass border-t border-border/50"
          >
            <div className="container mx-auto px-4 py-4 space-y-2">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  to={link.href}
                  onClick={(e) => {
                    handleNavClick(link.href, e);
                    setIsOpen(false);
                  }}
                  className="block px-4 py-3 text-foreground/80 hover:text-primary hover:bg-primary/5 rounded-lg transition-colors"
                >
                  {link.label}
                </Link>
              ))}
              <div className="pt-4 space-y-2 border-t border-border/50">
                {isAuthenticated ? (
                  <>
                    {packageInfo && (
                      <Link to="/pachete" onClick={() => setIsOpen(false)}>
                        <Button 
                          variant="ghost" 
                          className={`w-full gap-2 ${getPackageColor(packageInfo.package_tier)}`}
                        >
                          {getPackageIcon(packageInfo.package_tier)}
                          {PACKAGE_DETAILS[packageInfo.package_tier]?.name || 'Free'}
                        </Button>
                      </Link>
                    )}
                    <Link to="/cont" onClick={() => setIsOpen(false)}>
                      <Button variant="outline" className="w-full gap-2">
                        <User className="w-4 h-4" />
                        Contul meu
                      </Button>
                    </Link>
                    <Link to="/quiz" onClick={() => setIsOpen(false)}>
                      <Button variant="default" className="w-full">
                        Începe Quiz
                      </Button>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link to="/login" onClick={() => setIsOpen(false)}>
                      <Button variant="outline" className="w-full">
                        Autentificare
                      </Button>
                    </Link>
                    <Link to="/quiz" onClick={() => setIsOpen(false)}>
                      <Button variant="default" className="w-full">
                        Începe Quiz
                      </Button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;
