from sqlalchemy import Boolean, Column, String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB  # Changed from SQLite
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    file_path = Column(String)
    doc_type = Column(String)
    content = Column(Text)
    summary = Column(Text)
    meta_data = Column(JSONB)  # Changed from Text to JSONB
    is_processed = Column(Boolean, default=False)
    