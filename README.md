# End-to-End E-commerce Analytics Platform

## Project Overview

This project provides a comprehensive, end-to-end analytics solution for the Olist e-commerce dataset. The goal was to architect a modern data platform that simulates a real-world business environment, moving from raw data ingestion and warehousing to deployed machine learning models. The analysis uncovers key business trends through a Power BI dashboard, predicts customer churn using a classification model, and provides real-time product suggestions with a recommendation engine.

The project demonstrates a full data science workflow, from data engineering and warehousing to business intelligence and MLOps deployment.

![Streamlit App Screenshot](https://i.imgur.com/aed90e57-6920-4b10-9ed4-0ffce9f4c792.png)

---

## Key Features

* **Data Engineering & ETL**: Architected a robust Python pipeline that extracts data from a source MySQL database, transforms it, and loads it into a Snowflake cloud data warehouse for scalable analytics.
* **Business Intelligence Dashboard**: Developed an interactive Power BI dashboard connected directly to Snowflake, visualizing key performance indicators (KPIs) like sales trends over time, sales by geographic location, and top-selling product categories.
* **Predictive Modeling (Churn)**:
    * Engineered features for Recency, Frequency, and Monetary (RFM) analysis using SQL within Snowflake.
    * Trained a Logistic Regression model to predict customer churn, identifying and remediating a data leakage issue to establish a realistic performance baseline.
* **Machine Learning (Recommendations)**:
    * Developed a "Frequently Bought Together" recommendation engine by analyzing product co-purchase patterns from transaction data.
* **Interactive Application Deployment**: Deployed both the churn and recommendation models into a live, user-friendly web application using Streamlit, allowing for real-time predictions and decision support.

---

## Data Source

The project uses the popular **Brazilian E-Commerce Public Dataset by Olist**, which contains information on 100,000 orders from 2016 to 2018. The dataset is relational and split into multiple files, including information on customers, orders, payments, products, and sellers. It was sourced from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

---

## Technologies & Libraries

* **Python 3.x**
* **SQL**
* **Databases**: MySQL, Snowflake
* **BI Tool**: Power BI
* **Python Libraries**: pandas, SQLAlchemy, scikit-learn, streamlit, joblib, mysql-connector-python, snowflake-connector-python, snowflake-sqlalchemy

---

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [your-repository-url]
    cd [your-repository-name]
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Create a `requirements.txt` file by running `pip freeze > requirements.txt` in your terminal.)*

3.  **Set up the environment:**
    * Ensure you have active MySQL Server and Power BI Desktop installations.
    * Create a free Snowflake account.
    * Fill in your credentials in all Python scripts (`load_data.py`, `mysql_to_snowflake.py`, `train_churn_model.py`, `train_recommender.py`, `app.py`).

4.  **Execute the scripts in order:**
    Run the following commands from your terminal.
    ```bash
    # 1. Load data into MySQL
    python load_data.py
    
    # 2. Run ETL to move data to Snowflake
    python mysql_to_snowflake.py
    
    # 3. Train the ML models
    python train_churn_model.py
    python train_recommender.py
    
    # 4. Launch the web application
    streamlit run app.py
    ```

---

## Summary of Results

The project successfully created a full suite of analytics tools, providing both historical insights and predictive capabilities.

#### Churn Model Performance

The Logistic Regression model established a realistic baseline for predicting customer churn based on their purchase frequency and monetary value.

| Model                 | Accuracy | Precision (Churned) | Recall (Churned) | F1-Score (Churned) |
| :-------------------- | :------- | :------------------ | :--------------- | :----------------- |
| **Logistic Regression** | **57%** | **0.71** | **0.65** | **0.68** |

*Note: The primary goal was to build the end-to-end pipeline. The model's performance could be further improved by engineering more features (e.g., sentiment from reviews, product category preferences).*

#### Dashboard & Application Showcase

The Power BI dashboard provides a comprehensive overview of business health, while the Streamlit application successfully deploys the ML models for interactive use.

![Power BI Dashboard](https://i.imgur.com/3q1tL9w.png)
