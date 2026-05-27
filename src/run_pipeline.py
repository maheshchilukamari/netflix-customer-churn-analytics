"""
Run the full customer churn analytics pipeline.

Pipeline order:
1. Generate a realistic raw sample dataset.
2. Clean the raw dataset and create analysis features.
3. Export dashboard-ready summary CSV files.
4. Export static chart images for documentation if charting packages are installed.
"""

from generate_sample_data import main as generate_sample_data
from data_cleaning import main as clean_data
from analysis_exports import main as export_analysis_files


def main() -> None:
    """Execute every project step in the correct order."""
    generate_sample_data()
    clean_data()
    export_analysis_files()

    # Matplotlib and Seaborn are listed in requirements.txt. This try/except
    # keeps the data pipeline usable even before a new user installs them.
    try:
        from create_visuals import main as create_visuals

        create_visuals()
    except ModuleNotFoundError as error:
        print(f"Skipping chart image export because an optional package is missing: {error.name}")

    print("Customer churn analytics pipeline completed successfully.")


if __name__ == "__main__":
    main()
