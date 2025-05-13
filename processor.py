import pytesseract
from PIL import Image
import pdfplumber
from docx import Document as DocxDocument

def extract_text(file_path: str, file_type: str) -> str:
    if file_type == "application/pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages])
    elif file_type in ["image/jpeg", "image/png"]:
        return pytesseract.image_to_string(Image.open(file_path))
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")