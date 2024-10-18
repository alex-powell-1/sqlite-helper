![SQLite Logo](https://www.sqlite.org/images/sqlite370_banner.gif)

![Python Logo](https://www.python.org/static/img/python-logo.png)


# SQLite Database Wrapper

This project provides a simple wrapper around SQLite using Python's `sqlite3` module. It includes classes to represent database tables and columns, and provides methods to execute common SQL operations.

## Project Structure

## Classes

### `Column`

Represents a column in a SQLite table.

#### Attributes:
- `name` (str): The name of the column.
- `col_type` (str): The data type of the column.
- `constraints` (str, optional): Any constraints on the column (e.g., `PRIMARY KEY`, `NOT NULL`).

#### Methods:
- `__str__()`: Returns a string representation of the column.

### `Table`

Represents a SQLite table.

#### Attributes:
- `name` (str): The name of the table.
- `columns` (list of `Column`): A list of columns in the table.

#### Methods:
- `__init__(name, columns)`: Initializes the table with a name and a list of columns.

### `SQLiteDB`

SQLite database wrapper.

#### Attributes:
- `db_name` (str): The name of the database file.
- `conn` (sqlite3.Connection): The database connection.
- `cursor` (sqlite3.Cursor): The database cursor.

#### Methods:
- `connect()`: Connects to the SQLite database.
- `create_table(table)`: Creates a table in the database.
- `drop_table(table_name)`: Drops a table from the database.
- `execute_query(query)`: Executes a SQL query and returns a `Response` object.
- `close()`: Closes the database connection.

### `Response`

Represents the response from executing a SQL query.

#### Attributes:
- `rows` (list): The rows returned by the query.
- `rowcount` (int): The number of rows affected by the query.
- `status_code` (int): The status code of the query.

#### Methods:
- `__str__()`: Returns a string representation of the response.
- `determine_status_code(query)`: Determines the status code based on the query type.