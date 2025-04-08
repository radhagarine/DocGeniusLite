import os
import json
import datetime
import tempfile
from weasyprint import HTML
# Import python-docx properly
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import templates

def get_template_by_type(doc_type):
    """Get the appropriate template for the document type"""
    template_mapping = {
        "nda": templates.nda_template.generate,
        "invoice": templates.invoice_template.generate,
        "letter_of_intent": templates.letter_of_intent_template.generate,
        "proposal": templates.proposal_template.generate,
        "scope_of_work": templates.scope_of_work_template.generate
    }
    
    if doc_type not in template_mapping:
        raise ValueError(f"Document type '{doc_type}' is not supported")
    
    return template_mapping[doc_type]

def generate_document_content(doc_type, parameters):
    """Generate document content using the appropriate template"""
    template_generator = get_template_by_type(doc_type)
    content = template_generator(parameters)
    return content

def generate_pdf(content, title):
    """Generate a PDF file from HTML content"""
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
        tmp_html.write(content.encode('utf-8'))
        tmp_html_path = tmp_html.name
    
    # Create a temporary PDF file
    pdf_path = tmp_html_path.replace('.html', '.pdf')
    
    # Generate PDF
    HTML(tmp_html_path).write_pdf(pdf_path)
    
    # Clean up the HTML file
    os.unlink(tmp_html_path)
    
    return pdf_path

def generate_docx(content, title, doc_type):
    """Generate a DOCX file from content"""
    # Create a new Document
    doc = Document()
    
    # Add a title
    title_paragraph = doc.add_paragraph()
    title_run = title_paragraph.add_run(title)
    title_run.bold = True
    title_run.font.size = Pt(16)
    title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add the date
    date_paragraph = doc.add_paragraph()
    date_run = date_paragraph.add_run(datetime.datetime.now().strftime("%B %d, %Y"))
    date_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    # Add a line
    doc.add_paragraph("_" * 50)
    
    # This is a simple implementation - in a real app, you'd parse the HTML content
    # and convert it properly to DOCX format
    paragraphs = content.replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n\n')
    paragraphs = paragraphs.replace('<strong>', '').replace('</strong>', '')
    paragraphs = paragraphs.replace('<em>', '').replace('</em>', '')
    paragraphs = paragraphs.replace('&nbsp;', ' ')
    
    # Split by lines and add each as a paragraph
    for para in paragraphs.split('\n'):
        if para.strip():
            doc.add_paragraph(para.strip())
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_docx:
        docx_path = tmp_docx.name
    
    doc.save(docx_path)
    return docx_path

def get_document_parameters(doc_type):
    """Get the parameter definitions for a document type"""
    if doc_type == "nda":
        return templates.nda_template.PARAMETERS
    elif doc_type == "invoice":
        return templates.invoice_template.PARAMETERS
    elif doc_type == "letter_of_intent":
        return templates.letter_of_intent_template.PARAMETERS
    elif doc_type == "proposal":
        return templates.proposal_template.PARAMETERS
    elif doc_type == "scope_of_work":
        return templates.scope_of_work_template.PARAMETERS
    else:
        raise ValueError(f"Document type '{doc_type}' is not supported")
