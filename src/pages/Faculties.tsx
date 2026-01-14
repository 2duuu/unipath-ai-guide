import { useState } from "react";
import { motion } from "framer-motion";
import { Search, Filter, MapPin, Clock, Award, ArrowRight } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const faculties = [
  {
    id: 1,
    name: "Facultatea de Informatică",
    university: "Universitatea București",
    city: "București",
    duration: "4 ani",
    avgGrade: 9.2,
    domain: "IT & Tehnologie",
  },
  {
    id: 2,
    name: "Automatică și Calculatoare",
    university: "Universitatea Politehnica București",
    city: "București",
    duration: "4 ani",
    avgGrade: 9.0,
    domain: "Inginerie",
  },
  {
    id: 3,
    name: "Facultatea de Informatică",
    university: "Universitatea Babeș-Bolyai",
    city: "Cluj-Napoca",
    duration: "3 ani",
    avgGrade: 9.1,
    domain: "IT & Tehnologie",
  },
  {
    id: 4,
    name: "Cibernetică și Economie",
    university: "Academia de Studii Economice",
    city: "București",
    duration: "3 ani",
    avgGrade: 8.5,
    domain: "Economie",
  },
  {
    id: 5,
    name: "Facultatea de Medicină",
    university: "UMF Carol Davila",
    city: "București",
    duration: "6 ani",
    avgGrade: 9.5,
    domain: "Medicină",
  },
  {
    id: 6,
    name: "Drept",
    university: "Universitatea București",
    city: "București",
    duration: "4 ani",
    avgGrade: 8.8,
    domain: "Drept",
  },
];

const cities = ["Toate", "București", "Cluj-Napoca", "Iași", "Timișoara"];
const domains = ["Toate", "IT & Tehnologie", "Inginerie", "Economie", "Medicină", "Drept"];

const Faculties = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCity, setSelectedCity] = useState("Toate");
  const [selectedDomain, setSelectedDomain] = useState("Toate");

  const filteredFaculties = faculties.filter((faculty) => {
    const matchesSearch = faculty.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      faculty.university.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCity = selectedCity === "Toate" || faculty.city === selectedCity;
    const matchesDomain = selectedDomain === "Toate" || faculty.domain === selectedDomain;
    return matchesSearch && matchesCity && matchesDomain;
  });

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* Hero */}
      <section className="pt-32 pb-12 bg-hero-gradient">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center max-w-3xl mx-auto mb-10"
          >
            <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-6">
              Explorează <span className="text-primary">facultățile</span> din România
            </h1>
            <p className="text-lg text-muted-foreground">
              Caută și compară peste 150 de facultăți pentru a găsi cea potrivită pentru tine.
            </p>
          </motion.div>

          {/* Search & Filters */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="max-w-4xl mx-auto"
          >
            <div className="bg-card rounded-2xl border border-border p-4 shadow-lg">
              <div className="flex flex-col md:flex-row gap-4">
                {/* Search */}
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                  <Input
                    placeholder="Caută facultăți sau universități..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 h-12"
                  />
                </div>

                {/* City Filter */}
                <div className="flex gap-2 items-center">
                  <Filter className="w-5 h-5 text-muted-foreground" />
                  <select
                    value={selectedCity}
                    onChange={(e) => setSelectedCity(e.target.value)}
                    className="h-12 px-4 rounded-lg border border-border bg-background text-foreground"
                  >
                    {cities.map((city) => (
                      <option key={city} value={city}>{city}</option>
                    ))}
                  </select>
                </div>

                {/* Domain Filter */}
                <select
                  value={selectedDomain}
                  onChange={(e) => setSelectedDomain(e.target.value)}
                  className="h-12 px-4 rounded-lg border border-border bg-background text-foreground"
                >
                  {domains.map((domain) => (
                    <option key={domain} value={domain}>{domain}</option>
                  ))}
                </select>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Faculties Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center mb-8">
            <p className="text-muted-foreground">
              {filteredFaculties.length} facultăți găsite
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredFaculties.map((faculty, index) => (
              <motion.div
                key={faculty.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
                className="bg-card rounded-2xl border border-border p-6 hover:shadow-lg hover:border-primary/30 transition-all duration-300 group"
              >
                <div className="inline-flex px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium mb-4">
                  {faculty.domain}
                </div>

                <h3 className="font-display text-xl font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                  {faculty.name}
                </h3>
                <p className="text-muted-foreground text-sm mb-4">
                  {faculty.university}
                </p>

                <div className="flex flex-wrap gap-4 mb-6">
                  <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                    <MapPin className="w-4 h-4" />
                    {faculty.city}
                  </div>
                  <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                    <Clock className="w-4 h-4" />
                    {faculty.duration}
                  </div>
                  <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                    <Award className="w-4 h-4" />
                    Medie: {faculty.avgGrade}
                  </div>
                </div>

                <Button variant="outline" className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  Vezi compatibilitate AI
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Faculties;
