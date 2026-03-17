from database import initialize_db
from tracker import add_transaction, view_transactions, delete_transaction, monthly_summary

def main():
    initialize_db()

    while True:
        print("\n===== Finance Tracker =====")
        print("1. Add transaction")
        print("2. View all transactions")
        print("3. Delete a transaction")
        print("4. Monthly summary")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            type = input("Type (income/expense): ").lower()
            category = input("Category (e.g. food, salary, rent): ")
            amount = float(input("Amount: "))
            note = input("Note (optional, press Enter to skip): ")
            add_transaction(type, category, amount, note)

        elif choice == "2":
            view_transactions()

        elif choice == "3":
            transaction_id = int(input("Enter transaction ID to delete: "))
            delete_transaction(transaction_id)

        elif choice == "4":
            monthly_summary()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()