# Program: Personal Finance Tracker - main.py
# Purpose: Allow the user to add/view/delete financial transactions.
# Inputs:  Income/Expense, category, amount, date.
# Process: The user is guided step by step on entering a transaction. Functions serve
#          as building blocks to acheive a final output
# Outputs: A viewable table with all transactions, total savings/expenses, net income.
# Honor Code: On my honor, as an Aggie, I have neither given nor received unauthorized aid
#             on this academic work. 
#           The Aggie Code of Honor functions as a symbol to all Aggies, promoting understanding
#           and loyalty to truth and confidence in each other.

# these are the tools/libraries I need to import so I can use them
import sys  # lets me quit the program with sys.exit
import pandas as pd  # pandas is for working with tables of data (the DataFrame thing)
import sqlite3  # this is the database, it comes built into python which is cool
from datetime import datetime  # so I can get today's date and check date formats

# File setup
DB_FILE = "transactions.db"  # this is the name of my database file, it saves here

# Fixed Categories
# making lists of the categories so the user can pick from them later
income_categories = ["Salary", "Bonus", "Freelance", "Investment", "Other"]
expense_categories = ["Food", "Rent", "Utilities", "Entertainment", "Transportation",
                      "Healthcare", "Insurance", "Other"]

# =====================================================
# FILE INITIALIZATION & HELPERS
# =====================================================
def init_db():
    """Ensures SQLite database exists with proper schema."""
    # this makes the database table if it doesn't exist yet
    with sqlite3.connect(DB_FILE) as conn:  # connect to the database (the "with" auto closes it)
        cursor = conn.cursor()  # the cursor is what actually runs my sql commands
        # this big string is SQL, it makes a table with all my columns
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
        conn.commit()  # commit means actually save the changes


def load_transactions():
    """Reads data from SQLite into a pandas DataFrame."""
    init_db()  # make sure the table exists first before I try to read it
    try:  # try in case something goes wrong so it doesn't crash
        with sqlite3.connect(DB_FILE) as conn:
            # pandas can read straight from sql which is way easier than looping
            df = pd.read_sql_query("""SELECT id, date, description, category, amount,
            type
            FROM transactions ORDER BY date desc""", conn)  # order by date newest first
            # Ensure types align for Pandas formatting
            if not df.empty:  # only do this if there's actually data
                # make sure amount is a number, if it's broken turn it into 0.0
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
                # make the id a whole number (int) not a decimal
                df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
        return df  # give back the table of data
    except Exception as e:  # if anything broke, catch it here
        print(f"Error loading database: {e}")  # show the error so I know what happened
        # give back an empty table with the right columns so nothing else breaks
        return pd.DataFrame(columns=["id", "date", "description", "category", "amount", "type"])


