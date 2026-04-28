import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

DB_PATH = os.path.join("logs", "..", "expense_reporter.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT,
            category TEXT,
            amount REAL NOT NULL,
            source_file TEXT
        )
    """)

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")


def insert_expenses(df, source_file="unknown"):
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0
    for _, row in df.iterrows():
        # Check for duplicate before inserting
        cursor.execute("""
            SELECT COUNT(*) FROM expenses
            WHERE date = ? AND description = ? AND amount = ?
        """, (
            str(row["date"]),
            str(row.get("description", "")),
            float(row["amount"])
        ))

        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO expenses (date, description, category, amount, source_file)
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(row["date"]),
                str(row.get("description", "")),
                str(row.get("category", "Uncategorized")),
                float(row["amount"]),
                source_file
            ))
            inserted += 1
        else:
            skipped += 1

    conn.commit()
    conn.close()
    logger.info(f"Inserted {inserted} new records, skipped {skipped} duplicates from {source_file}.")


def fetch_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date")
    rows = cursor.fetchall()
    conn.close()
    return rows