from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:pass@localhost/smartdoc"
    ocr_engine: str = "tesseract"
    ai_model: str = "bert-base-uncased"
    s3_bucket: str = "your-bucket-name"

    class Config:
        env_file = ".env"

settings = Settings()