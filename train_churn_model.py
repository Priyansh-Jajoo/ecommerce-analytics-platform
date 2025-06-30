# train_churn_model.py
import snowflake.connector
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib  # For saving the model
import warnings

# Suppress the UserWarning from pandas
warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIGURATION: FILL IN YOUR SNOWFLAKE DETAILS ---
SNOWFLAKE_ACCOUNT = 'fac88810.us-east-1'  # <-- CHANGE THIS
SNOWFLAKE_USER = 'ETL_USER'
SNOWFLAKE_PASSWORD = 'Ha0ieidheb#rl9'  # <-- CHANGE THIS
SNOWFLAKE_DB = 'OLIST_DB'
SNOWFLAKE_WAREHOUSE = 'OLIST_WH'
SNOWFLAKE_SCHEMA = 'PUBLIC'


def get_clean_feature_data(engine):
    """
    Reads the pre-built, clean feature table from Snowflake.
    """
    print("Fetching clean feature data from Snowflake table 'CUSTOMER_CHURN_FEATURES'...")

    query = 'SELECT "RECENCY", "FREQUENCY", "MONETARY_VALUE", "CHURN" FROM CUSTOMER_CHURN_FEATURES'

    df = pd.read_sql(query, engine)
    print(f"Successfully fetched {len(df)} records for model training.")
    return df


def train_model():
    """
    Main function to orchestrate the model training pipeline.
    """
    snowflake_engine = None
    try:
        # --- Create a SQLAlchemy Engine for Snowflake ---
        print("Creating Snowflake SQLAlchemy engine...")

        connection_url = (
            f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/"
            f"{SNOWFLAKE_DB}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}"
        )
        snowflake_engine = create_engine(connection_url)
        print("Snowflake engine created successfully.")

        # 1. Get Data from our new clean table
        df = get_clean_feature_data(snowflake_engine)

        # THIS IS THE FIX FOR DATA LEAKAGE:
        # We remove 'recency' from the features so the model can't cheat.
        # It must now learn from only frequency and monetary value.
        X = df[['frequency', 'monetary_value']]
        y = df['churn']

        # 2. Split Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        print(f"\nData split: {len(X_train)} training samples, {len(X_test)} testing samples.")

        # 3. Train Model
        print("Training Logistic Regression model...")
        model = LogisticRegression(random_state=42, class_weight='balanced')
        model.fit(X_train, y_train)
        print("Model training complete.")

        # 4. Evaluate Model
        print("\n--- Model Evaluation ---")
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Not Churned', 'Churned']))

        # 5. Save Model
        model_filename = 'churn_model.pkl'
        print(f"\nSaving trained model to {model_filename}...")
        joblib.dump(model, model_filename)
        print("Model saved successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if snowflake_engine:
            snowflake_engine.dispose()
            print("\nSnowflake engine connection closed.")


if __name__ == '__main__':
    print("--- Starting Customer Churn Model Training Pipeline ---")
    train_model()
    print("\n--- Model Training Pipeline Complete! ---")
