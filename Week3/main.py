import os
from dotenv import load_dotenv

from usage_logger import UsageLogger
from llm_client import (
    LLMClient,
    GeminiProvider,
    OllamaProvider
)


def main():
    load_dotenv(override=True)

    logger = UsageLogger()

    try:
        provider_name = input(
            "Choose provider (gemini/ollama): "
        ).strip().lower()

        if provider_name == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                raise ValueError("GEMINI_API_KEY is missing in .env")

            provider = GeminiProvider(api_key)

        elif provider_name == "ollama":
            provider = OllamaProvider(model="llama3.2")

        else:
            raise ValueError("Choose gemini or ollama")

        client = LLMClient(
            provider=provider,
            logger=logger,
            provider_name=provider_name
        )

        prompt = input("Enter your question: ")

        print("\nGenerating response...\n")

        answer = client.generate(prompt)

        print("\nLLM Response:\n")
        print(answer)

    except Exception as error:
        print("\nError:", error)

    finally:
        logger.close()


if __name__ == "__main__":
    main()