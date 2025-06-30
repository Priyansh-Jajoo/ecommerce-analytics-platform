# 📦 End-to-End E-commerce Analytics Platform

This repository contains the complete source code for an end-to-end data analytics project built on the **Olist E-commerce dataset**. The project demonstrates a full data lifecycle — from raw data ingestion and warehousing to business intelligence, predictive modeling, and deployment in an interactive web application.

---

## 🛠️ Tech Stack & Tools
- Python
- MySQL
- Snowflake
- Power BI
- Scikit-learn
- Streamlit

---

## 📋 Project Overview

This project simulates a real-world analytics environment for an e-commerce company. The primary goal is to leverage data to drive business decisions by providing insights into historical performance, predicting future customer behavior, and offering real-time product recommendations. The platform integrates **data engineering**, **business intelligence**, and **machine learning** to create a comprehensive suite of analytical tools.

### 🔑 Key Features
- **ETL Pipeline**: Architected a robust Python pipeline to extract data from a transactional MySQL database, transform it, and load it into a Snowflake cloud data warehouse.
- **Business Intelligence Dashboard**: Developed an interactive Power BI dashboard connected to Snowflake for analyzing KPIs like sales trends, geographic performance, and top-selling product categories.
- **Predictive Modeling**: Built a machine learning model to predict customer churn using RFM (Recency, Frequency, Monetary) features. Addressed a data leakage issue to ensure realistic performance metrics.
- **Recommendation Engine**: Created a "frequently bought together" model using co-purchase pattern analysis.
- **Interactive Web Application**: Deployed both models in a Streamlit app for real-time insights accessible to non-technical users.

---

## 🏗️ Architecture

MySQL DB (Source)
↓
Python ETL Script
↓
Snowflake DWH (Cloud)
↓
Power BI & Python ML
↓
Streamlit App (Deployment)

---

## ⚙️ Setup and Installation

### 🔧 Prerequisites
- Python 3.8+
- MySQL Server
- Power BI Desktop
- Snowflake account

### 🔽 1. Clone the Repository
```
git clone [your-repository-url]
cd [your-repository-name]
🧱 2. Install Python Dependencies
It is recommended to create a virtual environment first.

pip install -r requirements.txt
Note: Create the requirements.txt file using:
pip freeze > requirements.txt
Includes: pandas, sqlalchemy, mysql-connector-python, snowflake-connector-python, snowflake-sqlalchemy, scikit-learn, joblib, streamlit

🗃️ 3. Set Up the Source Database (MySQL)
Download the Olist Dataset from Kaggle and place the CSV files in the project root.

Open load_data.py and add your MySQL root password.

Run:
python load_data.py
☁️ 4. Set Up the Cloud Warehouse (Snowflake)
Log in to your Snowflake account.

Open a new worksheet and run the commands from snowflake_setup.sql to create the warehouse, database, and user.

🛠️ 5. Run the ETL Pipeline
Open mysql_to_snowflake.py and fill in MySQL/Snowflake credentials.

Run:
python mysql_to_snowflake.py
🤖 6. Train the Machine Learning Models
Open train_churn_model.py and train_recommender.py and fill in your Snowflake credentials.

Run:
python train_churn_model.py
python train_recommender.py
🚀 7. Launch the Interactive Application
Open app.py and fill in your Snowflake credentials.

Run:
streamlit run app.py
Your web browser will automatically open with the live application.

📊 Dashboard Showcase



🤖 Application Showcase

