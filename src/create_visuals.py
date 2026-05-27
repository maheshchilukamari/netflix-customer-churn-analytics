"""
Create static chart images for the README and reports.

The dashboard CSV files are the main output for Tableau or Power BI. These PNG
charts give the project a quick visual preview on GitHub.
"""

from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ModuleNotFoundError:
    plt = None
    sns = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_customer_churn.csv"
IMAGES_DIR = PROJECT_ROOT / "images"


def draw_simple_bar_chart(
    chart_data: pd.DataFrame,
    category_column: str,
    value_column: str,
    title: str,
    y_label: str,
    output_path: Path,
    bar_color: tuple[int, int, int],
) -> None:
    """Create a simple PNG bar chart when Matplotlib is not installed."""
    width = 1100
    height = 650
    margin_left = 170
    margin_right = 60
    margin_top = 90
    margin_bottom = 170
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    max_value = max(float(chart_data[value_column].max()), 1)
    bar_count = len(chart_data)
    bar_gap = 26
    bar_width = max(30, int((chart_width - bar_gap * (bar_count - 1)) / bar_count))

    draw.text((margin_left, 30), title, fill="black", font=font)
    draw.line((margin_left, margin_top, margin_left, margin_top + chart_height), fill="black", width=2)
    draw.line(
        (margin_left, margin_top + chart_height, margin_left + chart_width, margin_top + chart_height),
        fill="black",
        width=2,
    )
    draw.text((20, margin_top + chart_height // 2), y_label, fill="black", font=font)

    for index, row in chart_data.reset_index(drop=True).iterrows():
        category = str(row[category_column])
        value = float(row[value_column])
        x0 = margin_left + index * (bar_width + bar_gap)
        bar_height = int((value / max_value) * chart_height)
        y0 = margin_top + chart_height - bar_height
        x1 = x0 + bar_width
        y1 = margin_top + chart_height

        draw.rectangle((x0, y0, x1, y1), fill=bar_color)
        draw.text((x0, y0 - 20), f"{value:,.1f}", fill="black", font=font)
        draw.text((x0, y1 + 12), category[:18], fill="black", font=font)

    image.save(output_path)


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

    if plt is None or sns is None:
        draw_simple_bar_chart(
            chart_data,
            "contract_type",
            "churn_rate_percent",
            "Churn Rate by Contract Type",
            "Churn Rate (%)",
            IMAGES_DIR / "churn_by_contract_type.png",
            (47, 128, 237),
        )
        return

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

    if plt is None or sns is None:
        draw_simple_bar_chart(
            chart_data,
            "payment_method",
            "churn_rate_percent",
            "Churn Rate by Payment Method",
            "Churn Rate (%)",
            IMAGES_DIR / "churn_by_payment_method.png",
            (39, 174, 96),
        )
        return

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

    if plt is None or sns is None:
        draw_simple_bar_chart(
            chart_data,
            "tenure_group",
            "monthly_revenue_loss",
            "Monthly Revenue Loss by Tenure Group",
            "Monthly Revenue Loss ($)",
            IMAGES_DIR / "revenue_loss_by_tenure_group.png",
            (242, 153, 74),
        )
        return

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
    if sns is not None:
        sns.set_theme(style="whitegrid", palette="deep")

    save_churn_by_contract_chart(df)
    save_churn_by_payment_chart(df)
    save_revenue_loss_chart(df)
    print(f"Chart images exported to: {IMAGES_DIR}")


if __name__ == "__main__":
    main()
