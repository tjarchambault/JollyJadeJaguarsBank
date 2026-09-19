"""Handle command-line menus and user interaction."""

# Program: Personal Finance Tracker - cli.py
# Purpose: Provide menus and collect user choices.
# Inputs: Keyboard input from the user.
# Process: Display choices and delegate actions to feature modules.
# Outputs: User selections and interaction results.
# Honor Code: On my honor, as an Aggie, I have neither given nor received
# unauthorized aid on this academic work.


def display_menu():
    """Display the main menu for Phase 3 features."""
    print()
    print("=" * 40)
    print("       PERSONAL FINANCE TRACKER")
    print("=" * 40)
    print("1. View Reports")
    print("2. Filter by Date")
    print("3. Filter by Category")
    print("4. Export Data")
    print("5. Help")
    print("6. Exit")
    print("=" * 40)


def get_user_choice():
    """Get and validate the user's menu choice."""
    while True:
        choice = input("Enter selection (1-6): ")

        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice

        print("Invalid selection. Please enter a number from 1 to 6.")


def main():
    """Run the main CLI menu."""
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            print("Reports selected.")
        elif choice == "2":
            print("Date filter selected.")
        elif choice == "3":
            print("Category filter selected.")
        elif choice == "4":
            print("Export data selected.")
        elif choice == "5":
            print("Help selected.")
        elif choice == "6":
            print("Thank you for using Personal Finance Tracker.")
            break


if __name__ == "__main__":
    main()
