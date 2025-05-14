from app.services.ai.ner_enhanced import NEREnhanced

def test_ner_extraction():
    ner = NEREnhanced()
    entities = ner.extract_entities_from_s3("dummy_key")
    assert isinstance(entities, dict)
    assert all(isinstance(v, list) for v in entities.values())