from database import get_connection
from datetime import date

def add_transaction(type, category, amount, note=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (type, category, amount, date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (type, category, amount, str(date.today()), note))

    conn.commit()
    conn.close()
    print(f"{type.capitalize()} of ${amount} added under '{category}'.")

def view_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No transactions found.")
        return

    print(f"\n{'ID':<5} {'Type':<10} {'Category':<15} {'Amount':<10} {'Date':<12} {'Note'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<10} {row[2]:<15} ${row[3]:<9} {row[4]:<12} {row[5] or ''}")

def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()
    print(f"Transaction {transaction_id} deleted.")

def monthly_summary():
    conn = get_connection()
    cursor = conn.cursor()

    month = str(date.today())[:7]  # Gets "YYYY-MM"

    cursor.execute("""
        SELECT type, SUM(amount) FROM transactions
        WHERE date LIKE ?
        GROUP BY type
    """, (f"{month}%",))

    rows = cursor.fetchall()
    conn.close()

    print(f"\n--- Summary for {month} ---")
    total_income = 0
    total_expenses = 0

    for row in rows:
        print(f"{row[0].capitalize()}: ${row[1]:.2f}")
        if row[0] == "income":
            total_income = row[1]
        else:
            total_expenses = row[1]

    print(f"Net: ${total_income - total_expenses:.2f}")