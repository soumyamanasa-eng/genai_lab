
import os
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod

import requests
from google import genai
from google.genai import types


@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int


class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt):
        pass


class GeminiProvider(LLMProvider):

    def __init__(self, api_key):
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=60000)
        )
        self.model = "gemini-3.8-flash"

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        usage = response.usage_metadata

        input_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0

        return LLMResult(
            text=response.text,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )


class OllamaProvider(LLMProvider):

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=(5, 60)
        )

        response.raise_for_status()
        data = response.json()

        return LLMResult(
            text=data.get("response", ""),
            input_tokens=data.get("prompt_eval_count", 0),
            output_tokens=data.get("eval_count", 0)
        )



class LLMClient:

    def __init__(self, provider, logger, provider_name):
        self.provider = provider
        self.logger = logger
        self.provider_name = provider_name

        self.max_retries = 3

        self.input_price = float(
            os.getenv("GEMINI_INPUT_PRICE_PER_MILLION", "0")
        )

        self.output_price = float(
            os.getenv("GEMINI_OUTPUT_PRICE_PER_MILLION", "0")
        )

    def is_temporary_error(self, error):

        if isinstance(error, (requests.Timeout, requests.ConnectionError)):
            return True

        if isinstance(error, requests.HTTPError):
            if error.response is not None:
                return error.response.status_code in [
                    408, 429, 500, 502, 503, 504
                ]

        error_code = getattr(error, "code", None)

        if error_code in [408, 429, 500, 502, 503, 504]:
            return True

        error_name = type(error).__name__.lower()

        temporary_names = [
            "timeout",
            "unavailable",
            "resourceexhausted",
            "internalservererror",
            "servererror"
        ]

        return any(name in error_name for name in temporary_names)

    def generate(self, prompt):

        for attempt in range(self.max_retries):

            start_time = time.time()

            try:
                result = self.provider.generate(prompt)

                latency = round(
                    (time.time() - start_time) * 1000, 2
                )

                total_tokens = (
                    result.input_tokens + result.output_tokens
                )

                if self.provider_name == "gemini":
                    cost = (
                        result.input_tokens * self.input_price
                        + result.output_tokens * self.output_price
                    ) / 1_000_000
                else:
                    cost = 0.0

                record = {
                    "provider": self.provider_name,
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "total_tokens": total_tokens,
                    "latency_ms": latency,
                    "estimated_cost": cost,
                    "status": "success",
                    "error": None
                }

                self.logger.log_call(record)

                return result.text

            except Exception as error:

                latency = round(
                    (time.time() - start_time) * 1000, 2
                )

                record = {
                    "provider": self.provider_name,
                    "input_tokens": None,
                    "output_tokens": None,
                    "total_tokens": None,
                    "latency_ms": latency,
                    "estimated_cost": None,
                    "status": "failed",
                    "error": str(error)
                }

                self.logger.log_call(record)

                if (
                    attempt < self.max_retries - 1
                    and self.is_temporary_error(error)
                ):
                    wait_time = 2 ** attempt
                    print(
                        f"Temporary error. Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    raise
