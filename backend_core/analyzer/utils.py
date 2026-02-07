from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io
import os

def generate_pdf_report(analysis_record):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, f"Analysis Report #{analysis_record.id}")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 70, f"Date: {analysis_record.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 100, "Summary Statistics")
    
    data = analysis_record.summary_data
    
    text_y = height - 125
    p.setFont("Helvetica", 12)
    p.drawString(50, text_y, f"Total Equipment Count: {data.get('total_count', 'N/A')}")
    text_y -= 20
    p.drawString(50, text_y, f"Average Pressure: {data.get('avg_pressure', 'N/A')} Pa")
    text_y -= 20
    p.drawString(50, text_y, f"Average Temperature: {data.get('avg_temp', 'N/A')} °C")
    
    text_y -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, text_y, "Equipment Type Distribution")
    
    text_y -= 30
    type_counts = data.get('type_counts', {})
    
    table_data = [['Equipment Type', 'Count']]
    for k, v in type_counts.items():
        table_data.append([k, str(v)])
        
    t = Table(table_data, colWidths=[200, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    
    t.wrapOn(p, width, height)
    t.drawOn(p, 50, text_y - (len(table_data) * 20))
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer
