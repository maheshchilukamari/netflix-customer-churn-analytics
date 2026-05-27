/*
Customer segmentation queries.

Use these outputs to identify customer groups that may need different retention
strategies.
*/

-- Segment customers by age group and internet service.
SELECT
    age_group,
    internet_service,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_percent,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(AVG(support_tickets), 2) AS avg_support_tickets
FROM cleaned_customer_churn
GROUP BY age_group, internet_service
ORDER BY churn_rate_percent DESC, customers DESC;

-- Find segments with both high churn and meaningful customer volume.
SELECT
    contract_type,
    tenure_group,
    payment_method,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_percent,
    ROUND(SUM(monthly_revenue_loss), 2) AS monthly_revenue_loss
FROM cleaned_customer_churn
GROUP BY contract_type, tenure_group, payment_method
HAVING COUNT(*) >= 20
ORDER BY churn_rate_percent DESC, monthly_revenue_loss DESC;

-- Compare support burden between churned and retained customers.
SELECT
    churn_status,
    COUNT(*) AS customers,
    ROUND(AVG(support_tickets), 2) AS avg_support_tickets,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(AVG(customer_lifetime_value), 2) AS avg_customer_lifetime_value
FROM cleaned_customer_churn
GROUP BY churn_status;
