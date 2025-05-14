import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from app.core.constants import MODEL_PATHS
from typing import Optional

class DocumentClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_model()

    def load_model(self):
        try:
            with open(MODEL_PATHS["classifier"], 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.vectorizer = model_data['vectorizer']
        except Exception as e:
            raise RuntimeError(f"Error loading classifier model: {str(e)}")

    def classify(self, text: str) -> Optional[str]:
        if not self.model or not self.vectorizer:
            return None
            
        X = self.vectorizer.transform([text])
        prediction = self.model.predict(X)
        return prediction[0]