import logging
import os
from ingest import load_all_files
from clean import clean_data
from db import initialize_db, insert_expenses, fetch_all_expenses
from analytics import generate_kpis, spend_by_category, spend_by_month, top_expenses
from report import export_excel, export_dashboard
from datetime import datetime

# --- Logging setup ---
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run():
    logger.info("Starting expense reporter...")

    # Step 1: Initialize database
    initialize_db()

    # Step 2: Load files from data folder
    df_raw = load_all_files("data")
    if df_raw is None:
        logger.warning("No files to process. Add CSV or Excel files to the data/ folder.")
        return

    # Step 3: Clean data
    df_clean = clean_data(df_raw)

    # Step 4: Store in database
    insert_expenses(df_clean)

    # Step 5: Print KPIs to terminal
    kpis = generate_kpis(df_clean)
    print("\n--- KPIs ---")
    for key, value in kpis.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\n--- Spend by Category ---")
    for cat, total in spend_by_category(df_clean).items():
        print(f"  {cat}: ${total}")

    print("\n--- Top 5 Expenses ---")
    print(top_expenses(df_clean).to_string(index=False))

    # Step 6: Export reports
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    export_excel(df_clean, output_path=f"output/expense_report_{timestamp}.xlsx")
    export_dashboard(df_clean, output_path=f"output/dashboard_{timestamp}.html")

    logger.info("Expense reporter finished successfully.")
    print("\nDone! Check the output/ folder for your reports.")


if __name__ == "__main__":
    run()