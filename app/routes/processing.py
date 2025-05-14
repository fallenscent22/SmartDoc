from fastapi import APIRouter, UploadFile, HTTPException
from app.services.storage.s3_handler import S3Handler
from app.services.ai.ner_enhanced import NEREnhanced
from app.schemas.response import ProcessingResponse

router = APIRouter()

@router.post("/process", response_model=ProcessingResponse)
async def process_document(file: UploadFile):
    if not file.filename:
        raise HTTPException(400, "Invalid filename")
    
    # Upload to S3
    s3 = S3Handler()
    file_key = await s3.upload_file(file)
    
    # Process with NER
    ner = NEREnhanced()
    entities = await ner.extract_entities_from_s3(file_key)
    
    return {
        "status": "success",
        "file_key": file_key,
        "entities": entities
    }