from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
import os
download_dir = os.path.dirname(os.path.abspath(__file__))
download_dir=download_dir+"\downloaded_documents2"

def save_string_to_pdf(text, filename):
    file_path = os.path.join(download_dir, filename)
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    style = styles['Normal']
    flowables = []
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        p = Paragraph(paragraph, style)
        flowables.append(p)
    
    # Construye el documento PDF
    doc.build(flowables)
    print("PDF file saved successfully.")
