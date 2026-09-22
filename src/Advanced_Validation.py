# PROGRAM: Personal Finance Tracker - Advanced_Validation.py
# PURPOSE: Validate report criteria and command-line input.
# INPUT: Dates, amounts, report options, category names, and menu choices.
# PROCESS: Normalize values, check constraints, and suggest corrections.
# OUTPUT: Validated values, helpful ValueError messages, and retry decisions.
# HONOR CODE: On my honor, as an Aggie, I have neither given nor
#             received unauthorized aid on this academic work.

"""Report and CLI input validation for the ISTM 601 Personal Finance Tracker.

Validators return normalized values and raise ValueError for invalid input.
Dates use YYYY-MM-DD, bounds are inclusive, and amounts use Decimal.
Only prompt_retry performs input/output; the other helpers are pure functions.
"""

# =====================================================
# HOW TO READ THIS FILE
# =====================================================
#
# A function is a reusable task. Its parameters are the information it receives.
# A return statement sends an answer back to the code that requested the task.
# Validation means checking input before a report or menu tries to use it.
# "Normalized" means a consistent form: for example, " CSV " becomes "csv".
# None means no value was supplied; it is different from zero or empty text.
# Raising ValueError stops the current task and explains what input was wrong.
# The calling CLI should catch that error, display it, and offer another try.
# Functions here do not generate reports or save files; they check the inputs.
# =====================================================

# =====================================================
# PYTHON TOOLS
# =====================================================
#
# These imports provide the tools used to check user input.
# =====================================================

# Imports give this file access to tools already included with Python.
# Mapping identifies dictionaries and similar collections of named values.
from collections.abc import Mapping
# date represents a calendar day; datetime also includes a time of day.
from datetime import date, datetime
# Decimal stores decimal numbers without the usual binary rounding artifacts.
# InvalidOperation identifies text that Decimal cannot interpret as a number.
from decimal import Decimal, InvalidOperation
# This tool compares spellings to suggest likely corrections for typing errors.
from difflib import get_close_matches
# re checks whether text follows a pattern, such as four digits for a year.
import re

# =====================================================
# DEFAULT CHOICES AND SETTINGS
# =====================================================
#
# Keep the accepted options and spelling settings together.
# =====================================================

# These named constants collect the default choices in one easy-to-edit place.
# Uppercase names mark settings that functions should not change while running.
# Parentheses group the choices into tuples, which are fixed sequences of items.
REPORT_TYPES = ("daily", "weekly", "monthly", "category", "date_range")
TIME_PERIODS = ("daily", "weekly", "monthly", "yearly", "custom")
EXPORT_FORMATS = ("text", "csv", "json")
MAIN_MENU_OPTIONS = ("1", "2", "3", "4", "5", "6")
# Similarity scores run from 0 to 1. A suggestion must score at least 0.6.
# This is a spelling similarity score, not a probability that a guess is right.
SUGGESTION_SIMILARITY_CUTOFF = 0.6


# =====================================================
# ERROR MESSAGES AND SHARED HELPERS
# =====================================================
#
# Build clear messages and reuse the same choice-checking rules.
# =====================================================

def generate_validation_error_message(field, value, requirement):
    """Build a consistent error explaining the rejected value and correction."""
    # An f-string inserts values into the braces. !r shows a value in a form
    # that exposes details such as quotes around text or an empty string.
    # Example: Invalid amount: 'abc'. Enter a finite number.
    return f"Invalid {field}: {value!r}. {requirement}"


def suggest_correction(value, valid_options):
    """Return the closest case-insensitive option, or None if none is close."""
    # Spelling comparisons only make sense for text (Python calls it str).
    if not isinstance(value, str):
        return None
    # Build a lookup table: cleaned spelling -> original display spelling.
    # strip removes spaces at either end; casefold ignores letter case.
    # Keeping the original spelling lets us suggest "Food" instead of "food".
    options = {
        str(option).strip().casefold(): str(option) for option in valid_options
    }
    # n=1 requests just the best match. Comparing dictionary keys uses the
    # cleaned spellings, so capitalization does not affect the suggestion.
    matches = get_close_matches(
        value.strip().casefold(),
        options,
        n=1,
        cutoff=SUGGESTION_SIMILARITY_CUTOFF,
    )
    # [0] selects the first match; Python counts positions starting at zero.
    # An empty matches list means nothing was similar enough to suggest.
    return options[matches[0]] if matches else None


