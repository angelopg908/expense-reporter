import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_data(df):
    original_count = len(df)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Drop rows missing critical fields
    df = df.dropna(subset=["date", "amount"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean amount column
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Standardize category column
    if "category" in df.columns:
        df["category"] = df["category"].str.strip().str.title()
    else:
        df["category"] = "Uncategorized"

    # Standardize description column
    if "description" in df.columns:
        df["description"] = df["description"].str.strip().str.title()
    else:
        df["description"] = ""

    cleaned_count = len(df)
    logger.info(f"Cleaned data: {original_count} rows in, {cleaned_count} rows out.")

    return df