"""
Gemini API client for TinyTroupe.
Handles communication with Google's Gemini models.
"""

import logging
import os
import time
from typing import Any, Dict, List, Optional

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError, RetryError

from tinytroupe import config_manager, utils

logger = logging.getLogger("tinytroupe")


class GeminiClient:
    """
    A client for interacting with Google's Gemini API.
    """

    def __init__(self):
        """Initialize the Gemini client."""
        self.api_key = None
        self.cache_api_calls = False
        self.api_cache = {}
        self._cache_lock = __import__("threading").Lock()
        self._concurrency_semaphore = None
        self._setup_from_config()

    def _setup_from_config(self):
        """Setup the client from configuration."""
        # Get API key from environment
        self.api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not self.api_key:
            # Try to load from .env file
            from pathlib import Path
            env_file = Path(__file__).parent.parent.parent / ".env"
            if env_file.exists():
                with open(env_file) as f:
                    for line in f:
                        if line.startswith("GOOGLE_GEMINI_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip()
                            break
        
        if not self.api_key:
            logger.warning(
                "GOOGLE_GEMINI_API_KEY not found. "
                "Client will not work until API key is set."
            )
            return

        # Configure the Gemini API
        genai.configure(api_key=self.api_key)

        # Setup concurrency control
        max_concurrent = config_manager.get("max_concurrent_model_calls")
        if max_concurrent and max_concurrent > 0:
            self._concurrency_semaphore = __import__("threading").Semaphore(
                max_concurrent
            )

        # Setup caching
        cache_api_calls = config_manager.get("cache_api_calls")
        cache_file_name = config_manager.get("cache_file_name")
        self.set_api_cache(cache_api_calls, cache_file_name)

    def _concurrency_slot(self):
        """Context manager for concurrency control."""
        class ConcurrencySlot:
            def __init__(self, semaphore):
                self.semaphore = semaphore

            def __enter__(self):
                if self.semaphore:
                    self.semaphore.acquire()
                return self

            def __exit__(self, *args):
                if self.semaphore:
                    self.semaphore.release()

        return ConcurrencySlot(self._concurrency_semaphore)

    def set_api_cache(self, cache_api_calls, cache_file_name=None):
        """
        Set the API cache configuration.

        Args:
            cache_api_calls (bool): Whether to cache API calls.
            cache_file_name (str): The name of the file to use for caching.
        """
        self.cache_api_calls = cache_api_calls
        if cache_file_name:
            self.cache_file_name = cache_file_name
        else:
            self.cache_file_name = "gemini_api_cache.pickle"

        if self.cache_api_calls:
            self._load_cache()

    def _load_cache(self):
        """Load the API cache from disk."""
        import pickle

        try:
            with open(self.cache_file_name, "rb") as f:
                self.api_cache = pickle.load(f)
                logger.info(f"Loaded API cache from {self.cache_file_name}")
        except FileNotFoundError:
            self.api_cache = {}

    def _save_cache(self):
        """Save the API cache to disk."""
        import pickle

        try:
            with open(self.cache_file_name, "wb") as f:
                pickle.dump(self.api_cache, f)
        except Exception as e:
            logger.warning(f"Failed to save API cache: {e}")

    def _get_cached_response(self, cache_key):
        """Get a cached response if available."""
        if not self.cache_api_calls:
            return None
        return self.api_cache.get(cache_key)

    def _to_cacheable_format(self, response):
        """Convert response to a cacheable format."""
        if response is None:
            return None
        # Store the raw response dict
        return response

    def _count_tokens(self, messages, model=None):
        """
        Count tokens in a message list.

        Args:
            messages (list): List of message dictionaries.
            model (str): The model to use for token counting.

        Returns:
            int: The number of tokens.
        """
        if model is None:
            model = config_manager.get("model")

        try:
            # Convert OpenAI format to Gemini format
            gemini_messages = self._convert_messages_to_gemini_format(messages)
            
            # Use Gemini's token counting
            gemini_model = genai.GenerativeModel(model)
            response = gemini_model.count_tokens(gemini_messages)
            return response.total_tokens
        except Exception as e:
            logger.warning(f"Token counting failed: {e}")
            raise NotImplementedError(f"Token counting not available for model {model}")

    def _convert_messages_to_gemini_format(self, messages):
        """
        Convert OpenAI message format to Gemini format.

        Args:
            messages (list): List of messages in OpenAI format.

        Returns:
            list: List of messages in Gemini format.
        """
        gemini_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            # Convert role names
            if role == "assistant":
                role = "model"
            elif role == "user":
                role = "user"
            elif role == "system":
                # System messages in Gemini are handled differently
                # We'll prepend them to the first user message
                continue

            gemini_messages.append({"role": role, "parts": [{"text": content}]})

        return gemini_messages

    def _raw_model_call(self, model, chat_api_params):
        """
        Make a raw call to the Gemini API.

        Args:
            model (str): The model to use.
            chat_api_params (dict): The parameters for the API call.

        Returns:
            dict: The response from the API.
        """
        messages = chat_api_params.get("messages", [])
        temperature = chat_api_params.get("temperature")
        max_completion_tokens = chat_api_params.get("max_completion_tokens")
        top_p = chat_api_params.get("top_p")
        stop = chat_api_params.get("stop")

        # Convert messages to Gemini format
        gemini_messages = self._convert_messages_to_gemini_format(messages)

        # Build generation config
        generation_config = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if max_completion_tokens is not None:
            generation_config["max_output_tokens"] = max_completion_tokens
        if top_p is not None:
            generation_config["top_p"] = top_p
        if stop is not None:
            generation_config["stop_sequences"] = [stop] if isinstance(stop, str) else stop

        try:
            gemini_model = genai.GenerativeModel(model)
            response = gemini_model.generate_content(
                gemini_messages,
                generation_config=generation_config if generation_config else None,
                stream=False,
            )

            # Convert Gemini response to OpenAI-like format for compatibility
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": response.text,
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,  # Gemini doesn't provide this in response
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise

    def _raw_model_response_extractor(self, response):
        """
        Extract the raw message from the API response.

        Args:
            response (dict): The response from the API.

        Returns:
            dict: The extracted message in OpenAI format.
        """
        if response is None:
            return None

        try:
            # Return the message dict (compatible with OpenAI format)
            return response["choices"][0]["message"]
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Failed to extract response: {e}")
            return None

    def _update_cost_stats(self, response, from_cache=False):
        """
        Update cost statistics (placeholder for now).

        Args:
            response (dict): The API response.
            from_cache (bool): Whether the response was from cache.
        """
        # Gemini pricing is different from OpenAI, implement as needed
        pass

    def send_message(
        self,
        current_messages,
        dedent_messages=True,
        model=None,
        temperature=None,
        max_completion_tokens=None,
        top_p=None,
        frequency_penalty=None,
        presence_penalty=None,
        stop=None,
        timeout=None,
        max_attempts=None,
        waiting_time=None,
        exponential_backoff_factor=None,
        n=1,
        response_format=None,
        enable_pydantic_model_return=False,
        echo=False,
    ):
        """
        Send a message to the Gemini API.

        Args:
            current_messages (list): List of message dictionaries.
            dedent_messages (bool): Whether to dedent messages.
            model (str): The model to use.
            temperature (float): Temperature for generation.
            max_completion_tokens (int): Maximum tokens to generate.
            top_p (float): Top-p sampling parameter.
            frequency_penalty (float): Frequency penalty (not supported by Gemini).
            presence_penalty (float): Presence penalty (not supported by Gemini).
            stop (str): Stop sequence.
            timeout (int): Timeout in seconds.
            max_attempts (int): Maximum retry attempts.
            waiting_time (int): Wait time between retries.
            exponential_backoff_factor (float): Backoff factor.
            n (int): Number of completions (not supported by Gemini).
            response_format: Response format specification.
            enable_pydantic_model_return (bool): Whether to return Pydantic model.
            echo (bool): Whether to echo input.

        Returns:
            dict: The response message.
        """
        from tinytroupe.clients import InvalidRequestError, NonTerminalError

        # Setup defaults from config
        self._setup_from_config()
        if model is None:
            model = config_manager.get("model")
        if temperature is None:
            temperature = config_manager.get("temperature", 0.7)
        if max_completion_tokens is None:
            max_completion_tokens = config_manager.get("max_completion_tokens")
        if timeout is None:
            timeout = config_manager.get("timeout")
        if max_attempts is None:
            max_attempts = config_manager.get("max_attempts")
        if waiting_time is None:
            waiting_time = config_manager.get("waiting_time")
        if exponential_backoff_factor is None:
            exponential_backoff_factor = config_manager.get("exponential_backoff_factor")

        # Dedent messages if needed
        if dedent_messages:
            for message in current_messages:
                if "content" in message:
                    message["content"] = utils.dedent(message["content"])

        # Build API parameters
        chat_api_params = {
            "model": model,
            "messages": current_messages,
            "temperature": temperature,
            "max_completion_tokens": max_completion_tokens,
            "top_p": top_p,
            "stop": stop,
            "timeout": timeout,
            "stream": False,
            "n": n,
        }

        if response_format is not None:
            chat_api_params["response_format"] = response_format

        # Remove None values
        chat_api_params = {k: v for k, v in chat_api_params.items() if v is not None}

        # Retry loop
        i = 0
        while i < max_attempts:
            try:
                i += 1

                try:
                    logger.debug(
                        f"Sending messages to Gemini API. Token count={self._count_tokens(current_messages, model)}."
                    )
                except NotImplementedError:
                    logger.debug(f"Token count not implemented for model {model}.")

                start_time = time.monotonic()
                logger.debug(f"Calling Gemini model {model}.")

                # Check cache
                cache_key = str((model, chat_api_params))
                pre_cached_response = self._get_cached_response(cache_key)

                should_wait_before_call = waiting_time > 0 and pre_cached_response is None

                if should_wait_before_call:
                    logger.info(
                        f"Waiting {waiting_time} seconds before next API request..."
                    )
                    time.sleep(waiting_time)

                with self._concurrency_slot():
                    response = None
                    cached_response = (
                        pre_cached_response
                        if pre_cached_response is not None
                        else self._get_cached_response(cache_key)
                    )

                    if cached_response is not None:
                        response = cached_response
                    else:
                        response = self._raw_model_call(model, chat_api_params)
                        if self.cache_api_calls:
                            with self._cache_lock:
                                existing = (
                                    self.api_cache.get(cache_key)
                                    if hasattr(self, "api_cache")
                                    else None
                                )
                                if existing is None:
                                    cacheable_response = self._to_cacheable_format(response)
                                    if cacheable_response is not None:
                                        self.api_cache[cache_key] = cacheable_response
                                        self._save_cache()
                                else:
                                    response = existing

                    raw_message = self._raw_model_response_extractor(response)
                    self._update_cost_stats(response, cached_response is not None)

                logger.debug(f"Got response from Gemini API: {response}")
                end_time = time.monotonic()
                logger.debug(
                    f"Got response in {end_time - start_time:.2f} seconds after {i} attempts."
                )

                if enable_pydantic_model_return:
                    return utils.to_pydantic_or_sanitized_dict(
                        raw_message,
                        model=response_format,
                    )
                else:
                    return utils.sanitize_dict(raw_message)

            except InvalidRequestError as e:
                logger.error(f"[{i}] Invalid request error, won't retry: {e}")
                return None

            except GoogleAPIError as e:
                logger.error(f"[{i}] Google API error: {e}")
                if "rate" in str(e).lower():
                    logger.warning(f"[{i}] Rate limit error, waiting and retrying...")
                    if waiting_time <= 0:
                        waiting_time = 2
                    time.sleep(waiting_time)
                    waiting_time = waiting_time * exponential_backoff_factor
                else:
                    if waiting_time <= 0:
                        waiting_time = 2
                    time.sleep(waiting_time)
                    waiting_time = waiting_time * exponential_backoff_factor

            except Exception as e:
                logger.error(f"[{i}] {type(e).__name__} Error: {e}")
                if waiting_time <= 0:
                    waiting_time = 2
                time.sleep(waiting_time)
                waiting_time = waiting_time * exponential_backoff_factor

        logger.error(f"Failed to get response after {max_attempts} attempts.")
        return None

    def get_embedding(self, text, model=None):
        """
        Get embeddings for text using Gemini.

        Args:
            text (str): The text to embed.
            model (str): The embedding model to use.

        Returns:
            list: The embedding vector.
        """
        if model is None:
            model = config_manager.get("embedding_model")

        try:
            result = genai.embed_content(model=model, content=text)
            return result["embedding"]
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            raise
