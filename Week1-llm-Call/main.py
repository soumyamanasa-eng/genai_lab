
import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send prompt to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="What is Artificial Intelligence? Explain in simple words."
)

# Display response
print("\nLLM Response:")
print(response.text)
