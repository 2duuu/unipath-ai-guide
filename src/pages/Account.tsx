import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate, Link } from "react-router-dom";
import { User, FileText, Calendar, CreditCard, LogOut, Download, ChevronRight, Loader2, Package, Lock, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useAuth } from "@/contexts/AuthContext";
import { getUserQuizResults, getUserQuizAttempts } from "@/services/api";
import { PackageInfoCard } from "@/components/PackageInfoCard";
import { getUserInvoices, type Invoice } from "@/services/invoices";
import { getPackageInfo, claimPackage } from "@/services/packages";
import { PackageInfo, PackageTier } from "@/lib/packages";
import { useToast } from "@/hooks/use-toast";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

const sidebarItems = [
  { id: "profile", label: "My Profile", icon: User },
  { id: "package", label: "My Plan", icon: Package },
  { id: "results", label: "Quiz Results", icon: FileText },
  { id: "appointments", label: "Appointments", icon: Calendar },
  { id: "payments", label: "Payments & Invoices", icon: CreditCard },
];

const mockAIResults = [
  {
    id: 1,
    date: "January 14 2026",
    mainMatch: "Applied Computer Science",
    compatibility: 87,
    description: "Your profile shows a strong inclination toward solving logical problems and abstract structures.",
  },
  {
    id: 2,
    date: "January 10 2026",
    mainMatch: "Automation and Computers",
    compatibility: 82,
    description: "Excellent aptitude for automated systems and programming.",
  },
];

const mockTestHistory = [
  { id: 1, date: "January 14 2026", type: "Full Quiz", questions: 25, score: "87%" },
  { id: 2, date: "January 10 2026", type: "Quick Quiz", questions: 10, score: "82%" },
  { id: 3, date: "January 5 2026", type: "Full Quiz", questions: 25, score: "79%" },
];

const mockAppointments = [
  { id: 1, date: "January 20 2026", time: "14:00", type: "Standard Consultation", status: "Confirmed" },
  { id: 2, date: "January 25 2026", time: "10:00", type: "Premium Session", status: "Pending" },
];