def _validate_choice(value, options, field):
    """Validate a text choice and preserve its canonical spelling."""
    # The leading underscore marks a helper intended for use inside this file.
    # Save the options as a tuple so matching and suggestions can reuse them,
    # even if the caller supplied a collection that can be read only once.
    options = tuple(options)
    # Check each allowed option. Returning immediately ends this function once
    # an exact match is found after ignoring surrounding spaces and case.
    if isinstance(value, str):
        for option in options:
            if value.strip().casefold() == option.casefold():
                return option
    # Reaching here means no valid choice matched. join builds a readable list
    # such as "daily, weekly, monthly" to explain what the user can enter.
    requirement = f"Choose one of: {', '.join(options)}."
    suggestion = suggest_correction(value, options)
    if suggestion is not None:
        requirement += f" Did you mean {suggestion!r}?"
    # A suggestion is advice only. Invalid input is never silently accepted.
    raise ValueError(
        generate_validation_error_message(field, value, requirement)
    )


# =====================================================
# DATE VALIDATION
# =====================================================
#
# Check calendar dates, allowed boundaries, and report ranges.
# =====================================================

def validate_date_format(value):
    """Return a date from a strict YYYY-MM-DD string or an existing date.

    Datetimes are rejected to avoid silently discarding time information.
    """
    # Other parts of the program may already have converted text into a date.
    # datetime is also considered a kind of date by Python, so exclude it.
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    # This pattern requires four year digits, two month digits, and two day
    # digits with hyphens between them. fullmatch checks the entire string.
    # The pattern checks the shape only; "2026-02-30" still needs a date check.
    if isinstance(value, str) and re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value
    ):
        try:
            # Python's calendar conversion checks month lengths and leap years.
            return date.fromisoformat(value)
        except ValueError:
            # pass continues to the shared error message below. It does not
            # accept the date or return a successful result.
            pass
    raise ValueError(
        generate_validation_error_message(
            "date", value, "Enter a real calendar date in YYYY-MM-DD format."
        )
    )


def check_date_boundaries(value, min_date=None, max_date=None):
    """Return a date within optional inclusive bounds; allow future dates."""
    # Convert the input and any supplied limits to dates before comparing them.
    # With no limit, use Python's earliest or latest supported calendar date.
    result = validate_date_format(value)
    lower = validate_date_format(min_date) if min_date is not None else date.min
    upper = validate_date_format(max_date) if max_date is not None else date.max
    # Reject contradictory limits before checking whether the date fits them.
    if lower > upper:
        raise ValueError("Minimum date must not be after maximum date.")
    # <= means "less than or equal to": both boundary dates are allowed.
    if not lower <= result <= upper:
        raise ValueError(
            generate_validation_error_message(
                "date",
                value,
                f"Choose a date from {lower.isoformat()} "
                f"to {upper.isoformat()}.",
            )
        )
    return result


def validate_report_date_range(
    start_date, end_date, min_date=None, max_date=None
):
    """Return (start, end); allow same-day reports and inclusive bounds."""
    # Reuse the single-date checks so both endpoints follow the same rules.
    start = check_date_boundaries(start_date, min_date, max_date)
    end = check_date_boundaries(end_date, min_date, max_date)
    # A report may cover one day, but it cannot run backward through time.
    if start > end:
        raise ValueError("Report start date must be on or before the end date.")
    # Return two dates together. The caller can receive them as start, end.
    return start, end


# =====================================================
# REPORT INPUT VALIDATION
# =====================================================
#
# Check report names, category selections, and time periods.
# =====================================================

def validate_report_type(value, valid_types=REPORT_TYPES):
    """Return a supported report name, matched without regard to case."""
    # Share the text-choice logic instead of repeating matching and errors.
    # The caller may supply a different valid_types list for another menu.
    return _validate_choice(value, valid_types, "report type")


def validate_category_filter(value, categories):
    """Return a canonical category name; None means no category restriction.

    categories must contain category names, supplied by the caller's data layer.
    Reject empty strings and unknown names, even with an empty catalog.
    """
    # None explicitly requests all categories. A blank string is not treated
    # as "all", because it may be an accidental missing answer.
    if value is None:
        return None
    # The caller supplies the actual category names; this file does not load
    # a CSV file or assume which categories a particular user has created.
    return _validate_choice(value, categories, "category")


def validate_time_period(value, valid_periods=TIME_PERIODS):
    """Return a supported period label; validate custom dates separately."""
    # This checks the label, such as "weekly". It does not calculate the dates
    # of that week; that is a separate responsibility of the reporting code.
    return _validate_choice(value, valid_periods, "time period")


# =====================================================
# NUMERIC VALIDATION
# =====================================================
#
# Check amounts and thresholds before using them in reports.
# =====================================================

