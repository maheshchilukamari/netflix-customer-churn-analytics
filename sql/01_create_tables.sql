/*
Create tables for the Customer Churn & Revenue Insights Dashboard project.

The SQL uses simple data types that are easy to adapt for SQLite or PostgreSQL.
Load data/customer_churn_raw.csv into raw_customer_churn, then use the cleaning
queries in 02_data_cleaning_queries.sql to create cleaned_customer_churn.
*/

DROP TABLE IF EXISTS raw_customer_churn;

CREATE TABLE raw_customer_churn (
    customer_id TEXT,
    gender TEXT,
    age_group TEXT,
    tenure INTEGER,
    contract_type TEXT,
    payment_method TEXT,
    monthly_charges NUMERIC,
    total_charges NUMERIC,
    internet_service TEXT,
    support_tickets INTEGER,
    churn_status TEXT,
    churn_reason TEXT
);

DROP TABLE IF EXISTS cleaned_customer_churn;

CREATE TABLE cleaned_customer_churn (
    customer_id TEXT PRIMARY KEY,
    gender TEXT,
    age_group TEXT,
    tenure INTEGER,
    tenure_group TEXT,
    contract_type TEXT,
    payment_method TEXT,
    monthly_charges NUMERIC,
    total_charges NUMERIC,
    internet_service TEXT,
    support_tickets INTEGER,
    churn_status TEXT,
    churn_reason TEXT,
    monthly_revenue_loss NUMERIC,
    annual_revenue_loss NUMERIC,
    customer_lifetime_value NUMERIC
);
