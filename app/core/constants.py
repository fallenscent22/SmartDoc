ALLOWED_FILE_TYPES = {"pdf", "docx", "txt", "pptx"}
MAX_FILE_SIZE_MB = 50
AWS_REGION = "us-west-2"
S3_BUCKET_NAME = "smartdoc-prod"
MODEL_PATHS = {
    "ner": "en_core_web_lg",
    "classifier": "models/classifier.pkl"
}
API_RATE_LIMIT = "100/minute"