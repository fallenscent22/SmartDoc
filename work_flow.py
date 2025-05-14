from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from transformers import pipeline
import json

from app.services.storage import file_processor
from info_extractor import extract_info
from app.services.ai.classifier import DocumentClassifier
from app.database import SessionLocal
from app.models.document import Document

app = FastAPI()

# Load summarizer once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Train classifier once
classifier = DocumentClassifier()
classifier.train(
    texts=[
        "Invoice for purchase of items totaling $200.",
        "Experienced software engineer with a strong background...",
        "This is a sample document of unknown category."
    ],
    labels=["invoice", "resume", "pdf"]
)

@app.post("/process")
async def process_file(file_id: str):
    db = SessionLocal()
    try:
        # Get file metadata
        doc_record = db.query(Document).filter(Document.id==file_id).first()
        if not doc_record:
            raise HTTPException(status_code=404, detail="Document not found")

        # Extract text
        text = file_processor.process_file(doc_record.file_path)

        # Predict type
        doc_type = classifier.classify(text)

        # Extract info
        info = extract_info(text, doc_type)

        # Summarize
        summary = summarizer(text[:1024], max_length=150)[0]['summary_text']

        # Print debug information
        print(f"File Path: {doc_record.file_path}")
        print(f"Extracted Text: {text}")
        print(f"Predicted Document Type: {doc_type}")
        print(f"Extracted Info: {info}")
        print(f"Summary: {summary}")

        # Save to DB
        doc_record.content = text
        doc_record.doc_type = doc_type
        doc_record.meta_data = json.dumps(info)
        doc_record.summary = summary
        db.commit()

        return {"status": "processed"}

    finally:
        db.close()
