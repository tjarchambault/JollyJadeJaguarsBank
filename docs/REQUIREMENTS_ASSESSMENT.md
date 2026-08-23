# JollyJadeJaguarsBank - Requirements Assessment & Feature Specification

**Course**: MSMIS 2028  
**Project**: Personal Finance Tracker  
**Team**: JollyJadeJaguars  
**Assessment Date**: August 23, 2026  
**Document Version**: 1.0

---

## Executive Summary

Your team has established an excellent project foundation with proper directory structure, development workflow documentation, and team role assignments. This document maps your planned architecture to the official course requirements and provides detailed feature specifications for each phase.

**Current Status**: ✅ **Phase 1 Planning Complete** - Ready to move to Phase 2 implementation

---

## Part 1: Requirements Compliance Matrix

### Official Project Requirements

The Personal Finance Tracker must implement the following **core requirements**:

| Requirement | Your Implementation | Status | Phase |
|-------------|-------------------|--------|-------|
| **1. Integrated Development Environment** | Python 3.10+ with pytest & virtual environment | ✅ Defined | All |
| **2. Modularity** | 7 source modules with clear separation of concerns | ✅ Planned | All |
| **3. Transaction Recording** | `transactions.py` + CLI module | ✅ Planned | Phase 2 |
| **4. Categorization** | `categories.py` module + transaction integration | ✅ Planned | Phase 2 |
| **5. Summary Generation** | `summaries.py` module (weekly/monthly reports) | ✅ Planned | Phase 3 |
| **6. Visualization** | `visualizations.py` with Turtle Graphics | ✅ Planned | Phase 4 |
| **7. External Libraries Documentation** | `requirements.txt` + phase reports | ✅ Started | All |
| **8. Code Documentation** | Module docstrings, function comments planned | ⚠️ To Be Implemented | All |

---

## Part 2: Detailed Feature Specifications by Phase

### PHASE 1: PROJECT PROPOSAL (Due Aug 30, 2026)

**Status**: 🟢 **IN PROGRESS**

#### Phase 1 Requirements

Your proposal must document:

1. ✅ **Project Overview (500 points)**
   - What you've done: README.md provides clear overview
   - **Still needed**: Expand with problem statement, target users, and specific financial goals

2. ✅ **Design and Features (1000 points)**
   - What you've done: Module structure defined in README.md
   - **Still needed**: 
     - Architecture diagram showing module interactions
     - Data flow diagrams
     - Class structure for Transaction object
     - Database schema (CSV structure)

3. ⚠️ **Data Validation and Exceptions (1000 points)**
   - What you've done: Mentioned in DEVELOPMENT.md
   - **Still needed**:
     - List all input validation rules (amount ranges, date formats, category constraints)
     - Define custom exception types (InvalidTransactionError, etc.)
     - Error handling strategy document
     - Edge cases to handle

4. ⚠️ **External Libraries (500 points)**
   - What you've done: Basic requirements.txt with pytest
   - **Still needed**:
     - Justify why Turtle is used for visualization
     - Explain which std library modules you'll leverage (csv, datetime, decimal, json, turtle)
     - Document optional dependencies (pandas, matplotlib) if considered
     - Licensing compliance notes

5. ✅ **Timeline and Task Allocation (500 points)**
   - What you've done: Module responsibilities assigned in README.md
   - **Still needed**: Detailed sprint breakdown with weekly milestones

6. ⚠️ **Generative AI Use (500 points)**
   - What you've done: AI usage policy documented
   - **Still needed**:
     - Specific examples of how AI will be used (code review, design brainstorming)
     - Verification strategy for AI-generated code
     - Team commitment to understanding and testing all code

7. ✅ **Documentation and Formatting (500 points)**
   - Your docs are well-organized and professional

8. ⚠️ **Writing Mechanics (500 points)**
   - Proofread all deliverables before submission

#### Phase 1 Deliverables Checklist

- [ ] Project Proposal PDF (consolidated from this document)
- [ ] System Architecture Diagram
- [ ] Data Schema Definition (CSV structure)
- [ ] Exception/Validation Strategy Document
- [ ] Team Roles & Responsibilities with timeline
- [ ] Risk Assessment & Mitigation Plan

