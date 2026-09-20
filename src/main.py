# Program: Personal Finance Tracker - main.py
# Purpose: Allow the user to add/view/delete financial transactions.
# Inputs:  Income/Expense, category, amount, date.
# Process: The user is guided step by step on entering a transaction. Functions serve
#          as building blocks to achieve a final output.
# Outputs: A viewable table with all transactions, total savings/expenses, net income.
# Honor Code: On my honor, as an Aggie, I have neither given nor received unauthorized aid
#             on this academic work.
#           The Aggie Code of Honor functions as a symbol to all Aggies, promoting understanding
#           and loyalty to truth and confidence in each other.

import sys
import sqlite3
import pandas as pd
from datetime import datetime
from rich.console import Console  # main object that handles all rich printing
from rich.table import Table      # Table builds the formatted table structure
from rich.panel import Panel      # Panel puts a bordered box around content
from rich import box              # box has all the different border styles

# create one Console object and reuse it everywhere in this file
console = Console(force_terminal=True)

# =====================================================
# CONSTANTS
# =====================================================
DB_FILE = "transactions.db"  # name of the database file, saves in the same folder

income_categories  = ["Salary", "Bonus", "Freelance", "Investment", "Other"]
expense_categories = ["Food", "Rent", "Utilities", "Entertainment", "Transportation",
                      "Healthcare", "Insurance", "Other"]

# =====================================================
# DATABASE FUNCTIONS
# =====================================================
def init_db():
    """Ensures SQLite database exists with proper schema."""
    # creates the transactions table if it doesnt exist yet
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT,
                category TEXT,
                amount REAL NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        conn.commit()  # commit saves the changes to disk


def load_transactions():
    """Reads data from SQLite into a pandas DataFrame."""
    init_db()  # make sure the table exists before we try to read it
    try:
        with sqlite3.connect(DB_FILE) as conn:
            # pandas can read straight from SQL which is easier than looping
            df = pd.read_sql_query("""
                SELECT id, date, description, category, amount, type
                FROM transactions
                ORDER BY date DESC
            """, conn)
            if not df.empty:  # only clean up types if there is actually data
                # make sure amount is a number, coerce turns bad values into 0.0
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
                # make id a whole number instead of a decimal
                df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
        return df
    except Exception as e:
        print(f"Error loading database: {e}")
        # return an empty DataFrame with the right columns so nothing else breaks
        return pd.DataFrame(columns=["id", "date", "description", "category", "amount", "type"])


def save_transaction(date, description, category, amount, t_type):
    """Insert a single transaction into the database. Returns True on success."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # the ? marks are placeholders, Python fills them in safely
            cursor.execute('''
                INSERT INTO transactions (date, description, category, amount, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, description, category, amount, t_type))
            conn.commit()
        return True   # True means it worked
    except Exception as e:
        print(f"Error saving transaction: {e}")
        return False  # False means it failed


def transaction_exists(t_id):
    """Returns True if a transaction with the given ID exists."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # SELECT 1 just checks if a row is there, we dont need the actual data
            cursor.execute("SELECT 1 FROM transactions WHERE id = ?", (t_id,))
            # fetchone returns None if nothing was found
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking transaction: {e}")
        return False


