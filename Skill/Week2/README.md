# Week 2 – LLM-Based Interactive Application

## Aim
To develop an interactive Python application that uses a Large Language Model (LLM) to answer user questions and generate responses.

## Objectives
- Integrate an LLM with a Python application.
- Support provider selection between Gemini and Ollama.
- Accept questions from the user through the terminal.
- Generate AI responses to user prompts.
- Understand how LLMs can generate explanations and programming code.

## Technologies Used
- Python
- Ollama
- Llama 3.2
- Gemini API (provider option)
- Requests
- VS Code

## Output

The program allows the user to select an LLM provider, enter a question, and receive a generated response.

### Sample Input
```text
Choose provider (gemini/ollama): ollama

Enter your question:
Give simple Python code for addition of 2 numbers
```

### Sample Output
```text
LLM Response:

Here is a simple Python function that takes two numbers
as input and returns their sum:

def add_numbers(num1, num2):
    return num1 + num2

# Example usage:
print(add_numbers(5, 7))  # Output: 12
```

The LLM also provides an explanation of the generated code.

## Results
The Python application successfully connected to the Ollama provider and generated a response for the user's prompt. It produced Python code for adding two numbers along with an explanation.

## Conclusion
The experiment demonstrated the integration of a locally running Large Language Model with a Python application. It helped understand how users can interact with an LLM through prompts and receive generated text, explanations, and programming code.
