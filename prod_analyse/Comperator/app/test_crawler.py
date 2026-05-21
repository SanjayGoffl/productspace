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
    assert crawler.is_valid_url("https://example.com/path") is True
    assert crawler.is_valid_url("http://test.org/path?q=1") is True

def test_is_valid_url_subdomain(crawler):
    assert crawler.is_valid_url("https://sub.example.com/path") is True
    assert crawler.is_valid_url("https://www.test.org") is True

def test_is_valid_url_unallowed_domain(crawler):
    assert crawler.is_valid_url("https://otherdomain.com/path") is False
    assert crawler.is_valid_url("https://example.org/path") is False

def test_is_valid_url_malformed(crawler):
    # Without scheme, urlparse treats the whole string as path and netloc as empty
    assert crawler.is_valid_url("example.com/path") is False
    # To fix this, urls usually need a scheme
    assert crawler.is_valid_url("https://") is False
