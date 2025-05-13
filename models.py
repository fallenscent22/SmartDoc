from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///documents.db')

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(String, primary_key=True)
    filename = Column(String)
    file_path = Column(String)  # File path
    doc_type = Column(String)
    content = Column(Text)
    summary = Column(Text)
    meta_data = Column(Text)  # JSON string

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
