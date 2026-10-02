import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).with_name("pocketsmart.db")

DEFAULT_CATEGORIES = [
    "Food", "Transport", "Shopping", "Education", "Bills",
    "Entertainment", "Health", "Travel", "Savings", "Other"
]

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income','expense')),
            note TEXT DEFAULT '',
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(amount, category, kind, note="", transaction_date=""):
    transaction_date = transaction_date or date.today().isoformat()
    conn = connect()
    cur = conn.execute(
        "INSERT INTO transactions(amount, category, type, note, date) VALUES (?, ?, ?, ?, ?)",
        (amount, category, kind, note, transaction_date)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM transactions WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)

def get_transactions():
    conn = connect()
    rows = conn.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_transaction(transaction_id):
    conn = connect()
    conn.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()

def get_summary():
    conn = connect()
    income = conn.execute(
        "SELECT COALESCE(SUM(amount),0) AS total FROM transactions WHERE type='income'"
    ).fetchone()["total"]
    expense = conn.execute(
        "SELECT COALESCE(SUM(amount),0) AS total FROM transactions WHERE type='expense'"
    ).fetchone()["total"]
    rows = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE type='expense'
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "balance": round(income - expense, 2),
        "by_category": [{"category": r["category"], "total": round(r["total"], 2)} for r in rows]
    }

def get_categories():
    return DEFAULT_CATEGORIES
