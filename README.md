# End-to-End E-commerce Analytics Platform
This repository contains the complete source code for an end-to-end data analytics project built on the Olist E-commerce dataset. The project demonstrates a full data lifecycle, from raw data ingestion and warehousing to business intelligence, predictive modeling, and deployment in an interactive web application.

🚀 Live Application
[Note: Add a link here if you choose to deploy the Streamlit app publicly using a service like Streamlit Community Cloud.]

📋 Project Overview
This project simulates a real-world analytics environment for an e-commerce company. The primary goal is to leverage data to drive business decisions by providing insights into historical performance, predicting future customer behavior, and offering real-time product recommendations. The platform integrates data engineering, business intelligence, and machine learning to create a comprehensive suite of analytical tools.

Key Features:
ETL Pipeline: A robust Python pipeline that extracts data from a transactional MySQL database, transforms it, and loads it into a Snowflake cloud data warehouse.

Business Intelligence Dashboard: An interactive Power BI dashboard connected to Snowflake for analyzing key performance indicators (KPIs), including sales trends, geographic performance, and top-selling product categories.

Predictive Modeling: A machine learning model that predicts customer churn based on their purchase history (Recency, Frequency, Monetary Value).

Recommendation Engine: A "frequently bought together" model that provides product recommendations based on co-purchase patterns.

Interactive Web Application: A web app built with Streamlit that serves both the churn prediction and recommendation models, allowing non-technical users to gain real-time insights.

🛠️ Tech Stack
Programming & Data Manipulation: Python, Pandas, SQL

Databases: MySQL (Source), Snowflake (Cloud Data Warehouse)

ETL & Pipeline: Python, SQLAlchemy

Business Intelligence: Microsoft Power BI

Machine Learning: Scikit-learn

Application Framework: Streamlit

🏗️ Architecture
The project follows a modern analytics architecture:

MySQL DB (Source) -> Python ETL Script -> Snowflake DWH (Cloud) -> Power BI & Python ML -> Streamlit App (Deployment)

⚙️ Setup and Installation
To run this project locally, please follow these steps:

Prerequisites
Python 3.8+

MySQL Server

Power BI Desktop

A free Snowflake account

1. Clone the Repository
git clone [your-repository-url]
cd [your-repository-name]

2. Install Python Dependencies
pip install -r requirements.txt

(Note: You will need to create a requirements.txt file by running pip freeze > requirements.txt in your terminal after installing all the libraries we used.)

3. Set Up the Source Database (MySQL)
Download the Olist Dataset from Kaggle and place the CSV files in the root of the project folder.

Open load_data.py and enter your MySQL root password.

Run the script to create the olist_db and populate it with data:

python load_data.py

4. Set Up the Cloud Warehouse (Snowflake)
Log in to your Snowflake account.

Open a new worksheet and run the SQL commands in the snowflake_setup.sql file to create the warehouse, database, and ETL_USER. (Note: You should save the Snowflake setup commands into a file with this name.)

5. Run the ETL Pipeline
Open mysql_to_snowflake.py and fill in your MySQL and Snowflake credentials.

Run the script to move data from MySQL to Snowflake:

python mysql_to_snowflake.py

6. Train the Machine Learning Models
Open train_churn_model.py and train_recommender.py and fill in your Snowflake credentials.

Run both scripts to train the models and create the .pkl files:

python train_churn_model.py
python train_recommender.py

7. Launch the Interactive Application
Open app.py and fill in your Snowflake credentials.

Run the Streamlit command from your terminal:

streamlit run app.py

Your web browser will automatically open with the live application.

📊 Dashboard Showcase
[Insert a screenshot of your completed Power BI dashboard here. This is crucial for showing the BI component of your project.]

Example:

🤖 Application Showcase
[Insert a screenshot of your running Streamlit application here. Showcasing the interactive part is very important.]
