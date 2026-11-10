import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";

const testimonials = [
  {
    name: "Maria Popescu",
    role: "Studentă la Informatică, UB",
    content:
      "M-a ajutat să aleg facultatea potrivită! Eram indecisă între mai multe domenii, dar testul AI și consilierul m-au ghidat perfect.",
    rating: 5,
    avatar: "MP",
  },
  {
    name: "Andrei Ionescu",
    role: "Student la Automatică, UPB",
    content:
      "Scorul de compatibilitate de 92% s-a confirmat! Sunt foarte mulțumit de alegerea mea și mă descurc excelent la facultate.",
    rating: 5,
    avatar: "AI",
  },
  {
    name: "Elena Dumitrescu",
    role: "Studentă la Economie, ASE",
    content:
      "Raportul personalizat m-a ajutat să înțeleg ce facultate mi se potrivește. Recomand tuturor elevilor de liceu!",
    rating: 5,
    avatar: "ED",
  },
];

const TestimonialsSection = () => {
  return (
    <section className="py-20 md:py-28 bg-secondary/30">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-2xl mx-auto mb-16"
        >
          <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
            Ce spun studenții noștri
          </h2>
          <p className="text-lg text-muted-foreground">
            Peste 5000 de elevi și-au găsit drumul corect cu ajutorul nostru.
          </p>
        </motion.div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-3 gap-6 md:gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative p-6 md:p-8 rounded-2xl bg-card border border-border/50 hover:shadow-lg transition-all duration-300"
            >
              {/* Quote icon */}
              <Quote className="absolute top-6 right-6 w-8 h-8 text-primary/20" />

              {/* Rating */}
              <div className="flex gap-1 mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star
                    key={i}
                    className="w-5 h-5 text-accent"
                    fill="currentColor"
                  />
                ))}
              </div>

              {/* Content */}
              <p className="text-foreground leading-relaxed mb-6">
                "{testimonial.content}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center font-display font-bold text-primary">
                  {testimonial.avatar}
                </div>
                <div>
                  <div className="font-semibold text-foreground">
                    {testimonial.name}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {testimonial.role}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
