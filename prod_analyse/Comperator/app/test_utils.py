import sys
from unittest.mock import MagicMock
import pytest

# Mock nltk and its submodules before importing utils
mock_nltk = MagicMock()
sys.modules['nltk'] = mock_nltk
sys.modules['nltk.corpus'] = MagicMock()

from utils import normalize_text, sample_words

@pytest.fixture(autouse=True)
def reset_mocks():
    sys.modules['nltk'].reset_mock()
    sys.modules['nltk.corpus'].reset_mock()
    yield

def test_normalize_text_removes_http_urls():
    text = "Visit http://example.com for info."
    assert normalize_text(text, []) == "Visit example.com for info."

def test_normalize_text_removes_https_urls():
    text = "Visit https://example.com for info."
    assert normalize_text(text, []) == "Visit example.com for info."

def test_normalize_text_removes_www():
    text = "Go to www.example.com"
    assert normalize_text(text, []) == "Go to example.com"

def test_normalize_text_removes_punctuation():
    # Note: the regex keeps \w, ., \s
    text = "Hello, World! This is a test."
    assert normalize_text(text, []) == "Hello World This is a test."

def test_normalize_text_handles_empty_string():
    assert normalize_text("", []) == ""

def test_normalize_text_preserves_underscores_and_dots():
    # \w includes _, and . is explicitly preserved
    text = "my_file_name.txt"
    assert normalize_text(text, []) == "my_file_name.txt"

def test_normalize_text_removes_emojis():
    text = "Hello 😊 world"
    assert normalize_text(text, []) == "Hello  world"

def test_sample_words():
    words = ["a", "b", "c", "d", "e"]
    sample = sample_words(words, 3)
    assert len(sample) == 3
    for word in sample:
        assert word in words

def test_sample_words_larger_sample_size():
    words = ["a", "b"]
    sample = sample_words(words, 5)
    assert len(sample) == 2
    for word in sample:
        assert word in words
