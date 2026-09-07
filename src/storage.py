"""Save and load transaction data using SQLite."""

# Program: Personal Finance Tracker - storage.py
# Purpose: Provide SQLite database storage for transaction data.
# Inputs: Transaction records.
# Process: Create, save, and load transaction data.
# Outputs: Transaction records from the database.
# Honor Code: The Aggie Code of Honor is an effort to unify the aims of all Texas A&M men and women toward a high code of ethics and personal dignity. For most, living under this code will be no problem, as it asks nothing of a person that is beyond reason. It only calls for honesty and integrity, characteristics that Aggies have always exemplified.

The Aggie Code of Honor functions as a symbol to all Aggies, promoting understanding and loyalty to truth and confidence in each other.

import sqlite3


DB_FILE = "transactions.db"


def init_db():
    """Create the transactions table if it does not already exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT,
                category TEXT,
                amount REAL NOT NULL,
                type TEXT NOT NULL
            )
        """)

        conn.commit()


def load_transactions():
    """Load all transactions from the SQLite database."""
    init_db()

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, date, description, category, amount, type
            FROM transactions
            ORDER BY date DESC
        """)

        return cursor.fetchall()


def save_transaction(date, description, category, amount, transaction_type):
    """Save one transaction to the SQLite database."""
    init_db()

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (date, description, category, amount, type)
            VALUES (?, ?, ?, ?, ?)
        """, (date, description, category, amount, transaction_type))

        conn.commit()
