# Week 6 – LLM Evaluation using Ollama

## Aim
To evaluate the performance of Llama 3.2 using a Golden Dataset of 30 questions and keyword-based evaluation.

## Objectives
- Run a Large Language Model locally using Ollama.
- Create a Golden Dataset containing 30 questions.
- Generate answers using Llama 3.2.
- Evaluate answers based on expected keywords.
- Calculate scores and classify responses as PASS or REVIEW.
- Store evaluation results in a CSV file.

## Technologies Used
- Python 3.12
- Ollama
- Llama 3.2
- Requests
- JSON
- CSV
- Visual Studio Code

## Output
The program generates answers for the 30 questions, checks the answers against expected keywords, calculates scores, and assigns PASS or REVIEW status.

### Terminal Output

```text
LLM EVALUATION - LLAMA 3.2

Question 1: What is Artificial Intelligence?
Answer: [Generated response]
Score: [Score]%
Status: [PASS/REVIEW]

...

FINAL EVALUATION SUMMARY

Total Questions : 30
PASS           : [Actual count]
REVIEW         : [Actual count]
ERROR          : [Actual count]
Average Score  : [Actual score]%

Results saved to results.csv
```

## Results
The Llama 3.2 model was evaluated using 30 predefined questions. The generated responses were checked using keyword matching. The results were stored in `results.csv`, including generated answers, matched keywords, scores, and evaluation status.

## Conclusion
The experiment demonstrated the evaluation of a locally running Large Language Model using Ollama. The model's responses were assessed against expected keywords, and the evaluation results were recorded for analysis.
