from fastapi import FastAPI,HTTPException
from sqlalchemy.orm import Session
from transformers import pipeline
import json

#import local models
from processor import extract_text
from info_extractor import extract_info
from classifier import DocClassifier
from database import Session, Document
from models import Document  # Replace with the actual path to your Document model

app = FastAPI()
@app.post("/process")
async def process_file(file_id: str):
    session = Session()
    
    try:
        # Get file metadata
        doc_record = session.query(Document).filter_by(id=file_id).first()
        if not doc_record:
            raise HTTPException(status_code=404, detail="Document not found")

        # Extract text
        text = extract_text(doc_record.file_path, doc_record.file_type)
        
        # Classify document
        classifier = DocClassifier()
        doc_type = classifier.predict(text)

        # Sample training (later replace with your actual training data)
        classifier = DocClassifier()
        classifier.train(
            texts=[
                "Invoice for purchase of items totaling $200.",
                "Experienced software engineer with a strong background...",
                "This is a sample document of unknown category."
            ],
            labels=[
                "invoice", "resume", "pdf"
          ]
     )
        doc_type = classifier.predict(text)
        
        # Extract information
        info = extract_info(text, doc_type)
        
        # Generate summary
        summarizer = pipeline("summarization")
        summary = summarizer(text[:1024], max_length=150)[0]['summary_text']
        
        # Update database
        doc_record.content = text
        doc_record.doc_type = doc_type
        doc_record.meta_data = json.dumps(info)
        doc_record.summary = summary
        
        session.commit()
        return {"status": "processed"}
    
    finally:
        session.close()