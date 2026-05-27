/*
Churn analysis queries.

Use these queries to understand where churn is concentrated and which customer
groups have the highest churn risk.
*/

-- Overall churn rate.
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM cleaned_customer_churn;

-- Churn rate by contract type.
SELECT
    contract_type,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM cleaned_customer_churn
GROUP BY contract_type
ORDER BY churn_rate_percent DESC;

-- Churn rate by payment method.
SELECT
    payment_method,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM cleaned_customer_churn
GROUP BY payment_method
ORDER BY churn_rate_percent DESC;

-- Churn rate by tenure group.
SELECT
    tenure_group,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM cleaned_customer_churn
GROUP BY tenure_group
ORDER BY
    CASE tenure_group
        WHEN '0-6 months' THEN 1
        WHEN '7-12 months' THEN 2
        WHEN '13-24 months' THEN 3
        WHEN '25-48 months' THEN 4
        ELSE 5
    END;

-- Top churn reasons.
SELECT
    churn_reason,
    COUNT(*) AS churned_customers
FROM cleaned_customer_churn
WHERE churn_status = 'Churned'
GROUP BY churn_reason
ORDER BY churned_customers DESC;
