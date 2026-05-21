import pytest
from simulation_server import LLMOrchestrator

def test_assign_backend_round_robin():
    orchestrator = LLMOrchestrator()
    # Mocking backends explicitly to avoid relying on real API keys logic
    orchestrator.backends = [
        {"name": "Backend 0"},
        {"name": "Backend 1"},
        {"name": "Backend 2"}
    ]

    assert orchestrator._assign_backend(0) == {"name": "Backend 0"}
    assert orchestrator._assign_backend(1) == {"name": "Backend 1"}
    assert orchestrator._assign_backend(2) == {"name": "Backend 2"}
    assert orchestrator._assign_backend(3) == {"name": "Backend 0"}
    assert orchestrator._assign_backend(4) == {"name": "Backend 1"}

def test_assign_backend_no_backends():
    orchestrator = LLMOrchestrator()
    orchestrator.backends = []

    with pytest.raises(ValueError, match="No LLM backends available."):
        orchestrator._assign_backend(0)

def test_assign_backend_ollama_availability():
    orchestrator = LLMOrchestrator()
    orchestrator.backends = [
        {"name": "Backend 0"},
        {"name": "Ollama", "available": False},
        {"name": "Backend 1"}
    ]

    assert orchestrator._assign_backend(0) == {"name": "Backend 0"}
    assert orchestrator._assign_backend(1) == {"name": "Backend 1"}
    assert orchestrator._assign_backend(2) == {"name": "Backend 0"}

def test_assign_backend_all_ollama_unavailable():
    orchestrator = LLMOrchestrator()
    orchestrator.backends = [
        {"name": "Ollama", "available": False},
        {"name": "Ollama", "available": False}
    ]

    # If all available filtered are empty, it falls back to all backends
    assert orchestrator._assign_backend(0) == {"name": "Ollama", "available": False}
    assert orchestrator._assign_backend(1) == {"name": "Ollama", "available": False}
