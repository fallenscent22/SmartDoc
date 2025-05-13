from typing import List
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
class DocClassifier:
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression())
        ])
        self.is_trained = False
    
    def train(self, texts: List[str], labels: List[str]):
        self.model.fit(texts, labels)
        self.is_trained = True
    
    def predict(self, text: str) -> str:
        if not self.is_trained:
            raise ValueError("Classifier not trained.")
        return self.model.predict([text])[0]