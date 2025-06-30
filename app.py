import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import joblib

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Olist E-commerce Analytics",
    page_icon="🛍️",
    layout="wide"
)

# --- DATABASE CONNECTION ---
# Use st.secrets for secure credential management in a real deployment
# For this project, we'll place them here.
SNOWFLAKE_ACCOUNT = 'fac88810.us-east-1'
SNOWFLAKE_USER = 'ETL_USER'
SNOWFLAKE_PASSWORD = 'Ha0ieidheb#rl9'
SNOWFLAKE_DB = 'OLIST_DB'
SNOWFLAKE_WAREHOUSE = 'OLIST_WH'
SNOWFLAKE_SCHEMA = 'PUBLIC'


@st.cache_resource
def get_snowflake_engine():
    """Creates a SQLAlchemy engine for Snowflake."""
    try:
        connection_url = (
            f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/"
            f"{SNOWFLAKE_DB}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}"
        )
        engine = create_engine(connection_url)
        return engine
    except Exception as e:
        st.error(f"Error creating database engine: {e}")
        return None


engine = get_snowflake_engine()


# --- LOAD MODELS ---
@st.cache_data
def load_model(model_path):
    """Loads a saved model from a .pkl file."""
    try:
        with open(model_path, 'rb') as file:
            model = joblib.load(file)
        return model
    except FileNotFoundError:
        st.error(f"Error: Model file not found at {model_path}")
        return None


churn_model = load_model('churn_model.pkl')
recommender_model = load_model('recommender_model.pkl')


# --- LOAD DATA ---
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data(query):
    """Loads data from Snowflake using a SQL query."""
    if engine:
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


# Load data for selectors and displaying info
customers_df = load_data(
    'SELECT "customer_unique_id", "RECENCY", "FREQUENCY", "MONETARY_VALUE" FROM CUSTOMER_CHURN_FEATURES')
products_df = load_data('SELECT "product_id", "product_category_name" FROM "PRODUCTS"')

# --- UI LAYOUT ---
st.title("🛍️ Olist E-commerce Analytics Dashboard")
st.markdown("This interactive dashboard provides churn predictions and product recommendations.")

# --- TABS FOR DIFFERENT MODELS ---
tab1, tab2 = st.tabs(["🔥 Customer Churn Predictor", "🤝 Product Recommender"])

# --- CHURN PREDICTOR TAB ---
with tab1:
    st.header("Predict Customer Churn")

    if churn_model is not None and not customers_df.empty:
        # Customer selection
        customer_id = st.selectbox(
            "Select a Customer ID to predict churn:",
            options=customers_df['customer_unique_id'],
            index=0
        )

        if customer_id:
            # Get features for the selected customer
            customer_features = customers_df[customers_df['customer_unique_id'] == customer_id]

            if not customer_features.empty:
                # Prepare features for prediction (must match training format)
                features_for_prediction = customer_features[['frequency', 'monetary_value']]

                # Predict churn
                prediction_proba = churn_model.predict_proba(features_for_prediction)[0]
                prediction = churn_model.predict(features_for_prediction)[0]

                # Display results
                st.subheader(f"Prediction for Customer: `{customer_id}`")

                churn_probability = prediction_proba[1]  # Probability of the '1' class (churn)

                if prediction == 1:
                    st.error(f"**High Risk of Churn** (Probability: {churn_probability:.2%})")
                else:
                    st.success(f"**Low Risk of Churn** (Probability: {churn_probability:.2%})")

                # Show customer's features
                st.write("Customer's Purchase Behavior:")
                st.metric("Recency (days since last purchase)", f"{customer_features.iloc[0]['recency']:.0f}")
                st.metric("Frequency (total orders)", f"{customer_features.iloc[0]['frequency']:.0f}")
                st.metric("Monetary Value (total spend)", f"R$ {customer_features.iloc[0]['monetary_value']:.2f}")

# --- RECOMMENDER TAB ---
with tab2:
    st.header("Find Product Recommendations")

    if recommender_model is not None and not products_df.empty:
        # Product selection
        product_id = st.selectbox(
            "Select a Product ID to get recommendations:",
            options=products_df['product_id'],
            index=0
        )

        if product_id:
            # Get recommendations from our model
            recommendations = recommender_model.get(product_id, [])

            st.subheader(f"Top 5 Recommendations for Product: `{product_id}`")

            if recommendations:
                # Get details for the recommended products
                recommended_products_df = products_df[products_df['product_id'].isin(recommendations)]
                st.table(recommended_products_df)
            else:
                st.warning("No specific recommendations found for this product. Showing popular items instead.")
                # Fallback: show some popular items if no specific recommendation is found
                st.table(products_df.head(5))

# --- clean up engine ---
if engine:
    engine.dispose()