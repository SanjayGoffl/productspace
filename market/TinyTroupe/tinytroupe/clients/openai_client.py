import configparser
import logging
import os
import pickle
import threading
import time
from contextlib import contextmanager
from typing import Union

import httpx
import openai
import tiktoken
from openai import APITimeoutError, AzureOpenAI, OpenAI

from tinytroupe import config_manager, utils
from tinytroupe.control import transactional

logger = logging.getLogger("tinytroupe")

# We'll use various configuration elements below
config = utils.read_config_file()

###########################################################################
# Client class
###########################################################################


class OpenAIClient:
    """
    A utility class for interacting with the OpenAI API.
    """

    @config_manager.config_defaults(
        cache_api_calls="cache_api_calls",
        cache_file_name="cache_file_name",
        max_concurrent_model_calls="max_concurrent_model_calls",
    )
    def __init__(
        self,
        cache_api_calls=None,
        cache_file_name=None,
        max_concurrent_model_calls=None,
    ) -> None:
        logger.debug("Initializing OpenAIClient")
        self._cache_lock = threading.RLock()
        self._max_concurrent_model_calls = self._normalize_concurrency_limit(
            max_concurrent_model_calls
        )
        self._concurrency_semaphore = (
            threading.BoundedSemaphore(self._max_concurrent_model_calls)
            if self._max_concurrent_model_calls is not None
            else None
        )

        # Initialize cost tracking variables
        self._cost_stats_lock = threading.RLock()
        self._reset_cost_stats()

        self.set_api_cache(cache_api_calls, cache_file_name)

    @staticmethod
    def _normalize_concurrency_limit(value):
        if value is None:
            return None

        try:
            candidate = int(value)
        except (TypeError, ValueError):
            logger.warning(
                "Invalid concurrency limit '%s'. Concurrency protection disabled.",
                value,
            )
            return None

        if candidate <= 0:
            return None

        return candidate

    @config_manager.config_defaults(cache_file_name="cache_file_name")
    def set_api_cache(self, cache_api_calls, cache_file_name=None):
        """
        Enables or disables the caching of API calls.

        Args:
        cache_file_name (str): The name of the file to use for caching API calls.
        """
        self.cache_api_calls = cache_api_calls
        self.cache_file_name = cache_file_name
        if self.cache_api_calls:
            # load the cache, if any
            self.api_cache = self._load_cache()

    def _reset_cost_stats(self):
        """
        Resets the cost statistics to zero.
        """
        with self._cost_stats_lock:
            self._input_tokens = 0
            self._output_tokens = 0
            self._total_tokens = 0
            self._model_calls = 0
            self._cached_calls = 0

    @config_manager.config_defaults(timeout="timeout")
    def _setup_from_config(self, timeout=None):
        """
        Sets up the Gemini API configurations for this client.
        """
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key:
            genai.configure(api_key=api_key)
        self.client = None

    @config_manager.config_defaults(
        model="model",
        temperature="temperature",
        max_completion_tokens="max_completion_tokens",
        frequency_penalty="frequency_penalty",
        presence_penalty="presence_penalty",
        timeout="timeout",
        max_attempts="max_attempts",
        waiting_time="waiting_time",
        exponential_backoff_factor="exponential_backoff_factor",
        response_format=None,
        echo=None,
    )
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
        Sends a message to the OpenAI API and returns the response.

        Args:
        current_messages (list): A list of dictionaries representing the conversation history.
        dedent_messages (bool): Whether to dedent the messages before sending them to the API.
        model (str): The ID of the model to use for generating the response.
        temperature (float): Controls the "creativity" of the response. Higher values result in more diverse responses.
        max_completion_tokens (int): The maximum number of tokens (words or punctuation marks) to generate in the response.
        top_p (float): Controls the "quality" of the response. Higher values result in more coherent responses.
        frequency_penalty (float): Controls the "repetition" of the response. Higher values result in less repetition.
        presence_penalty (float): Controls the "diversity" of the response. Higher values result in more diverse responses.
        stop (str): A string that, if encountered in the generated response, will cause the generation to stop.
        max_attempts (int): The maximum number of attempts to make before giving up on generating a response.
        timeout (int): The maximum number of seconds to wait for a response from the API.
        waiting_time (int): The number of seconds to wait between requests.
        exponential_backoff_factor (int): The factor by which to increase the waiting time between requests.
        n (int): The number of completions to generate.
        response_format: The format of the response, if any.
        echo (bool): Whether to echo the input message in the response.
        enable_pydantic_model_return (bool): Whether to enable Pydantic model return instead of dict when possible.

        Returns:
        A dictionary representing the generated response.
        """

        from tinytroupe.clients import (  # avoid circular import
            InvalidRequestError,
            NonTerminalError,
        )

        def aux_exponential_backoff():
            nonlocal waiting_time

            # in case waiting time was initially set to 0
            if waiting_time <= 0:
                waiting_time = 2

            logger.info(
                f"Request failed. Waiting {waiting_time} seconds between requests..."
            )
            time.sleep(waiting_time)

            # exponential backoff
            waiting_time = waiting_time * exponential_backoff_factor

        # setup the OpenAI configurations for this client.
        self._setup_from_config()

        # dedent the messages (field 'content' only) if needed (using textwrap)
        if dedent_messages:
            for message in current_messages:
                if "content" in message:
                    message["content"] = utils.dedent(message["content"])

        # We need to adapt the parameters to the API type, so we create a dictionary with them first
        chat_api_params = {
            "model": model,
            "messages": current_messages,
            "temperature": temperature,
            "max_completion_tokens": max_completion_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stop": stop,
            "timeout": timeout,
            "stream": False,
            "n": n,
        }

        if response_format is not None:
            chat_api_params["response_format"] = response_format

        # remove any parameter that is None, so we use the API defaults
        chat_api_params = {k: v for k, v in chat_api_params.items() if v is not None}

        i = 0
        while i < max_attempts:
            try:
                i += 1

                try:
                    logger.debug(
                        f"Sending messages to OpenAI API. Token count={self._count_tokens(current_messages, model)}."
                    )
                except NotImplementedError:
                    logger.debug(f"Token count not implemented for model {model}.")

                start_time = time.monotonic()
                logger.debug(
                    f"Calling model with client class {self.__class__.__name__}."
                )

                ###############################################################
                # call the model, either from the cache or from the API
                ###############################################################
                cache_key = str((model, chat_api_params))  # need string to be hashable

                pre_cached_response = self._get_cached_response(cache_key)

                should_wait_before_call = (
                    waiting_time > 0 and pre_cached_response is None
                )

                if should_wait_before_call:
                    logger.info(
                        f"Waiting {waiting_time} seconds before next API request (to avoid throttling)..."
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
                                    # Convert to cacheable format before storing
                                    cacheable_response = self._to_cacheable_format(response)
                                    if cacheable_response is not None:
                                        self.api_cache[cache_key] = cacheable_response
                                        self._save_cache()
                                else:
                                    response = existing

                    raw_message = self._raw_model_response_extractor(response)

                    # Update cost statistics
                    self._update_cost_stats(response, cached_response is not None)

                logger.debug(f"Got response from API: {response}")
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

                # there's no point in retrying if the request is invalid
                # so we return None right away
                return None

            except openai.BadRequestError as e:
                logger.error(f"[{i}] Invalid request error, won't retry: {e}")

                # there's no point in retrying if the request is invalid
                # so we return None right away
                return None

            except openai.RateLimitError:
                logger.warning(
                    f"[{i}] Rate limit error, waiting a bit and trying again."
                )
                aux_exponential_backoff()

            except NonTerminalError as e:
                logger.error(f"[{i}] Non-terminal error: {e}")
                aux_exponential_backoff()

            except APITimeoutError as e:
                logger.error(f"[{i}] API Timeout error: {e}")
                # no exponential timeout backoff here, just retry

            except Exception as e:
                logger.error(f"[{i}] {type(e).__name__} Error: {e}")
                aux_exponential_backoff()

        logger.error(f"Failed to get response after {max_attempts} attempts.")
        return None

    def _raw_model_call(self, model, chat_api_params):
        """
        Calls the Gemini API or Ollama API with the given parameters.
        """
        import google.generativeai as genai
        import ollama

        messages = chat_api_params.get("messages", [])
        
        class MockMessage:
            def __init__(self, content):
                self.content = content
            def to_dict(self):
                return {"role": "assistant", "content": self.content}
        class MockChoice:
            def __init__(self, content):
                self.message = MockMessage(content)
        class MockResponse:
            def __init__(self, content):
                self.choices = [MockChoice(content)]
            def model_dump(self):
                return {"choices": [{"message": {"role": "assistant", "content": self.choices[0].message.content}}]}

        try:
            gemini_messages = []
            for msg in messages:
                role = "user" if msg["role"] in ["user", "system"] else "model"
                gemini_messages.append({"role": role, "parts": [msg["content"]]})
                
            generative_model = genai.GenerativeModel(model)
            response = generative_model.generate_content(gemini_messages)
            if not response.parts:
                raise ValueError("Gemini returned empty parts")
            return MockResponse(response.text)
            
        except Exception as e:
            logger.error(f"Gemini API failed with error: {e}. Falling back to Ollama qwen3:8b.")
            fallback_model = "qwen3:8b"
            ollama_messages = [{"role": m["role"], "content": m["content"]} for m in messages]
            response = ollama.chat(model=fallback_model, messages=ollama_messages)
            content = response.get("message", {}).get("content", "")
            return MockResponse(content)

    def _is_reasoning_model(self, model):
        return "o1" in model or "o3" in model

    def _raw_model_response_extractor(self, response):
        """
        Extracts the response from the API response. Subclasses should
        override this method to implement their own response extraction.
        """
        return response.choices[0].message.to_dict()

    def _to_cacheable_format(self, response):
        """
        Converts an API response to a dictionary format that can be pickled.
        This is necessary because some response types (like ParsedChatCompletion
        with generic types) cannot be pickled directly.
        """
        try:
            # Try model_dump() first (Pydantic v2)
            if hasattr(response, "model_dump"):
                return response.model_dump()
            # Fall back to dict() for older Pydantic models
            elif hasattr(response, "dict"):
                return response.dict()
            # If it's already a dict, return as-is
            elif isinstance(response, dict):
                return response
            else:
                # Last resort: try to convert to dict
                return dict(response)
        except Exception as e:
            logger.warning(f"Could not convert response to cacheable format: {e}")
            # Return None to indicate caching should be skipped
            return None

    def _from_cached_format(self, cached_dict):
        """
        Reconstructs a ChatCompletion object from a cached dictionary.
        """
        class MockMessage:
            def __init__(self, content):
                self.content = content
            def to_dict(self):
                return {"role": "assistant", "content": self.content}
        class MockChoice:
            def __init__(self, content):
                self.message = MockMessage(content)
        class MockResponse:
            def __init__(self, content):
                self.choices = [MockChoice(content)]
            def model_dump(self):
                return {"choices": [{"message": {"role": "assistant", "content": self.choices[0].message.content}}]}

        try:
            if "choices" in cached_dict and len(cached_dict["choices"]) > 0:
                return MockResponse(cached_dict["choices"][0]["message"]["content"])
        except Exception as e:
            logger.warning(f"Could not reconstruct response from cache: {e}")
        return None

    def _get_cached_response(self, cache_key):
        if not self.cache_api_calls:
            return None

        cache_store = getattr(self, "api_cache", None)
        if cache_store is None:
            return None

        with self._cache_lock:
            cached_dict = cache_store.get(cache_key)
            if cached_dict is None:
                return None
            # Reconstruct the ChatCompletion object from the cached dict
            return self._from_cached_format(cached_dict)

    @contextmanager
    def _concurrency_slot(self):
        if self._concurrency_semaphore is None:
            yield
            return

        self._concurrency_semaphore.acquire()
        try:
            yield
        finally:
            self._concurrency_semaphore.release()

    def _count_tokens(self, messages: list, model: str):
        """
        Count the number of OpenAI tokens in a list of messages using tiktoken.

        Adapted from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

        Args:
        messages (list): A list of dictionaries representing the conversation history.
        model (str): The name of the model to use for encoding the string.
        """
        try:
            try:
                encoding = tiktoken.encoding_for_model(model)
            except KeyError:
                logger.debug(
                    "Token count: model not found. Using cl100k_base encoding."
                )
                encoding = tiktoken.get_encoding("cl100k_base")

            if (
                model
                in {
                    "gpt-3.5-turbo-0613",
                    "gpt-3.5-turbo-16k-0613",
                    "gpt-4-0314",
                    "gpt-4-32k-0314",
                    "gpt-4-0613",
                    "gpt-4-32k-0613",
                }
                or "o1" in model
                or "o3" in model
            ):  # assuming o1/3 models work the same way
                tokens_per_message = 3
                tokens_per_name = 1
            elif model == "gpt-3.5-turbo-0301":
                tokens_per_message = (
                    4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
                )
                tokens_per_name = -1  # if there's a name, the role is omitted
            elif "gpt-3.5-turbo" in model:
                logger.debug(
                    "Token count: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
                )
                return self._count_tokens(messages, model="gpt-3.5-turbo-0613")
            elif ("gpt-4" in model) or ("ppo" in model):
                logger.debug(
                    "Token count: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
                )
                return self._count_tokens(messages, model="gpt-4-0613")
            elif "gpt-5" in model:
                logger.debug(
                    "Token count: no info on GPT-5 tokenizer yet, so we are just reusing GPT-4's."
                )
                return self._count_tokens(messages, model="gpt-4-0613")
            else:
                raise NotImplementedError(
                    f"""_count_tokens() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
                )

            num_tokens = 0
            for message in messages:
                num_tokens += tokens_per_message
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":
                        num_tokens += tokens_per_name
            num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
            return num_tokens

        except Exception as e:
            logger.error(f"Error counting tokens: {e}")
            return None

    def _save_cache(self):
        """
        Saves the API cache to disk. We use pickle to do that because some obj
        are not JSON serializable.
        """
        # use pickle to save the cache
        with open(self.cache_file_name, "wb") as f:
            pickle.dump(self.api_cache, f)

    def _load_cache(self):
        """
        Loads the API cache from disk.
        """
        if os.path.exists(self.cache_file_name):
            try:
                with open(self.cache_file_name, "rb") as f:
                    return pickle.load(f)
            except (EOFError, pickle.UnpicklingError) as e:
                logger.warning(f"Cache file exists but could not be loaded: {e}. Starting with empty cache.")
                return {}
        return {}

    @config_manager.config_defaults(model="embedding_model")
    def get_embedding(self, text, model=None):
        """
        Gets the embedding of the given text using the specified model.

        Args:
        text (str): The text to embed.
        model (str): The name of the model to use for embedding the text.

        Returns:
        The embedding of the text.
        """
        response = self._raw_embedding_model_call(text, model)
        return self._raw_embedding_model_response_extractor(response)

    def _raw_embedding_model_call(self, text, model):
        """
        Calls the Gemini API to get the embedding of the given text.
        """
        import google.generativeai as genai
        result = genai.embed_content(
            model=model,
            content=text,
            task_type="retrieval_document",
        )
        
        class MockEmbeddingData:
            def __init__(self, embedding):
                self.embedding = embedding
        class MockEmbeddingResponse:
            def __init__(self, embedding):
                self.data = [MockEmbeddingData(embedding)]
                
        return MockEmbeddingResponse(result['embedding'])

    def _raw_embedding_model_response_extractor(self, response):
        """
        Extracts the embedding from the API response. Subclasses should
        override this method to implement their own response extraction.
        """
        return response.data[0].embedding

    def _update_cost_stats(self, response, was_cached):
        """
        Updates the cost statistics based on the API response.

        Args:
            response: The response object from the API.
            was_cached (bool): Whether this response came from cache.
        """
        with self._cost_stats_lock:
            if was_cached:
                self._cached_calls += 1
            else:
                self._model_calls += 1

            # Extract token usage from response if available
            if hasattr(response, "usage") and response.usage is not None:
                usage = response.usage
                if hasattr(usage, "prompt_tokens") and usage.prompt_tokens is not None:
                    self._input_tokens += usage.prompt_tokens
                if hasattr(usage, "completion_tokens") and usage.completion_tokens is not None:
                    self._output_tokens += usage.completion_tokens
                if hasattr(usage, "total_tokens") and usage.total_tokens is not None:
                    self._total_tokens += usage.total_tokens

                # Log the latest values in debug mode
                logger.debug(
                    f"Cost stats updated - Input tokens: {usage.prompt_tokens if hasattr(usage, 'prompt_tokens') else 0}, "
                    f"Output tokens: {usage.completion_tokens if hasattr(usage, 'completion_tokens') else 0}, "
                    f"Total tokens: {usage.total_tokens if hasattr(usage, 'total_tokens') else 0}, "
                    f"Cached: {was_cached}"
                )

    def get_cost_stats(self):
        """
        Returns the current cost statistics.

        Returns:
            dict: A dictionary containing cost statistics with keys:
                - input_tokens: Number of input/prompt tokens used
                - output_tokens: Number of output/completion tokens used
                - total_tokens: Total number of tokens used
                - model_calls: Number of actual API calls made
                - cached_calls: Number of calls served from cache
        """
        with self._cost_stats_lock:
            return {
                "input_tokens": self._input_tokens,
                "output_tokens": self._output_tokens,
                "total_tokens": self._total_tokens,
                "model_calls": self._model_calls,
                "cached_calls": self._cached_calls,
            }

    def pretty_print_cost_stats(self):
        """
        Pretty prints the cost statistics to the console.
        """
        stats = self.get_cost_stats()
        print("\n" + "=" * 60)
        print("LLM API COST STATISTICS")
        print("=" * 60)
        print(f"Input tokens:         {stats['input_tokens']:,}")
        print(f"Output tokens:        {stats['output_tokens']:,}")
        print(f"Total tokens:         {stats['total_tokens']:,}")
        print(f"Model API calls:      {stats['model_calls']:,}")
        print(f"Cached calls:         {stats['cached_calls']:,}")
        print(f"Total calls:          {stats['model_calls'] + stats['cached_calls']:,}")
        if stats["model_calls"] > 0:
            print(
                f"Avg tokens per call:  {stats['total_tokens'] / stats['model_calls']:.1f}"
            )
        print("=" * 60 + "\n")

    def reset_cost_stats(self):
        """
        Resets the cost statistics. This is the public method that users should call.
        """
        self._reset_cost_stats()
        logger.info("Cost statistics have been reset.")