---

### PHASE 2: TRANSACTION RECORDING (Due Sep 13, 2026)

**Status**: 🟡 **READY TO START**

#### Phase 2 Requirements

Implement core transaction management functionality:

1. **Transaction Recording** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/transactions.py
   
   Data Model (Transaction Class):
   ├── amount (Decimal) - transaction amount
   ├── date (datetime.date) - transaction date
   ├── category (str) - transaction category
   ├── description (str) - optional transaction description
   ├── transaction_type (str) - 'income' or 'expense'
   ├── transaction_id (UUID) - unique identifier
   └── Methods:
       ├── __init__(...) - constructor with validation
       ├── to_dict() - export to dictionary
       ├── from_dict() - import from dictionary
       ├── validate() - data validation
       └── get_summary() - formatted output
   ```

2. **Data Persistence** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/storage.py
   
   Functions:
   ├── save_transaction(transaction) - write to CSV
   ├── load_transactions() - read from CSV
   ├── load_transaction(transaction_id) - retrieve one record
   ├── update_transaction(transaction) - modify existing
   ├── delete_transaction(transaction_id) - remove record
   └── get_all_transactions() - return full list
   
   CSV Format (transactions.csv):
   transaction_id, date, amount, type, category, description
   uuid-1234-5678, 2026-08-23, 1500.00, income, salary, Monthly salary
   uuid-2345-6789, 2026-08-20, 45.99, expense, groceries, Weekly groceries
   ```

3. **Categorization System** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/categories.py
   
   Default Categories:
   ├── Income: [Salary, Freelance, Investment, Bonus, Other]
   ├── Expense: [Food, Utilities, Entertainment, Transportation, Healthcare, Shopping, Savings, Other]
   
   Functions:
   ├── load_categories() - get valid categories
   ├── validate_category(category, type) - verify category exists
   ├── add_category(name, type) - user-defined categories
   ├── list_categories(type) - display available categories
   └── get_category_list() - return all as list
   ```

4. **Command-Line Interface (Phase 2)** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/cli.py (Phase 2 subset)
   
   Menu Options:
   1. Add Transaction
      ├── Prompt for date
      ├── Prompt for amount (validate numeric)
      ├── Prompt for type (income/expense)
      ├── Prompt for category (show available)
      ├── Prompt for description
      └── Confirm and save
   
   2. View All Transactions
      ├── Display table format
      ├── Show date, type, category, amount, description
      └── Total income/expense summary
   
   3. View Transactions by Category
      ├── Prompt for category
      ├── Filter and display matching transactions
      └── Show category totals
   
   4. Exit
   ```

5. **Input Validation** ✅ Planned
   
   **Required Validation Rules**:
   ```
   Amount:
   └── Must be Decimal or float > 0
   
   Date:
   ├── Must be valid calendar date
   ├── Cannot be in future (optional business rule)
   └── Format: YYYY-MM-DD
   
   Category:
   └── Must be in predefined/user-defined list
   
   Type:
   └── Must be 'income' or 'expense'
   
   Description:
   └── Optional, max 500 characters
   ```

6. **Error Handling** ✅ Planned
   
   **Required Custom Exceptions**:
   ```
   exceptions.py:
   ├── InvalidTransactionError - bad transaction data
   ├── InvalidAmountError - amount validation failed
   ├── InvalidDateError - date validation failed
   ├── StorageError - file I/O problems
   ├── CategoryError - category not found
   └── DuplicateTransactionError - ID already exists
   ```

7. **Unit Tests** ✅ Planned
   
   **Required Test Coverage**:
   ```
   tests/test_transactions.py:
   ├── test_transaction_creation_valid
   ├── test_transaction_creation_invalid_amount
   ├── test_transaction_creation_invalid_date
   ├── test_transaction_validation
   └── test_transaction_to_from_dict
   
   tests/test_storage.py:
   ├── test_save_transaction
   ├── test_load_transactions
   ├── test_update_transaction
   ├── test_delete_transaction
   └── test_csv_file_format
   
   tests/test_categories.py:
   ├── test_load_default_categories
   ├── test_validate_category_valid
   ├── test_validate_category_invalid
   └── test_add_custom_category
   ```

