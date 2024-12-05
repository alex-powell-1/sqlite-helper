import sqlite3


class SQLite:
    """Class for interacting with SQLite database. Includes method for replacing a table with a new schema."""

    db = "sqlite.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def create_table(self, table, columns):
        self.cursor.execute(f"CREATE TABLE {table} ({columns});")
        self.conn.commit()

    def get_schema(self, table, obj=False):
        self.cursor.execute(
            f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';"
        )
        schema = self.cursor.fetchone()

        if schema:
            return schema[0]
        else:
            return "Table not found."

    def copy_table(self, table_name: str, new_table_name: str):
        schema = db.get_schema(table_name)
        try:
            db.cursor.execute(schema.replace(table_name, new_table_name))
            db.conn.commit()
        except Exception as e:
            if e.args[0] == f"table {new_table_name} already exists":
                self.drop_table(new_table_name)
                db.cursor.execute(schema.replace(table_name, new_table_name))
                db.conn.commit()

        else:
            print(f"Table {new_table_name} created successfully.")

            # Copy data from the old table to the new table
            db.cursor.execute(
                f"INSERT INTO {new_table_name} SELECT * FROM {table_name};"
            )
            db.conn.commit()
            print(f"Data copied from {table_name} to {new_table_name} successfully.")
        return schema

    def replace_table(self, table_name: str):
        # Save the schema to a file and ask the user to edit it
        with open("schema.txt", "w") as f:
            f.write(db.get_schema(table_name))
        will_proceed = input(
            "Current Schema has been exported.\nPlease change the schema.txt file to your liking and then proceed. Do you want to proceed? (Y/N): "
        )
        if will_proceed.lower() != "y":
            return
        # Read the new schema file
        try:
            with open("schema.txt", "r") as f:
                schema = f.read()
        except FileNotFoundError:
            print(
                "Schema file not found. Do not move the schema.txt file in the root. Try again."
            )
            return
        except Exception as e:
            print(f"Error: {e}")
            return

        # Print the new schema and ask the user to confirm
        print(f"Schema:\n\n{schema}\n")
        will_proceed = input("Schema Preview: Do you want to proceed? (Y/N): ")
        if will_proceed.lower() != "y":
            return

        # Create the temp table
        self.copy_table(table_name, f"{table_name}_temp")
        # Drop the original table. Current Data is saved in the temp table.
        self.drop_table(table_name)
        # Recreate the table with the new schema
        self.cursor.execute(schema)
        # Get columns from the new table and temp tables
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        original_columns = [col[1] for col in self.cursor.fetchall()]
        self.cursor.execute(f"PRAGMA table_info({table_name}_temp);")
        temp_columns = [col[1] for col in self.cursor.fetchall()]
        # Find common columns
        common_columns = [col for col in original_columns if col in temp_columns]
        # Construct the INSERT statement with common columns
        columns_str = ", ".join(common_columns)
        query = f"INSERT INTO {table_name} ({columns_str}) SELECT {columns_str} FROM {table_name}_temp;"
        self.cursor.execute(query)
        # Drop the temp table
        self.drop_table(f"{table_name}_temp")
        # Commit the changes
        self.conn.commit()

    def insert(self, table, columns, values):
        self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values});")
        self.conn.commit()

    def update(self, table, column, value, condition):
        self.cursor.execute(f"UPDATE {table} SET {column} = {value} WHERE {condition};")
        self.conn.commit()

    def add_column(self, table, column: str):
        self.cursor.execute(f"ALTER TABLE {table} ADD {column};")
        self.conn.commit()

    def delete_column(self, table: str, column: str):
        try:
            self.cursor.execute(f"ALTER TABLE {table} DROP COLUMN {column};")
        except Exception as e:
            print(f"Error: {e}")
        else:
            print(f"Column {column} deleted successfully.")
            self.conn.commit()

    def rename_column(self, table: str, column: str, new_column: str):
        try:
            self.cursor.execute(
                f"ALTER TABLE {table} RENAME COLUMN {column} TO {new_column};"
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        else:
            print(f"Column {column} renamed to {new_column} successfully.")

    def drop_table(self, table):
        self.cursor.execute(f"DROP TABLE {table};")
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Example Usage
    db = SQLite()
    db.replace_table("appointment_services")
    # This will send the schema of the table to the schema.txt file
    # The user can edit the schema and then proceed
    db.close()
