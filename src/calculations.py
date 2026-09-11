```python
"""Calculate basic financial totals."""

# Program: Personal Finance Tracker - calculations.py
# Purpose: Calculate income, expenses, and net savings.
# Inputs: Transaction records.
# Process: Group and total transaction amounts.
# Outputs: Financial totals.
# Honor Code: On my honor, as an Aggie, I have neither given nor received unauthorized aid on this academic work.


def total_income(transactions):
    """Calculate the total amount of income transactions."""
    if not transactions:
        return 0.00

    return sum(
        float(transaction[4])
        for transaction in transactions
        if transaction[5].lower() == "income"
    )


def total_expenses(transactions):
    """Calculate the total amount of expense transactions."""
    if not transactions:
        return 0.00

    return sum(
        float(transaction[4])
        for transaction in transactions
        if transaction[5].lower() == "expense"
    )


def net_savings(transactions):
    """Calculate net savings by subtracting expenses from income."""
    income = total_income(transactions)
    expenses = total_expenses(transactions)

    return income - expenses
```
def calculate_category_total(transactions, category):
    """Calculate total expenses for a selected category."""
    total = 0.00

    for transaction in transactions:
        if (
            transaction[5].lower() == "expense"
            and transaction[3].lower() == category.lower()
        ):
            total += float(transaction[4])

    return total
