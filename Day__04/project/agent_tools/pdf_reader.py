from pypdf import PdfReader

def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a given PDF file path."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text