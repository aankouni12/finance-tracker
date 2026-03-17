import pytest
import os
import sqlite3
from database import initialize_db, get_connection
from tracker import add_transaction, view_transactions, delete_transaction, monthly_summary

# Use a separate test database so we don't mess with real data
TEST_DB = "test_finance.db"

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    monkeypatch.setattr("database.DB_NAME", TEST_DB)
    monkeypatch.setattr("tracker.get_connection", lambda: sqlite3.connect(TEST_DB))
    initialize_db()
    yield
    os.remove(TEST_DB)

def test_add_income():
    add_transaction("income", "salary", 2500)
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0][1] == "income"
    assert rows[0][3] == 2500

def test_add_expense():
    add_transaction("expense", "food", 50)
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0][1] == "expense"
    assert rows[0][3] == 50

def test_delete_transaction():
    add_transaction("income", "salary", 2500)
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM transactions")
    row = cursor.fetchone()
    conn.close()
    delete_transaction(row[0])
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 0

def test_multiple_transactions():
    add_transaction("income", "salary", 3000)
    add_transaction("expense", "rent", 1000)
    add_transaction("expense", "food", 200)
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 3