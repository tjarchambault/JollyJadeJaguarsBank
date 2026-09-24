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


def get_menu_selection():
    """Capture the user's menu selection."""
    choice = input("Enter your selection: ")
    return choice

def validate_menu_input(choice):
    """Confirm that the user's menu selection is valid."""
    if choice in ["1", "2", "3", "4", "5", "6"]:
        return True

    return False

def handle_invalid_menu_choice():
    """Handle an invalid menu selection."""
    print("Invalid selection. Please choose a valid menu option.")

def display_report_menu():
    """Display the available reports."""
    print()
    print("========================================")
    print("             REPORTS MENU")
    print("========================================")
    print("1. Income Report")
    print("2. Expense Report")
    print("3. Net Savings Report")
    print("4. Category Report")
    print("5. Back to Main Menu")
    print("========================================")

def get_report_selection():
    """Capture which report the user wants to run."""
    choice = input("Enter your report selection: ")
    return choice

def display_report_options():
    """Display filtering and export options."""
    print()
    print("========================================")
    print("           REPORT OPTIONS")
    print("========================================")
    print("1. Filter by Date")
    print("2. Filter by Category")
    print("3. Export Report")
    print("4. Back to Reports Menu")
    print("========================================")

def prompt_for_date_range():
    """Get the start and end dates from the user."""
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    return start_date, end_date

def prompt_for_category_filter():
    """Get one or more categories from the user."""
    categories = input("Enter category or categories, separated by commas: ")

    selected_categories = [category.strip() for category in categories.split(",")]

    return selected_categories

def prompt_for_time_period():
    """Get the time period grouping from the user."""
    print()
    print("Choose a time period grouping:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    print("4. Yearly")

    choice = input("Enter your selection: ")

    return choice

def prompt_for_export_format():
    """Get the desired output format from the user."""
    print()
    print("Choose an output format:")
    print("1. CSV")
    print("2. JSON")
    print("3. TXT")

    choice = input("Enter your selection: ")

    return choice

def format_report_output(report_data):
    """Pretty-print report data for readability."""
    print()
    print("========================================")
    print("             REPORT RESULTS")
    print("========================================")

    for item, value in report_data.items():
        print(f"{item}: {value}")

    print("========================================")

def display_pagination(current_page, total_pages):
    """Display pagination information for long reports."""
    print()
    print(f"Page {current_page} of {total_pages}")

    if current_page < total_pages:
        print("Enter 'n' for next page.")
    
    if current_page > 1:
        print("Enter 'p' for previous page.")

    print("Enter 'q' to return.")

def add_report_summary(report_data):
    """Show totals and key statistics from a report."""
    print()
    print("========================================")
    print("            REPORT SUMMARY")
    print("========================================")

    for item, value in report_data.items():
        print(f"{item}: {value}")

    print("========================================")


def add_section_headers(title):
    """Add a header to organize report output into sections."""
    print()
    print("========================================")
    print(f"            {title}")
    print("========================================")

def show_back_option():
    """Return to the previous menu."""
    return "0"

def show_exit_option():
    """Show an option for the user to exit the program."""
    return "6"

def handle_navigation(choice, menu_stack):
    """Track menu navigation using a menu stack."""
    if choice == "0":
        if menu_stack:
            return menu_stack.pop()
        return None

    elif choice == "6":
        return "exit"

    menu_stack.append(choice)
    return choice

def return_to_previous_menu(menu_stack):
    """Go back one level in the menu stack."""
    if len(menu_stack) > 1:
        menu_stack.pop()
        return menu_stack[-1]

    return None

def format_table(headers, rows):
    """Display data in table format."""
    print()
    print(" | ".join(headers))
    print("-" * 50)

    for row in rows:
        print(" | ".join(str(value) for value in row))

def format_currency(amount):
    """Format an amount as a dollar value."""
    return f"${amount:,.2f}"

def add_visual_separator():
    """Add a visual separator to improve readability."""
    print("-" * 50)

def display_help():
    """Show command help text."""
    print()
    print("========================================")
    print("                 HELP")
    print("========================================")
    print("1. View Reports       - View financial reports")
    print("2. Filter by Date     - Filter transactions by date")
    print("3. Filter by Category - Filter transactions by category")
    print("4. Export Data        - Export financial data")
    print("5. Help               - Show this help information")
    print("6. Exit               - Exit the program")
    print("========================================")

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
