import jsPDF from 'jspdf';

interface QuizResult {
  id: number;
  created_at: string;
  quiz_type: string;
  main_match_field: string;
  compatibility_score: number;
  description: string;
  matched_universities: string[];
}

export const generateQuizResultPDF = (result: QuizResult, userName: string) => {
  const pdf = new jsPDF();
  
  // Set font
  pdf.setFont('helvetica');
  
  // Title
  pdf.setFontSize(20);
  pdf.setTextColor(33, 150, 243); // Blue color
  pdf.text('UniHub - Raport Quiz Rezultate', 105, 20, { align: 'center' });
  
  // Line separator
  pdf.setDrawColor(200, 200, 200);
  pdf.line(20, 25, 190, 25);
  
  // User info
  pdf.setFontSize(12);
  pdf.setTextColor(0, 0, 0);
  pdf.text(`Student: ${userName}`, 20, 35);
  
  // Date
  const date = new Date(result.created_at);
  pdf.text(`Data: ${date.toLocaleDateString('ro-RO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })}`, 20, 42);
  
  // Quiz type
  pdf.text(`Tip Quiz: ${result.quiz_type === 'initial' ? 'Quiz Inițial' : 'Quiz Extended'}`, 20, 49);
  
  // Line separator
  pdf.line(20, 53, 190, 53);
  
  // Main match section
  pdf.setFontSize(16);
  pdf.setTextColor(33, 150, 243);
  pdf.text('Compatibilitate Principală', 20, 63);
  
  pdf.setFontSize(14);
  pdf.setTextColor(0, 0, 0);
  pdf.text(result.main_match_field, 20, 72);
  
  // Compatibility score
  pdf.setFontSize(12);
  pdf.setTextColor(76, 175, 80); // Green
  pdf.text(`Scor Compatibilitate: ${Math.round(result.compatibility_score)}%`, 20, 80);
  
  // Description
  pdf.setFontSize(12);
  pdf.setTextColor(0, 0, 0);
  pdf.text('Descriere:', 20, 92);
  
  // Split description into lines
  const descriptionLines = pdf.splitTextToSize(result.description, 170);
  pdf.setFontSize(11);
  pdf.text(descriptionLines, 20, 100);
  
  // Calculate Y position after description
  let currentY = 100 + (descriptionLines.length * 6);
  
  // Universities section
  if (result.matched_universities && result.matched_universities.length > 0) {
    currentY += 10;
    pdf.setFontSize(14);
    pdf.setTextColor(33, 150, 243);
    pdf.text('Universități Recomandate:', 20, currentY);
    
    currentY += 8;
    pdf.setFontSize(11);
    pdf.setTextColor(0, 0, 0);
    
    result.matched_universities.forEach((uni, index) => {
      pdf.text(`${index + 1}. ${uni}`, 25, currentY);
      currentY += 6;
    });
  }
  
  // Footer
  pdf.setFontSize(9);
  pdf.setTextColor(150, 150, 150);
  pdf.text('UniHub - Platforma de Ghidare Academică bazată pe AI', 105, 285, { align: 'center' });
  pdf.text('www.unihub.ro', 105, 290, { align: 'center' });
  
  // Save the PDF
  const fileName = `UniHub_Rezultate_${result.main_match_field.replace(/\s+/g, '_')}_${date.toISOString().split('T')[0]}.pdf`;
  pdf.save(fileName);
};
