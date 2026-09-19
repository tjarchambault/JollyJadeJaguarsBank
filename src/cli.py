"""Handle command-line menus and user interaction."""

# Program: Personal Finance Tracker - cli.py
# Purpose: Provide menus and collect user choices.
# Inputs: Keyboard input from the user.
# Process: Display choices and delegate actions to feature modules.
# Outputs: User selections and interaction results.
# Honor Code: [Add the team's honor code statement here.]


def display_main_menu():
    """Display the main menu for Phase 3 features."""
    print()
    print("========================================")
    print("       PERSONAL FINANCE TRACKER")
    print("========================================")
    print("1. View Reports")
    print("2. Filter by Date")
    print("3. Filter by Category")
    print("4. Export Data")
    print("5. Help")
    print("6. Exit")
    print("========================================")


def get_user_choice():
    """Get a menu choice placeholder."""
    # Future work: read and validate a menu selection.
    pass


def main():
    """Run the main CLI menu."""
    while True:
        display_main_menu()
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