def save_transaction(date, description, category, amount, t_type):
    """Insert a single transaction into the database. Returns True on success."""
    # this function actually saves a new transaction into the database
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # the ? marks are placeholders, python fills them in safely (stops hacking)
            cursor.execute('''
                INSERT INTO transactions (date, description, category, amount, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, description, category, amount, t_type))  # these fill in the ?
            conn.commit()  # save it
        return True  # True means it worked
    except Exception as e:
        print(f"Error saving transaction: {e}")
        return False  # False means it didn't work


def transaction_exists(t_id):
    """Returns True if a transaction with the given ID exists."""
    # checks if a transaction is really in the database before I try to delete it
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # SELECT 1 just checks if a row is there, don't need the actual data
            cursor.execute("SELECT 1 FROM transactions WHERE id = ?", (t_id,))
            # fetchone gets one row, if it's None then nothing was found
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking transaction: {e}")
        return False


def delete_transaction_by_id(t_id):
    """Delete a transaction by ID. Returns True on success."""
    # this deletes one transaction using its id number
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # DELETE removes the row where the id matches
            cursor.execute("DELETE FROM transactions WHERE id = ?", (t_id,))
            conn.commit()  # save the deletion
        return True
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False


def print_table(df):
    """Prints a view of transactions."""
    # this prints out the transactions in a nice looking table
    if df.empty:  # if there's no data just say so and stop
        print("\nNo records found.")
        return
    df_sorted = df.sort_values(by="date", ascending=False)  # sort newest first
    print("\n" + "=" * 90)  # "=" * 90 makes a line of 90 equal signs, looks like a border
    # the <5 and <10 stuff lines up the columns so they're even (left aligned)
    print(f"{'ID':<5} | {'Date':<10} | {'Type':<8} | {'Category':<15} | {'Description':<25} | {'Amount':<10}")
    print("-" * 90)  # a line of dashes under the headers
    for _, row in df_sorted.iterrows():  # loop through every row one at a time
        # if the description is empty (NaN) just put N/A instead
        desc = str(row['description']) if pd.notna(row['description']) else "N/A"
        print(
            f"{int(row['id']):<5} | "
            f"{str(row['date']):<10} | "
            f"{str(row['type']):<8} | "
            f"{str(row['category']):<15} | "
            f"{desc[:25]:<25} | "  # [:25] cuts off long descriptions at 25 letters
            f"${row['amount']:<9.2f}"  # .2f means show 2 decimal places like money
        )
    print("=" * 90)  # bottom border


# =====================================================
# CALCULATION HELPERS (split out so they're reusable + testable)
# =====================================================
def total_income(df):
    """Sum of all income amounts."""
    # only add up the rows where type is Income
    if df.empty:  # if no data, just return 0 so nothing crashes
        return 0.0
    return df[df["type"] == "Income"]["amount"].sum()


def total_expenses(df):
    """Sum of all expense amounts."""
    # only add up the rows where type is Expense
    if df.empty:
        return 0.0
    return df[df["type"] == "Expense"]["amount"].sum()


def calculate_net_savings(df):
    """Income minus expenses."""
    # savings is just money in minus money out
    return total_income(df) - total_expenses(df)


# =====================================================
# CORE FEATURES
# =====================================================
def view_transactions():
    """Lists all transactions."""
    # shows all the transactions to the user
    print("\n--- All Transactions ---")
    df = load_transactions()  # get the data from the database
    print_table(df)  # print it out nicely


def add_transaction():
    """Prompts and adds new entry to database."""
    # this asks the user a bunch of questions to make a new transaction
    print("\n--- Add New Transaction ---")

    # 1. Type
    while True:  # keep asking until they pick something valid
        t_choice = input("Select type (1: Income, 2: Expense, 0: Cancel): ").strip()  # strip removes extra spaces
        if t_choice == "0":
            return  # Returns to main menu
        if t_choice == "1":
            t_type = "Income"
            categories = income_categories  # use the income list
            break  # break stops the while loop
        elif t_choice == "2":
            t_type = "Expense"
            categories = expense_categories  # use the expense list
            break
        print("Invalid selection. Choose 1, 2, or 0.")  # only shows if they typed wrong

    # 2. Category
    print(f"\nSelect {t_type} Category:")
    # enumerate gives me a number AND the item, starting at 1 so it looks nice
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat}")

    while True:
        try:  # try because they might type letters instead of a number
            c_input = input("Select category number (0 to Cancel): ").strip()
            if c_input == "0":
                return
            choice = int(c_input)  # turn what they typed into a number
            # check the number is actually one of the choices in the list
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]  # minus 1 because lists start at 0
                break
            print(f"Please select a number between 1 and {len(categories)}.")
        except ValueError:  # this happens if int() fails cause they typed a word
            print("Invalid input. Please enter a number.")

    # 3. Description
    description = input("Enter description (0 to Cancel): ").strip()
    if description == "0":
        return
    if not description:  # if they just hit enter and left it blank
        description = "N/A"  # put N/A so it's not empty

    # 4. Amount
    while True:
        try:
            a_input = input("Enter amount ($) (0 to Cancel): ").strip()
            if a_input == "0":
                return
            amount = float(a_input)  # float because money can have decimals
            if amount > 0:  # can't have a negative or zero amount
                break
            print("Amount must be greater than zero.")
        except ValueError:  # they typed something that's not a number
            print("Please enter a valid numeric value.")

    # 5. Date
    today_str = datetime.now().strftime("%Y-%m-%d")  # get today's date as text
    date_input = input(f"Enter date (YYYY-MM-DD) [Default: {today_str}, 0 to Cancel]: ").strip()

    if date_input == "0":
        return
    elif date_input:  # if they typed a date
        try:
            # strptime checks if the date is in the right format, errors if not
            datetime.strptime(date_input, "%Y-%m-%d")
            t_date = date_input
        except ValueError:
            print("Invalid format. Defaulting to today's date.")
            t_date = today_str  # if the date was bad just use today
    else:  # they left it blank so use today
        t_date = today_str

    # Save via data-layer helper
    # call my save function and check if it returned True or False
    if save_transaction(t_date, description, category, amount, t_type):
        print("\nTransaction recorded successfully.")
    else:
        print("\nTransaction could not be saved.")


def delete_transaction():
    """Removes a record from the database by ID."""
    # lets the user delete a transaction they don't want
    df = load_transactions()
    if df.empty:  # can't delete anything if there's nothing there
        print("\nNo records to delete.")
        return
    print_table(df)  # show them the table so they can see the ids

    try:
        t_id_input = input("\nEnter Transaction ID to delete (0 to Cancel): ").strip()
        if t_id_input == "0":
            return
        t_id = int(t_id_input)  # turn the id into a number
    except ValueError:
        print("Invalid ID format. Returning to menu.")
        return

    # Check existence via data-layer helper
    # make sure that id actually exists before asking to delete it
    if not transaction_exists(t_id):
        print("Transaction ID not found.")
        return

    # ask them to confirm so they don't delete something by accident
    confirm = input(f"Are you sure you want to delete transaction #{t_id}? (Y/N): ").strip().lower()  # lower makes Y or y both work
    if confirm == 'y':
        if delete_transaction_by_id(t_id):  # call the delete function
            print("\nTransaction deleted successfully.")
        else:
            print("\nTransaction could not be deleted.")
    else:
        print("\nDeletion cancelled.")


def calculate_totals():
    """Loads data, calculates totals, and prints the financial summary."""
    # this ties everything together: get data, do the math, then show it
    df = load_transactions()  # grab all the data first

    # call my reusable calculation helpers instead of doing the math right here
    income = total_income(df)
    expenses = total_expenses(df)
    net = calculate_net_savings(df)

    print("\n" + "=" * 40)  # top border line
    print("FINANCIAL SUMMARY")
    print("=" * 40)
    # :.2f rounds to 2 decimals so it looks like proper money ($5.00 not $5.0)
    print(f"Total Income   : ${income:.2f}")
    print(f"Total Expenses : ${expenses:.2f}")
    print(f"Net Savings    : ${net:.2f}")
    print("=" * 40)  # bottom border line


# =====================================================
# MAIN LOOP
# =====================================================
def main():
    """Main loop."""
    # this is the main part that runs the whole program
    init_db()  # set up the database right at the start just in case
    while True:  # loop forever so the menu keeps coming back until they quit
        try:  # try so a weird error doesn't crash the whole thing
            # print out the menu every time so the user knows their options
            print("\n" + "=" * 40)
            print("        PERSONAL FINANCE TRACKER       ")
            print("=" * 40)
            print("1. Add Transaction")
            print("2. View Transactions")
            print("3. Delete Transaction")
            print("4. Calculate Totals")
            print("5. Quit")
            choice = input("\nEnter selection (1-5): ").strip()  # ask what they want to do

            # check what number they picked and call the right function
            if choice == "1":
                add_transaction()
            elif choice == "2":
                view_transactions()
            elif choice == "3":
                delete_transaction()
            elif choice == "4":
                calculate_totals()
            elif choice == "5":
                print("\nThank you for using Simple Finance Tracker.")
                sys.exit(0)  # this actually quits the program
            else:
                print("Invalid choice. Please select a number from 1 to 5.")  # they typed something wrong

        # Catches normal cancellation keystrokes
        # this happens if they hit Ctrl+C or Ctrl+D to cancel
        except (KeyboardInterrupt, EOFError):
            print("\n\nAction cancelled. Returning to main menu...")
            continue  # continue goes back to the top of the while loop
        # Hard catch for weird numpad/terminal escape sequences
        # this catches any other weird error so the program keeps running
        except Exception:
            print("\n\nInvalid key detected. Returning to main menu...")
            continue


# this checks if the file is being run directly (not imported)
# if it is, then start the program by calling main()
if __name__ == "__main__":  # note: __name__ has double underscores on each side
    main()
