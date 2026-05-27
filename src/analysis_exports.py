"""
Create dashboard-ready summary CSV files from the cleaned churn dataset.

These outputs can be imported directly into Tableau, Power BI, Excel, or Google
Sheets for dashboard building.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_customer_churn.csv"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"


def load_cleaned_data(file_path: Path = CLEANED_DATA_PATH) -> pd.DataFrame:
    """Load cleaned customer data."""
    return pd.read_csv(file_path)


def add_churn_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Create a numeric churn flag so averages can calculate churn rates."""
    dataset = df.copy()
    dataset["churn_flag"] = dataset["churn_status"].eq("Churned").astype(int)
    return dataset


def create_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize churn by key business dimensions."""
    summary = (
        df.groupby(["contract_type", "payment_method"], dropna=False)
        .agg(
            customers=("customer_id", "count"),
            churned_customers=("churn_flag", "sum"),
            churn_rate=("churn_flag", "mean"),
            avg_monthly_charges=("monthly_charges", "mean"),
            avg_tenure=("tenure", "mean"),
        )
        .reset_index()
    )

    summary["churn_rate"] = (summary["churn_rate"] * 100).round(2)
    summary["avg_monthly_charges"] = summary["avg_monthly_charges"].round(2)
    summary["avg_tenure"] = summary["avg_tenure"].round(1)
    return summary


def create_revenue_loss_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize monthly and annual revenue loss by contract and tenure group."""
    summary = (
        df.groupby(["contract_type", "tenure_group"], dropna=False)
        .agg(
            churned_customers=("churn_flag", "sum"),
            monthly_revenue_loss=("monthly_revenue_loss", "sum"),
            annual_revenue_loss=("annual_revenue_loss", "sum"),
            avg_lost_monthly_revenue=("monthly_revenue_loss", "mean"),
        )
        .reset_index()
    )

    money_columns = ["monthly_revenue_loss", "annual_revenue_loss", "avg_lost_monthly_revenue"]
    summary[money_columns] = summary[money_columns].round(2)
    return summary


def create_segment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Create customer segmentation metrics for dashboard filters and charts."""
    segment = (
        df.groupby(["age_group", "streaming_plan", "tenure_group"], dropna=False)
        .agg(
            customers=("customer_id", "count"),
            churned_customers=("churn_flag", "sum"),
            churn_rate=("churn_flag", "mean"),
            avg_support_tickets=("support_tickets", "mean"),
            avg_monthly_charges=("monthly_charges", "mean"),
            total_monthly_revenue=("monthly_charges", "sum"),
            monthly_revenue_loss=("monthly_revenue_loss", "sum"),
        )
        .reset_index()
    )

    segment["churn_rate"] = (segment["churn_rate"] * 100).round(2)
    rounded_columns = [
        "avg_support_tickets",
        "avg_monthly_charges",
        "total_monthly_revenue",
        "monthly_revenue_loss",
    ]
    segment[rounded_columns] = segment[rounded_columns].round(2)
    return segment


def export_dashboard_files(df: pd.DataFrame) -> None:
    """Write all dashboard summary files to the dashboard folder."""
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    create_churn_summary(df).to_csv(DASHBOARD_DIR / "churn_summary.csv", index=False)
    create_revenue_loss_summary(df).to_csv(DASHBOARD_DIR / "revenue_loss_summary.csv", index=False)
    create_segment_analysis(df).to_csv(DASHBOARD_DIR / "segment_analysis.csv", index=False)


def main() -> None:
    """Create dashboard-ready analysis files."""
    cleaned_df = load_cleaned_data()
    cleaned_df = add_churn_flag(cleaned_df)
    export_dashboard_files(cleaned_df)
    print(f"Dashboard CSV files exported to: {DASHBOARD_DIR}")


if __name__ == "__main__":
    main()
