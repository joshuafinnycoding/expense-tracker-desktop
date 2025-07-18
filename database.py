import sqlite3
from datetime import datetime

DB_FILE = "expenses.db"

def connect_db(db_file=DB_FILE):
    return sqlite3.connect(db_file)

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category_id INTEGER,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    conn.commit()

def add_expense(conn, amount, category, description, date=None):
    cursor = conn.cursor()
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    # Ensure category exists
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category,))
    category_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO expenses (amount, category_id, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category_id, description, date))
    conn.commit()

def delete_expense(conn, expense_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()

def get_expenses(conn, start_date=None, end_date=None):
    cursor = conn.cursor()
    query = """
        SELECT expenses.id, amount, categories.name, description, date
        FROM expenses
        LEFT JOIN categories ON expenses.category_id = categories.id
    """
    params = []
    if start_date and end_date:
        query += " WHERE date BETWEEN ? AND ?"
        params = [start_date, end_date]
    elif start_date:
        query += " WHERE date >= ?"
        params = [start_date]
    elif end_date:
        query += " WHERE date <= ?"
        params = [end_date]
    cursor.execute(query, params)
    return cursor.fetchall()

def get_monthly_summary(conn, year, month):
    cursor = conn.cursor()
    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-31"
    query = """
        SELECT categories.name, SUM(amount)
        FROM expenses
        LEFT JOIN categories ON expenses.category_id = categories.id
        WHERE date BETWEEN ? AND ?
        GROUP BY categories.name
    """
    cursor.execute(query, (start, end))
    return cursor.fetchall()
import sqlite3

DB_NAME = "expenses.db"
conn = None

def initialize_db():
    global conn
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT,
            date TEXT,
            notes TEXT
        )
    """)
    conn.commit()

def close_db():
    global conn
    if conn:
        conn.close()