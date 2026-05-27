/*
Revenue analysis queries.

These queries quantify how much monthly and annual recurring revenue is at risk
because of churn.
*/

-- Total recurring revenue and estimated revenue loss.
SELECT
    ROUND(SUM(monthly_charges), 2) AS total_monthly_recurring_revenue,
    ROUND(SUM(monthly_revenue_loss), 2) AS lost_monthly_recurring_revenue,
    ROUND(SUM(annual_revenue_loss), 2) AS estimated_annual_revenue_loss
FROM cleaned_customer_churn;

-- Revenue loss by contract type.
SELECT
    contract_type,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(monthly_revenue_loss), 2) AS monthly_revenue_loss,
    ROUND(SUM(annual_revenue_loss), 2) AS annual_revenue_loss,
    ROUND(AVG(CASE WHEN churn_status = 'Churned' THEN monthly_charges END), 2) AS avg_lost_customer_mrr
FROM cleaned_customer_churn
GROUP BY contract_type
ORDER BY monthly_revenue_loss DESC;

-- Revenue loss by tenure group.
SELECT
    tenure_group,
    SUM(CASE WHEN churn_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(monthly_revenue_loss), 2) AS monthly_revenue_loss,
    ROUND(SUM(annual_revenue_loss), 2) AS annual_revenue_loss
FROM cleaned_customer_churn
GROUP BY tenure_group
ORDER BY monthly_revenue_loss DESC;

-- High-value churned customers for retention review.
SELECT
    customer_id,
    contract_type,
    tenure,
    payment_method,
    internet_service,
    support_tickets,
    monthly_charges,
    annual_revenue_loss,
    churn_reason
FROM cleaned_customer_churn
WHERE churn_status = 'Churned'
ORDER BY monthly_charges DESC
LIMIT 25;
