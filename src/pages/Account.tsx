import { useState } from "react";
import { motion } from "framer-motion";
import { User, FileText, Calendar, CreditCard, LogOut, Download, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const sidebarItems = [
  { id: "profile", label: "Profilul Meu", icon: User },
  { id: "results", label: "Rezultate Quiz", icon: FileText },
  { id: "appointments", label: "Programări", icon: Calendar },
  { id: "payments", label: "Plăți & Facturi", icon: CreditCard },
];

const mockAIResults = [
  {
    id: 1,
    date: "14 Ianuarie 2026",
    mainMatch: "Informatică și Științe Aplicate",
    compatibility: 87,
    description: "Profilul tău indică o puternică înclinație către rezolvarea problemelor logice și structuri abstracte.",
  },
  {
    id: 2,
    date: "10 Ianuarie 2026",
    mainMatch: "Automatică și Calculatoare",
    compatibility: 82,
    description: "Aptitudini excelente pentru sisteme automatizate și programare.",
  },
];

const mockTestHistory = [
  { id: 1, date: "14 Ianuarie 2026", type: "Quiz Complet", questions: 25, score: "87%" },
  { id: 2, date: "10 Ianuarie 2026", type: "Quiz Rapid", questions: 10, score: "82%" },
  { id: 3, date: "5 Ianuarie 2026", type: "Quiz Complet", questions: 25, score: "79%" },
];

const mockInvoices = [
  { id: "INV-001", date: "14 Ianuarie 2026", package: "Pachet Standard", amount: "249 lei", status: "Plătit" },
  { id: "INV-002", date: "5 Ianuarie 2026", package: "Pachet Basic", amount: "99 lei", status: "Plătit" },
];

const mockAppointments = [
  { id: 1, date: "20 Ianuarie 2026", time: "14:00", type: "Consultanță Standard", status: "Confirmat" },
  { id: 2, date: "25 Ianuarie 2026", time: "10:00", type: "Sesiune Premium", status: "În așteptare" },
];

const Account = () => {
  const [activeSection, setActiveSection] = useState("profile");

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
                AP
              </div>
              <div>
                <h1 className="font-display text-2xl md:text-3xl font-bold">Salut, Alex!</h1>
                <p className="opacity-90">Bine ai revenit pe UniHub.</p>
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
                    <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-destructive hover:bg-destructive/10 transition-colors text-left">
                      <LogOut className="w-5 h-5" />
                      Deconectare
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
                    <Tabs defaultValue="ai-results" className="w-full">
                      <TabsList className="w-full justify-start rounded-none border-b bg-transparent p-0">
                        <TabsTrigger
                          value="ai-results"
                          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-4"
                        >
                          Rezultate AI
                        </TabsTrigger>
                        <TabsTrigger
                          value="history"
                          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-4"
                        >
                          Istoric Teste
                        </TabsTrigger>
                        <TabsTrigger
                          value="invoices"
                          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-4"
                        >
                          Facturi
                        </TabsTrigger>
                      </TabsList>

                      <TabsContent value="ai-results" className="p-6 space-y-6">
                        {mockAIResults.map((result) => (
                          <div key={result.id} className="space-y-4">
                            <div>
                              <h3 className="font-semibold text-foreground">Ultimul Raport AI</h3>
                              <p className="text-sm text-muted-foreground">Generat pe {result.date}</p>
                            </div>
                            <Card className="border-border/50">
                              <CardContent className="p-6">
                                <div className="flex items-start justify-between mb-4">
                                  <div>
                                    <h4 className="font-semibold text-lg">Compatibilitate Principală</h4>
                                    <p className="text-primary font-bold text-xl mt-1">{result.mainMatch}</p>
                                  </div>
                                  <Badge className="bg-green-100 text-green-700 text-lg px-3 py-1">
                                    {result.compatibility}%
                                  </Badge>
                                </div>
                                <p className="text-muted-foreground">{result.description}</p>
                                <Button className="mt-4 gap-2">
                                  <Download className="w-4 h-4" />
                                  Descarcă Raportul Complet (PDF)
                                </Button>
                              </CardContent>
                            </Card>
                          </div>
                        ))}
                      </TabsContent>

                      <TabsContent value="history" className="p-6">
                        <div className="space-y-4">
                          {mockTestHistory.map((test) => (
                            <Card key={test.id} className="border-border/50">
                              <CardContent className="p-4 flex items-center justify-between">
                                <div>
                                  <p className="font-medium">{test.type}</p>
                                  <p className="text-sm text-muted-foreground">{test.date} • {test.questions} întrebări</p>
                                </div>
                                <Badge variant="secondary">{test.score}</Badge>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      </TabsContent>

                      <TabsContent value="invoices" className="p-6">
                        <div className="space-y-4">
                          {mockInvoices.map((invoice) => (
                            <Card key={invoice.id} className="border-border/50">
                              <CardContent className="p-4 flex items-center justify-between">
                                <div>
                                  <p className="font-medium">{invoice.package}</p>
                                  <p className="text-sm text-muted-foreground">{invoice.id} • {invoice.date}</p>
                                </div>
                                <div className="text-right">
                                  <p className="font-semibold">{invoice.amount}</p>
                                  <Badge className="bg-green-100 text-green-700">{invoice.status}</Badge>
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      </TabsContent>
                    </Tabs>
                  </CardContent>
                </Card>
              )}

              {activeSection === "results" && (
                <Card className="border-border/50">
                  <CardHeader>
                    <CardTitle>Rezultatele Tale Quiz</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {mockAIResults.map((result) => (
                      <Card key={result.id} className="border-border/50">
                        <CardContent className="p-6">
                          <div className="flex items-start justify-between mb-4">
                            <div>
                              <p className="text-sm text-muted-foreground">{result.date}</p>
                              <p className="text-primary font-bold text-xl mt-1">{result.mainMatch}</p>
                            </div>
                            <Badge className="bg-green-100 text-green-700 text-lg px-3 py-1">
                              {result.compatibility}%
                            </Badge>
                          </div>
                          <p className="text-muted-foreground">{result.description}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </CardContent>
                </Card>
              )}

              {activeSection === "appointments" && (
                <Card className="border-border/50">
                  <CardHeader>
                    <CardTitle>Programările Tale</CardTitle>
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
                              <p className="text-sm text-muted-foreground">{appointment.date} la {appointment.time}</p>
                            </div>
                          </div>
                          <Badge variant={appointment.status === "Confirmat" ? "default" : "secondary"}>
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
                    <CardTitle>Plăți & Facturi</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {mockInvoices.map((invoice) => (
                      <Card key={invoice.id} className="border-border/50">
                        <CardContent className="p-4 flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center">
                              <CreditCard className="w-6 h-6 text-accent" />
                            </div>
                            <div>
                              <p className="font-medium">{invoice.package}</p>
                              <p className="text-sm text-muted-foreground">{invoice.id} • {invoice.date}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="font-semibold">{invoice.amount}</p>
                            <Button variant="ghost" size="sm" className="gap-1">
                              <Download className="w-4 h-4" />
                              Descarcă
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </CardContent>
                </Card>
              )}
            </motion.div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Account;