const Account = () => {
  const [activeSection, setActiveSection] = useState("profile");
  const { user, loading, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [quizResults, setQuizResults] = useState<any[]>([]);
  const [quizAttempts, setQuizAttempts] = useState<any[]>([]);
  const [loadingQuizResults, setLoadingQuizResults] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loadingInvoices, setLoadingInvoices] = useState(false);
  const [packageInfo, setPackageInfo] = useState<PackageInfo | null>(null);
  const [showLockedDialog, setShowLockedDialog] = useState(false);
  const [showRevertDialog, setShowRevertDialog] = useState(false);
  const [isReverting, setIsReverting] = useState(false);
  const { toast } = useToast();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login');
    }
  }, [loading, isAuthenticated, navigate]);

  // Fetch quiz results when component mounts
  useEffect(() => {
    if (isAuthenticated && !loading) {
      fetchQuizResults();
      fetchInvoices();
      fetchPackageInfo();
    }

    // Listen for quiz save events
    const handleQuizSaved = () => {
      fetchQuizResults();
    };

    window.addEventListener('quizSaved', handleQuizSaved);

    return () => {
      window.removeEventListener('quizSaved', handleQuizSaved);
    };
  }, [isAuthenticated, loading]);

  const fetchPackageInfo = async () => {
    try {
      const info = await getPackageInfo();
      setPackageInfo(info);
    } catch (error) {
      console.error('Failed to fetch package info:', error);
      setPackageInfo({
        package_tier: PackageTier.FREE,
        purchased_at: null,
        expires_at: null,
        features: []
      });
    }
  };

  const fetchQuizResults = async () => {
    setLoadingQuizResults(true);
    try {
      const [resultsData, attemptsData] = await Promise.all([
        getUserQuizResults(),
        getUserQuizAttempts()
      ]);
      setQuizResults(resultsData.quiz_results || []);
      setQuizAttempts(attemptsData.quiz_attempts || []);
    } catch (error) {
      console.error('Failed to fetch quiz results:', error);
    } finally {
      setLoadingQuizResults(false);
    }
  };

  const fetchInvoices = async () => {
    setLoadingInvoices(true);
    try {
      const data = await getUserInvoices();
      setInvoices(data.invoices || []);
    } catch (error) {
      console.error('Failed to fetch invoices:', error);
    } finally {
      setLoadingInvoices(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const hasActivePackage = packageInfo && packageInfo.package_tier !== PackageTier.FREE;

  const handleDownloadPDF = (attemptId: number) => {
    if (!hasActivePackage) {
      setShowLockedDialog(true);
    } else {
      // TODO: Implement PDF download
      alert('PDF download will be available soon!');
    }
  };

  const handleUpgradeClick = () => {
    setShowLockedDialog(false);
    navigate('/pachete');
  };

  const handleRevertToFree = async () => {
    setIsReverting(true);
    try {
      await claimPackage(PackageTier.FREE);
      
      // Dispatch event to update navbar
      window.dispatchEvent(new CustomEvent('packageUpdated'));
      
      // Refresh package info
      await fetchPackageInfo();
      setRefreshKey(prev => prev + 1);
      
      toast({
        title: 'Plan Updated',
        description: 'You successfully switched back to the free plan.',
      });
      
      setShowRevertDialog(false);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Could not switch back to the free plan. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsReverting(false);
    }
  };

  // Show loading spinner while checking auth
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  // Don't render anything if not authenticated (will redirect)
  if (!isAuthenticated || !user) {
    return null;
  }

  // Get user initials for avatar
  const getInitials = () => {
    if (user.name) {
      return user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    }
    return user.username.slice(0, 2).toUpperCase();
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4">
          {/* Header with gradient */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-primary rounded-2xl p-8 mb-8 text-primary-foreground"
          >
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-white/20 flex items-center justify-center text-2xl font-bold">
                {getInitials()}
              </div>
              <div>
                <h1 className="font-display text-2xl md:text-3xl font-bold">Hi, {user.name || user.username}!</h1>
                <p className="opacity-90">Welcome back to UniHub.</p>
              </div>
            </div>
          </motion.div>

          <div className="grid lg:grid-cols-4 gap-8">
            {/* Sidebar */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="lg:col-span-1"
            >
              <Card className="border-border/50 overflow-hidden">
                <CardContent className="p-0">
                  <nav className="space-y-1 p-2">
                    {sidebarItems.map((item) => (
                      <button
                        key={item.id}
                        onClick={() => setActiveSection(item.id)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-left ${
                          activeSection === item.id
                            ? "bg-primary/10 text-primary font-medium"
                            : "text-foreground/70 hover:bg-muted hover:text-foreground"
                        }`}
                      >
                        <item.icon className="w-5 h-5" />
                        {item.label}
                        {activeSection === item.id && (
                          <ChevronRight className="w-4 h-4 ml-auto" />
                        )}
                      </button>
                    ))}
                    <div className="border-t border-border/50 my-2" />
                    <button 
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-destructive hover:bg-destructive/10 transition-colors text-left"
                    >
                      <LogOut className="w-5 h-5" />
                      Log out
                    </button>
                  </nav>
                </CardContent>
              </Card>
            </motion.div>

            {/* Main Content */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-3"
            >
              {activeSection === "profile" && (
                <Card className="border-border/50">
                  <CardContent className="p-0">
                    <Tabs defaultValue="user-info" className="w-full">
                      <TabsList className="w-full justify-start rounded-none border-b bg-transparent p-0">
                        <TabsTrigger
                          value="user-info"
                          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-4"
                        >
                          Account Info
                        </TabsTrigger>
                        <TabsTrigger
                          value="ai-results"
                          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-4"
                        >
                          AI Results
                        </TabsTrigger>
                        <TabsTrigger
                          value="history"
                          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-4"
                        >
                          Test History
                        </TabsTrigger>
                      </TabsList>

                      <TabsContent value="user-info" className="p-6">
                        <div className="space-y-6">
                          <div>
                            <h3 className="font-semibold text-lg mb-4">Personal Information</h3>
                            <div className="space-y-4">
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <Label className="text-muted-foreground text-sm">Name</Label>
                                  <p className="font-medium mt-1">{user.name || 'Not set'}</p>
                                </div>
                                <div>
                                  <Label className="text-muted-foreground text-sm">Username</Label>
                                  <p className="font-medium mt-1">{user.username}</p>
                                </div>
                              </div>
                              <div>
                                <Label className="text-muted-foreground text-sm">Email</Label>
                                <p className="font-medium mt-1">{user.email}</p>
                              </div>
                              <div>
                                <Label className="text-muted-foreground text-sm">Verification status</Label>
                                <div className="mt-1">
                                  {user.is_verified ? (
                                    <Badge className="bg-green-100 text-green-700">Verified</Badge>
                                  ) : (
                                    <Badge variant="secondary">Not verified</Badge>
                                  )}
                                </div>
                              </div>
                              {user.created_at && (
                                <div>
                                  <Label className="text-muted-foreground text-sm">Member since</Label>
                                  <p className="font-medium mt-1">
                                    {new Date(user.created_at).toLocaleDateString('en-US', {
                                      year: 'numeric',
                                      month: 'long',
                                      day: 'numeric'
                                    })}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </TabsContent>

                      <TabsContent value="ai-results" className="p-6 space-y-6">
                        {loadingQuizResults ? (
                          <div className="flex justify-center py-8">
                            <Loader2 className="w-8 h-8 animate-spin text-primary" />
                          </div>
                        ) : quizResults.length > 0 ? (
                          quizResults.map((result) => (
                            <div key={result.id} className="space-y-4">
                              <div>
                                <h3 className="font-semibold text-foreground">
                                  {result.quiz_type === 'initial' ? 'Initial Quiz' : 'Extended Quiz'}
                                </h3>
                                <p className="text-sm text-muted-foreground">
                                  Generated on {new Date(result.created_at).toLocaleDateString('en-US', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric',
                                    hour: '2-digit',
                                    minute: '2-digit'
                                  })}
                                </p>
                              </div>
                              <Card className="border-border/50">
                                <CardContent className="p-6">
                                  <div className="flex items-start justify-between mb-4">
                                    <div>
                                      <h4 className="font-semibold text-lg">Primary Match</h4>
                                      <p className="text-primary font-bold text-xl mt-1">{result.main_match_field}</p>
                                    </div>
                                    <Badge className="bg-green-100 text-green-700 text-lg px-3 py-1">
                                      {Math.round(result.compatibility_score)}%
                                    </Badge>
                                  </div>
                                  <p className="text-muted-foreground">{result.description}</p>
                                  {result.matched_universities && result.matched_universities.length > 0 && (
                                    <div className="mt-4">
                                      <p className="font-semibold text-sm mb-2">Recommended Universities:</p>
                                      <ul className="list-disc list-inside text-sm text-muted-foreground">
                                        {result.matched_universities.map((uni, idx) => (
                                          <li key={idx}>{uni}</li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                  <Button 
                                    variant={hasActivePackage ? "default" : "secondary"}
                                    className={`mt-4 gap-2 ${!hasActivePackage ? 'opacity-60' : ''}`}
                                    onClick={() => handleDownloadPDF(result.id)}
                                  >
                                    {!hasActivePackage && <Lock className="w-4 h-4" />}
                                    {hasActivePackage && <Download className="w-4 h-4" />}
                                    Download Full Report (PDF)
                                    {!hasActivePackage && (
                                      <span className="ml-2 text-xs opacity-75">(Premium)</span>
                                    )}
                                  </Button>
                                </CardContent>
                              </Card>
                            </div>
                          ))
                        ) : (
                          <div className="text-center py-8">
                            <p className="text-muted-foreground">You haven't completed any quizzes yet.</p>
                            <Link to="/quiz">
                              <Button className="mt-4">Take the Quiz</Button>
                            </Link>
                          </div>
                        )}
                      </TabsContent>

                      <TabsContent value="history" className="p-6">
                        {loadingQuizResults ? (
                          <div className="flex justify-center py-8">
                            <Loader2 className="w-8 h-8 animate-spin text-primary" />
                          </div>
                        ) : quizAttempts.length > 0 ? (
                          <div className="space-y-4">
                            {quizAttempts.map((attempt) => (
                              <Card key={attempt.id} className="border-border/50">
                                <CardContent className="p-4">
                                  <div className="flex items-center justify-between mb-3">
                                    <div>
                                      <p className="font-medium">{attempt.quiz_label}</p>
                                      <p className="text-sm text-muted-foreground">
                                        {new Date(attempt.created_at).toLocaleDateString('en-US', {
                                          year: 'numeric',
                                          month: 'long',
                                          day: 'numeric',
                                          hour: '2-digit',
                                          minute: '2-digit'
                                        })} • {attempt.num_questions} questions
                                      </p>
                                    </div>
                                    <div className="text-right">
                                      <Badge className="bg-green-100 text-green-700">
                                        {Math.round(attempt.score_percentage)}%
                                      </Badge>
                                      <p className="text-sm text-muted-foreground mt-1">{attempt.main_match}</p>
                                    </div>
                                  </div>
                                  <Button
                                    variant={hasActivePackage ? "default" : "secondary"}
                                    size="sm"
                                    className={`w-full ${!hasActivePackage ? 'opacity-60' : ''}`}
                                    onClick={() => handleDownloadPDF(attempt.id)}
                                  >
                                    {!hasActivePackage && <Lock className="w-4 h-4 mr-2" />}
                                    {hasActivePackage && <Download className="w-4 h-4 mr-2" />}
                                    Download PDF Report
                                    {!hasActivePackage && (
                                      <span className="ml-2 text-xs opacity-75">(Premium)</span>
                                    )}
                                  </Button>
                                </CardContent>
                              </Card>
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-8">
                            <p className="text-muted-foreground">You haven't saved any quizzes yet.</p>
                            <Link to="/quiz">
                              <Button className="mt-4">Take and Save a Quiz</Button>
                            </Link>
                          </div>
                        )}
                      </TabsContent>
                    </Tabs>
                  </CardContent>
                </Card>
              )}

              {activeSection === "package" && (
                <div className="space-y-6">
                  <Card className="border-border/50">
                    <CardHeader>
                      <CardTitle>My Plan</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <PackageInfoCard key={refreshKey} />
                      
                      {packageInfo && packageInfo.package_tier !== PackageTier.FREE && (
                        <div className="mt-6 pt-6 border-t border-border/50">
                          <div className="flex items-start gap-3 p-4 rounded-lg bg-amber-500/10 border border-amber-500/20 mb-4">
                            <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
                            <div className="flex-1">
                              <h4 className="font-semibold text-amber-900 mb-1">Switch Back to Free</h4>
                              <p className="text-sm text-amber-800">
                                You can move back to the free plan anytime. You will lose access to all premium features.
                              </p>
                            </div>
                          </div>
                          <Button 
                            variant="outline" 
                            className="w-full border-destructive/50 text-destructive hover:bg-destructive/10"
                            onClick={() => setShowRevertDialog(true)}
                          >
                            Cancel Premium Plan
                          </Button>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                  
                  <Card className="border-border/50">
                    <CardHeader>
                      <CardTitle>Upgrade Your Plan</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground mb-4">
                        Want more features? Explore the available plans and pick the best fit for you.
                      </p>
                      <Button asChild>
                        <Link to="/pachete">View All Plans</Link>
                      </Button>
                    </CardContent>
                  </Card>
                </div>
              )}

              {activeSection === "results" && (
                <Card className="border-border/50">
                  <CardHeader>
                    <CardTitle>Your Quiz Results</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {loadingQuizResults ? (
                      <div className="flex justify-center py-8">
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                      </div>
                    ) : quizAttempts.length > 0 ? (
                      (() => {
                        // Show only the most recent quiz attempt
                        const latestAttempt = quizAttempts[0];
                        return (
                          <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 }}
                          >
                            <Card className="border-border/50 overflow-hidden hover:border-primary/30 transition-all duration-300">
                              <CardContent className="p-6">
                                <div className="flex items-start justify-between mb-4">
                                  <div className="flex-1">
                                    <p className="text-sm text-muted-foreground mb-1">
                                      {new Date(latestAttempt.created_at).toLocaleDateString('en-US', {
                                        day: 'numeric',
                                        month: 'long',
                                        year: 'numeric'
                                      })}
                                    </p>
                                    <h3 className="text-primary font-bold text-xl mb-2">
                                      {latestAttempt.main_match}
                                    </h3>
                                    <p className="text-muted-foreground text-sm mb-3">
                                      {latestAttempt.quiz_label} • {latestAttempt.num_questions} questions
                                    </p>
                                  </div>
                                  <Badge className="bg-green-100 text-green-700 text-lg px-4 py-2 font-bold">
                                    {Math.round(latestAttempt.score_percentage)}%
                                  </Badge>
                                </div>
                                
                                <div className="bg-muted/50 rounded-lg p-4 mb-4">
                                  <p className="text-foreground/80 leading-relaxed">
                                    Your profile shows a strong inclination toward this specialization,
                                    based on your compatibility quiz answers.
                                  </p>
                                </div>

                                <div className="flex gap-2">
                                  <Button
                                    variant={hasActivePackage ? "default" : "secondary"}
                                    size="sm"
                                    className={`flex-1 ${!hasActivePackage ? 'opacity-60' : ''}`}
                                    onClick={() => handleDownloadPDF(latestAttempt.id)}
                                  >
                                    {!hasActivePackage && <Lock className="w-4 h-4 mr-2" />}
                                    {hasActivePackage && <Download className="w-4 h-4 mr-2" />}
                                    Download PDF Report
                                    {!hasActivePackage && (
                                      <span className="ml-2 text-xs opacity-75">(Premium)</span>
                                    )}
                                  </Button>
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    asChild
                                  >
                                    <Link to="/quiz">
                                      <ChevronRight className="w-4 h-4 mr-2" />
                                      Retake Quiz
                                    </Link>
                                  </Button>
                                </div>
                              </CardContent>
                            </Card>
                          </motion.div>
                        );
                      })()
                    ) : (
                      <div className="text-center py-12">
                        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                          <FileText className="w-8 h-8 text-primary" />
                        </div>
                        <h3 className="font-semibold text-lg mb-2">No quizzes completed yet</h3>
                        <p className="text-muted-foreground mb-6">
                          Complete your first quiz to receive personalized recommendations
                        </p>
                        <Button asChild>
                          <Link to="/quiz">Start Quiz</Link>
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}

              {activeSection === "appointments" && (
                <Card className="border-border/50">
                  <CardHeader>
                    <CardTitle>Your Appointments</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {mockAppointments.map((appointment) => (
                      <Card key={appointment.id} className="border-border/50">
                        <CardContent className="p-4 flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                              <Calendar className="w-6 h-6 text-primary" />
                            </div>
                            <div>
                              <p className="font-medium">{appointment.type}</p>
                              <p className="text-sm text-muted-foreground">{appointment.date} at {appointment.time}</p>
                            </div>
                          </div>
                          <Badge variant={appointment.status === "Confirmed" ? "default" : "secondary"}>
                            {appointment.status}
                          </Badge>
                        </CardContent>
                      </Card>
                    ))}
                  </CardContent>
                </Card>
              )}

              {activeSection === "payments" && (
                <Card className="border-border/50">
                  <CardHeader>
                    <CardTitle>Payments & Invoices</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {loadingInvoices ? (
                      <div className="flex justify-center py-8">
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                      </div>
                    ) : invoices.length === 0 ? (
                      <div className="text-center py-8 text-muted-foreground">
                        You don't have any invoices yet.
                      </div>
                    ) : (
                      invoices.map((invoice) => (
                        <Card key={invoice.id} className="border-border/50">
                          <CardContent className="p-4 flex items-center justify-between">
                            <div className="flex items-center gap-4">
                              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center">
                                <CreditCard className="w-6 h-6 text-accent" />
                              </div>
                              <div>
                                <p className="font-medium">{invoice.package}</p>
                                <p className="text-sm text-muted-foreground">
                                  {invoice.invoice_number} • {new Date(invoice.date).toLocaleDateString('en-US', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                  })}
                                </p>
                              </div>
                            </div>
                            <div className="text-right">
                              <p className="font-semibold">€{invoice.amount.toFixed(2)}</p>
                              <Badge className="mt-1 bg-green-100 text-green-700">
                                {invoice.status === 'paid' ? 'Paid' : invoice.status}
                              </Badge>
                            </div>
                          </CardContent>
                        </Card>
                      ))
                    )}
                  </CardContent>
                </Card>
              )}
            </motion.div>
          </div>
        </div>
      </main>

      {/* Locked Feature Dialog */}
      <Dialog open={showLockedDialog} onOpenChange={setShowLockedDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-full bg-amber-500/10">
              <Lock className="w-6 h-6 text-amber-600" />
            </div>
            <DialogTitle className="text-center">Premium Feature Locked</DialogTitle>
            <DialogDescription className="text-center pt-2">
              PDF downloads are available only for premium users.
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

      {/* Revert to Free Dialog */}
      <Dialog open={showRevertDialog} onOpenChange={setShowRevertDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-full bg-destructive/10">
              <AlertTriangle className="w-6 h-6 text-destructive" />
            </div>
            <DialogTitle className="text-center">Are you sure?</DialogTitle>
            <DialogDescription className="text-center pt-2">
              If you switch back to the free plan, you'll lose access to all premium features, including:
              <ul className="list-disc text-left mt-3 space-y-1 pl-6">
                <li>Advanced AI comparisons</li>
                <li>PDF report downloads</li>
                <li>University compatibility analysis</li>
                <li>Unlimited AI chat</li>
              </ul>
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="flex-col sm:flex-col gap-2 sm:gap-2">
            <Button 
              variant="destructive" 
              onClick={handleRevertToFree} 
              disabled={isReverting}
              className="w-full"
            >
              {isReverting ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                'Yes, switch to Free'
              )}
            </Button>
            <Button 
              variant="outline" 
              onClick={() => setShowRevertDialog(false)} 
              disabled={isReverting}
              className="w-full"
            >
              Cancel
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Footer />
    </div>
  );
};

export default Account;
