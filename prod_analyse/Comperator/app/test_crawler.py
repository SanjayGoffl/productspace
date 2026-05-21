

import pytest
from crawler import BeautifulSoupCrawler

@pytest.fixture
def crawler():
    return BeautifulSoupCrawler(
        name="test_crawler",
        allowed_domains=["example.com", "test.org"],
        start_urls=["https://example.com"]
    )

def test_is_valid_url_exact_match(crawler):
    assert crawler.is_valid_url("https://example.com/page") is True
    assert crawler.is_valid_url("http://test.org/path") is True

def test_is_valid_url_subdomain(crawler):
    assert crawler.is_valid_url("https://sub.example.com/page") is True
    assert crawler.is_valid_url("http://blog.test.org/post") is True

def test_is_valid_url_invalid_domain(crawler):
    assert crawler.is_valid_url("https://other.com/page") is False
    assert crawler.is_valid_url("http://example.net") is False

def test_is_valid_url_empty(crawler):
    assert crawler.is_valid_url("") is False

def test_is_valid_url_different_scheme(crawler):
    assert crawler.is_valid_url("ftp://example.com/file") is True

def test_is_valid_url_no_scheme(crawler):
    assert crawler.is_valid_url("//example.com/page") is True

def test_is_valid_url_with_port(crawler):
    assert crawler.is_valid_url("https://example.com:8080") is False

def test_is_valid_url_suffix_match(crawler):
    assert crawler.is_valid_url("https://notexample.com/page") is True
