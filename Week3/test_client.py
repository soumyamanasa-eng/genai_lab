
import unittest

from llm_client import LLMClient, LLMResult


class FakeProvider:

    def generate(self, prompt):
        return LLMResult(
            text="This is a test response.",
            input_tokens=8,
            output_tokens=5
        )


class FakeLogger:

    def __init__(self):
        self.records = []

    def log_call(self, record):
        self.records.append(record)
        return True


class TestLLMClient(unittest.TestCase):

    def test_successful_generation(self):

        provider = FakeProvider()
        logger = FakeLogger()

        client = LLMClient(
            provider=provider,
            logger=logger,
            provider_name="gemini"
        )

        response = client.generate("Hello")

        # Check generated response
        self.assertEqual(
            response,
            "This is a test response."
        )

        # Check MongoDB logging data
        self.assertEqual(len(logger.records), 1)

        record = logger.records[0]

        self.assertEqual(record["input_tokens"], 8)
        self.assertEqual(record["output_tokens"], 5)
        self.assertEqual(record["total_tokens"], 13)
        self.assertEqual(record["status"], "success")


if __name__ == "__main__":
    unittest.main()
