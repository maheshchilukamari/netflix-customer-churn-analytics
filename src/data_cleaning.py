"""
Clean the raw customer churn dataset and create modeling-ready features.

The cleaning steps are written as small functions so beginners can understand,
test, and reuse each step.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "customer_churn_raw.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_customer_churn.csv"
DASHBOARD_DATA_PATH = PROJECT_ROOT / "dashboard" / "cleaned_customer_churn.csv"


def load_raw_data(file_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load raw customer churn data from a CSV file."""
    return pd.read_csv(file_path)


def standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove extra spaces from text columns without changing numeric columns."""
    cleaned_df = df.copy()
    text_columns = cleaned_df.select_dtypes(include="object").columns

    for column in text_columns:
        cleaned_df[column] = cleaned_df[column].astype("string").str.strip()

    return cleaned_df


def remove_duplicate_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Keep the first record for each customer_id and remove duplicate customers."""
    return df.drop_duplicates(subset=["customer_id"], keep="first").copy()


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to useful numeric and text data types."""
    cleaned_df = df.copy()

    # errors="coerce" turns invalid numeric values into NaN so we can clean them.
    cleaned_df["tenure"] = pd.to_numeric(cleaned_df["tenure"], errors="coerce")
    cleaned_df["monthly_charges"] = pd.to_numeric(cleaned_df["monthly_charges"], errors="coerce")
    cleaned_df["total_charges"] = pd.to_numeric(cleaned_df["total_charges"], errors="coerce")
    cleaned_df["support_tickets"] = pd.to_numeric(cleaned_df["support_tickets"], errors="coerce")

    return cleaned_df


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values with sensible business rules."""
    cleaned_df = df.copy()

    # Missing total charges are estimated from monthly charge times tenure.
    estimated_total_charges = cleaned_df["monthly_charges"] * cleaned_df["tenure"]
    cleaned_df["total_charges"] = cleaned_df["total_charges"].fillna(estimated_total_charges)

    # If payment method is missing, mark it as Unknown instead of deleting the row.
    cleaned_df["payment_method"] = cleaned_df["payment_method"].fillna("Unknown")

    # Numeric columns should not have missing values after this point.
    numeric_defaults = {
        "tenure": cleaned_df["tenure"].median(),
        "monthly_charges": cleaned_df["monthly_charges"].median(),
        "total_charges": cleaned_df["total_charges"].median(),
        "support_tickets": 0,
    }
    cleaned_df = cleaned_df.fillna(value=numeric_defaults)

    return cleaned_df


def create_tenure_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Create easy-to-read tenure groups for analysis and dashboards."""
    cleaned_df = df.copy()

    bins = [-np.inf, 6, 12, 24, 48, np.inf]
    labels = ["0-6 months", "7-12 months", "13-24 months", "25-48 months", "49+ months"]
    cleaned_df["tenure_group"] = pd.cut(cleaned_df["tenure"], bins=bins, labels=labels)

    return cleaned_df


def create_revenue_loss_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add revenue fields that quantify the value of churned customers."""
    cleaned_df = df.copy()

    churned_mask = cleaned_df["churn_status"].eq("Churned")
    cleaned_df["monthly_revenue_loss"] = np.where(churned_mask, cleaned_df["monthly_charges"], 0)
    cleaned_df["annual_revenue_loss"] = cleaned_df["monthly_revenue_loss"] * 12
    cleaned_df["customer_lifetime_value"] = cleaned_df["total_charges"]

    return cleaned_df


def clean_customer_churn_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Run all cleaning and feature engineering steps in order."""
    cleaned_df = (
        raw_df.pipe(standardize_text_columns)
        .pipe(remove_duplicate_customers)
        .pipe(fix_data_types)
        .pipe(clean_missing_values)
        .pipe(create_tenure_groups)
        .pipe(create_revenue_loss_metrics)
    )

    # Round currency columns so dashboard values look clean.
    currency_columns = [
        "monthly_charges",
        "total_charges",
        "monthly_revenue_loss",
        "annual_revenue_loss",
        "customer_lifetime_value",
    ]
    cleaned_df[currency_columns] = cleaned_df[currency_columns].round(2)

    # Convert count-like fields back to integers after numeric cleaning.
    cleaned_df["tenure"] = cleaned_df["tenure"].round(0).astype(int)
    cleaned_df["support_tickets"] = cleaned_df["support_tickets"].round(0).astype(int)

    return cleaned_df


def export_cleaned_data(cleaned_df: pd.DataFrame) -> None:
    """Save cleaned data to both data/processed and dashboard folders."""
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    cleaned_df.to_csv(PROCESSED_DATA_PATH, index=False)
    cleaned_df.to_csv(DASHBOARD_DATA_PATH, index=False)


def main() -> None:
    """Load, clean, and export the customer churn dataset."""
    raw_df = load_raw_data()
    cleaned_df = clean_customer_churn_data(raw_df)
    export_cleaned_data(cleaned_df)
    print(f"Cleaned dataset exported with {len(cleaned_df):,} customers.")
    print(f"Processed file: {PROCESSED_DATA_PATH}")
    print(f"Dashboard file: {DASHBOARD_DATA_PATH}")


if __name__ == "__main__":
    main()
