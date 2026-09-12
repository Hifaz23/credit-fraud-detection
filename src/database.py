from pathlib import Path
import json
import sqlite3
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "fraud_predictions.db"


def initialize_database():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                transaction_json TEXT,
                fraud_probability REAL,
                prediction INTEGER,
                decision TEXT
            )
        """)


def save_prediction(
    transaction: dict,
    fraud_probability: float,
    prediction: int,
    decision: str
):
    timestamp = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            INSERT INTO predictions (
                timestamp,
                transaction_json,
                fraud_probability,
                prediction,
                decision
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                json.dumps(transaction),
                fraud_probability,
                prediction,
                decision
            )
        )