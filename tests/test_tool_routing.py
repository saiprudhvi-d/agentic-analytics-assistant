import pytest
from src.tools.calculator import calculate, extract_expression
from src.agents.orchestrator import classify_intent, run_agent

class TestCalculator:
    def test_addition(self):
        r = calculate("What is 250 + 750?")
        assert r.success and "1,000" in r.output
    def test_percentage(self):
        r = calculate("What is 15% of 84500?")
        assert r.success and "12,675" in r.output
    def test_multiplication(self):
        r = calculate("250 * 12")
        assert r.success and "3,000" in r.output
    def test_division(self):
        r = calculate("100 / 4")
        assert r.success and "25" in r.output
    def test_division_by_zero(self):
        r = calculate("100 / 0")
        assert not r.success
    def test_extract_pct(self):
        e = extract_expression("What is 20% of 5000?")
        assert "20" in e and "5000" in e

class TestIntentClassification:
    def test_calc_arithmetic(self):
        assert classify_intent("What is 250 + 750?")[0] == "calculation"
    def test_calc_percentage(self):
        assert classify_intent("What is 15% of 84500?")[0] == "calculation"
    def test_data_revenue(self):
        assert classify_intent("What was the total revenue in Q3?")[0] == "data_query"
    def test_data_average(self):
        assert classify_intent("What is the average sales per month?")[0] == "data_query"
    def test_summarize(self):
        assert classify_intent("Summarize the key trends")[0] == "summarize"

class TestAgentRouting:
    def test_routes_calc(self):
        r = run_agent("What is 500 * 24?")
        assert r.tool_used == "calculator" and r.success
    def test_routes_percentage(self):
        r = run_agent("Calculate 10% of 50000")
        assert r.tool_used == "calculator" and "5,000" in r.answer
    def test_empty_fails(self):
        r = run_agent("")
        assert not r.success and r.tool_used == "none"
