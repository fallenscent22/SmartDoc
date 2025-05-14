from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    owner_id: int

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    file_key: str

    class Config:
        orm_mode = True