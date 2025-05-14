import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print("Error loading spaCy model:", e)
    nlp = None

def extract_info(text: str, doc_type: str) -> dict:
    info = {
        "names": [],
        "dates": [],
        "emails": [],
        "phone_numbers": [],
        "amounts": [],
        "text": text  # Always include fallback text
    }

    if nlp is None:
        return info  # Return basic info if NLP fails

    doc = nlp(text)
    
    # Common Named Entity Recognition
    info["names"] = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    info["dates"] = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

    # Resume-specific extraction
    if doc_type.lower() == "resume":
        info["emails"] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        info["phone_numbers"] = re.findall(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){2}\d{4}', text)

    # Invoice-specific extraction
    elif doc_type.lower() == "invoice":
        info["amounts"] = re.findall(r'(?:\$|₹|€)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        print(f"Extracted Amounts: {info['amounts']}")

    return info
