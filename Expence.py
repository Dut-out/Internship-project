def expense_tracker():
    expenses = {}
    
    while True:
        print("\n1. Add Expense | 2. View Totals | 3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            category = input("Enter category (e.g., Food, Travel): ").capitalize()
            amount = float(input("Enter amount: "))
            expenses[category] = expenses.get(category, 0) + amount
            print("Expense added!")
        elif choice == '2':
            print("\n--- Total Expenses ---")
            for cat, total in expenses.items():
                print(f"{cat}: ${total:.2f}")
        elif choice == '3':
            break

if __name__ == "__main__":
    expense_tracker()