#### Phase 2 Deliverables

```
Phase 2 Submission:
├── docs/Phase-2-Project-Report.pdf
│   ├── Progress on each requirement
│   ├── Module descriptions
│   ├── How to run (main.py instructions)
│   ├── User instructions with examples
│   ├── Challenges encountered & solutions
│   ├── AI usage documentation
│   └── Future improvements
└── Phase2_JollyJadeJaguars.zip
    ├── src/
    │   ├── main.py - entry point, calls CLI
    │   ├── transactions.py - Transaction class ✅
    │   ├── storage.py - CSV read/write ✅
    │   ├── categories.py - Category management ✅
    │   ├── cli.py - User interface (Phase 2 subset) ✅
    │   └── exceptions.py - Custom exceptions ✅
    ├── tests/
    │   ├── test_transactions.py ✅
    │   ├── test_storage.py ✅
    │   ├── test_categories.py ✅
    │   └── conftest.py - shared fixtures
    ├── data/
    │   ├── transactions.csv - sample data
    │   └── categories.csv - default categories
    ├── docs/
    │   ├── Phase-1-Project-Proposal.pdf
    │   ├── Phase-2-Project-Report.pdf
    │   ├── DEVELOPMENT.md
    │   └── REQUIREMENTS_ASSESSMENT.md
    └── requirements.txt - pytest, pytest-cov
```

#### Phase 2 Testing Checklist

- [ ] All unit tests pass: `pytest tests/ -v`
- [ ] Code coverage > 80%: `pytest --cov=src`
- [ ] No syntax errors: `python -m py_compile src/*.py`
- [ ] Can add transaction via CLI
- [ ] Can view all transactions
- [ ] CSV file persists data between runs
- [ ] Category validation works
- [ ] Invalid inputs are rejected

---

### PHASE 3: REPORTING & EXCEPTION HANDLING (Due Sep 27, 2026)

**Status**: 🟡 **READY AFTER PHASE 2**

#### Phase 3 Requirements

Add reporting, visualization prep, and comprehensive error handling:

1. **Summary Generation** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/summaries.py
   
   Report Types:
   
   1. Daily Summary
      ├── Date as parameter
      ├── Total income
      ├── Total expenses
      └── Net (income - expenses)
   
   2. Weekly Summary
      ├── Week dates (Mon-Sun)
      ├── Income by category
      ├── Expenses by category
      ├── Weekly total
      └── Comparison to previous week
   
   3. Monthly Summary
      ├── Month/Year as parameter
      ├── Income breakdown by category
      ├── Expense breakdown by category
      ├── Savings (income - expenses)
      ├── Average daily transaction
      └── Trend from previous month
   
   4. Category Summary
      ├── Show all transactions in category
      ├── Total amount spent/earned
      ├── Number of transactions
      └── Average per transaction
   
   Functions:
   ├── get_daily_summary(date)
   ├── get_weekly_summary(week_start)
   ├── get_monthly_summary(year, month)
   ├── get_category_summary(category, type)
   ├── get_date_range_summary(start_date, end_date)
   └── calculate_savings_rate()
   ```

2. **Enhanced Exception Handling** ✅ Planned
   
   **Required Implementation**:
   ```
   Updates to all modules:
   
   src/transactions.py:
   ├── Validate amount is positive
   ├── Validate date format and logic
   ├── Handle missing fields
   └── Raise custom exceptions
   
   src/storage.py:
   ├── Handle missing CSV file
   ├── Handle corrupted CSV data
   ├── Handle file permission errors
   ├── Handle disk space issues
   └── Provide recovery options
   
   src/summaries.py:
   ├── Handle invalid date ranges
   ├── Handle empty result sets
   ├── Handle calculation errors
   └── Provide meaningful error messages
   ```

3. **Advanced CLI Features** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/cli.py (Phase 3 additions)
   
   Menu Options:
   1-3. (Previous from Phase 2)
   
   4. View Daily Summary
      ├── Prompt for date
      ├── Display day's income/expenses
      └── Show running balance
   
   5. View Weekly Summary
      ├── Show this week vs. last week
      ├── Display category breakdown
      └── Savings rate
   
   6. View Monthly Summary
      ├── Prompt for month/year
      ├── Detailed breakdown
      ├── Year-to-date totals
      └── Comparisons
   
   7. Generate Report
      ├── Choose date range
      ├── Choose format (table, list, summary)
      └── Save to file or display
   ```

