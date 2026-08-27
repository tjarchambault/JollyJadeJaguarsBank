# External Libraries

Our team plans to use the following external Python libraries/modules in the project:

## 1. sqlite3

**Purpose:**
`sqlite3` will be used to store transactions permanently in a database.

**Why it is appropriate:**
The application needs a way to save transaction information so that it does not disappear when the program closes. SQLite provides a lightweight database that can store and retrieve the application's data without requiring a separate database server.

## 2. datetime

**Purpose:**
`datetime` will be used to work with dates and times and help validate date-related user input.

**Why it is appropriate:**
The application may need to record transaction dates or other date-related information. The `datetime` module provides built-in functionality for working with and validating dates and times.

## 3. pandas

**Purpose:**
`pandas` will be used to read and work with SQL data and assist with reporting and data analysis.

**Why it is appropriate:**
Pandas makes it easier to organize, filter, analyze, and manipulate data retrieved from the database. This will be useful when creating reports based on transaction data.

## 4. matplotlib.pyplot

**Purpose:**
`matplotlib.pyplot` will be used to generate charts and visualizations for reporting and dashboards.

**Why it is appropriate:**
Charts can make transaction and reporting data easier to understand. Matplotlib provides tools for creating visual representations of the data processed by the application.

## Conclusion

These libraries were selected because each supports an important part of the project's functionality. SQLite will provide permanent data storage, datetime will support date and time handling, pandas will assist with data processing and reporting, and matplotlib.pyplot will provide data visualization.
