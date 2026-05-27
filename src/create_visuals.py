"""
Create static chart images for the README and reports.

The dashboard CSV files are the main output for Tableau or Power BI. These PNG
charts give the project a quick visual preview on GitHub.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_customer_churn.csv"
IMAGES_DIR = PROJECT_ROOT / "images"


def load_data() -> pd.DataFrame:
    """Load cleaned data and add a numeric churn flag for chart calculations."""
    df = pd.read_csv(CLEANED_DATA_PATH)
    df["churn_flag"] = df["churn_status"].eq("Churned").astype(int)
    return df


def save_churn_by_contract_chart(df: pd.DataFrame) -> None:
    """Save a bar chart showing churn rate by contract type."""
    chart_data = (
        df.groupby("contract_type", as_index=False)["churn_flag"]
        .mean()
        .assign(churn_rate_percent=lambda data: data["churn_flag"] * 100)
        .sort_values("churn_rate_percent", ascending=False)
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(data=chart_data, x="contract_type", y="churn_rate_percent", color="#2F80ED")
    plt.title("Churn Rate by Contract Type")
    plt.xlabel("Contract Type")
    plt.ylabel("Churn Rate (%)")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "churn_by_contract_type.png", dpi=160)
    plt.close()


def save_churn_by_payment_chart(df: pd.DataFrame) -> None:
    """Save a bar chart showing churn rate by payment method."""
    chart_data = (
        df.groupby("payment_method", as_index=False)["churn_flag"]
        .mean()
        .assign(churn_rate_percent=lambda data: data["churn_flag"] * 100)
        .sort_values("churn_rate_percent", ascending=False)
    )

    plt.figure(figsize=(9, 5))
    sns.barplot(data=chart_data, x="payment_method", y="churn_rate_percent", color="#27AE60")
    plt.title("Churn Rate by Payment Method")
    plt.xlabel("Payment Method")
    plt.ylabel("Churn Rate (%)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "churn_by_payment_method.png", dpi=160)
    plt.close()


def save_revenue_loss_chart(df: pd.DataFrame) -> None:
    """Save a bar chart showing lost monthly revenue by tenure group."""
    tenure_order = ["0-6 months", "7-12 months", "13-24 months", "25-48 months", "49+ months"]
    chart_data = (
        df.groupby("tenure_group", as_index=False)["monthly_revenue_loss"]
        .sum()
        .assign(tenure_group=lambda data: pd.Categorical(data["tenure_group"], tenure_order, ordered=True))
        .sort_values("tenure_group")
    )

    plt.figure(figsize=(9, 5))
    sns.barplot(data=chart_data, x="tenure_group", y="monthly_revenue_loss", color="#F2994A")
    plt.title("Monthly Revenue Loss by Tenure Group")
    plt.xlabel("Tenure Group")
    plt.ylabel("Monthly Revenue Loss ($)")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "revenue_loss_by_tenure_group.png", dpi=160)
    plt.close()


def main() -> None:
    """Create all portfolio chart images."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()

    # A consistent theme makes all charts look like they belong together.
    sns.set_theme(style="whitegrid", palette="deep")

    save_churn_by_contract_chart(df)
    save_churn_by_payment_chart(df)
    save_revenue_loss_chart(df)
    print(f"Chart images exported to: {IMAGES_DIR}")


if __name__ == "__main__":
    main()
