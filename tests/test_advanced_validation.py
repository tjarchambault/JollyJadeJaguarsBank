# PROGRAM: Personal Finance Tracker - test_advanced_validation.py
# PURPOSE: Verify report validation and error recovery behavior.
# INPUT: Valid and invalid sample values and simulated retry responses.
# PROCESS: Call validators and compare results or errors with expectations.
# OUTPUT: Pytest results identifying passing and failing checks.
# HONOR CODE: On my honor, as an Aggie, I have neither given nor
#             received unauthorized aid on this academic work.

"""Behavioral tests for report validation and error recovery."""

from datetime import date, datetime
from decimal import Decimal

import pytest

from src import Advanced_Validation as validation


@pytest.mark.parametrize(
    "value",
    [
        "2025-02-29",
        "2026-04-31",
        "2026-2-01",
        "09/22/2026",
        "",
        None,
        20260922,
        datetime(2026, 9, 22),
    ],
)
def test_invalid_dates(value):
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validation.validate_date_format(value)


def test_leap_day_and_date_objects():
    leap_day = date(2024, 2, 29)
    assert validation.validate_date_format("2024-02-29") == leap_day
    assert validation.validate_date_format(leap_day) == leap_day
    assert validation.validate_report_date_range(leap_day, leap_day) == (
        leap_day,
        leap_day,
    )
    assert validation.validate_report_date_range(
        "2025-12-31", "2026-01-01"
    ) == (date(2025, 12, 31), date(2026, 1, 1))


def test_date_bounds_are_inclusive():
    for day in ("2026-01-01", "2026-12-31"):
        assert validation.check_date_boundaries(day, "2026-01-01", "2026-12-31")
    with pytest.raises(ValueError):
        validation.check_date_boundaries("2025-12-31", "2026-01-01")
    with pytest.raises(ValueError):
        validation.check_date_boundaries("2027-01-01", max_date="2026-12-31")
    with pytest.raises(ValueError):
        validation.check_date_boundaries(
            "2026-06-01", "2026-12-31", "2026-01-01"
        )
    with pytest.raises(ValueError):
        validation.validate_report_date_range("2026-09-22", "2026-09-21")


def test_choices_and_category_spelling():
    assert validation.validate_report_type(" MONTHLY ") == "monthly"
    assert validation.validate_time_period("Weekly") == "weekly"
    assert (
        validation.validate_category_filter(" food ", ["Food", "Salary"])
        == "Food"
    )
    assert validation.validate_category_filter(None, []) is None
    assert validation.validate_export_format("CSV") == "csv"
    assert validation.validate_export_format("txt") == "text"
    assert validation.validate_menu_selection(6) == "6"
    assert validation.validate_menu_selection(" q ", ["q", "r"]) == "q"


@pytest.mark.parametrize(
    "validator,value",
    [
        (validation.validate_report_type, "unknown"),
        (validation.validate_time_period, None),
        (validation.validate_export_format, "pdf"),
        (validation.validate_menu_selection, 7),
        (validation.validate_menu_selection, True),
        (validation.validate_menu_selection, 1.0),
        (validation.validate_menu_selection, ""),
    ],
)
def test_invalid_choices(validator, value):
    with pytest.raises(ValueError):
        validator(value)


def test_unknown_and_empty_categories():
    with pytest.raises(ValueError, match="Did you mean 'Food'"):
        validation.validate_category_filter("Fod", ["Food", "Salary"])
    for category, catalog in [("Food", []), ("", ["Food"])]:
        with pytest.raises(ValueError):
            validation.validate_category_filter(category, catalog)


@pytest.mark.parametrize(
    "value",
    [
        True,
        None,
        "abc",
        "",
        "NaN",
        "sNaN",
        "Infinity",
        float("inf"),
        float("nan"),
        [],
        Decimal("-Infinity"),
    ],
)
def test_invalid_numbers(value):
    with pytest.raises(ValueError):
        validation.validate_numeric_range(value)


def test_numeric_precision_and_limits():
    assert validation.validate_numeric_range(
        "0.12345678901234567890123456789"
    ) == Decimal("0.12345678901234567890123456789")
    assert validation.validate_numeric_range("10.00", 0, 10) == Decimal("10.00")
    assert validation.validate_numeric_range(-2, -2, 0) == Decimal(-2)
    assert validation.validate_threshold_input("0") == Decimal(0)
    for value, lower, upper in [
        (11, 0, 10),
        (-1, 0, 10),
        (5, 10, 0),
        (5, "NaN", 10),
    ]:
        with pytest.raises(ValueError):
            validation.validate_numeric_range(value, lower, upper)
    with pytest.raises(ValueError):
        validation.validate_threshold_input("-0.01")


def test_filters_normalize_without_mutating_input():
    original = {
        "start_date": "2026-09-01",
        "end_date": "2026-09-22",
        "category": "food",
        "min_amount": "1.25",
        "max_amount": "20",
        "transaction_type": "Expense",
        "time_period": "Custom",
    }
    snapshot = original.copy()
    result = validation.validate_filter_options(original, ["Food"])
    assert original == snapshot
    assert result == {
        "start_date": date(2026, 9, 1),
        "end_date": date(2026, 9, 22),
        "category": "Food",
        "min_amount": Decimal("1.25"),
        "max_amount": Decimal("20"),
        "transaction_type": "expense",
        "time_period": "custom",
    }
    assert validation.validate_filter_options(None) == {}
    assert validation.validate_filter_options({}) == {}


@pytest.mark.parametrize(
    "options",
    [
        [],
        {"unexpected": "value"},
        {"start_date": "2026-09-01"},
        {"end_date": "2026-09-01"},
        {"min_amount": 20, "max_amount": 10},
        {"min_amount": -1},
        {"max_amount": None},
        {"transaction_type": "refund"},
        {"time_period": "custom"},
        {
            "start_date": "2026-09-01",
            "end_date": "2026-09-22",
            "time_period": "weekly",
        },
    ],
)
def test_invalid_filter_combinations(options):
    with pytest.raises(ValueError):
        validation.validate_filter_options(options)


@pytest.mark.parametrize(
    "answer,expected",
    [(" YES ", True), ("y", True), ("n", False), ("No", False)],
)
def test_retry_answers(answer, expected):
    assert validation.prompt_retry(input_func=lambda prompt: answer) is expected


def test_retry_reprompts():
    answers = iter(["maybe", "", "yes"])
    messages = []
    assert validation.prompt_retry(
        input_func=lambda prompt: next(answers), output_func=messages.append
    )
    assert len(messages) == 2
    assert all("y/yes" in message for message in messages)


@pytest.mark.parametrize("exception", [EOFError, KeyboardInterrupt])
def test_retry_cancellation(exception):
    def interrupted_input(prompt):
        raise exception

    assert validation.prompt_retry(input_func=interrupted_input) is False


def test_help_errors_and_suggestions():
    assert "YYYY-MM-DD" in validation.provide_help_text("DATES")
    assert "csv" in validation.provide_help_text()
    with pytest.raises(ValueError, match="help topic"):
        validation.provide_help_text("unknown")
    message = validation.generate_validation_error_message(
        "amount", "abc", "Enter a number."
    )
    assert (
        "amount" in message
        and "abc" in message
        and "Enter a number." in message
    )
    assert (
        validation.suggest_correction("montly", ["daily", "monthly"])
        == "monthly"
    )
    assert validation.suggest_correction(" FOOD ", ["Food"]) == "Food"
    assert validation.suggest_correction("zzzz", ["Food"]) is None
    assert validation.suggest_correction(None, ["Food"]) is None
    assert validation.suggest_correction("Food", []) is None
