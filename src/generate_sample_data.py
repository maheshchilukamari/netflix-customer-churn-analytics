"""
Generate a realistic Netflix-style customer churn dataset.

This script creates a reproducible raw CSV file for a streaming subscription business.
The generated data intentionally includes a small number of missing values and
duplicate rows so the cleaning script has realistic work to do.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# A fixed random seed makes the sample dataset the same every time we run it.
RANDOM_SEED = 42

# Project paths are built from this file location so the script can be run from
# any folder, not only from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "customer_churn_raw.csv"


def choose_churn_reason(churned: bool, contract_type: str, support_tickets: int) -> str:
    """Return a realistic churn reason for churned customers."""
    if not churned:
        return "Not churned"

    if support_tickets >= 4:
        reasons = ["Poor customer support", "Technical issues", "Product dissatisfaction"]
        probabilities = [0.50, 0.30, 0.20]
    elif contract_type == "Month-to-month":
        reasons = ["Price too high", "Competitor offer", "Temporary need ended"]
        probabilities = [0.40, 0.35, 0.25]
    else:
        reasons = ["Moved location", "Product dissatisfaction", "Competitor offer"]
        probabilities = [0.35, 0.30, 0.35]

    return str(np.random.choice(reasons, p=probabilities))


def calculate_churn_probability(
    tenure: int,
    contract_type: str,
    payment_method: str,
    monthly_charges: float,
    support_tickets: int,
) -> float:
    """Calculate churn probability from common business risk factors."""
    probability = 0.08

    # Customers on flexible contracts usually have less friction when leaving.
    if contract_type == "Month-to-month":
        probability += 0.23
    elif contract_type == "One year":
        probability += 0.08

    # Newer customers often churn before habits and value are established.
    if tenure <= 6:
        probability += 0.18
    elif tenure <= 12:
        probability += 0.10
    elif tenure >= 49:
        probability -= 0.05

    # Many support tickets can signal frustration or product fit issues.
    if support_tickets >= 4:
        probability += 0.16
    elif support_tickets >= 2:
        probability += 0.06

    # Electronic check can be a churn-risk signal because it may reflect billing friction.
    if payment_method == "Electronic check":
        probability += 0.08

    # Higher bills may increase churn pressure.
    if monthly_charges >= 90:
        probability += 0.06
    elif monthly_charges < 45:
        probability -= 0.03

    # Keep the value between realistic lower and upper limits.
    return float(np.clip(probability, 0.03, 0.82))


def build_customer_dataset(row_count: int = 1500) -> pd.DataFrame:
    """Build the raw customer churn DataFrame."""
    np.random.seed(RANDOM_SEED)

    customer_ids = [f"CUST-{customer_id:05d}" for customer_id in range(1, row_count + 1)]

    genders = np.random.choice(["Female", "Male"], size=row_count, p=[0.51, 0.49])
    age_groups = np.random.choice(
        ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        size=row_count,
        p=[0.09, 0.24, 0.26, 0.21, 0.14, 0.06],
    )
    contract_types = np.random.choice(
        ["Month-to-month", "One year", "Two year"],
        size=row_count,
        p=[0.54, 0.25, 0.21],
    )
    payment_methods = np.random.choice(
        ["Credit card", "Bank transfer", "Electronic check", "Mailed check"],
        size=row_count,
        p=[0.33, 0.28, 0.29, 0.10],
    )
    streaming_plans = np.random.choice(
        ["Basic", "Standard", "Premium", "Mobile"],
        size=row_count,
        p=[0.28, 0.39, 0.25, 0.08],
    )

    rows = []
    for index in range(row_count):
        contract_type = contract_types[index]
        payment_method = payment_methods[index]
        streaming_plan = streaming_plans[index]

        # Tenure is shaped so month-to-month customers are more likely to be new.
        if contract_type == "Month-to-month":
            tenure = int(np.random.gamma(shape=2.0, scale=9.0))
        elif contract_type == "One year":
            tenure = int(np.random.normal(loc=28, scale=14))
        else:
            tenure = int(np.random.normal(loc=46, scale=16))
        tenure = int(np.clip(tenure, 1, 72))

        service_base_charge = {
            "Mobile": 9.99,
            "Basic": 15.49,
            "Standard": 22.99,
            "Premium": 29.99,
        }[streaming_plan]
        contract_discount = {
            "Month-to-month": 0,
            "One year": -5,
            "Two year": -9,
        }[contract_type]
        monthly_charges = round(
            service_base_charge + contract_discount + np.random.normal(loc=0, scale=12),
            2,
        )
        monthly_charges = float(np.clip(monthly_charges, 7.99, 39.99))

        # Support tickets loosely rise with higher charges and premium streaming plans.
        ticket_lambda = 0.8 + (monthly_charges > 25) * 0.4 + (streaming_plan == "Premium") * 0.2
        support_tickets = int(np.random.poisson(lam=ticket_lambda))

        churn_probability = calculate_churn_probability(
            tenure=tenure,
            contract_type=contract_type,
            payment_method=payment_method,
            monthly_charges=monthly_charges,
            support_tickets=support_tickets,
        )
        churned = bool(np.random.random() < churn_probability)
        churn_status = "Churned" if churned else "Stayed"
        churn_reason = choose_churn_reason(churned, contract_type, support_tickets)

        # Total charges are approximate lifetime revenue for the customer.
        total_charges = round(monthly_charges * tenure + np.random.normal(loc=0, scale=35), 2)
        total_charges = max(total_charges, monthly_charges)

        rows.append(
            {
                "customer_id": customer_ids[index],
                "gender": genders[index],
                "age_group": age_groups[index],
                "tenure": tenure,
                "contract_type": contract_type,
                "payment_method": payment_method,
                "monthly_charges": monthly_charges,
                "total_charges": round(total_charges, 2),
                "streaming_plan": streaming_plan,
                "support_tickets": support_tickets,
                "churn_status": churn_status,
                "churn_reason": churn_reason,
            }
        )

    dataset = pd.DataFrame(rows)

    # Add a few missing values to make the cleaning step realistic.
    missing_total_indexes = np.random.choice(dataset.index, size=18, replace=False)
    dataset.loc[missing_total_indexes, "total_charges"] = np.nan

    missing_payment_indexes = np.random.choice(dataset.index, size=10, replace=False)
    dataset.loc[missing_payment_indexes, "payment_method"] = np.nan

    # Add duplicate records that the cleaning pipeline should remove.
    duplicate_rows = dataset.sample(n=20, random_state=RANDOM_SEED)
    dataset = pd.concat([dataset, duplicate_rows], ignore_index=True)

    # Shuffle rows so duplicates are not all at the bottom of the raw file.
    dataset = dataset.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    return dataset


def main() -> None:
    """Generate the raw CSV file."""
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset = build_customer_dataset()
    dataset.to_csv(RAW_DATA_PATH, index=False)
    print(f"Generated raw dataset with {len(dataset):,} rows: {RAW_DATA_PATH}")


if __name__ == "__main__":
    main()
