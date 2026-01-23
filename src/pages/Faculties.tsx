import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Search, Filter, MapPin, Users, Award, ArrowRight, Loader2, X, Lock, Sparkles } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getPackageInfo } from "@/services/packages";
import { PackageInfo, PackageTier } from "@/lib/packages";
import { useNavigate } from "react-router-dom";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface University {
  id: number;
  name: string;
  name_en: string;
  city: string;
  country: string;
  description: string;
  tuition_annual_eur: number | null;
  tuition_annual_ron: number | null;
  acceptance_rate: number | null;
  student_count: number | null;
  type: string;
  programs_count: number;
  program_fields: string[];
  website: string;
  national_rank: number | null;
}

const fieldTranslations: Record<string, string> = {
  "stem": "STEM",
  "business": "Business & Economics",
  "arts_humanities": "Arts & Humanities",
  "medicine": "Medicine",
  "law": "Law",
  "social_sciences": "Social Sciences",
  "engineering": "Engineering",
  "it": "IT & Technology",
};

const Faculties = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCity, setSelectedCity] = useState("All");
  const [selectedDomain, setSelectedDomain] = useState("All");
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedUniversity, setSelectedUniversity] = useState<University | null>(null);
  const [packageInfo, setPackageInfo] = useState<PackageInfo | null>(null);
  const [packageLoading, setPackageLoading] = useState(true);
  const [showLockedDialog, setShowLockedDialog] = useState(false);

  // Fetch universities from API
  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/universities');
        if (!response.ok) {
          throw new Error('Failed to fetch universities');
        }
        const data = await response.json();
        setUniversities(data.universities || []);
        setError(null);
      } catch (err) {
        console.error('Error fetching universities:', err);
        setError('We could not load universities. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchUniversities();
  }, []);

  // Fetch package info
  useEffect(() => {
    const fetchPackageInfo = async () => {
      try {
        setPackageLoading(true);
        const info = await getPackageInfo();
        setPackageInfo(info);
      } catch (err) {
        console.error('Error fetching package info:', err);
        // Set free tier as default if not logged in or error
        setPackageInfo({
          package_tier: PackageTier.FREE,
          purchased_at: null,
          expires_at: null,
          features: []
        });
      } finally {
        setPackageLoading(false);
      }
    };

    fetchPackageInfo();
  }, []);

  const hasActivePackage = packageInfo && packageInfo.package_tier !== PackageTier.FREE;

  const handleAICompatibility = (university: University) => {
    if (!hasActivePackage) {
      // Show locked dialog instead of direct redirect
      setShowLockedDialog(true);
    } else {
      // TODO: Implement AI compatibility feature
      alert(`AI compatibility for ${university.name} will be available soon!`);
    }
  };

  const handleUpgradeClick = () => {
    setShowLockedDialog(false);
    navigate('/pachete');
  };

  // Get unique cities from universities
  const cities = ["All", ...Array.from(new Set(universities.map(u => u.city).filter(Boolean)))].sort();
  
  // Get unique domains from universities
  const domains = ["All", ...Array.from(new Set(
    universities.flatMap(u => u.program_fields.map(f => fieldTranslations[f] || f))
  ))].sort();

  const filteredUniversities = universities.filter((university) => {
    const matchesSearch = university.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      university.name_en.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCity = selectedCity === "All" || university.city === selectedCity;
    const matchesDomain = selectedDomain === "All" || 
      university.program_fields.some(f => (fieldTranslations[f] || f) === selectedDomain);
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
              Explore <span className="text-primary">universities</span> in Romania
            </h1>
            <p className="text-lg text-muted-foreground">
              Search and compare universities to find the right one for you.
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
                    placeholder="Search universities..."
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

      {/* Universities Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
              <span className="ml-3 text-muted-foreground">Loading universities...</span>
            </div>
          ) : error ? (
            <div className="text-center py-20">
              <p className="text-destructive mb-4">{error}</p>
              <Button onClick={() => window.location.reload()}>
                Try again
              </Button>
            </div>
          ) : (
            <>
              <div className="flex justify-between items-center mb-8">
                <p className="text-muted-foreground">
                  {filteredUniversities.length} universities found
                </p>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredUniversities.map((university, index) => (
                  <motion.div
                    key={university.id}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4, delay: index * 0.05 }}
                    className="bg-card rounded-2xl border border-border p-6 hover:shadow-lg hover:border-primary/30 transition-all duration-300 group"
                  >
                    <div className="flex gap-2 mb-4 flex-wrap">
                      {university.type && (
                        <span className="inline-flex px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium">
                          {university.type === 'public' ? 'Public' : 'Private'}
                        </span>
                      )}
                      {university.national_rank && (
                        <span className="inline-flex px-3 py-1 rounded-full bg-amber-500/10 text-amber-600 text-xs font-medium">
                          #{university.national_rank} in Romania
                        </span>
                      )}
                    </div>

                    <h3 className="font-display text-xl font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                      {university.name}
                    </h3>
                    <p className="text-muted-foreground text-sm mb-4 line-clamp-2">
                      {university.description || "University in Romania"}
                    </p>

                    <div className="flex flex-wrap gap-4 mb-6">
                      <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                        <MapPin className="w-4 h-4" />
                        {university.city}
                      </div>
                      {university.student_count && (
                        <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                          <Users className="w-4 h-4" />
                          {university.student_count.toLocaleString()} students
                        </div>
                      )}
                      <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                        <Award className="w-4 h-4" />
                        {university.programs_count} programs
                      </div>
                    </div>

                    {(university.tuition_annual_ron || university.tuition_annual_eur) && (
                      <p className="text-sm text-muted-foreground mb-4">
                        Tuition: {university.tuition_annual_ron 
                          ? `${university.tuition_annual_ron.toLocaleString()} RON/an` 
                          : `${university.tuition_annual_eur?.toLocaleString()} EUR/an`}
                      </p>
                    )}

                    <div className="flex flex-col gap-2">
                      <Button 
                        variant="outline" 
                        className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
                        onClick={() => setSelectedUniversity(university)}
                      >
                        View details
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                      
                      <Button 
                        variant={hasActivePackage ? "default" : "secondary"}
                        className={`w-full relative ${!hasActivePackage ? 'opacity-60' : ''}`}
                        onClick={() => handleAICompatibility(university)}
                        disabled={packageLoading}
                      >
                        {!hasActivePackage && (
                          <Lock className="w-4 h-4 mr-2" />
                        )}
                        {hasActivePackage && (
                          <Sparkles className="w-4 h-4 mr-2" />
                        )}
                        Check AI compatibility
                        {!hasActivePackage && (
                          <span className="ml-2 text-xs opacity-75">(Premium)</span>
                        )}
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>

              {filteredUniversities.length === 0 && !loading && (
                <div className="text-center py-20">
                  <p className="text-muted-foreground text-lg mb-2">
                    We couldn't find universities matching your filters
                  </p>
                  <p className="text-muted-foreground text-sm">
                    Try adjusting the filters or search term
                  </p>
                </div>
              )}
            </>
          )}
        </div>
      </section>

      {/* University Details Modal */}
      {selectedUniversity && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.2 }}
            className="bg-background rounded-2xl border border-border max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          >
            {/* Modal Header */}
            <div className="sticky top-0 bg-background border-b border-border p-6 flex justify-between items-start">
              <div>
                <h2 className="font-display text-2xl font-bold text-foreground mb-2">
                  {selectedUniversity.name}
                </h2>
                <p className="text-muted-foreground">{selectedUniversity.city}, {selectedUniversity.country}</p>
              </div>
              <button
                onClick={() => setSelectedUniversity(null)}
                className="p-2 hover:bg-secondary rounded-lg transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 space-y-6">
              {/* Tags */}
              <div className="flex gap-2 flex-wrap">
                {selectedUniversity.type && (
                  <span className="inline-flex px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium">
                    {selectedUniversity.type === 'public' ? 'Public' : 'Private'}
                  </span>
                )}
                {selectedUniversity.national_rank && (
                  <span className="inline-flex px-3 py-1 rounded-full bg-amber-500/10 text-amber-600 text-xs font-medium">
                    #{selectedUniversity.national_rank} in Romania
                  </span>
                )}
              </div>

              {/* Description */}
              <div>
                <h3 className="font-semibold text-foreground mb-2">Description</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {selectedUniversity.description || "No details are available for this university."}
                </p>
              </div>

              {/* Key Information */}
              <div className="grid md:grid-cols-2 gap-4">
                {selectedUniversity.student_count && (
                  <div className="bg-secondary/50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Users className="w-5 h-5 text-primary" />
                      <span className="font-semibold text-foreground">Student count</span>
                    </div>
                    <p className="text-muted-foreground">{selectedUniversity.student_count.toLocaleString()}</p>
                  </div>
                )}
                
                <div className="bg-secondary/50 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Award className="w-5 h-5 text-primary" />
                    <span className="font-semibold text-foreground">Study programs</span>
                  </div>
                  <p className="text-muted-foreground">{selectedUniversity.programs_count}</p>
                </div>

                {selectedUniversity.acceptance_rate && (
                  <div className="bg-secondary/50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="font-semibold text-foreground">Acceptance rate</span>
                    </div>
                    <p className="text-muted-foreground">{(selectedUniversity.acceptance_rate * 100).toFixed(1)}%</p>
                  </div>
                )}

                {(selectedUniversity.tuition_annual_ron || selectedUniversity.tuition_annual_eur) && (
                  <div className="bg-secondary/50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="font-semibold text-foreground">Annual tuition</span>
                    </div>
                    <p className="text-muted-foreground">
                      {selectedUniversity.tuition_annual_ron 
                        ? `${selectedUniversity.tuition_annual_ron.toLocaleString()} RON` 
                        : `${selectedUniversity.tuition_annual_eur?.toLocaleString()} EUR`}
                    </p>
                  </div>
                )}
              </div>

              {/* Program Fields */}
              {selectedUniversity.program_fields.length > 0 && (
                <div>
                  <h3 className="font-semibold text-foreground mb-3">Fields of study</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedUniversity.program_fields.map((field) => (
                      <span
                        key={field}
                        className="px-3 py-1 rounded-full bg-primary/10 text-primary text-sm"
                      >
                        {fieldTranslations[field] || field}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Website Link */}
              {selectedUniversity.website && (
                <div>
                  <a
                    href={selectedUniversity.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-primary hover:underline"
                  >
                    Visit university website
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </a>
                </div>
              )}

              {/* Close Button */}
              <Button
                onClick={() => setSelectedUniversity(null)}
                className="w-full"
              >
                Close
              </Button>
            </div>
          </motion.div>
        </div>
      )}

      {/* Locked Feature Dialog */}
      <Dialog open={showLockedDialog} onOpenChange={setShowLockedDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-full bg-amber-500/10">
              <Lock className="w-6 h-6 text-amber-600" />
            </div>
            <DialogTitle className="text-center">Premium Feature Locked</DialogTitle>
            <DialogDescription className="text-center pt-2">
              AI compatibility is available only for premium users.
              Upgrade now to unlock this feature and more!
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="flex-col sm:flex-col gap-2 sm:gap-2">
            <Button onClick={handleUpgradeClick} className="w-full">
              Upgrade to Premium
            </Button>
            <Button variant="outline" onClick={() => setShowLockedDialog(false)} className="w-full">
              Maybe later
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Faculties;
