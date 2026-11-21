
import unittest
from budget import FeatureBudget


class TestFeatureBudget(unittest.TestCase):

    def setUp(self):
        self.budget = FeatureBudget(
            requests_per_day=2000,
            avg_input_tokens=1200,
            avg_output_tokens=300,
            peak_requests_per_minute=30,
            input_price_per_million=0.30,
            output_price_per_million=1.20,
            rpm_limit=60,
            tpm_limit=100000,
            monthly_budget_usd=50,
            daily_budget_usd=2,
            safety_margin_percent=20,
        )

    def test_token_and_cost_calculation(self):
        result = self.budget.calculate()

        self.assertEqual(result["input_tokens_day"], 2400000)
        self.assertEqual(result["output_tokens_day"], 600000)
        self.assertEqual(result["total_tokens_day"], 3000000)

        self.assertAlmostEqual(result["daily_cost_usd"], 1.44)
        self.assertAlmostEqual(result["monthly_cost_usd"], 43.20)

    def test_budget_exceeded(self):
        budget = FeatureBudget(
            requests_per_day=10000,
            avg_input_tokens=1200,
            avg_output_tokens=300,
            peak_requests_per_minute=30,
            input_price_per_million=0.30,
            output_price_per_million=1.20,
            rpm_limit=60,
            tpm_limit=100000,
            monthly_budget_usd=10,
            daily_budget_usd=0.50,
            safety_margin_percent=20,
        )

        result = budget.calculate()

        self.assertFalse(result["daily_budget_ok"])
        self.assertFalse(result["monthly_budget_ok"])

    def test_rate_limits_within_capacity(self):
        result = self.budget.calculate()

        self.assertTrue(result["rpm_ok"])
        self.assertTrue(result["tpm_ok"])

    def test_rate_limits_exceeded(self):
        budget = FeatureBudget(
            requests_per_day=2000,
            avg_input_tokens=1200,
            avg_output_tokens=300,
            peak_requests_per_minute=100,
            input_price_per_million=0.30,
            output_price_per_million=1.20,
            rpm_limit=60,
            tpm_limit=100000,
            monthly_budget_usd=50,
            daily_budget_usd=2,
            safety_margin_percent=20,
        )

        result = budget.calculate()

        self.assertFalse(result["rpm_ok"])
        self.assertFalse(result["tpm_ok"])

    def test_zero_traffic(self):
        budget = FeatureBudget(
            requests_per_day=0,
            avg_input_tokens=1200,
            avg_output_tokens=300,
            peak_requests_per_minute=0,
            input_price_per_million=0.30,
            output_price_per_million=1.20,
            rpm_limit=60,
            tpm_limit=100000,
            monthly_budget_usd=50,
            daily_budget_usd=2,
            safety_margin_percent=20,
        )

        result = budget.calculate()

        self.assertEqual(result["total_tokens_day"], 0)
        self.assertEqual(result["daily_cost_usd"], 0)
        self.assertEqual(result["monthly_cost_usd"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
