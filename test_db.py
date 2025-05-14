from app.database import Session
from models import Document

session = Session()

# Query all records
documents = session.query(Document).all()

# Print all document info
for doc in documents:
    print(f"ID: {doc.id}, Filename: {doc.filename}, File Path: {doc.file_path}, Doc Type: {doc.doc_type}")

session.close()
