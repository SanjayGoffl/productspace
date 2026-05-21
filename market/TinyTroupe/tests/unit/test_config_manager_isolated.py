import unittest
from unittest.mock import MagicMock, patch
import logging
import sys
import os

# Add the tinytroupe directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Mock dependencies before importing tinytroupe
sys.modules["rich"] = MagicMock()
sys.modules["rich.jupyter"] = MagicMock()
sys.modules["llama_index"] = MagicMock()
sys.modules["llama_index.core"] = MagicMock()
sys.modules["llama_index.readers"] = MagicMock()
sys.modules["llama_index.readers.web"] = MagicMock()
sys.modules["llama_index.embeddings"] = MagicMock()
sys.modules["llama_index.embeddings.openai"] = MagicMock()
sys.modules["llama_index.embeddings.azure_openai"] = MagicMock()

# Mock tinytroupe.utils which is imported in tinytroupe/__init__.py
mock_utils = MagicMock()
sys.modules["tinytroupe.utils"] = mock_utils

from tinytroupe import ConfigManager, get_config

class TestConfigManager(unittest.TestCase):

    def test_parse_concurrency_limit(self):
        cm = ConfigManager()

        # Test None
        self.assertEqual(cm._parse_concurrency_limit(None, 4), 4)

        # Test int/float
        self.assertEqual(cm._parse_concurrency_limit(5, 4), 5)
        self.assertEqual(cm._parse_concurrency_limit(5.5, 4), 5)

        # Test str
        self.assertEqual(cm._parse_concurrency_limit("10", 4), 10)
        self.assertEqual(cm._parse_concurrency_limit("  20  ", 4), 20)
        self.assertEqual(cm._parse_concurrency_limit("", 4), 4)

        # Test special tokens
        self.assertIsNone(cm._parse_concurrency_limit("NONE", 4))
        self.assertIsNone(cm._parse_concurrency_limit("off", 4))
        self.assertIsNone(cm._parse_concurrency_limit("disable", 4))
        self.assertIsNone(cm._parse_concurrency_limit("DISABLED", 4))

        # Test invalid string
        with patch("logging.warning") as mock_warning:
            self.assertEqual(cm._parse_concurrency_limit("invalid", 4), 4)
            mock_warning.assert_called_once()

        # Test non-positive integers
        self.assertIsNone(cm._parse_concurrency_limit(0, 4))
        self.assertIsNone(cm._parse_concurrency_limit(-1, 4))

        # Test other types
        self.assertEqual(cm._parse_concurrency_limit([], 4), 4)

    def test_config_manager_get(self):
        cm = ConfigManager()
        cm._config = {"test_key": "test_value"}

        # Test valid key
        self.assertEqual(cm.get("test_key"), "test_value")

        # Test case-insensitivity
        self.assertEqual(cm.get("TEST_KEY"), "test_value")

        # Test invalid key with default
        self.assertEqual(cm.get("non_existent", "default"), "default")
        self.assertIsNone(cm.get("non_existent"))

    def test_config_manager_update(self):
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
        self.assertEqual(cm.get("test_key"), "new_value")

        # Test case-insensitive update
        cm.update("TEST_KEY", "newer_value")
        self.assertEqual(cm.get("test_key"), "newer_value")

        # Test unknown key
        with patch("logging.warning") as mock_warning:
            cm.update("unknown_key", "value")
            mock_warning.assert_called_once()

        # Test loglevel update
        cm.update("loglevel", "debug")
        self.assertEqual(cm.get("loglevel"), "DEBUG")
        self.assertEqual(cm.get("loglevel_console"), "DEBUG")
        self.assertEqual(cm.get("loglevel_file"), "DEBUG")
        mock_utils.set_loglevel.assert_called_with("debug")

        # Test loglevel_console update
        cm.update("loglevel_console", "warning")
        self.assertEqual(cm.get("loglevel_console"), "WARNING")
        mock_utils.set_console_loglevel.assert_called_with("warning")

        # Test loglevel_file update
        cm.update("loglevel_file", "error")
        self.assertEqual(cm.get("loglevel_file"), "ERROR")
        mock_utils.set_file_loglevel.assert_called_with("error")

        # Test log_include_thread_id update
        cm.update("log_include_thread_id", "true")
        self.assertTrue(cm.get("log_include_thread_id"))
        mock_utils.set_include_thread_info.assert_called_with(True)

        cm.update("log_include_thread_id", False)
        self.assertFalse(cm.get("log_include_thread_id"))
        mock_utils.set_include_thread_info.assert_called_with(False)

        # Test max_concurrent_model_calls update
        cm.update("max_concurrent_model_calls", "NONE")
        self.assertIsNone(cm.get("max_concurrent_model_calls"))

        cm.update("max_concurrent_model_calls", 10)
        self.assertEqual(cm.get("max_concurrent_model_calls"), 10)

    def test_config_manager_update_multiple(self):
        cm = ConfigManager()
        cm._config = {"key1": "v1", "key2": "v2"}

        cm.update_multiple({"key1": "new_v1", "key2": "new_v2"})
        self.assertEqual(cm.get("key1"), "new_v1")
        self.assertEqual(cm.get("key2"), "new_v2")

    def test_config_manager_reset(self):
        cm = ConfigManager()
        with patch.object(cm, "_initialize_from_config") as mock_init:
            cm.reset()
            mock_init.assert_called_once()

    def test_config_manager_getitem(self):
        cm = ConfigManager()
        cm._config = {"test_key": "test_value"}

        self.assertEqual(cm["test_key"], "test_value")
        self.assertEqual(cm["TEST_KEY"], "test_value")

    def test_config_manager_config_defaults(self):
        cm = ConfigManager()
        cm._config = {"model": "gpt-4o", "temperature": 0.5}

        @cm.config_defaults(model="model", temp="temperature")
        def test_func(param1, model=None, temp=None):
            return param1, model, temp

        # Test with None values
        self.assertEqual(test_func("val", model=None, temp=None), ("val", "gpt-4o", 0.5))

        # Test with provided values
        self.assertEqual(test_func("val", model="gpt-3.5-turbo", temp=0.7), ("val", "gpt-3.5-turbo", 0.7))

        # Test mixed
        self.assertEqual(test_func("val", model=None, temp=0.7), ("val", "gpt-4o", 0.7))

    def test_get_config(self):
        with patch("tinytroupe.config_manager") as mock_cm:
            mock_cm.get.return_value = "config_value"

            # Test override
            self.assertEqual(get_config("any_key", override_value="override"), "override")
            mock_cm.get.assert_not_called()

            # Test fallback
            self.assertEqual(get_config("any_key"), "config_value")
            mock_cm.get.assert_called_with("any_key")

if __name__ == '__main__':
    unittest.main()
