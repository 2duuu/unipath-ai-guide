import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, Phone, MapPin, Clock, Calendar, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { toast } from "@/hooks/use-toast";

const Contact = () => {
  const [contactForm, setContactForm] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const [appointmentForm, setAppointmentForm] = useState({
    name: "",
    email: "",
    phone: "",
    date: "",
    time: "",
    package: "",
  });

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: "Mesaj trimis!",
      description: "Îți vom răspunde în cel mai scurt timp posibil.",
    });
    setContactForm({ name: "", email: "", subject: "", message: "" });
  };

  const handleAppointmentSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: "Programare confirmată!",
      description: `Ședința ta a fost programată pentru ${appointmentForm.date} la ora ${appointmentForm.time}.`,
    });
    setAppointmentForm({ name: "", email: "", phone: "", date: "", time: "", package: "" });
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-4">
              Contactează-ne
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Suntem aici să te ajutăm! Trimite-ne un mesaj sau programează o ședință de consultanță.
            </p>
          </motion.div>

          {/* Contact Info Cards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12"
          >
            {[
              { icon: Mail, label: "Email", value: "contact@unihub.ro" },
              { icon: Phone, label: "Telefon", value: "+40 721 234 567" },
              { icon: MapPin, label: "Locație", value: "București, România" },
              { icon: Clock, label: "Program", value: "Luni-Vineri: 9:00-18:00" },
            ].map((item, index) => (
              <Card key={index} className="text-center border-border/50">
                <CardContent className="pt-6">
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mx-auto mb-3">
                    <item.icon className="w-6 h-6 text-primary" />
                  </div>
                  <p className="font-semibold text-foreground">{item.label}</p>
                  <p className="text-sm text-muted-foreground">{item.value}</p>
                </CardContent>
              </Card>
            ))}
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Card className="border-border/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Mail className="w-5 h-5 text-primary" />
                    Trimite-ne un mesaj
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleContactSubmit} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="contact-name">Nume complet</Label>
                        <Input
                          id="contact-name"
                          value={contactForm.name}
                          onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                          placeholder="Ion Popescu"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="contact-email">Email</Label>
                        <Input
                          id="contact-email"
                          type="email"
                          value={contactForm.email}
                          onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                          placeholder="ion@email.com"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="contact-subject">Subiect</Label>
                      <Input
                        id="contact-subject"
                        value={contactForm.subject}
                        onChange={(e) => setContactForm({ ...contactForm, subject: e.target.value })}
                        placeholder="Despre ce este vorba?"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="contact-message">Mesaj</Label>
                      <Textarea
                        id="contact-message"
                        value={contactForm.message}
                        onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                        placeholder="Scrie mesajul tău aici..."
                        rows={5}
                        required
                      />
                    </div>
                    <Button type="submit" className="w-full gap-2">
                      <Send className="w-4 h-4" />
                      Trimite mesajul
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>

            {/* Appointment Form */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Card className="border-border/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Calendar className="w-5 h-5 text-accent" />
                    Programează o ședință
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleAppointmentSubmit} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="appointment-name">Nume complet</Label>
                        <Input
                          id="appointment-name"
                          value={appointmentForm.name}
                          onChange={(e) => setAppointmentForm({ ...appointmentForm, name: e.target.value })}
                          placeholder="Ion Popescu"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="appointment-email">Email</Label>
                        <Input
                          id="appointment-email"
                          type="email"
                          value={appointmentForm.email}
                          onChange={(e) => setAppointmentForm({ ...appointmentForm, email: e.target.value })}
                          placeholder="ion@email.com"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="appointment-phone">Telefon</Label>
                      <Input
                        id="appointment-phone"
                        type="tel"
                        value={appointmentForm.phone}
                        onChange={(e) => setAppointmentForm({ ...appointmentForm, phone: e.target.value })}
                        placeholder="+40 7XX XXX XXX"
                        required
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="appointment-date">Data</Label>
                        <Input
                          id="appointment-date"
                          type="date"
                          value={appointmentForm.date}
                          onChange={(e) => setAppointmentForm({ ...appointmentForm, date: e.target.value })}
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="appointment-time">Ora</Label>
                        <Select
                          value={appointmentForm.time}
                          onValueChange={(value) => setAppointmentForm({ ...appointmentForm, time: value })}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Alege ora" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="09:00">09:00</SelectItem>
                            <SelectItem value="10:00">10:00</SelectItem>
                            <SelectItem value="11:00">11:00</SelectItem>
                            <SelectItem value="12:00">12:00</SelectItem>
                            <SelectItem value="14:00">14:00</SelectItem>
                            <SelectItem value="15:00">15:00</SelectItem>
                            <SelectItem value="16:00">16:00</SelectItem>
                            <SelectItem value="17:00">17:00</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="appointment-package">Tip consultanță</Label>
                      <Select
                        value={appointmentForm.package}
                        onValueChange={(value) => setAppointmentForm({ ...appointmentForm, package: value })}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Alege tipul" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="free">Ședință gratuită de cunoaștere</SelectItem>
                          <SelectItem value="basic">Pachet Basic - Discuție rezultate</SelectItem>
                          <SelectItem value="standard">Pachet Standard - Consultanță completă</SelectItem>
                          <SelectItem value="premium">Pachet Premium - Sesiune dedicată</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <Button type="submit" variant="accent" className="w-full gap-2">
                      <Calendar className="w-4 h-4" />
                      Programează ședința
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Contact;
