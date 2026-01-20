import { useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, GraduationCap, User, Badge } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { plans } from "@/data/plans";
import { BenefitsModal } from "@/components/BenefitsModal";

const navLinks = [
  { href: "/", label: "Acasă" },
  { href: "/cum-functioneaza", label: "Cum funcționează AI" },
  { href: "/pachete", label: "Pachete" },
  { href: "/facultati", label: "Facultăți" },
  { href: "/contact", label: "Contact" },
];

const packageLevels: Record<string, { label: string; color: string }> = {
  choose_confidently: { label: "Level 1", color: "bg-blue-500" },
  prepare_to_apply: { label: "Level 2", color: "bg-purple-500" },
  apply_with_support: { label: "Level 3", color: "bg-amber-500" },
};

const getPackageDisplay = (pkg?: string | null) => {
  if (!pkg) {
    return { label: "Free", color: "bg-gray-400", name: "Gratuit" };
  }
  const plan = plans.find(p => p.key === pkg);
  if (plan) {
    return { 
      label: pkg === "choose_confidently" ? "L1" : pkg === "prepare_to_apply" ? "L2" : "L3",
      color: pkg === "choose_confidently" ? "bg-blue-500" : pkg === "prepare_to_apply" ? "bg-purple-500" : "bg-amber-500",
      name: plan.name
    };
  }
  return { label: "Free", color: "bg-gray-400", name: "Gratuit" };
};

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showBenefitsModal, setShowBenefitsModal] = useState(false);
  const { isAuthenticated, user } = useAuth();
  const packageDisplay = getPackageDisplay(user?.package_level);

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-50 glass border-b border-border/50"
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Package and Logo */}
          <div className="flex items-center gap-3 relative">
            <div className="relative group">
              <button
                onClick={() => setShowBenefitsModal(!showBenefitsModal)}
                title={packageDisplay.name}
                className="hidden md:flex items-center group"
              >
                {/* Gradient Hat Icon with Package Color */}
                <motion.div 
                  className={`w-10 h-10 rounded-xl ${packageDisplay.color} flex items-center justify-center shadow-md transition-all duration-300`}
                  whileHover={{ rotate: [0, -5, 5, -5, 5, 0], scale: 1.1 }}
                  transition={{ duration: 0.5 }}
                >
                  <GraduationCap className="w-6 h-6 text-white" />
                </motion.div>
              </button>
              
              {/* Hover Tooltip - Package Name with Fade */}
              <motion.div
                initial={{ opacity: 0, y: -5 }}
                whileHover={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
                className="absolute left-0 -bottom-8 bg-gray-900 text-white text-xs px-2 py-1 rounded whitespace-nowrap pointer-events-none opacity-0 group-hover:opacity-100"
              >
                {packageDisplay.name}
              </motion.div>
              
              <BenefitsModal 
                open={showBenefitsModal} 
                onOpenChange={setShowBenefitsModal} 
                packageKey={user?.package_level} 
              />
            </div>
            
            <Link to="/" className="flex items-center gap-2 group">
              <span className="font-display font-bold text-xl text-foreground">
                Uni<span className="text-primary">Hub</span>
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className="px-4 py-2 text-sm font-medium text-foreground/80 hover:text-primary transition-colors rounded-lg hover:bg-primary/5"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <Link to="/cont">
                <Button variant="ghost" size="sm" className="gap-2">
                  <User className="w-4 h-4" />
                  {user?.username || 'Contul meu'}
                </Button>
              </Link>
            ) : (
              <Link to="/login">
                <Button variant="outline" size="sm">
                  Autentificare
                </Button>
              </Link>
            )}
            <Link to="/quiz">
              <Button variant="default" size="sm">
                Începe Quiz
              </Button>
            </Link>
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
                  onClick={() => setIsOpen(false)}
                  className="block px-4 py-3 text-foreground/80 hover:text-primary hover:bg-primary/5 rounded-lg transition-colors"
                >
                  {link.label}
                </Link>
              ))}
              <div className="pt-4 space-y-2 border-t border-border/50">
                <Link to="/pachete" onClick={() => setIsOpen(false)}>
                  <Button variant="secondary" className="w-full gap-2">
                    <div className={`w-6 h-6 rounded-full ${packageDisplay.color} flex items-center justify-center text-white text-xs font-bold`}>
                      {packageDisplay.label === "Free" ? "F" : packageDisplay.label}
                    </div>
                    <span className="flex-1 text-left">{packageDisplay.name}</span>
                  </Button>
                </Link>
                {isAuthenticated ? (
                  <Link to="/cont" onClick={() => setIsOpen(false)}>
                    <Button variant="outline" className="w-full gap-2">
                      <User className="w-4 h-4" />
                      {user?.username || 'Contul meu'}
                    </Button>
                  </Link>
                ) : (
                  <Link to="/login" onClick={() => setIsOpen(false)}>
                    <Button variant="outline" className="w-full gap-2">
                      <User className="w-4 h-4" />
                      Autentificare
                    </Button>
                  </Link>
                )}
                <Link to="/quiz" onClick={() => setIsOpen(false)}>
                  <Button variant="default" className="w-full">
                    Începe Quiz
                  </Button>
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;
