# Expense Reporter

A Python automation tool that processes expense data from CSV/Excel files,
stores it in a SQLite database, and generates Excel reports and interactive dashboards.

## Features
- Reads CSV and Excel files automatically
- Cleans and validates data with pandas
- Stores expenses in SQLite with duplicate detection
- Generates formatted Excel reports
- Creates interactive HTML dashboards with Plotly
- Timestamped outputs on every run
- Full logging system

## Tech Stack
- Python 3.14
- pandas
- SQLite / SQLAlchemy
- openpyxl
- Plotly
- pytest

## Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Usage
1. Add your CSV or Excel files to the `data/` folder
2. Files must have these columns: `date`, `amount`, `description`, `category`
3. Run the tool:
python main.py
4. Find your reports in the `output/` folder

## Output
- `output/expense_report_YYYY-MM-DD_HH-MM-SS.xlsx` — formatted Excel report
- `output/dashboard_YYYY-MM-DD_HH-MM-SS.html` — interactive Plotly dashboard