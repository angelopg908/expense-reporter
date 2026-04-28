import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"date", "amount"}


def load_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(filepath)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    logger.info(f"Loaded {len(df)} rows from {filepath}")
    return df


def validate_columns(df, filepath):
    missing = REQUIRED_COLUMNS - set(df.columns.str.lower())
    if missing:
        raise ValueError(f"Missing required columns in {filepath}: {missing}")


def load_all_files(data_folder="data"):
    all_dataframes = []

    files = [f for f in os.listdir(data_folder) if f.endswith((".csv", ".xlsx", ".xls"))]

    if not files:
        logger.warning("No data files found in the data folder.")
        return None

    for filename in files:
        filepath = os.path.join(data_folder, filename)
        df = load_file(filepath)
        df.columns = df.columns.str.lower().str.strip()
        validate_columns(df, filename)
        df["source_file"] = filename
        all_dataframes.append(df)

    combined = pd.concat(all_dataframes, ignore_index=True)
    logger.info(f"Total rows loaded: {len(combined)}")
    return combined