
import os
import time
from datetime import datetime, timezone

from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()


class UsageLogger:

    def __init__(self):
        mongodb_uri = os.getenv("MONGODB_URI")

        if not mongodb_uri:
            raise ValueError("MONGODB_URI is missing in .env file")

        self.client = MongoClient(
            mongodb_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=10000,
            retryWrites=True
        )

        # Test MongoDB connection
        self.client.admin.command("ping")

        self.db = self.client["llm_monitoring"]
        self.collection = self.db["api_usage"]

        print("MongoDB connected successfully!")

    def log_call(self, record):

        record["timestamp"] = datetime.now(timezone.utc)

        # Try inserting the record up to 3 times
        for attempt in range(3):
            try:
                self.collection.insert_one(record)
                print("Usage record saved successfully!")
                return True

            except Exception as error:
                print(f"Logging attempt {attempt + 1} failed: {error}")

                if attempt < 2:
                    time.sleep(2 ** attempt)

        print("Failed to save usage record.")
        return False

    def close(self):
        self.client.close()
        print("MongoDB connection closed.")
