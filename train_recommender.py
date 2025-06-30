# train_recommender.py
import pandas as pd
from sqlalchemy import create_engine
import joblib
from collections import defaultdict
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIGURATION: FILL IN YOUR SNOWFLAKE DETAILS ---
SNOWFLAKE_ACCOUNT = 'fac88810.us-east-1'
SNOWFLAKE_USER = 'ETL_USER'
SNOWFLAKE_PASSWORD = 'Ha0ieidheb#rl9'
SNOWFLAKE_DB = 'OLIST_DB'
SNOWFLAKE_WAREHOUSE = 'OLIST_WH'
SNOWFLAKE_SCHEMA = 'PUBLIC'


def get_copurchase_data(engine):
    """
    Runs a query in Snowflake to find all pairs of products that were
    purchased together in the same order.
    """
    print("Running co-purchase query in Snowflake... (This may take a minute)")

    # This query self-joins the ORDER_ITEMS table to find product pairs.
    query = """
    SELECT
        a."product_id" AS product_a,
        b."product_id" AS product_b
    FROM "ORDER_ITEMS" a
    JOIN "ORDER_ITEMS" b ON a."order_id" = b."order_id"
    WHERE a."product_id" != b."product_id";
    """

    df = pd.read_sql(query, engine)
    print(f"Successfully fetched {len(df)} co-purchased product pairs.")
    return df


def create_recommendation_model(df):
    """
    Processes the co-purchase data to create a recommendation model.
    The model is a dictionary where each key is a product_id and the value is a
    list of recommended product_ids, sorted by co-purchase frequency.
    """
    print("\nCalculating co-purchase frequencies...")
    # Count how many times each pair of products was purchased together
    copurchase_counts = df.groupby(['product_a', 'product_b']).size().reset_index(name='count')
    print("Frequency calculation complete.")

    print("Building recommendation dictionary...")
    recommendations = defaultdict(list)

    # Sort by the most frequent co-purchases
    copurchase_counts = copurchase_counts.sort_values('count', ascending=False)

    # For each product, store a list of its most frequent co-purchased items
    for index, row in copurchase_counts.iterrows():
        product_a = row['product_a']
        product_b = row['product_b']

        # Add B to A's recommendation list if it's not already full (top 5)
        if len(recommendations[product_a]) < 5:
            recommendations[product_a].append(product_b)

    print("Recommendation dictionary built.")
    return recommendations


def train_recommender():
    """
    Main function to orchestrate the recommendation model training.
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

        # 1. Get Data
        copurchase_df = get_copurchase_data(snowflake_engine)

        # 2. Create Model
        recommender_model = create_recommendation_model(copurchase_df)

        # 3. Save Model
        model_filename = 'recommender_model.pkl'
        print(f"\nSaving recommendation model to {model_filename}...")
        joblib.dump(recommender_model, model_filename)
        print("Model saved successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if snowflake_engine:
            snowflake_engine.dispose()
            print("\nSnowflake engine connection closed.")


if __name__ == '__main__':
    print("--- Starting Recommendation Engine Training ---")
    train_recommender()
    print("\n--- Recommendation Engine Training Complete! ---")