4. **Data Validation Enhancements** ✅ Planned
   
   **Required Validations**:
   ```
   Add to existing validations:
   
   Date Ranges:
   ├── End date >= Start date
   ├── Dates within reasonable bounds
   └── Handle leap years correctly
   
   Category Filtering:
   ├── Case-insensitive matching
   ├── Partial name matching (optional)
   └── Show suggestions for typos
   
   Amount Aggregations:
   ├── Handle decimal precision (use Decimal class)
   ├── Verify currency consistency
   └── Check for overflow in totals
   
   Edge Cases:
   ├── Empty transaction history
   ├── Single transaction summaries
   ├── Leap day transactions
   └── Year boundary transitions
   ```

5. **Comprehensive Testing** ✅ Planned
   
   **Required Test Coverage**:
   ```
   tests/test_summaries.py:
   ├── test_daily_summary_valid
   ├── test_daily_summary_empty
   ├── test_weekly_summary
   ├── test_monthly_summary
   ├── test_category_summary
   ├── test_date_range_summary
   └── test_invalid_date_range
   
   tests/test_error_handling.py:
   ├── test_invalid_amount
   ├── test_invalid_date
   ├── test_invalid_category
   ├── test_missing_file
   ├── test_corrupted_csv
   └── test_empty_database
   ```

6. **Logging System** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/logger.py
   
   Setup:
   ├── Log file: logs/app.log
   ├── Console output for errors
   ├── Rotation when file > 10MB
   
   Log Levels:
   ├── DEBUG - detailed flow information
   ├── INFO - general information (transactions added, etc.)
   ├── WARNING - data inconsistencies, handled errors
   ├── ERROR - unhandled exceptions
   └── CRITICAL - system failures
   
   Log Points:
   ├── Transaction creation/modification/deletion
   ├── CSV file operations
   ├── Summary calculations
   ├── All exceptions caught
   └── Report generation
   ```

#### Phase 3 Deliverables

```
Phase 3 Submission:
├── docs/Phase-3-Project-Report.pdf
└── Phase3_JollyJadeJaguars.zip
    ├── src/
    │   ├── main.py - updated entry point
    │   ├── transactions.py - enhanced validation
    │   ├── storage.py - robust error handling
    │   ├── categories.py
    │   ├── summaries.py - ALL REPORTS ✅
    │   ├── cli.py - Phase 3 full menu ✅
    │   ├── exceptions.py - expanded exceptions ✅
    │   └── logger.py - logging system ✅
    ├── tests/
    │   ├── test_transactions.py
    │   ├── test_storage.py
    │   ├── test_categories.py
    │   ├── test_summaries.py ✅
    │   ├── test_error_handling.py ✅
    │   └── conftest.py
    ├── data/
    │   ├── transactions.csv
    │   ├── categories.csv
    │   └── logs/app.log (generated)
    └── docs/
        ├── Phase-1-Project-Proposal.pdf
        ├── Phase-2-Project-Report.pdf
        ├── Phase-3-Project-Report.pdf
        ├── DEVELOPMENT.md
        └── REQUIREMENTS_ASSESSMENT.md