def _parse_decimal(value, field):
    """Convert supported numeric input to a finite Decimal without rounding."""
    # Python treats True and False as numbers in some situations. Reject them
    # explicitly so a yes/no answer cannot accidentally become an amount.
    if isinstance(value, bool) or not isinstance(
        value, (str, int, float, Decimal)
    ):
        raise ValueError(
            generate_validation_error_message(
                field, value, "Enter a finite number."
            )
        )
    try:
        # Input from the keyboard is text. Decimal can read "12.50" directly.
        # Converting floats through text avoids exposing extra binary digits,
        # but cannot repair rounding already done before this function ran.
        result = Decimal(str(value).strip())
    except InvalidOperation:
        # Turn Decimal's technical conversion error into our normal input
        # error. "from None" hides that underlying error's chained traceback.
        raise ValueError(
            generate_validation_error_message(
                field, value, "Enter a finite number."
            )
        ) from None
    # Decimal also understands infinity and NaN ("not a number"). Neither
    # represents a usable amount, even though the conversion itself succeeded.
    if not result.is_finite():
        raise ValueError(
            generate_validation_error_message(
                field, value, "Enter a finite number."
            )
        )
    return result


def validate_numeric_range(value, min_value=None, max_value=None):
    """Return a finite Decimal inside optional inclusive numeric limits."""
    # Convert numbers and limits to the same type so comparisons are reliable.
    # A missing limit remains None, meaning this side has no restriction.
    result = _parse_decimal(value, "number")
    lower = (
        _parse_decimal(min_value, "minimum") if min_value is not None else None
    )
    upper = (
        _parse_decimal(max_value, "maximum") if max_value is not None else None
    )
    # First check the limits make sense; then check each supplied boundary.
    # Strict < and > comparisons allow values exactly equal to the limits.
    if lower is not None and upper is not None and lower > upper:
        raise ValueError("Minimum value must not exceed maximum value.")
    if lower is not None and result < lower:
        raise ValueError(f"Number must be at least {lower}.")
    if upper is not None and result > upper:
        raise ValueError(f"Number must be at most {upper}.")
    return result


def validate_threshold_input(value, min_value=0, max_value=None):
    """Return a threshold as Decimal; thresholds are nonnegative by default."""
    # A threshold is a cutoff amount, such as a spending alert at $100.
    # Reuse range validation; the default minimum of zero forbids negatives.
    return validate_numeric_range(value, min_value, max_value)


# =====================================================
# CLI INPUT VALIDATION
# =====================================================
#
# Check menu choices, export formats, and combined filters.
# =====================================================

def validate_menu_selection(value, valid_options=MAIN_MENU_OPTIONS):
    """Return a menu key as text; default to the CLI's choices 1 through 6."""
    # Accept keyboard text or an integer, but reject True, False, and decimals
    # such as 1.0. Those are not the menu keys shown to the user.
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError("Menu selection must be a valid menu key.")
    # Convert both sides to text so the integer 1 and keyboard input "1" can
    # match the same menu key. Return text because the existing CLI uses it.
    return _validate_choice(
        str(value), tuple(str(item) for item in valid_options), "menu selection"
    )


def validate_export_format(value, valid_formats=EXPORT_FORMATS):
    """Return text, csv, or json by default; accept txt as an alias for text."""
    # People may recognize the .txt extension, so accept "txt" as "text".
    # This only validates a format name; it does not create an exported file.
    if isinstance(value, str) and value.strip().casefold() == "txt":
        value = "text"
    return _validate_choice(value, valid_formats, "export format")


