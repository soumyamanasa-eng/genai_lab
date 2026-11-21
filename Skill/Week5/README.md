# Week 5 – Token Economics and Budget Estimator

## Aim
To estimate LLM usage costs and evaluate token usage, API rate limits, and budget constraints.

## Objectives
- Calculate daily and monthly token consumption.
- Estimate API input and output costs.
- Check daily and monthly budget limits.
- Estimate peak requests per minute and tokens per minute.
- Apply a safety margin to cost calculations.
- Test the budget calculator using unit tests.

## Technologies Used
- Python
- `dataclasses`
- `python-dotenv`
- Unit Testing (`unittest`)
- VS Code

## Output

The program calculates daily and monthly usage costs, token consumption, rate limits, and budget status.

### Budget Report

| Metric | Result |
|---|---:|
| Input tokens/day | 2,400,000 |
| Output tokens/day | 600,000 |
| Total tokens/day | 3,000,000 |
| Daily cost | $1.44 |
| Monthly cost | $43.20 |
| Daily cost with safety margin | $1.728 |
| Monthly cost with safety margin | $51.84 |
| Peak RPM with margin | 36 |
| Peak TPM with margin | 54,000 |

### Budget Checks
- Daily budget ($2): PASS
- Monthly budget ($50): REVIEW
- RPM limit (60): PASS
- TPM limit (100,000): PASS

### Unit Test Output

```text
test_budget_exceeded ... ok
test_rate_limits_exceeded ... ok
test_rate_limits_within_capacity ... ok
test_token_and_cost_calculation ... ok
test_zero_traffic ... ok

Ran 5 tests

OK
```

## Results
All five unit tests passed successfully. The estimated daily cost remained within the daily budget, but the monthly cost with the safety margin exceeded the monthly budget. The rate limits remained within the configured limits.

## Conclusion
The experiment demonstrated how token usage, API pricing, rate limits, and safety margins can be used to estimate LLM costs and determine whether a planned usage pattern fits within a defined budget.
