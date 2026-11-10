import { Link } from "react-router-dom";
import { GraduationCap, Mail, Phone, MapPin, Facebook, Instagram, Linkedin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-foreground text-primary-foreground py-16">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-10 md:gap-8">
          {/* Brand */}
          <div className="lg:col-span-1">
            <Link to="/" className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
                <GraduationCap className="w-6 h-6 text-primary-foreground" />
              </div>
              <span className="font-display font-bold text-xl">
                Uni<span className="text-primary">Hub</span>
              </span>
            </Link>
            <p className="text-primary-foreground/70 text-sm mb-6">
              Ghidare personalizată pentru viitorul tău academic. Alege facultatea potrivită cu ajutorul AI-ului nostru.
            </p>
            <div className="flex gap-3">
              {[Facebook, Instagram, Linkedin].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-10 h-10 rounded-lg bg-primary-foreground/10 flex items-center justify-center hover:bg-primary/30 transition-colors"
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-display font-semibold mb-4">Navigare</h4>
            <ul className="space-y-3">
              {[
                { label: "Acasă", href: "/" },
                { label: "Cum funcționează AI", href: "/cum-functioneaza" },
                { label: "Pachete", href: "/pachete" },
                { label: "Facultăți", href: "/facultati" },
                { label: "Quiz", href: "/quiz" },
              ].map((link) => (
                <li key={link.href}>
                  <Link
                    to={link.href}
                    className="text-primary-foreground/70 hover:text-primary transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-display font-semibold mb-4">Resurse</h4>
            <ul className="space-y-3">
              {[
                "Blog",
                "Ghid alegere facultate",
                "FAQ",
                "Termeni și condiții",
                "Politica de confidențialitate",
              ].map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    className="text-primary-foreground/70 hover:text-primary transition-colors text-sm"
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-display font-semibold mb-4">Contact</h4>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <Mail className="w-5 h-5 text-primary mt-0.5" />
                <span className="text-primary-foreground/70 text-sm">
                  contact@unihub.ro
                </span>
              </li>
              <li className="flex items-start gap-3">
                <Phone className="w-5 h-5 text-primary mt-0.5" />
                <span className="text-primary-foreground/70 text-sm">
                  +40 721 234 567
                </span>
              </li>
              <li className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-primary mt-0.5" />
                <span className="text-primary-foreground/70 text-sm">
                  București, România
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-12 pt-8 border-t border-primary-foreground/10 text-center text-primary-foreground/50 text-sm">
          © {new Date().getFullYear()} UniHub. Toate drepturile rezervate.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
