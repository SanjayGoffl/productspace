import pytest
from unittest.mock import MagicMock, patch
import logging
import sys
import os

# Add the tinytroupe directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from tinytroupe import ConfigManager, get_config, config_manager

def test_parse_concurrency_limit():
    cm = ConfigManager()

    # Test None
    assert cm._parse_concurrency_limit(None, 4) == 4

    # Test int/float
    assert cm._parse_concurrency_limit(5, 4) == 5
    assert cm._parse_concurrency_limit(5.5, 4) == 5

    # Test str
    assert cm._parse_concurrency_limit("10", 4) == 10
    assert cm._parse_concurrency_limit("  20  ", 4) == 20
    assert cm._parse_concurrency_limit("", 4) == 4

    # Test special tokens
    assert cm._parse_concurrency_limit("NONE", 4) is None
    assert cm._parse_concurrency_limit("off", 4) is None
    assert cm._parse_concurrency_limit("disable", 4) is None
    assert cm._parse_concurrency_limit("DISABLED", 4) is None

    # Test invalid string
    with patch("logging.warning") as mock_warning:
        assert cm._parse_concurrency_limit("invalid", 4) == 4
        mock_warning.assert_called_once()

    # Test non-positive integers
    assert cm._parse_concurrency_limit(0, 4) is None
    assert cm._parse_concurrency_limit(-1, 4) is None

    # Test other types
    assert cm._parse_concurrency_limit([], 4) == 4

def test_config_manager_get():
    cm = ConfigManager()
    cm._config = {"test_key": "test_value"}

    # Test valid key
    assert cm.get("test_key") == "test_value"

    # Test case-insensitivity
    assert cm.get("TEST_KEY") == "test_value"

    # Test invalid key with default
    assert cm.get("non_existent", "default") == "default"
    assert cm.get("non_existent") is None

def test_config_manager_update():
    cm = ConfigManager()
    cm._config = {
        "test_key": "initial_value",
        "loglevel": "INFO",
        "loglevel_console": "INFO",
        "loglevel_file": "INFO",
        "log_include_thread_id": False,
        "max_concurrent_model_calls": 4
    }

    # Test standard update
    cm.update("test_key", "new_value")
    assert cm.get("test_key") == "new_value"

    # Test case-insensitive update
    cm.update("TEST_KEY", "newer_value")
    assert cm.get("test_key") == "newer_value"

    # Test unknown key
    with patch("logging.warning") as mock_warning:
        cm.update("unknown_key", "value")
        mock_warning.assert_called_once()

    # Test loglevel update
    with patch("tinytroupe.utils.set_loglevel") as mock_set_loglevel:
        cm.update("loglevel", "debug")
        assert cm.get("loglevel") == "DEBUG"
        assert cm.get("loglevel_console") == "DEBUG"
        assert cm.get("loglevel_file") == "DEBUG"
        mock_set_loglevel.assert_called_with("debug")

    # Test loglevel_console update
    with patch("tinytroupe.utils.set_console_loglevel") as mock_set_console:
        cm.update("loglevel_console", "warning")
        assert cm.get("loglevel_console") == "WARNING"
        mock_set_console.assert_called_with("warning")

    # Test loglevel_file update
    with patch("tinytroupe.utils.set_file_loglevel") as mock_set_file:
        cm.update("loglevel_file", "error")
        assert cm.get("loglevel_file") == "ERROR"
        mock_set_file.assert_called_with("error")

    # Test log_include_thread_id update
    with patch("tinytroupe.utils.set_include_thread_info") as mock_set_thread:
        cm.update("log_include_thread_id", "true")
        assert cm.get("log_include_thread_id") is True
        mock_set_thread.assert_called_with(True)

        cm.update("log_include_thread_id", False)
        assert cm.get("log_include_thread_id") is False
        mock_set_thread.assert_called_with(False)

    # Test max_concurrent_model_calls update
    cm.update("max_concurrent_model_calls", "NONE")
    assert cm.get("max_concurrent_model_calls") is None

    cm.update("max_concurrent_model_calls", 10)
    assert cm.get("max_concurrent_model_calls") == 10

def test_config_manager_update_multiple():
    cm = ConfigManager()
    cm._config = {"key1": "v1", "key2": "v2"}

    cm.update_multiple({"key1": "new_v1", "key2": "new_v2"})
    assert cm.get("key1") == "new_v1"
    assert cm.get("key2") == "new_v2"

def test_config_manager_reset():
    cm = ConfigManager()
    with patch.object(cm, "_initialize_from_config") as mock_init:
        cm.reset()
        mock_init.assert_called_once()

def test_config_manager_getitem():
    cm = ConfigManager()
    cm._config = {"test_key": "test_value"}

    assert cm["test_key"] == "test_value"
    assert cm["TEST_KEY"] == "test_value"

def test_config_manager_config_defaults():
    cm = ConfigManager()
    cm._config = {"model": "gpt-4o", "temperature": 0.5}

    @cm.config_defaults(model="model", temp="temperature")
    def test_func(param1, model=None, temp=None):
        return param1, model, temp

    # Test with None values
    assert test_func("val", model=None, temp=None) == ("val", "gpt-4o", 0.5)

    # Test with provided values
    assert test_func("val", model="gpt-3.5-turbo", temp=0.7) == ("val", "gpt-3.5-turbo", 0.7)

    # Test mixed
    assert test_func("val", model=None, temp=0.7) == ("val", "gpt-4o", 0.7)

def test_get_config():
    with patch("tinytroupe.config_manager.get") as mock_get:
        mock_get.return_value = "config_value"

        # Test override
        assert get_config("any_key", override_value="override") == "override"
        mock_get.assert_not_called()

        # Test fallback
        assert get_config("any_key") == "config_value"
        mock_get.assert_called_with("any_key")
