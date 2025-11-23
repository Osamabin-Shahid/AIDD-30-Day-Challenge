from pypdf import PdfReader

def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a given PDF file path."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
