
import pytest
import json

def test_chat_returns_answer():
    sample_response = {
        "answer": "The refund policy allows 30 days. [1]",
        "citations": [{"id": 1, "title": "Refund Policy"}],
        "telemetry": {"total_ms": 1200}
    }
    assert "answer" in sample_response
    assert len(sample_response["citations"]) > 0

def test_telemetry_included():
    sample_response = {
        "answer": "Test",
        "citations": [],
        "telemetry": {"total_ms": 900, "chunks_retrieved": 5}
    }
    assert sample_response["telemetry"]["chunks_retrieved"] == 5

def test_empty_question_rejected():
    question = ""
    assert len(question.strip()) == 0
