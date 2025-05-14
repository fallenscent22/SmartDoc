from flask_cors import CORS # Import CORS for handling cross-origin requests
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from werkzeug.utils import secure_filename
import pdfplumber
from docx import Document as DocxDocument
import spacy
from transformers import pipeline
import re

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text(filepath, ext):
    if ext == 'pdf':
        with pdfplumber.open(filepath) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext == 'docx':
        doc = DocxDocument(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == 'txt':
        with open(filepath, encoding='utf-8') as f:
            return f.read()
    else:
        return ""

def classify_document(text):
    # Simple keyword-based classification (replace with ML model for production)
    if "invoice" in text.lower():
        return "Invoice"
    elif "resume" in text.lower() or "curriculum vitae" in text.lower():
        return "Resume"
    elif "report" in text.lower():
        return "Report"
    else:
        return "General Document"

def extract_entities(text, doc_type):
    doc = nlp(text)
    entities = {}

    # Common extractions
    entities["emails"] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    entities["phone_numbers"] = re.findall(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){2}\d{4}', text)
    entities["dates"] = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

    if doc_type == "Resume":
        # Resume-specific
        entities["name"] = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), None)
        entities["company"] = next((ent.text for ent in doc.ents if ent.label_ == "ORG"), None)
        # Try to extract role/title
        role_match = re.search(r'(Role|Position|Title)[:\-]?\s*([A-Za-z ]+)', text, re.IGNORECASE)
        if role_match:
            entities["role"] = role_match.group(2).strip()
        else:
            entities["role"] = None

    elif doc_type == "Invoice":
        # Invoice-specific
        entities["invoice_number"] = None
        invoice_match = re.search(r'(Invoice\s*(Number|No\.?)[:\-]?\s*)([A-Za-z0-9\-]+)', text, re.IGNORECASE)
        if invoice_match:
            entities["invoice_number"] = invoice_match.group(3).strip()
        # Vendor/Company
        entities["vendor"] = next((ent.text for ent in doc.ents if ent.label_ == "ORG"), None)
        # Amounts
        amounts = re.findall(r'(?:\$|₹|€)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        entities["amounts"] = amounts
        # Try to find total
        total_match = re.search(r'(Total\s*[:\-]?\s*)(\$?\d[\d,\.]*)', text, re.IGNORECASE)
        if total_match:
            entities["total"] = total_match.group(2).strip()
        else:
            entities["total"] = None

    else:
        # General extraction
        entities["persons"] = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        entities["organizations"] = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        entities["money"] = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]

    return entities

def summarize_text(text):
    # HuggingFace models have a max token limit; truncate if needed
    if len(text) > 1000:
        text = text[:1000]
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Main route serving the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Optional: Catch-all route for SPA routing
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

# Add the API endpoint
@app.route('/api/process', methods=['POST'])
def process_document():
    if 'document' not in request.files:
        app.logger.error('No file part in request')
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['document']
    if file.filename == '':
        app.logger.error('Empty filename')
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        ext = filename.rsplit('.', 1)[1].lower()
        try:
            content = extract_text(filepath, ext)
            doc_type = classify_document(content)
            summary = summarize_text(content)
            entities = extract_entities(content, doc_type)
            # Remove empty or None entities
            filtered_entities = {k: v for k, v in entities.items() if v and (not isinstance(v, list) or len(v) > 0)}
        except Exception as e:
            app.logger.error(f"Failed to process document: {e}")
            return jsonify({'error': 'Failed to process document'}), 500

        return jsonify({
            'status': 'success',
            'doc_type': doc_type,
            'summary': summary,
            'entities': filtered_entities
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':

    app.run(debug=True)