```

---

### PHASE 4: USER INTERFACE & VISUALIZATIONS (Due Oct 11, 2026)

**Status**: 🔵 **PLANNED**

#### Phase 4 Requirements

Complete project with visualizations and final polish:

1. **Turtle Graphics Visualizations** ✅ Planned (REQUIRED)
   
   **Required Implementation**:
   ```
   Module: src/visualizations.py
   
   Visualization 1: Income vs. Expenses Bar Chart
   ├── Horizontal or vertical bars
   ├── Monthly breakdown
   ├── Color-coded (income=green, expense=red)
   ├── Labels with amounts
   └── Title and axis labels
   
   Visualization 2: Expense Category Pie Chart
   ├── Circle chart showing expense distribution
   ├── Each category as different color
   ├── Percentage labels
   ├── Legend with category names
   └── Title
   
   Visualization 3: Savings Trend Line
   ├── Line graph showing cumulative savings over time
   ├── X-axis: dates or weeks
   ├── Y-axis: cumulative amount
   ├── Grid lines for reference
   └── Start date to current date
   
   Visualization 4: Category Spending (Your Choice)
   ├── Could be: stacked bar, multiple line, scatter, etc.
   ├── Shows spending patterns
   ├── Interactive if possible
   └── Provides financial insight
   
   Functions:
   ├── draw_income_vs_expenses(transactions, period)
   ├── draw_category_distribution(transactions, type)
   ├── draw_savings_trend(transactions)
   ├── draw_custom_chart(data, chart_type)
   └── save_visualization(filename)
   ```

2. **Enhanced CLI (Phase 4)** ✅ Planned
   
   **Required Implementation**:
   ```
   Module: src/cli.py (Phase 4 additions)
   
   Menu Options:
   1-7. (Previous from Phase 3)
   
   8. View Visualizations
      ├── Choose visualization type
      ├── Choose date range
      ├── Display Turtle graphics
      ├── Option to save as image
      └── Return to menu
   
   9. Export Report
      ├── Choose format (text, CSV, JSON)
      ├── Choose date range
      ├── Save to file
      └── Show save location
   
   10. Settings
       ├── Default currency
       ├── Budget limits (optional)
       ├── Category preferences
       └── Display preferences
   
   11. Help
       └── Show usage instructions
   
   12. Exit
   ```

3. **Full Integration Testing** ✅ Planned
   
   **Required Test Coverage**:
   ```
   tests/test_visualizations.py:
   ├── test_visualization_creates_file
   ├── test_bar_chart_generation
   ├── test_pie_chart_generation
   ├── test_line_chart_generation
   ├── test_visualization_with_empty_data
   └── test_visualization_with_large_dataset
   
   tests/test_integration.py:
   ├── test_add_transaction_to_summary_to_report
   ├── test_full_workflow_with_multiple_transactions
   ├── test_data_persistence_across_sessions
   ├── test_report_generation_with_visualization
   └── test_cli_menu_navigation
   ```

4. **Documentation Completion** ✅ Planned
   
   **Required Documentation**:
   ```
   Project Report must include:
   ├── Complete feature summary
   ├── How to install and run
   ├── Step-by-step user guide
   ├── Example input/output
   ├── All challenges and solutions
   ├── AI usage throughout project
   ├── Future enhancement ideas
   ├── Code quality metrics
   └── Team contribution summary
   
   Code Documentation:
   ├── All functions have docstrings
   ├── Complex logic has inline comments
   ├── Module headers with course info
   ├── README for each major module
   └── API documentation
   ```

5. **Code Quality & Performance** ✅ Planned
   
   **Required Implementation**:
   ```
   Code Review Checklist:
   ├── PEP 8 compliance
   ├── DRY principle (no code duplication)
   ├── Appropriate use of functions
   ├── Proper variable naming
   ├── No hardcoded values (use constants)
   ├── Performance optimized (O(n) or better)
   └── Memory efficient
   
   Test Coverage:
   ├── Overall coverage > 85%
   ├── All functions tested
   ├── Edge cases covered
   ├── Error paths tested
   └── Integration tests pass
   ```

#### Phase 4 Deliverables

```
Phase 4 Submission (FINAL):
├── docs/Phase-4-Final-Project-Report.pdf
└── Phase4_JollyJadeJaguars.zip
    ├── src/
    │   ├── main.py - fully integrated
    │   ├── transactions.py
    │   ├── storage.py
    │   ├── categories.py
    │   ├── summaries.py
    │   ├── visualizations.py - FULL IMPLEMENTATION ✅
    │   ├── cli.py - COMPLETE MENU ✅
    │   ├── exceptions.py
    │   ├── logger.py
    │   └── __init__.py - package initialization
    ├── tests/
    │   ├── test_transactions.py
    │   ├── test_storage.py
    │   ├── test_categories.py
    │   ├── test_summaries.py
    │   ├── test_error_handling.py
    │   ├── test_visualizations.py ✅
    │   ├── test_integration.py ✅
    │   └── conftest.py
    ├── data/
    │   ├── transactions.csv
    │   ├── categories.csv
    │   └── logs/app.log
    ├── images/
    │   ├── income_vs_expenses.png
    │   ├── category_distribution.png
    │   ├── savings_trend.png
    │   └── [additional visualizations]
    ├── docs/
    │   ├── Phase-1-Project-Proposal.pdf
    │   ├── Phase-2-Project-Report.pdf
    │   ├── Phase-3-Project-Report.pdf
    │   ├── Phase-4-Final-Project-Report.pdf
    │   ├── DEVELOPMENT.md
    │   ├── REQUIREMENTS_ASSESSMENT.md
    │   ├── API_DOCUMENTATION.md (new)
    │   └── USER_GUIDE.md (new)
    ├── .gitignore
    ├── requirements.txt - with all dependencies
    └── README.md - updated with all features