def delete_transaction_by_id(t_id):
    """Delete a transaction by ID. Returns True on success."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (t_id,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False


# =====================================================
# CALCULATION FUNCTIONS
# =====================================================
def total_income(df):
    """Sum of all income amounts."""
    # filter to income rows only then sum the amount column
    if df.empty:
        return 0.0
    return df[df["type"] == "Income"]["amount"].sum()


def total_expenses(df):
    """Sum of all expense amounts."""
    # filter to expense rows only then sum the amount column
    if df.empty:
        return 0.0
    return df[df["type"] == "Expense"]["amount"].sum()


def calculate_net_savings(df):
    """Income minus expenses."""
    # net savings is simply money in minus money out
    return total_income(df) - total_expenses(df)


# =====================================================
# DISPLAY FUNCTIONS
# =====================================================
def print_table(df):
    """Prints a formatted view of transactions."""
    if df.empty:
        console.print("\n[black]No records found.[/black]")
        return

    # sort newest first so the most recent transactions are at the top
    df_sorted = df.sort_values(by="date", ascending=False)

    table = Table(
        title="[black]Transactions[/black]",
        box=box.ROUNDED,
        header_style="black"
    )

    # each column gets a style, no_wrap prevents values breaking onto a new line
    table.add_column("ID",          style="black", no_wrap=True, justify="left")
    table.add_column("Date",        style="black", no_wrap=True)
    table.add_column("Type",        no_wrap=True)   # colored per row below
    table.add_column("Category",    style="black", no_wrap=True)
    table.add_column("Description", style="black", no_wrap=True)
    table.add_column("Amount",      no_wrap=True, justify="right")  # colored per row

    for _, row in df_sorted.iterrows():
        # if the description is empty put N/A so the cell is never blank
        desc = str(row["description"]) if pd.notna(row["description"]) else "N/A"

        # color the type and amount based on whether it is income or expense
        if row["type"] == "Income":
            type_str   = "[green]Income[/green]"
            amount_str = f"[green]${row['amount']:.2f}[/green]"
        else:
            type_str   = "[red]Expense[/red]"
            amount_str = f"[red]${row['amount']:.2f}[/red]"

        table.add_row(
            str(int(row["id"])),
            str(row["date"]),
            type_str,
            str(row["category"]),
            desc[:25],      # cut long descriptions off at 25 characters
            amount_str
        )

    console.print(table)


# =====================================================
# TRANSACTION FUNCTIONS
# =====================================================
def view_transactions():
    """Lists all transactions."""
    df = load_transactions()  # get all transactions from the database
    print_table(df)           # pass the DataFrame to print_table to display


def add_transaction():

    # 1. Type
    while True:
        console.print(Panel(
            "[black]1.[/black] Income\n"
            "\n"
            "[black]2.[/black] Expense\n"
            "\n"
            "[black]0.[/black] Cancel",
            title="[black]Select Transaction Type[/black]",
            border_style="black",
            box=box.ROUNDED
        ))

        t_choice = input("\nEnter selection (1, 2, or 0): ").strip()
        if t_choice == "0":
            return
        if t_choice == "1":
            t_type     = "Income"
            categories = income_categories
            break
        elif t_choice == "2":
            t_type     = "Expense"
            categories = expense_categories
            break
        console.print("[black]Invalid selection. Choose 1, 2, or 0.[/black]")

    # 2. Category
    cat_table = Table(box=box.SIMPLE, show_header=False)
    cat_table.add_column("Num",      style="black", justify="right")
    cat_table.add_column("Category", style="black")

    for idx, cat in enumerate(categories, start=1):
        cat_table.add_row(f"{idx}.", cat)

    console.print(Panel(
        cat_table,
        title=f"[black]Select {t_type} Category[/black]",
        border_style="black",
        box=box.ROUNDED
    ))

    while True:
        try:
            c_input = input("Select category number (0 to Cancel): ").strip()
            if c_input == "0":
                return
            choice = int(c_input)
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            console.print(f"[black]Please select a number between 1 and {len(categories)}.[/black]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")

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
            console.print("[red]Amount must be greater than zero.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid numeric value.[/red]")

    # 5. Date
    today_str = datetime.now().strftime("%Y-%m-%d")
    while True:
        date_input = input(
            f"Enter date (YYYY-MM-DD) [press Enter for today ({today_str}), 0 to Cancel]: "
        ).strip()
        if date_input == "0":
            return
        if not date_input:
            t_date = today_str
            break
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            t_date = date_input
            break
        except ValueError:
            console.print("[red]Invalid format. Please use YYYY-MM-DD (example: 2025-01-15).[/red]")

    # save to database and report success or failure
    if save_transaction(t_date, description, category, amount, t_type):
        console.print(Panel(
            f"[green]Transaction recorded successfully.[/green]\n"
            f"[black]Type     :[/black] "
            f"[{'green' if t_type == 'Income' else 'red'}]{t_type}[/{'green' if t_type == 'Income' else 'red'}]\n"
            f"[black]Category :[/black] [black]{category}[/black]\n"
            f"[black]Desc     :[/black] [black]{description}[/black]\n"
            f"[black]Amount   :[/black] [{'green' if t_type == 'Income' else 'red'}]${amount:.2f}[/{'green' if t_type == 'Income' else 'red'}]\n"
            f"[black]Date     :[/black] [black]{t_date}[/black]",
            title="[black]Saved[/black]",
            border_style="black",
            box=box.ROUNDED
        ))
    else:
        console.print(Panel(
            "[red]Transaction could not be saved.[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red",
            box=box.ROUNDED
        ))

def delete_transaction():
    """Removes a record from the database by ID."""
    df = load_transactions()

    if df.empty:
        console.print("\n[black]No records to delete.[/black]")
        return

    print_table(df)  # show the table so the user can see the IDs

    while True:
        t_id_input = input("\nEnter Transaction ID to delete (0 to Cancel): ").strip()
        if t_id_input == "0":
            return
        try:
            t_id = int(t_id_input)  # convert to int, fails if they type letters
            if t_id > 0:            # IDs should always be positive
                break
            console.print("[black]Please enter a positive ID number.[/black]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a numeric ID.[/red]")

    # check the ID actually exists before asking to confirm
    if not transaction_exists(t_id):
        console.print("[red]Transaction ID not found.[/red]")
        retry = input("Would you like to delete a different transaction? (Y/N): ").strip().lower()
        if retry == "y":
            delete_transaction()  # restart the function from the top
        return

    # ask for confirmation so they dont delete something by accident
    confirm = input(
        f"Are you sure you want to delete transaction #{t_id}? (Y/N): "
    ).strip().lower()

    if confirm == "y":
        if delete_transaction_by_id(t_id):
            console.print("\n[green]Transaction deleted successfully.[/green]")
        else:
            console.print("\n[red]Transaction could not be deleted.[/red]")
    else:
        console.print("\n[black]Deletion cancelled.[/black]")


def calculate_totals():
    """Loads data, calculates totals, and prints the financial summary."""
    df = load_transactions()  # get all transactions from the database

    # call the reusable calculation helpers
    income   = total_income(df)
    expenses = total_expenses(df)
    net      = calculate_net_savings(df)

    # pick color for net savings based on whether it is positive or negative
    # green means they saved money, red means they spent more than they earned
    net_color = "green" if net >= 0 else "red"
    net_str   = f"+${net:.2f}" if net >= 0 else f"-${abs(net):.2f}"

    # Panel gives the summary its own clean bordered box
    console.print(Panel(
        f"[black]Total Income   :[/black]   [green]${income:.2f}[/green]\n"
        f"[black]Total Expenses :[/black]   [red]${expenses:.2f}[/red]\n"
        f"[black]Net Savings    :[/black]   [{net_color}]{net_str}[/{net_color}]",
        title="[black]Financial Summary[/black]",
        border_style="black",
        box=box.ROUNDED
    ))


# =====================================================
# REPORT FUNCTIONS
# =====================================================
def report_savings_by_category():
    """Prints net savings per category based on income categories only."""

    df = load_transactions()  # get all transactions as a DataFrame from the database

    if df.empty:
        console.print("\n[black]No transactions found.[/black]")
        return

    # filter to income rows only since savings come from income
    # expense categories like Food or Rent are not relevant here
    income = df[df["type"] == "Income"]

    if income.empty:
        console.print("\n[black]No income transactions found.[/black]")
        return

    # groupby category and sum the amounts within each group
    # sort descending so the highest earning category is at the top
    summary = (
        income.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    # rename amount to Total Income so the column header makes sense
    summary = summary.rename(columns={"amount": "Total Income"})

    # pull total expenses as a single number to subtract from income
    # we dont break expenses down by category here since savings is about
    # how much income is left after ALL expenses are accounted for

    total_income_amount   = summary["Total Income"].sum()

    table = Table(
        title="[black]Savings by Category[/black]",
        box=box.ROUNDED,
        show_footer=True,
        header_style="black"
    )

    table.add_column("Category",     style="black", no_wrap=True)
    table.add_column(
        "Total Income",
        style="black",   # income is always green
        justify="right",
        footer=f"[black]${total_income_amount:.2f}[/black]",
        footer_style="black"
    )

    # iterrows() loops through the DataFrame one row at a time
    # _ is a throwaway variable for the index since we dont need it
    for _, row in summary.iterrows():
        table.add_row(
            str(row["category"]),
            f"[green]${row['Total Income']:.2f}[/green]"
        )

    console.print(table)


def report_expenses_by_category():
    """Prints a summary of total expenses grouped by category."""

    df = load_transactions()  # get all transactions as a DataFrame from the database

    if df.empty:
        console.print("\n[black]No transactions found.[/black]")
        return

    # boolean filtering - creates a new DataFrame with only Expense rows
    # Income rows are excluded since this report is expenses only
    expenses = df[df["type"] == "Expense"]

    if expenses.empty:
        console.print("\n[black]No expense transactions found.[/black]")
        return

    # groupby splits the DataFrame into groups based on the category column
    # .sum() adds up all the amounts within each group
    # .reset_index() turns the grouped result back into a normal flat DataFrame
    # .sort_values() puts the highest spending category at the top
    summary = (
        expenses.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    total = summary["amount"].sum()  # grand total across all categories

    table = Table(
        title="[black]Expenses by Category[/black]",
        box=box.ROUNDED,
        show_footer=True,
        header_style="black"
    )

    table.add_column("Category",    style="black", no_wrap=True)
    table.add_column(
        "Total Spent",
        style="black",     # expenses are always red
        justify="black",
        footer=f"[black]${total:.2f}[/black]",
        footer_style="black"
    )

    # iterrows() loops through the DataFrame one row at a time
    for _, row in summary.iterrows():
        table.add_row(
            str(row["category"]),
            f"${row['amount']:.2f}"
        )

    console.print(table)

def report_summary_by_period():
    """Prints income, expenses, and net savings grouped by user selected time period."""

    df = load_transactions()  # get all transactions as a DataFrame from the database

    if df.empty:
        console.print("\n[black]No transactions found.[/black]")
        return

    # show the period selection menu in a Panel so it matches the rest of the app
    console.print(Panel(
        "[black]1.[/black] Daily\n"
        "\n"
        "[black]2.[/black] Weekly\n"
        "\n"
        "[black]3.[/black] Monthly\n"
        "\n"
        "[black]4.[/black] Yearly\n"
        "\n"
        "[black]0.[/black] Cancel",
        title="[black]Select Time Period[/black]",
        border_style="black",
        box=box.ROUNDED
    ))

    choice = input("\nEnter selection: ").strip()

    # map the user choice to a pandas period string and a display label
    # these period strings are what pandas uses in .dt.to_period()
    # D = day, W = week, M = month, Y = year
    period_map = {
        "1": ("D", "Daily"),
        "2": ("W", "Weekly"),
        "3": ("M", "Monthly"),
        "4": ("Y", "Yearly")
    }

    if choice == "0":
        return

    # check if they picked a valid option before doing anything else
    if choice not in period_map:
        console.print("[black]Invalid selection.[/black]")
        return

    # unpack the period string and label from the map
    period_str, period_label = period_map[choice]

    # pd.to_datetime converts date strings into datetime objects
    # errors="coerce" turns bad dates into NaT instead of crashing
    # .dt.to_period() groups by the chosen time period
    df["period"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period(period_str)

    # if every single date failed to parse we have nothing to group by
    if df["period"].isna().all():
        console.print("\n[black]No valid dates found in records.[/black]")
        return

    # groupby groups by period AND type at the same time
    # .unstack() pivots the type values into their own columns
    # fill_value=0 fills missing period/type combos with 0 instead of NaN
    summary = (
        df.groupby(["period", "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    # unstack only creates columns for types that actually exist in the data
    # if no income exists yet the Income column wont be there so we add it as 0
    if "Income" not in summary.columns:
        summary["Income"] = 0.0
    if "Expense" not in summary.columns:
        summary["Expense"] = 0.0

    # vectorized math - pandas applies this across every row automatically
    summary["Net Savings"] = summary["Income"] - summary["Expense"]

    # sort oldest to newest so the report reads chronologically
    summary = summary.sort_values("period")

    # totals for the footer row
    total_income  = summary["Income"].sum()
    total_expense = summary["Expense"].sum()
    total_net     = summary["Net Savings"].sum()

    # pick footer color for net based on whether overall savings is positive
    total_net_color = "green" if total_net >= 0 else "red"
    total_net_str   = f"+${total_net:.2f}" if total_net >= 0 else f"-${abs(total_net):.2f}"

    table = Table(
        title=f"[black]{period_label} Summary[/black]",
        box=box.ROUNDED,
        show_footer=True,
        header_style="black"
    )

    table.add_column(
        period_label,         # column header changes based on selected period
        style="black",
        no_wrap=True,
        footer="[black]TOTAL[/black]"
    )
    table.add_column(
        "Income",
        style="green",        # income is always green
        justify="right",
        footer=f"[dark_green]${total_income:.2f}[/dark_green]"
    )
    table.add_column(
        "Expenses",
        style="red",          # expenses are always red
        justify="right",
        footer=f"[bold red]${total_expense:.2f}[/bold red]"
    )
    table.add_column(
        "Net Savings",
        justify="right",
        footer=f"[dark {total_net_color}]{total_net_str}[/dark {total_net_color}]"
    )

    for _, row in summary.iterrows():
        net = row["Net Savings"]

        # pick color per row based on whether that period was positive or negative
        net_color = "dark green" if net >= 0 else "red"
        net_str   = f"+${net:.2f}" if net >= 0 else f"-${abs(net):.2f}"

        table.add_row(
            str(row["period"]),
            f"${row['Income']:.2f}",
            f"${row['Expense']:.2f}",
            f"[{net_color}]{net_str}[/{net_color}]"  # inline color per row
        )

    console.print(table)


# =====================================================
# REPORTS MENU
# =====================================================
def reports_menu():
    """Sub-menu for selecting which report to run."""
    # this runs in its own loop so the user can run multiple reports
    # without going back to the main menu each time
    while True:
        console.print(Panel(
            "[black]1.[/black] Savings by Category\n"
            "\n"
            "[black]2.[/black] Expenses by Category\n"
            "\n"
            "[black]3.[/black] Summary by Period\n"
            "\n"
            "[black]0.[/black] Back to Main Menu",
            title="[black]Reports Menu[/black]",
            border_style="black",
            box=box.ROUNDED
        ))

        choice = input("\nEnter selection: ").strip()

        if choice == "1":
            report_savings_by_category()
            input("\nPress Enter to return to Reports Menu...")
        elif choice == "2":
            report_expenses_by_category()
            input("\nPress Enter to return to Reports Menu...")
        elif choice == "3":
            report_summary_by_period()
            input("\nPress Enter to return to Reports Menu...")
        elif choice == "0":
            return  # returning from this function drops back to the main menu loop
        else:
            console.print("[red]Invalid choice. Please select 1, 2, 3, or 0.[/red]")


# =====================================================
# MAIN LOOP
# =====================================================
def main():
    """Main loop - displays menu and routes user to the right feature."""
    init_db()  # set up the database right at the start just in case it doesnt exist

    while True:
        try:
            # Panel wraps the entire menu in a clean bordered box
            console.print(Panel(
                "[black]1.[/black] Add Transaction\n"
                "\n"
                "[black]2.[/black] View Transactions\n"
                "\n"
                "[black]3.[/black] Delete Transaction\n"
                "\n"
                "[black]4.[/black] Calculate Totals\n"
                "\n"
                "[black]5.[/black] Reports\n"
                "\n"
                "[black]6.[/black] Quit",
                title="[black]Personal Finance Tracker[/black]",
                border_style="black",
                box=box.ROUNDED
            ))

            choice = input("\nEnter selection (1-6): ").strip()

            # route to the right function based on what they picked
            if choice == "1":
                add_transaction()
                input("\nPress Enter to return to Main Menu...")  # returns to main menu after adding a transaction
            elif choice == "2":
                view_transactions()
                input("\nPress Enter to return to Main Menu...")  # returns to main menu after viewing transactions
            elif choice == "3":
                delete_transaction()
                input("\nPress Enter to return to Main Menu...")  # returns to main menu after deleting a transaction
            elif choice == "4":
                calculate_totals()
                input("\nPress Enter to return to Main Menu...")  # returns to main menu after calculating totals
            elif choice == "5":
                reports_menu()
                #input("\nPress Enter to return to Main Menu...")  # returns to main menu after viewing reports
            elif choice == "6":
                # Panel for the goodbye message so it stands out
                console.print(Panel(
                    "[black]Thank you for using Personal Finance Tracker.[/black]",
                    border_style="black",
                    box=box.ROUNDED
                ))
                sys.exit(0)
            else:
                console.print("[red]Invalid choice. Please select a number from 1 to 6.[/red]")

        # this happens if the user hits Ctrl+C or Ctrl+D
        except (KeyboardInterrupt, EOFError):
            console.print("\n[black]Action cancelled. Returning to main menu...[/black]")
            continue

        # catches any unexpected error so the program keeps running
        except Exception as e:
            console.print(f"\n[red]Unexpected error: {e}[/red]")
            continue


# only runs if this file is executed directly, not if it is imported
if __name__ == "__main__":
    main()