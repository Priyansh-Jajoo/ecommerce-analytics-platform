# load_data.py
import mysql.connector
import pandas as pd
import os
import sys
import numpy as np  # Import numpy for NaN handling

# --- DATABASE CONNECTION DETAILS ---
# IMPORTANT: Replace with your MySQL root password set during installation
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Priyansh@123'  # <--- CHANGE THIS
DB_NAME = 'olist_db'
# Directory containing the Olist CSV files
# Assumes the script is in the same directory as the CSVs
DATA_DIR = '.'


def check_dependencies():
    """Checks if required Python libraries are installed."""
    try:
        import pandas
        import mysql.connector
        import numpy
    except ImportError as e:
        print(f"Error: A required library is not installed: {e.name}")
        print("Please install it by running:")
        print(f"pip install {e.name}")
        sys.exit(1)  # Exit the script if dependencies are missing


def create_database_and_tables():
    """Connects to MySQL, creates the database and tables."""
    try:
        # Connect to MySQL server
        print("Connecting to MySQL server...")
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = db.cursor()
        print("Connection successful.")

        # Create the database if it doesn't exist
        print(f"Creating database '{DB_NAME}' if it doesn't exist...")
        # Using utf8mb4 for better character support
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {DB_NAME}")
        print(f"Database '{DB_NAME}' is ready.")

        # Get all CSV files from the directory
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        if not csv_files:
            print(f"Error: No Olist CSV files found in the directory '{os.path.abspath(DATA_DIR)}'.")
            print("Please make sure the script is in the same folder as the dataset files.")
            return False

        for filename in csv_files:
            # Read the CSV to get column names
            filepath = os.path.join(DATA_DIR, filename)
            df = pd.read_csv(filepath, nrows=1, encoding='utf-8')

            # Clean up filename to create a valid table name
            table_name = filename.replace('olist_', '').replace('_dataset.csv', '').replace('.csv', '').replace('-',
                                                                                                                '_')
            print(f"\nProcessing file: {filename} -> Creating table: {table_name}")

            # Generate the CREATE TABLE SQL statement
            cols_with_types = []
            for col in df.columns:
                # A more robust type inference
                col_type = "TEXT"  # Default to TEXT
                if 'timestamp' in col:
                    col_type = "DATETIME"
                elif 'price' in col or 'freight_value' in col:
                    col_type = "DECIMAL(10, 2)"
                elif '_id' in col or '_zip_code_prefix' in col or '_state' in col or 'order_status' in col:
                    col_type = "VARCHAR(255)"
                elif 'score' in col or 'qty' in col or 'lenght' in col or 'weight' in col or 'cm' in col:  # Use 'lenght' to catch typo in original data
                    col_type = "DECIMAL(10,1)"  # Use decimal for floats with potential NaNs

                clean_col = col.replace(' ', '_')
                cols_with_types.append(f"`{clean_col}` {col_type}")

            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols_with_types)})"

            print("Executing CREATE TABLE statement...")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")  # Drop if exists to start fresh
            cursor.execute(create_table_sql)
            print(f"Table '{table_name}' created successfully.")

        cursor.close()
        db.close()
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def insert_data_into_tables():
    """Connects to the created database and inserts data from CSVs."""
    try:
        # Connect to the olist_db database
        print("\nConnecting to the database for data insertion...")
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = db.cursor()
        print("Connection successful.")

        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]

        for filename in csv_files:
            table_name = filename.replace('olist_', '').replace('_dataset.csv', '').replace('.csv', '').replace('-',
                                                                                                                '_')
            filepath = os.path.join(DATA_DIR, filename)

            print(f"\nLoading data from '{filename}' into table '{table_name}'...")

            df_reader = pd.read_csv(filepath, chunksize=1000, encoding='utf-8')

            total_rows = 0
            for chunk in df_reader:
                chunk.columns = [col.replace(' ', '_') for col in chunk.columns]

                # THIS IS THE FIX:
                # Convert the entire chunk to object type and replace numpy's NaN
                # with Python's None, which is understood by the database driver as NULL.
                chunk = chunk.astype(object).replace(np.nan, None)

                rows = [tuple(x) for x in chunk.to_numpy()]

                cols = ', '.join([f"`{c}`" for c in chunk.columns])
                placeholders = ', '.join(['%s'] * len(chunk.columns))
                insert_sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

                cursor.executemany(insert_sql, rows)
                total_rows += len(rows)

            db.commit()
            print(f"Successfully inserted {total_rows} rows into '{table_name}'.")

        cursor.close()
        db.close()
        print("\nAll data has been loaded into the database.")

    except mysql.connector.Error as err:
        print(f"Database error during insertion: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during insertion: {e}")


if __name__ == '__main__':
    print("--- E-commerce Data Pipeline: Step 1 ---")
    print("This script will create a MySQL database and load it with the Olist dataset.")

    check_dependencies()

    if create_database_and_tables():
        insert_data_into_tables()
        print("\n--- Step 1 Complete! ---")
    else:
        print("\n--- Step 1 Failed. Please check the errors above. ---")