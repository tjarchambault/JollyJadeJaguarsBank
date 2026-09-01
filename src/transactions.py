"""Create and enter income and expense transactions."""

# Program: Personal Finance Tracker - transactions.py
# Purpose: Manage creation and entry of income and expense transactions.
# Inputs: Date, description, category, amount, and transaction type.
# Process: Create and prepare transaction records for other modules.
# Outputs: Transaction records.
# Honor Code: [Add the team's honor code statement here.]

# Fixed Categories for Income and Expense Transactions
import os
import sys
import pandas as pd
import sqlite3
from datetime import datetime

# File setup
DB_FILE = "transactions.db"

# Fixed Categories
income_categories = ["Salary", "Bonus", "Freelance", "Investment", "Other"]
expense_categories = ["Food", "Rent", "Utilities", "Entertainment", "Transportation", 
                      "Healthcare", "Insurance", "Other"]

# Fixed Categories for Income and Expense Transactions
income_categories = ["Salary", "Bonus", "Freelance", "Investment", "Other"]
expense_categories = ["Food", "Rent", "Utilities", "Entertainment", "Transportation", 
                      "Healthcare", "Insurance", "Other"]

def view_transactions():
    """Lists all transactions."""
    print("\n--- All Transactions ---")
    df = load_transactions() # type: ignore
    print_table(df) # type: ignore

def add_transaction():
    """Prompts and adds new entry to database."""
    print("\n--- Add New Transaction ---")
    
    # 1. Type
    while True:
        t_choice = input("Select type (1: Income, 2: Expense, 0: Cancel): ").strip()
        if t_choice == "0": 
            return # Returns to main menu
        if t_choice == "1":
            t_type = "Income"
            categories = income_categories # type: ignore
            break
        elif t_choice == "2":
            t_type = "Expense"
            categories = expense_categories # type: ignore
            break
        print("Invalid selection. Choose 1, 2, or 0.")

    # 2. Category
    print(f"\nSelect {t_type} Category:")
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat}")
    
    while True:
        try:
            c_input = input("Select category number (0 to Cancel): ").strip()
            if c_input == "0": 
                return
            
            choice = int(c_input)
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            print(f"Please select a number between 1 and {len(categories)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # 3. Description
    description = input("Enter description (0 to Cancel): ").strip()
    if description == "0":
        return
    if not description:
        description = "N/A"

    # 4. Amount
    while True:
        try:
            a_input = input("Enter amount ($) (0 to Cancel): ").strip()
            if a_input == "0":
                return
            
            amount = float(a_input)
            if amount > 0:
                break
            print("Amount must be greater than zero.")
        except ValueError:
            print("Please enter a valid numeric value.")

    # 5. Date
    today_str = datetime.now().strftime("%Y-%m-%d") # type: ignore
    date_input = input(f"Enter date (YYYY-MM-DD) [Default: {today_str}, 0 to Cancel]: ").strip()
    
    if date_input == "0":
        return
    elif date_input:
        try:
            datetime.strptime(date_input, "%Y-%m-%d") # type: ignore
            t_date = date_input
        except ValueError:
            print("Invalid format. Defaulting to today's date.")
            t_date = today_str
    else:
        t_date = today_str

    # Save directly to SQLite
    with sqlite3.connect(DB_FILE) as conn: # type: ignore
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (date, description, category, amount, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (t_date, description, category, amount, t_type))
        conn.commit()
        
    print("\nTransaction recorded successfully.")

    # 2. Category
    print(f"\nSelect {t_type} Category:")
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat}")
    
    while True:
        try:
            c_input = input("Select category number (0 to Cancel): ").strip()
            if c_input == "0": 
                return
            
            choice = int(c_input)
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            print(f"Please select a number between 1 and {len(categories)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # 3. Description
    description = input("Enter description (0 to Cancel): ").strip()
    if description == "0":
        return
    if not description:
        description = "N/A"

    # 4. Amount
    while True:
        try:
            a_input = input("Enter amount ($) (0 to Cancel): ").strip()
            if a_input == "0":
                return
            
            amount = float(a_input)
            if amount > 0:
                break
            print("Amount must be greater than zero.")
        except ValueError:
            print("Please enter a valid numeric value.")

    # 5. Date
    today_str = datetime.now().strftime("%Y-%m-%d") # type: ignore
    date_input = input(f"Enter date (YYYY-MM-DD) [Default: {today_str}, 0 to Cancel]: ").strip()
    
    if date_input == "0":
        return
    elif date_input:
        try:
            datetime.strptime(date_input, "%Y-%m-%d") # type: ignore
            t_date = date_input
        except ValueError:
            print("Invalid format. Defaulting to today's date.")
            t_date = today_str
    else:
        t_date = today_str

    # Save directly to SQLite
    with sqlite3.connect(DB_FILE) as conn: # type: ignore
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (date, description, category, amount, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (t_date, description, category, amount, t_type))
        conn.commit()
        
    print("\nTransaction recorded successfully.")

def main():
    """Run the Personal Finance Tracker application."""
    """Main loop."""
    """More to come in the transaction space"""
    init_db() # type: ignore

    while True:
        try:
            print("\n" + "=" * 40)
            print("        PERSONAL FINANCE TRACKER       ")
            print("=" * 40)
            print("1. Add Transaction")
            print("2. View Transactions")
            print("3. Delete Transaction")
            print("4. Calculate Totals")
            print("5. Quit")

            choice = input("\nEnter selection (1-5): ").strip()

            if choice == "1":
                add_transaction()
            elif choice == "2":
                view_transactions()
            elif choice == "3":
                delete_transaction() # type: ignore
            elif choice == "4":
                calculate_totals() # type: ignore
            elif choice == "5":
                print("\nThank you for using Simple Finance Tracker.")
                sys.exit(0)
            else:
                print("Invalid choice. Please select a number from 1 to 5.")

        # Catches normal cancellation keystrokes
        except (KeyboardInterrupt, EOFError):
            print("\n\nAction cancelled. Returning to main menu...")
            continue
        # Hard catch for weird numpad/terminal escape sequences 
        except Exception:
            print("\n\nInvalid key detected. Returning to main menu...")
            continue# Future work: connect the CLI and feature modules here.
    pass


if __name__ == "__main__":
    main()
