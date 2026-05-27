# Executive Summary

## Project Snapshot

This project analyzes churn for a Netflix-style streaming subscription company using Python, SQL, and dashboard-ready CSV outputs. The cleaned dataset contains 1,500 unique customers after removing 20 duplicate raw records.

## Key Metrics

| Metric | Value |
| --- | ---: |
| Total customers | 1,500 |
| Churned customers | 424 |
| Overall churn rate | 28.27% |
| Monthly recurring revenue | $29,980.83 |
| Lost monthly recurring revenue | $9,042.66 |
| Estimated annual revenue loss | $108,511.92 |

## Key Insights

- Month-to-month customers had the highest churn rate at 40%, compared with 19% for one-year contracts and 9% for two-year contracts.
- Customers in the first 6 months had a 48% churn rate, making early lifecycle retention the clearest opportunity.
- Electronic check customers had the highest payment-method churn rate at 35%.
- Competitor offers and price concerns were the most common churn reasons.

## Recommendations

- Build a first-90-day onboarding journey that targets month-to-month customers.
- Offer upgrade incentives that move high-risk customers from month-to-month contracts into annual plans.
- Review pricing and competitor positioning for customers citing price or competitor offers.
- Monitor support tickets as an early churn signal and trigger proactive outreach after multiple tickets.
