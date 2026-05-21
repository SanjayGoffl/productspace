import sys
from unittest.mock import MagicMock
fastapi_mock = MagicMock()
sys.modules['fastapi'] = fastapi_mock
sys.modules['fastapi.responses'] = MagicMock()
sys.modules['fastapi.middleware.cors'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['httpx'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

import pytest
import asyncio
from simulation_server import LLMOrchestrator

def test_assign_backend():
    orchestrator = LLMOrchestrator()

    # Replace initialized backends with test data
    orchestrator.backends = [
        {"name": "Backend1"},
        {"name": "Backend2"},
        {"name": "Backend3"}
    ]

    # Test valid assignment logic
    assert orchestrator._assign_backend(0) == {"name": "Backend1"}
    assert orchestrator._assign_backend(1) == {"name": "Backend2"}
    assert orchestrator._assign_backend(2) == {"name": "Backend3"}
    assert orchestrator._assign_backend(3) == {"name": "Backend1"}

    # Test fallback when Ollama is configured
    orchestrator.backends = [
        {"name": "Backend1", "available": True},
        {"name": "Backend2", "available": True},
        {"name": "Ollama", "available": False},
        {"name": "Backend3", "available": True}
    ]
    assert orchestrator._assign_backend(0) == {"name": "Backend1", "available": True}
    assert orchestrator._assign_backend(1) == {"name": "Backend2", "available": True}
    assert orchestrator._assign_backend(2) == {"name": "Backend3", "available": True}
    assert orchestrator._assign_backend(3) == {"name": "Backend1", "available": True}

    # Test fallback when only Ollama is available but available is False
    orchestrator.backends = [
        {"name": "Ollama", "available": False},
        {"name": "Ollama", "available": False}
    ]
    assert orchestrator._assign_backend(0) == {"name": "Ollama", "available": False}

    # Test ValueError when no backends are configured
    orchestrator.backends = []
    with pytest.raises(ValueError, match="No LLM backends available."):
        orchestrator._assign_backend(0)
