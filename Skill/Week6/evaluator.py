def evaluate_response(response, expected_keywords):
    response = response.lower()

    matched_keywords = [
        keyword for keyword in expected_keywords
        if keyword.lower() in response
    ]

    score = len(matched_keywords) / len(expected_keywords) * 100

    if score >= 50:
        status = "PASS"
    else:
        status = "REVIEW"

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords,
        "status": status
    }


if __name__ == "__main__":
    response = "Artificial intelligence enables machines to perform tasks requiring intelligence."
    keywords = ["machines", "intelligence"]

    result = evaluate_response(response, keywords)
    print(result)