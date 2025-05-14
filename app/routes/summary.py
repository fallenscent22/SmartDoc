from fastapi import APIRouter, HTTPException
from app.services.ai.transformer_clf import SummaryGenerator
from app.schemas.response import SummaryResponse

router = APIRouter()

@router.post("/summarize", response_model=SummaryResponse)
async def generate_summary(file_key: str):
    if not file_key:
        raise HTTPException(400, "Invalid file key")
    
    generator = SummaryGenerator()
    summary = await generator.generate_summary(file_key)
    
    return {
        "status": "success",
        "summary": summary,
        "length": len(summary)
    }