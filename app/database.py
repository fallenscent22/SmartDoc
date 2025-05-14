from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./documents.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class DBDocument(Base):  # Renaming the class to DBDocument to match the previous change
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
