from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///documents.db')

class Document(Base):
    __tablename__ = 'documents'

    id = Column(String, primary_key=True)
    filename = Column(String)
    file_path = Column(String)
    doc_type = Column(String)  # Was 'file_type' in code earlier
    content = Column(Text)
    summary = Column(Text)
    meta_data = Column(Text)  # JSON string (optional metadata)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