```

---

## Part 3: Team Task Allocation for Each Phase

### Phase 2 (Sep 13) Task Grid

| Task | Owner | Depends On | Estimated Hrs |
|------|-------|-----------|-----------------|
| Transaction Model | Dev 1 | Categories module | 4-6 |
| Storage/CSV Layer | Dev 2 | Transaction model | 5-7 |
| Categories Module | Lead | Nothing | 3-4 |
| Input Validation | Dev 3 | Transaction model | 3-5 |
| CLI Interface (Phase 2) | Dev 1 | All above | 6-8 |
| Unit Tests | Dev 4 | All modules | 8-10 |
| Documentation | Lead | All above | 4-6 |

**Parallel Work Opportunities**: Dev 1 (model), Dev 2 (storage), Lead (categories) can work simultaneously after initial design meeting.

### Phase 3 (Sep 27) Task Grid

| Task | Owner | Depends On | Estimated Hrs |
|------|-------|-----------|-----------------|
| Summary Reports | Dev 1 | Phase 2 complete | 8-10 |
| Exception Handling | Dev 3 | Phase 2 modules | 6-8 |
| Advanced CLI | Dev 1 | Summary reports | 5-7 |
| Logging System | Dev 4 | Phase 2 complete | 4-5 |
| Test Suite Expansion | Dev 4 | All new features | 10-12 |
| Error Scenarios | Dev 2, 3 | New features | 4-6 |
| Documentation | Lead | All above | 5-7 |

### Phase 4 (Oct 11) Task Grid

| Task | Owner | Depends On | Estimated Hrs |
|------|-------|-----------|-----------------|
| Turtle Visualizations | Dev 3 | Phase 3 complete | 10-12 |
| Final CLI Polish | Dev 1 | Phase 3 complete | 4-5 |
| Integration Testing | Dev 4 | All modules | 8-10 |
| Code Review & Refactor | All | All modules | 6-8 |
| Documentation Finalization | Lead | All above | 6-8 |
| Testing Edge Cases | Dev 2, 3 | All modules | 6-8 |

---

## Part 4: Data Structures Reference

### Transaction Object Schema

```python
class Transaction:
    """
    Represents a single financial transaction.
    
    Attributes:
        transaction_id (str): Unique UUID
        date (datetime.date): Transaction date (YYYY-MM-DD)
        amount (Decimal): Amount in currency units (positive)
        type (str): 'income' or 'expense'
        category (str): Valid category name
        description (str): Optional details (max 500 chars)
    """
