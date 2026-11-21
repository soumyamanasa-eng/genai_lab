import json
import csv
import time
import requests

from evaluator import evaluate_response

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def ask_ollama(question):
    payload = {
        "model": MODEL,
        "prompt": question,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()["response"]


def main():
    with open("golden_set.json", "r", encoding="utf-8") as file:
        golden_set = json.load(file)

    results = []

    print("=" * 60)
    print("LLM EVALUATION - LLAMA 3.2")
    print("=" * 60)

    for item in golden_set:
        question = item["question"]
        expected_keywords = item["expected_keywords"]

        print(f"\nQuestion {item['id']}: {question}")

        try:
            answer = ask_ollama(question)
            evaluation = evaluate_response(answer, expected_keywords)

            print("Answer:", answer)
            print("Score:", evaluation["score"], "%")
            print("Status:", evaluation["status"])

            results.append({
                "id": item["id"],
                "question": question,
                "answer": answer,
                "expected_keywords": ", ".join(expected_keywords),
                "matched_keywords": ", ".join(evaluation["matched_keywords"]),
                "score": evaluation["score"],
                "status": evaluation["status"]
            })

            time.sleep(1)

        except Exception as error:
            print("Error:", error)

            results.append({
                "id": item["id"],
                "question": question,
                "answer": "ERROR: " + str(error),
                "expected_keywords": ", ".join(expected_keywords),
                "matched_keywords": "",
                "score": 0,
                "status": "ERROR"
            })

    with open("results.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "id",
            "question",
            "answer",
            "expected_keywords",
            "matched_keywords",
            "score",
            "status"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    passed = sum(1 for item in results if item["status"] == "PASS")
    reviewed = sum(1 for item in results if item["status"] == "REVIEW")
    errors = sum(1 for item in results if item["status"] == "ERROR")

    print("\n" + "=" * 60)
    print("FINAL EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total Questions : {len(results)}")
    print(f"PASS           : {passed}")
    print(f"REVIEW         : {reviewed}")
    print(f"ERROR          : {errors}")
    print(f"Average Score  : {sum(item['score'] for item in results) / len(results):.2f}%")
    print("\nResults saved to results.csv")


if __name__ == "__main__":
    main()