import sqlite3


class Column:
    """Represents a column in a SQLite table"""

    def __init__(self, name: str, col_type: str, constraints=""):
        self.name = name
        self.col_type = col_type
        self.constraints = constraints

    def __str__(self):
        return f"{self.name} {self.col_type} {self.constraints}".strip()


class Table:
    """Represents a SQLite table"""

    def __init__(self, name, columns: Column):
        self.name = name
        self.columns = columns
        self.columns_def = ",".join([str(column) for column in columns])


class SQLiteDB:
    """SQLite database wrapper"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table: Table):
        create_table_query = (
            f"CREATE TABLE IF NOT EXISTS {table.name} ({table.columns_def})"
        )
        return self.execute_query(create_table_query)

    def drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        return self.execute_query(query)

    def execute_query(self, query):
        self.connect()
        try:
            self.cursor.execute(query)
        except sqlite3.Error as e:
            print(f"Error: {e}")
            print(f"Query: {query}")
            self.close()
            return Response([], 0, query)
        except sqlite3.OperationalError as e:
            print(f"OperationalError: {e}")
            print(f"Query: {query}")
            self.close()
            return Response([], 0, query)
        except Exception as e:
            print(f"Error: {e}")
            print(f"Query: {query}")
            self.close()
            return Response([], 0, query)

        rows = self.cursor.fetchall()
        if self.cursor.rowcount > 0:
            self.conn.commit()
        self.close()
        return Response(rows, self.cursor.rowcount, query)

    def close(self):
        if self.conn:
            self.conn.close()


class Response:
    def __init__(self, rows, rowcount, query):
        self.rows = rows
        self.rowcount = rowcount
        self.status_code = self.determine_status_code(query)

    def __str__(self):
        str = f"Status Code: {self.status_code}, Number of Rows: {self.rowcount}"
        for row in self.rows:
            str += f"\n{row}"
        return str

    def determine_status_code(self, query):
        if query.strip().upper().startswith("SELECT"):
            self.rowcount = len(self.rows)
            if self.rowcount > 0:
                return 200
            return 404
        else:
            if self.rowcount > 0:
                return 201
            else:
                self.rowcount = 0
                return 404


if __name__ == "__main__":
    db = SQLiteDB("example.db")
    response = db.execute_query(
        'INSERT INTO users (name, age, email) VALUES ("John", 30, "john@gmail.com")'
    )
    print(response)

    response = db.execute_query("SELECT * FROM users")
    print(response)

    update = db.execute_query('UPDATE users SET name="John Doe" WHERE name="John"')

    response = db.execute_query("SELECT * FROM users")
    print(response)
