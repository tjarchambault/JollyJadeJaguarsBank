"""
Custom exception classes for JollyJadeJaguarsBank.

Course: MSMIS 2028
Team: JollyJadeJaguars
Module: Exception Handling & Validation
Purpose: Centralized exception definitions for the application
Date: August 23, 2026

This module defines all custom exceptions used throughout the application
to provide clear, specific error handling and debugging information.
"""


class JollyJadeJaguarsException(Exception):
    """Base exception class for all JollyJadeJaguarsBank exceptions.
    
    All custom exceptions inherit from this to allow catching all
    application-specific errors with a single except clause.
    """
    pass


class InvalidTransactionError(JollyJadeJaguarsException):
    """Raised when a transaction object contains invalid data.
    
    This is a general-purpose exception for transaction data validation
    failures. Use more specific exceptions below when appropriate.
    
    Example:
        raise InvalidTransactionError("Transaction missing required fields")
    """
    pass


class InvalidAmountError(InvalidTransactionError):
    """Raised when transaction amount is invalid.
    
    Amount must be a positive number (int, float, or Decimal).
    
    Validation rules:
        - Must be numeric (int, float, or Decimal)
        - Must be greater than 0
        - Should not exceed reasonable currency limits
    
    Example:
        raise InvalidAmountError("Amount must be positive, got -50.00")
    """
    pass


class InvalidDateError(InvalidTransactionError):
    """Raised when transaction date is invalid.
    
    Date must be a valid calendar date in the past or present.
    
    Validation rules:
        - Must be valid calendar date (YYYY-MM-DD format)
        - Cannot be in the future
        - Must handle leap years correctly
    
    Example:
        raise InvalidDateError("Date cannot be in the future: 2027-01-01")
    """
    pass


class InvalidCategoryError(InvalidTransactionError):
    """Raised when transaction category is invalid or not found.
    
    Category must exist in the predefined list or user-defined categories.
    
    Validation rules:
        - Must be in the category list
        - Case-sensitive matching
        - Cannot be empty
    
    Example:
        raise InvalidCategoryError("Category 'InvalidCat' not found")
    """
    pass


class InvalidTransactionTypeError(InvalidTransactionError):
    """Raised when transaction type is not 'income' or 'expense'.
    
    Type must be exactly 'income' or 'expense'.
    
    Validation rules:
        - Must be one of: 'income' or 'expense'
        - Case-sensitive
    
    Example:
        raise InvalidTransactionTypeError("Type must be 'income' or 'expense', got 'revenue'")
    """
    pass


class DuplicateTransactionError(InvalidTransactionError):
    """Raised when attempting to create a transaction with duplicate ID.
    
    Each transaction must have a unique ID. This prevents accidental
    overwriting of existing transactions.
    
    Example:
        raise DuplicateTransactionError(f"Transaction {tx_id} already exists")
    """
    pass


class StorageError(JollyJadeJaguarsException):
    """Raised when file I/O operations fail.
    
    This covers all storage layer errors including file not found,
    permission issues, and corrupted data.
    
    Example:
        raise StorageError("Cannot write to transactions.csv: Permission denied")
    """
    pass


class FileNotFoundError(StorageError):
    """Raised when a required data file is missing.
    
    Example:
        raise FileNotFoundError("transactions.csv not found in data/")
    """
    pass


class CorruptedDataError(StorageError):
    """Raised when CSV data is corrupted or unreadable.
    
    This includes malformed headers, inconsistent field counts,
    or invalid data types in CSV records.
    
    Example:
        raise CorruptedDataError("Row 5: Expected 6 fields, got 4")
    """
    pass


class CategoryError(JollyJadeJaguarsException):
    """Raised when category operations fail.
    
    This covers loading, validating, adding, or managing categories.
    
    Example:
        raise CategoryError("Failed to load categories from categories.csv")
    """
    pass


class SummaryCalculationError(JollyJadeJaguarsException):
    """Raised when summary report calculations fail.
    
    This includes date range errors, empty datasets, or calculation issues.
    
    Example:
        raise SummaryCalculationError("End date must be >= start date")
    """
    pass


class InvalidDateRangeError(SummaryCalculationError):
    """Raised when provided date range is invalid.
    
    Validation rules:
        - End date must be >= start date
        - Dates must be valid calendar dates
        - Range should be within reasonable bounds
    
    Example:
        raise InvalidDateRangeError("Start date (2026-09-01) > end date (2026-08-01)")
    """
    pass


class VisualizationError(JollyJadeJaguarsException):
    """Raised when visualization generation fails.
    
    This covers Turtle graphics errors, image saving issues, or data errors.
    
    Example:
        raise VisualizationError("No transaction data to visualize")
    """
    pass


class CLIError(JollyJadeJaguarsException):
    """Raised when CLI operations encounter errors.
    
    This covers invalid user input, menu navigation, or command execution.
    
    Example:
        raise CLIError("Invalid menu selection: '99'")
    """
    pass


# Exception hierarchy reference:
#
# JollyJadeJaguarsException (base)
# ├── InvalidTransactionError
# │   ├── InvalidAmountError
# │   ├── InvalidDateError
# │   ├── InvalidCategoryError
# │   ├── InvalidTransactionTypeError
# │   └── DuplicateTransactionError
# ├── StorageError
# │   ├── FileNotFoundError
# │   └── CorruptedDataError
# ├── CategoryError
# ├── SummaryCalculationError
# │   └── InvalidDateRangeError
# ├── VisualizationError
# └── CLIError
