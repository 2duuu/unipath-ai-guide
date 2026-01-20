"""
PDF Generation for quiz results and university recommendations.
Generates downloadable PDFs for premium package users.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any


def generate_recommendation_pdf(
    student_name: str,
    quiz_results: Dict[str, Any],
    university_recommendations: List[Dict[str, Any]],
    program_recommendations: List[Dict[str, Any]]
) -> BytesIO:
    """
    Generate a PDF summary of AI recommendations for a student.
    
    Args:
        student_name: Name of the student
        quiz_results: Quiz results dictionary
        university_recommendations: List of recommended universities
        program_recommendations: List of recommended programs
        
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
    )
    
    # Title
    story.append(Paragraph("UniHub AI Recommendations Report", title_style))
    story.append(Paragraph(f"Generated for: {student_name}", styles['Normal']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Quiz Results Summary
    story.append(Paragraph("Quiz Results Summary", heading_style))
    
    if quiz_results:
        main_field = quiz_results.get('main_match_field', 'N/A')
        compatibility = quiz_results.get('compatibility_score', 0)
        
        story.append(Paragraph(f"<b>Primary Field of Interest:</b> {main_field}", styles['Normal']))
        story.append(Paragraph(f"<b>Compatibility Score:</b> {compatibility:.1f}%", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # University Recommendations
    story.append(Paragraph("Recommended Universities", heading_style))
    
    if university_recommendations:
        uni_data = [['Rank', 'University', 'Location', 'Match Score']]
        
        for idx, uni in enumerate(university_recommendations[:10], 1):
            uni_data.append([
                str(idx),
                uni.get('name', 'N/A'),
                uni.get('city', 'N/A'),
                f"{uni.get('match_score', 0):.1f}%"
            ])
        
        uni_table = Table(uni_data, colWidths=[0.7*inch, 3*inch, 1.5*inch, 1.3*inch])
        uni_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(uni_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Program Recommendations
    story.append(Paragraph("Recommended Academic Programs", heading_style))
    
    if program_recommendations:
        prog_data = [['Rank', 'Program', 'University', 'Match']]
        
        for idx, prog in enumerate(program_recommendations[:10], 1):
            prog_data.append([
                str(idx),
                prog.get('name', 'N/A')[:40],  # Truncate long names
                prog.get('university_name', 'N/A')[:30],
                f"{prog.get('match_score', 0):.1f}%"
            ])
        
        prog_table = Table(prog_data, colWidths=[0.7*inch, 2.5*inch, 2*inch, 1*inch])
        prog_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(prog_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Footer note
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "<i>Note: These recommendations are AI-generated based on your quiz responses. "
        "Please conduct additional research and consult with academic advisors before making final decisions.</i>",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
