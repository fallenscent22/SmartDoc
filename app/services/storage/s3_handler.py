import boto3
from botocore.exceptions import ClientError
from app.core.constants import S3_BUCKET_NAME, AWS_REGION

class S3Handler:
    def __init__(self):
        self.s3 = boto3.client('s3', region_name=AWS_REGION)
    
    async def upload_file(self, file) -> str:
        try:
            file_key = f"uploads/{file.filename}"
            self.s3.upload_fileobj(file.file, S3_BUCKET_NAME, file_key)
            return file_key
        except ClientError as e:
            raise RuntimeError(f"S3 upload error: {str(e)}")