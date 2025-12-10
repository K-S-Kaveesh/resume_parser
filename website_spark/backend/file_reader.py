import PyPDF2
from docx import Document
import io

def extract_text_from_pdf(file_stream):
    """Extract text from PDF file"""
    try:
        # Reset stream position
        file_stream.seek(0)
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")

def extract_text_from_docx(file_stream):
    """Extract text from DOCX file"""
    try:
        # Reset stream position
        file_stream.seek(0)
        doc = Document(file_stream)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading DOCX file: {str(e)}")

def read_file(file, filename):
    """Read file content based on file extension"""
    try:
        # For in-memory file objects, we need to read the content
        if hasattr(file, 'read'):
            content = file.read()
            # Create a new BytesIO object for processing
            from io import BytesIO
            file_stream = BytesIO(content) if isinstance(content, bytes) else BytesIO(content.encode('utf-8'))
        else:
            file_stream = file
        
        if filename.lower().endswith('.pdf'):
            return extract_text_from_pdf(file_stream)
        elif filename.lower().endswith('.docx'):
            return extract_text_from_docx(file_stream)
        else:
            raise Exception("Unsupported file format. Please upload PDF or DOCX files.")
    except Exception as e:
        raise Exception(f"Error processing file {filename}: {str(e)}")