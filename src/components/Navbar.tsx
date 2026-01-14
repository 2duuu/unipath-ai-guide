import { useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, GraduationCap, User } from "lucide-react";
import { Button } from "@/components/ui/button";

const navLinks = [
  { href: "/", label: "Acasă" },
  { href: "/cum-functioneaza", label: "Cum funcționează AI" },
  { href: "/pachete", label: "Pachete" },
  { href: "/facultati", label: "Facultăți" },
  { href: "/quiz", label: "Pula" },
  { href: "/contact", label: "Contact" },
];

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

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
            <div className="w-10 h-10 rounded-xl bg-gradient-primary flex items-center justify-center shadow-md group-hover:shadow-glow transition-shadow duration-300">
              <GraduationCap className="w-6 h-6 text-primary-foreground" />
            </div>
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
                className="px-4 py-2 text-sm font-medium text-foreground/80 hover:text-primary transition-colors rounded-lg hover:bg-primary/5"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-3">
            <Link to="/cont">
              <Button variant="ghost" size="sm" className="gap-2">
                <User className="w-4 h-4" />
                Contul meu
              </Button>
            </Link>
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
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;
