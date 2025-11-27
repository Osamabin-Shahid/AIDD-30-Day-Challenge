from pypdf import PdfReader

def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a given PDF file path."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
<<<<<<< HEAD
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text
=======
        text += page.extract_text() or ""
    return text
>>>>>>> 539cafef22c343296a45d89a856cc310c4bc78d3
