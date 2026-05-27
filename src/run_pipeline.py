"""
Run the full customer churn analytics pipeline.

Pipeline order:
1. Generate a realistic raw sample dataset.
2. Clean the raw dataset and create analysis features.
3. Export dashboard-ready summary CSV files.
4. Export static chart images for documentation.
"""

from generate_sample_data import main as generate_sample_data
from data_cleaning import main as clean_data
from analysis_exports import main as export_analysis_files
from create_visuals import main as create_visuals


def main() -> None:
    """Execute every project step in the correct order."""
    generate_sample_data()
    clean_data()
    export_analysis_files()

    create_visuals()

    print("Customer churn analytics pipeline completed successfully.")


if __name__ == "__main__":
    main()
