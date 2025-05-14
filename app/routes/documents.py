from fastapi import APIRouter, HTTPException, File, UploadFile, BackgroundTasks
from app.services.storage.file_processor import process_document
from app.utils.security import validate_file
from app.services.storage.s3_handler import store_file  # Import store_file
from app.schemas.document import DocumentCreate, Document

router = APIRouter()

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not await validate_file(file):
        raise HTTPException(400, "Invalid file type")
    
    file_uuid = await store_file(file)
    background_tasks.add_task(process_document, file_uuid)
    
    return {"id": file_uuid, "status": "processing_started"}
@router.post("/")
async def create_document(file: UploadFile = File(...)):  # Use UploadFile
    try:
        file_key = await store_file(file)
        return {"file_key": file_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # HTTPException imported