def validate_filter_options(
    options, categories=(), min_date=None, max_date=None
):
    """Return normalized filters; reject unknown or conflicting fields.

    Supported keys: start_date, end_date, category, transaction_type,
    min_amount, max_amount, time_period. Supply both dates or neither.
    Explicit dates may only be combined with the custom time period. None as the
    entire options argument means no filters. Input mappings are never modified.
    """
    # Filters narrow down which transactions a report should include.
    # A mapping pairs names with values, for example {"category": "Food"}.
    # No options means there is nothing to restrict, so return an empty dict.
    if options is None:
        return {}
    if not isinstance(options, Mapping):
        raise ValueError("Filter options must be a mapping.")
    # This set lists the field names the reporting interface understands.
    # Reject misspelled or extra fields instead of silently ignoring them.
    allowed = {
        "start_date",
        "end_date",
        "category",
        "transaction_type",
        "min_amount",
        "max_amount",
        "time_period",
    }
    # Set subtraction finds supplied field names missing from the allowed set.
    unknown = set(options) - allowed
    if unknown:
        unknown_names = ", ".join(sorted(map(str, unknown)))
        raise ValueError(f"Unknown filter options: {unknown_names}")
    # Work on a copy so checking filters does not change the caller's input.
    result = dict(options)
    has_start = "start_date" in result
    has_end = "end_date" in result
    # These yes/no values differ only when exactly one endpoint was supplied.
    if has_start != has_end:
        raise ValueError("Supply both start_date and end_date.")
    # Replace supplied date strings with validated dates. Paired assignment
    # stores the two returned dates in their corresponding dictionary entries.
    if has_start:
        result["start_date"], result["end_date"] = validate_report_date_range(
            result["start_date"], result["end_date"], min_date, max_date
        )
    # Only validate optional fields when present; omitted fields stay omitted.
    if "category" in result:
        result["category"] = validate_category_filter(
            result["category"], categories
        )
    if "transaction_type" in result:
        result["transaction_type"] = _validate_choice(
            result["transaction_type"],
            ("income", "expense"),
            "transaction type",
        )
    # Both amount filters must be nonnegative. The loop applies the same rule
    # to each field without duplicating the conversion and error handling.
    for key in ("min_amount", "max_amount"):
        if key in result:
            result[key] = validate_numeric_range(result[key], min_value=0)
    # Valid individual amounts can still conflict: a minimum of 50 and a
    # maximum of 10 cannot describe a usable range. Check them together too.
    if "min_amount" in result and "max_amount" in result:
        validate_numeric_range(
            result["min_amount"], max_value=result["max_amount"]
        )
    # Avoid two competing instructions about which dates to use. Explicit
    # start/end dates describe a custom period, not a separate weekly period.
    if "time_period" in result:
        result["time_period"] = validate_time_period(result["time_period"])
        if has_start and result["time_period"] != "custom":
            raise ValueError("Explicit dates require the custom time period.")
        if result["time_period"] == "custom" and not has_start:
            raise ValueError(
                "A custom time period requires start_date and end_date."
            )
    return result


# =====================================================
# ERROR RECOVERY AND HELP
# =====================================================
#
# Offer another attempt and explain the available input choices.
# =====================================================

def prompt_retry(
    prompt="Try again? [y/n]: ", *, input_func=None, output_func=None
):
    """Ask for yes/no; return False on EOF or keyboard interruption.

    Optional input/output functions make the prompt reusable and testable.
    """
    # Normally read uses input (keyboard) and write uses print (screen).
    # Tests can provide replacement functions to simulate answers without
    # waiting for a person. The * above requires these replacements by name.
    read = input if input_func is None else input_func
    write = print if output_func is None else output_func
    # Keep asking until a return statement ends the function with True/False.
    # This loop avoids calling the function repeatedly from inside itself.
    while True:
        try:
            answer = read(prompt).strip().casefold()
        except (EOFError, KeyboardInterrupt):
            # EOF means input ended; KeyboardInterrupt usually means Ctrl+C.
            # Treat either as choosing not to retry instead of showing an error.
            return False
        # Accept short or full answers after ignoring spaces and letter case.
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        # Any other answer explains the choices and starts another loop turn.
        write("Please enter y/yes or n/no.")


def provide_help_text(topic=None):
    """Return all validation help, or help for one named topic."""
    # Keep each topic's explanation together in a dictionary. Adjacent strings
    # in parentheses form one message while keeping source lines readable.
    topics = {
        "dates": (
            "Use YYYY-MM-DD. Start must be on or before end; "
            "bounds are inclusive."
        ),
        "reports": f"Report types: {', '.join(REPORT_TYPES)}.",
        "categories": (
            "Use an available category name (case-insensitive); None means all."
        ),
        "periods": (
            f"Time periods: {', '.join(TIME_PERIODS)}. Custom requires dates."
        ),
        "numbers": (
            "Enter finite numbers. Thresholds and amount filters "
            "must be nonnegative."
        ),
        "menu": "Choose a displayed menu key (main menu: 1 through 6).",
        "export": "Export formats: text (or txt), csv, json.",
        "filters": (
            "Filter by paired dates, category, transaction_type, "
            "min_amount, max_amount, or time_period. "
            "Explicit dates require a custom period."
        ),
    }
    # With no topic, join all explanations using \n (a new line) between them.
    # Return text instead of printing so a CLI can decide where to display it.
    if topic is None:
        return "\n".join(topics.values())
    # Validate the topic against the dictionary's keys before looking up its
    # message. An unknown topic gets a helpful error rather than a lookup crash.
    return topics[_validate_choice(topic, topics, "help topic")]
