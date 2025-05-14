from fastapi import UploadFile, HTTPException
import mimetypes
from app.core.constants import ALLOWED_FILE_TYPES

async def validate_file(file: UploadFile):
    allowed_types = {
        'application/pdf', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }
    
    # Verify MIME type
    if file.content_type not in allowed_types:
        return False

    # Verify extension
    extension = file.filename.split('.')[-1].lower()
    if extension not in ALLOWED_FILE_TYPES:
        return False

    return True