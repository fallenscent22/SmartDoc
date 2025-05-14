from pydantic import BaseModel
from typing import Dict, List

class ProcessingResponse(BaseModel):
    status: str
    file_key: str
    entities: Dict[str, List[str]]

class SummaryResponse(BaseModel):
    status: str
    summary: str
    length: int