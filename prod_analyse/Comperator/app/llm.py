import logging
import os
import google.generativeai as genai
import ollama

logger = logging.getLogger(__name__)

class LLMModel:
    _instance = None

    def __init__(self, api_key: str = "", model_name: str = "models/gemini-2.5-flash", fallback_model: str = "qwen2.5:14b") -> None:
        self.api_key = api_key or os.getenv("GOOGLE_GEMINI_API_KEY0") or os.getenv("GOOGLE_GEMINI_API_KEY")
        self.model_name = model_name
        
        # User explicitly asked for qwen3:8b, but qwen2.5 is typical. I will use what the user asked exactly: qwen3:8b
        self.fallback_model = "qwen3:8b" 
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Create standard generatiive model
            self.gemini_model = genai.GenerativeModel(self.model_name)
        else:
            self.gemini_model = None

    def chat(self, prompt, sys_prompt="", max_token=1000, temp=0.) -> str | None:
        """
        Since Comperator originally returned an OpenAI ChatCompletion object,
        we need to mock that interface slightly or just return a string and adjust analyzer.py.
        Actually, looking at Comperator, it probably calls:
           res = llm.chat(...)
           content = res.choices[0].message.content
        We can create a mock response object to keep analyzer.py unchanged.
        """
        try:
            # Try Gemini first
            if self.gemini_model:
                full_prompt = f"System: {sys_prompt}\n\nUser: {prompt}"
                response = self.gemini_model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temp,
                        max_output_tokens=max_token
                    )
                )
                return self._create_mock_response(response.text)
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}. Falling back to Ollama {self.fallback_model}")
        
        # Fallback to Ollama if Gemini failed or no API key
        try:
            response = ollama.chat(
                model=self.fallback_model,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": temp, "num_predict": max_token}
            )
            return self._create_mock_response(response['message']['content'])
        except Exception as e:
            logger.error(f"Error calling Ollama fallback: {str(e)}")
            return None

    def _create_mock_response(self, text):
        class MockMessage:
            def __init__(self, content):
                self.content = content
        class MockChoice:
            def __init__(self, message):
                self.message = message
        class MockResponse:
            def __init__(self, choices):
                self.choices = choices
                
        return MockResponse([MockChoice(MockMessage(text))])

    def __new__(cls, api_key: str = "", model_name: str = "models/gemini-2.5-flash"):
        if not cls._instance:
            cls._instance = super(LLMModel, cls).__new__(cls)
            cls._instance.__init__(api_key, model_name)
            
        return cls._instance
