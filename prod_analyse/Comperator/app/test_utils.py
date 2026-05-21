import sys
from unittest.mock import MagicMock
sys.modules['nltk'] = MagicMock()
sys.modules['nltk.corpus'] = MagicMock()

import pytest
from utils import normalize_text

@pytest.fixture(autouse=True)
def reset_mocks():
    if 'nltk' in sys.modules and hasattr(sys.modules['nltk'], 'reset_mock'):
        sys.modules['nltk'].reset_mock()
    if 'nltk.corpus' in sys.modules and hasattr(sys.modules['nltk.corpus'], 'reset_mock'):
        sys.modules['nltk.corpus'].reset_mock()

def test_normalize_text_removes_http_https():
    text = "Check this out https://example.com and http://test.org"
    result = normalize_text(text, [])
    assert result == "Check this out example.com and test.org"

def test_normalize_text_removes_www():
    text = "Visit www.example.com for more info"
    result = normalize_text(text, [])
    assert result == "Visit example.com for more info"

def test_normalize_text_removes_special_characters():
    text = "Hello, world! This is a test: punctuation should go away; right?"
    result = normalize_text(text, [])
    assert result == "Hello world This is a test punctuation should go away right"

def test_normalize_text_keeps_periods_and_whitespace():
    text = "This. is. fine.  "
    result = normalize_text(text, [])
    assert result == "This. is. fine.  "

def test_normalize_text_keeps_alphanumerics():
    text = "Testing 12345"
    result = normalize_text(text, [])
    assert result == "Testing 12345"

def test_normalize_text_empty_string():
    text = ""
    result = normalize_text(text, [])
    assert result == ""

def test_normalize_text_mixed():
    text = "WOW! Check out https://www.amazing-website.com/test-page for details... It's 100% awesome."
    result = normalize_text(text, [])
    assert result == "WOW Check out amazingwebsite.comtestpage for details... Its 100 awesome."