```

### CSV Schema (transactions.csv)

```csv
transaction_id,date,amount,type,category,description
550e8400-e29b-41d4-a716-446655440001,2026-08-23,1500.00,income,salary,August paycheck
550e8400-e29b-41d4-a716-446655440002,2026-08-20,45.99,expense,groceries,Weekly groceries
550e8400-e29b-41d4-a716-446655440003,2026-08-18,120.00,expense,utilities,Electric bill
```

### Categories (categories.csv)

```csv
category,type,description
Salary,income,Regular employment income
Freelance,income,Contract work
Investment,income,Investment returns
Bonus,income,Performance bonus
Food,expense,Groceries and restaurants
Utilities,expense,Water, electric, gas
Entertainment,expense,Movies, games, hobbies
Transportation,expense,Gas, transit, parking
Healthcare,expense,Medical, pharmacy
Shopping,expense,Clothing, household
Savings,expense,Transfers to savings
```

---

## Part 5: Success Criteria Checklist

### Phase 2 Success = All of:
- [ ] All 7 source modules exist with proper structure
- [ ] Transaction class fully implements CRUD operations
- [ ] CSV storage works without errors
- [ ] CLI can add, view, filter transactions
- [ ] Unit test coverage > 80%
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Phase 2 Report documents all features
- [ ] No unhandled exceptions when running

### Phase 3 Success = All of (+ Phase 2):
- [ ] 4 different report types generate correctly
- [ ] Exception handling covers all error cases
- [ ] CLI reports menu works
- [ ] Logging captures all important events
- [ ] Tests for summaries and errors pass
- [ ] Test coverage > 85%
- [ ] Phase 3 Report documents improvements

### Phase 4 Success = All of (+ Phases 2-3):
- [ ] 4 Turtle visualizations display correctly
- [ ] Visualizations save as image files
- [ ] Full CLI menu navigable without errors
- [ ] Integration tests pass
- [ ] All code documented with docstrings
- [ ] Test coverage > 85%
- [ ] Project runs end-to-end without errors
- [ ] Final Report is comprehensive

---

## Part 6: Common Pitfalls to Avoid

### Coding Pitfalls
- ❌ Hardcoding dates, amounts, or categories → ✅ Use constants or config files
- ❌ Using floats for money → ✅ Use `Decimal` class
- ❌ No input validation → ✅ Validate everything with clear error messages
- ❌ Catching generic `Exception` → ✅ Use custom exceptions
- ❌ No docstrings or comments → ✅ Document every module and function

### Architecture Pitfalls
- ❌ Mixing data model and file I/O logic → ✅ Separate into modules
- ❌ CLI directly reading/writing files → ✅ Use storage layer abstraction
- ❌ Hardcoded category list → ✅ Load from CSV or config

### Testing Pitfalls
- ❌ Only testing happy path → ✅ Test error cases and edge cases
- ❌ No fixtures or test data → ✅ Use conftest.py for shared setup
- ❌ Tests depend on external files → ✅ Mock file operations

### Collaboration Pitfalls
- ❌ Multiple people editing same file → ✅ Use feature branches, merge frequently
- ❌ No agreed interface contracts → ✅ Define function signatures upfront
- ❌ Silent merge conflicts → ✅ Use pull request reviews

---

## Next Steps

1. **Before Phase 2 (by Aug 29)**
   - Finalize and submit Phase 1 Project Proposal
   - Create branches for each developer
   - Distribute this requirements document to team

2. **Week 1 of Phase 2 (Aug 26-30)**
   - Hold design review meeting
   - Finalize Transaction class interface
   - Assign specific functions to each developer

3. **Week 2 of Phase 2 (Sep 2-7)**
   - All modules completed and tested individually
   - Begin integration testing
   - Start Phase 2 Project Report

4. **Week 3 of Phase 2 (Sep 8-13)**
   - Final testing and bug fixes
   - Complete Phase 2 Project Report
   - Submit deliverables

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Aug 23, 2026 | Initial assessment and requirements alignment |

---

**Prepared by**: GitHub Copilot  
**For Team**: JollyJadeJaguars  
**Course**: MSMIS 2028 - Python Programming Project  
**Status**: Ready for Team Review

