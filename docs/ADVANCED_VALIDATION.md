# Advanced validation

`src/Advanced_Validation.py` implements the 15 functions assigned in issues
#231–#249. The module uses only Python's standard library. Existing transaction
validation placeholders remain separate. Report generation and CLI integration
are still scaffolded; these functions are ready for callers to use.

Validators return normalized values, rather than booleans. Invalid input raises
`ValueError` with a message suitable for display in the CLI. Catch that exception
and call `prompt_retry()` to ask whether the user wants to enter input again.

| Function | Input and result |
| --- | --- |
| `validate_date_format(value)` | Strict `YYYY-MM-DD` or `date` → `date`; rejects impossible dates and datetimes |
| `check_date_boundaries(value, min_date=None, max_date=None)` | Date within inclusive optional bounds → `date` |
| `validate_report_date_range(start_date, end_date, min_date=None, max_date=None)` | Ordered dates → `(start, end)`; same-day ranges allowed |
| `validate_report_type(value, valid_types=REPORT_TYPES)` | Daily, weekly, monthly, category, date_range → canonical name |
| `validate_category_filter(value, categories)` | Case-insensitive name → catalog spelling; `None` means all categories |
| `validate_time_period(value, valid_periods=TIME_PERIODS)` | Daily, weekly, monthly, yearly, custom → canonical label |
| `validate_numeric_range(value, min_value=None, max_value=None)` | Finite number within inclusive optional bounds → `Decimal` |
| `validate_threshold_input(value, min_value=0, max_value=None)` | Threshold → `Decimal`; nonnegative by default |
| `validate_menu_selection(value, valid_options=MAIN_MENU_OPTIONS)` | Displayed menu key → string; defaults to 1 through 6 |
| `validate_export_format(value, valid_formats=EXPORT_FORMATS)` | Text, csv, json → canonical name; txt aliases text |
| `validate_filter_options(options, categories=(), min_date=None, max_date=None)` | Filter mapping → new validated dictionary |
| `generate_validation_error_message(field, value, requirement)` | Error details → message string |
| `prompt_retry(prompt=..., input_func=..., output_func=...)` | Yes/no prompt → boolean; EOF or Ctrl+C means no |
| `provide_help_text(topic=None)` | Optional topic → help string |
| `suggest_correction(value, valid_options)` | Misspelled choice → closest option or `None` |

Dates have no implicit historical or future cutoff; callers set bounds when
required. Numeric values are not rounded. Pass money as strings or `Decimal` to
preserve precision. Booleans, NaN, and infinity are rejected as numeric inputs.
Choice matching trims whitespace and ignores case; date strings remain strict.
Category catalogs are iterables of names supplied by the data layer.

Filters support `start_date`, `end_date`, `category`, `transaction_type`,
`min_amount`, `max_amount`, and `time_period`. Unknown keys are errors. Dates
must be paired, amount bounds must be nonnegative and ordered, and transaction
types are income or expense. A custom period requires dates; explicit dates
cannot accompany another period. An empty mapping or `None` means no filters.

Help topics are dates, reports, categories, periods, numbers, menu, export, and
filters. The helpers return text; callers decide when to print it. Suggestions
never automatically accept or replace invalid input.

Example from a module inside `src/`:

```python
from Advanced_Validation import validate_report_date_range, prompt_retry

while True:
    try:
        start, end = validate_report_date_range(
            input("Start date (YYYY-MM-DD): "),
            input("End date (YYYY-MM-DD): "),
        )
        break
    except ValueError as error:
        print(error)
        if not prompt_retry():
            break
```

Run tests from the repository root with `python -m pytest tests/`.

This module, its tests, and this documentation were drafted with Codex assistance
and should be reviewed by the team before submission.

## Course coding standards

The module and its tests follow the supplied *Python Coding Standards for
ISTM 601* (2026-08-12): program headers covering purpose, input, processing,
output, and the supplied honor-code wording; descriptive snake_case names;
named constants; four-space indentation; lines of at most 80 characters;
f-strings; and documentation of non-obvious behavior. The honor-code statement
is the course's required header text; team members must confirm it accurately
reflects their work before submission.

The validation file is an importable library and the test file runs through
pytest, so neither needs a main program. These changes apply to the new
validation work; the remaining project scaffolds have not been audited against
the supplied standards.
