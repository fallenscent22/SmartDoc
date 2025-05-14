from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from app.core.constants import MODEL_PATHS
from typing import Dict, Any

class SummaryGenerator:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.summarizer = None
        self.load_model()

    def load_model(self):
        try:
            self.summarizer = pipeline("summarization", model="t5-small")
        except Exception as e:
            raise RuntimeError(f"Error loading transformer model: {str(e)}")

    def generate_summary(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        if not self.summarizer:
            return {"error": "Model not loaded"}
            
        summary = self.summarizer(
            text,
            max_length=max_length,
            min_length=30,
            do_sample=False
        )
        return summary[0]['summary_text']