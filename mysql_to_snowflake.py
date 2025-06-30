# mysql_to_snowflake.py
import mysql.connector
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# --- CONFIGURATION: FILL IN YOUR DETAILS HERE ---

# 1. MySQL Connection Details
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Priyansh@123'  # <-- CHANGE THIS to your MySQL password
MYSQL_DB = 'olist_db'

# 2. Snowflake Connection Details
# Find your account identifier in the URL: https://<account_identifier>.snowflakecomputing.com
SNOWFLAKE_ACCOUNT = 'fac88810.us-east-1'  # <-- CHANGE THIS (e.g., fac88810.us-east-1)
SNOWFLAKE_USER = 'ETL_USER'  # The user we created in the Snowflake worksheet
SNOWFLAKE_PASSWORD = 'Ha0ieidheb#rl9'  # <-- CHANGE THIS to the password you set for ETL_USER
SNOWFLAKE_DB = 'OLIST_DB'
SNOWFLAKE_WAREHOUSE = 'OLIST_WH'
SNOWFLAKE_SCHEMA = 'PUBLIC'  # This is the default schema in a new database


def get_mysql_tables(cursor, db_name):
    """
    Fetches a list of all tables from the MySQL database using the
    standard information_schema. This is a robust method that avoids
    the 'Unread result' error.
    """
    print("Getting list of tables from MySQL...")
    # This query asks the database for a list of all its tables.
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = %s"
    cursor.execute(query, (db_name,))

    # We immediately fetch all results to ensure none are left unread.
    tables = [table[0] for table in cursor.fetchall()]
    return tables


def etl_pipeline():
    """
    Connects to MySQL, extracts data from each table,
    and loads it into a corresponding table in Snowflake.
    """
    mysql_conn = None
    snowflake_conn = None
    try:
        # --- Connect to MySQL ---
        print("Connecting to MySQL...")
        mysql_conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        mysql_cursor = mysql_conn.cursor()
        print("MySQL connection successful.")

        # --- Get list of tables from MySQL ---
        tables = get_mysql_tables(mysql_cursor, MYSQL_DB)
        print(f"Found {len(tables)} tables in MySQL: {tables}")

        # --- Connect to Snowflake ---
        print("\nConnecting to Snowflake... (this may take up to 60 seconds)")
        snowflake_conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DB,
            schema=SNOWFLAKE_SCHEMA,
            timeout=60  # Add a 60-second timeout to prevent indefinite hanging
        )
        print("Snowflake connection successful.")

        # --- Loop through tables, extract from MySQL, and load to Snowflake ---
        for table_name in tables:
            print(f"\n--- Processing table: {table_name} ---")

            # 1. EXTRACT data from MySQL using Pandas
            print(f"  1. Extracting data from MySQL table '{table_name}'...")
            sql_query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(sql_query, mysql_conn)
            print(f"     Extracted {len(df)} rows.")

            # 2. TRANSFORM (simple cleanse)
            snowflake_table_name = table_name.upper()

            # 3. LOAD data into Snowflake
            print(f"  2. Loading data into Snowflake table '{snowflake_table_name}'...")
            success, nchunks, nrows, _ = write_pandas(
                conn=snowflake_conn,
                df=df,
                table_name=snowflake_table_name,
                auto_create_table=True,
                overwrite=True
            )
            if success:
                print(f"     Successfully loaded {nrows} rows into '{snowflake_table_name}'.")
            else:
                print(f"     Failed to load data into '{snowflake_table_name}'.")

    except mysql.connector.Error as mysql_err:
        print(f"MySQL Error: {mysql_err}")
    except snowflake.connector.Error as sf_err:
        print(f"Snowflake Error: {sf_err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # --- Close connections ---
        if mysql_conn and mysql_conn.is_connected():
            mysql_cursor.close()
            mysql_conn.close()
            print("\nMySQL connection closed.")
        if snowflake_conn:
            snowflake_conn.close()
            print("Snowflake connection closed.")


if __name__ == '__main__':
    print("--- Starting ETL Pipeline: MySQL to Snowflake ---")
    etl_pipeline()
    print("\n--- ETL Pipeline Complete! ---")