# info_extractor.py
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_info(text: str, doc_type: str) -> dict:
    doc = nlp(text)
    info = {}
    
    # Common entities
    info['names'] = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    info['dates'] = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    
    # Type-specific extraction
    if doc_type == "invoice":
        info['amounts'] = re.findall(r'\$\d+[\d,.]*', text)
    elif doc_type == "resume":
        info['emails'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    else:
        info['text'] = text  # Fallback content 
    return info


