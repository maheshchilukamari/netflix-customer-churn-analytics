/*
Data cleaning SQL.

These queries show how the Python cleaning logic can be translated into SQL.
They trim text, remove duplicate customers, fill missing values, create tenure
groups, and calculate revenue loss fields.
*/

DELETE FROM cleaned_customer_churn;

INSERT INTO cleaned_customer_churn (
    customer_id,
    gender,
    age_group,
    tenure,
    tenure_group,
    contract_type,
    payment_method,
    monthly_charges,
    total_charges,
    streaming_plan,
    support_tickets,
    churn_status,
    churn_reason,
    monthly_revenue_loss,
    annual_revenue_loss,
    customer_lifetime_value
)
WITH ranked_customers AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(customer_id)
            ORDER BY TRIM(customer_id)
        ) AS duplicate_rank
    FROM raw_customer_churn
),
standardized AS (
    SELECT
        TRIM(customer_id) AS customer_id,
        TRIM(gender) AS gender,
        TRIM(age_group) AS age_group,
        CAST(tenure AS INTEGER) AS tenure,
        TRIM(contract_type) AS contract_type,
        COALESCE(NULLIF(TRIM(payment_method), ''), 'Unknown') AS payment_method,
        CAST(monthly_charges AS NUMERIC) AS monthly_charges,
        CAST(total_charges AS NUMERIC) AS total_charges,
        TRIM(streaming_plan) AS streaming_plan,
        CAST(support_tickets AS INTEGER) AS support_tickets,
        TRIM(churn_status) AS churn_status,
        TRIM(churn_reason) AS churn_reason
    FROM ranked_customers
    WHERE duplicate_rank = 1
),
cleaned AS (
    SELECT
        customer_id,
        gender,
        age_group,
        tenure,
        CASE
            WHEN tenure <= 6 THEN '0-6 months'
            WHEN tenure <= 12 THEN '7-12 months'
            WHEN tenure <= 24 THEN '13-24 months'
            WHEN tenure <= 48 THEN '25-48 months'
            ELSE '49+ months'
        END AS tenure_group,
        contract_type,
        payment_method,
        monthly_charges,
        COALESCE(total_charges, monthly_charges * tenure) AS total_charges,
        streaming_plan,
        COALESCE(support_tickets, 0) AS support_tickets,
        churn_status,
        churn_reason
    FROM standardized
)
SELECT
    customer_id,
    gender,
    age_group,
    tenure,
    tenure_group,
    contract_type,
    payment_method,
    ROUND(monthly_charges, 2) AS monthly_charges,
    ROUND(total_charges, 2) AS total_charges,
    streaming_plan,
    support_tickets,
    churn_status,
    churn_reason,
    CASE
        WHEN churn_status = 'Churned' THEN ROUND(monthly_charges, 2)
        ELSE 0
    END AS monthly_revenue_loss,
    CASE
        WHEN churn_status = 'Churned' THEN ROUND(monthly_charges * 12, 2)
        ELSE 0
    END AS annual_revenue_loss,
    ROUND(total_charges, 2) AS customer_lifetime_value
FROM cleaned;

-- Quality check: row count after duplicate removal.
SELECT COUNT(*) AS cleaned_customer_count
FROM cleaned_customer_churn;

-- Quality check: missing values that still need attention.
SELECT
    SUM(CASE WHEN customer_id IS NULL OR customer_id = '' THEN 1 ELSE 0 END) AS missing_customer_id,
    SUM(CASE WHEN payment_method IS NULL OR payment_method = '' THEN 1 ELSE 0 END) AS missing_payment_method,
    SUM(CASE WHEN total_charges IS NULL THEN 1 ELSE 0 END) AS missing_total_charges
FROM cleaned_customer_churn;
