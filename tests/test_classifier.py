from app.services.ai.transformer_clf import SummaryGenerator

def test_summary_generation():
    generator = SummaryGenerator()
    test_text = "This is a sample document text."
    summary = generator.generate_summary(test_text)
    assert isinstance(summary, str)
    assert len(summary) > 0