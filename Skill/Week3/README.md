# Week 3 – Gemini API Monitoring with MongoDB and Retry Handling

## Aim
To develop a Python application that integrates the Gemini API with MongoDB to generate AI responses, record API usage, and handle temporary errors using retry mechanisms.

## Objectives
- Connect Python to MongoDB.
- Integrate the Gemini API.
- Allow users to enter questions through the terminal.
- Generate responses using Gemini.
- Store API usage records in MongoDB.
- Implement retry handling for temporary errors.
- Close the database connection after execution.

## Technologies Used
- Python
- Google Gemini API
- MongoDB
- PyMongo
- VS Code
- Google Gen AI SDK

## Output

The application successfully connects to MongoDB, accepts a user question, generates an AI response using Gemini, and saves API usage records.

### Sample Input

```text
MongoDB connected successfully!

Choose provider (gemini/ollama): gemini

Enter your question:
What is machine learning? Explain shortly
```

### Sample Output

```text
Generating response...

Usage record saved successfully!
Temporary error. Retrying in 1 seconds...
Usage record saved successfully!
Temporary error. Retrying in 2 seconds...
Usage record saved successfully!

LLM Response:

Machine Learning (ML) is a branch of Artificial
Intelligence (AI) where computers learn from data
to make decisions or predictions, rather than
following strictly pre-written rules.

Common examples: Spam filters, Netflix recommendations,
and facial recognition.

MongoDB connection closed.
```

## Results
The application successfully connected to MongoDB and generated a response using Gemini. API usage records were saved successfully, and the retry mechanism handled temporary errors by retrying requests. The database connection was closed at the end of execution.

## Conclusion
The experiment demonstrated the integration of Gemini API with MongoDB for AI response generation and usage logging. It also demonstrated retry handling for temporary failures and proper database connection management.
