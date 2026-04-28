import pandas as pd
import logging

logger = logging.getLogger(__name__)


def generate_kpis(df):
    kpis = {}

    # Total spend
    kpis["total_spend"] = round(df["amount"].sum(), 2)

    # Average transaction
    kpis["average_transaction"] = round(df["amount"].mean(), 2)

    # Highest single expense
    kpis["highest_expense"] = round(df["amount"].max(), 2)

    # Number of transactions
    kpis["total_transactions"] = len(df)

    logger.info(f"KPIs generated: {kpis}")
    return kpis


def spend_by_category(df):
    if "category" not in df.columns:
        return {}

    result = (
        df.groupby("category")["amount"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .to_dict()
    )

    logger.info(f"Spend by category calculated: {len(result)} categories.")
    return result


def spend_by_month(df):
    df["month"] = df["date"].dt.to_period("M").astype(str)

    result = (
        df.groupby("month")["amount"]
        .sum()
        .round(2)
        .to_dict()
    )

    logger.info(f"Spend by month calculated: {len(result)} months.")
    return result


def top_expenses(df, n=5):
    result = (
        df.nlargest(n, "amount")[["date", "description", "category", "amount"]]
        .reset_index(drop=True)
    )

    logger.info(f"Top {n} expenses retrieved.")
    return result