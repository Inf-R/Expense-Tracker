import argparse
from storage import JSONStorage
from services import ExpenseService


def interactive_mode(service):
    while True:
        print("\n====== Expense Tracker ======")
        print("1. Add Expense")
        print("2. List Expenses")
        print("3. Summary")
        print("4. Summary by Month")
        print("5. Delete Expense")
        print("6. Update Expense")
        print("7. Filter by Category")
        print("8. Exit")

        choice = input("Choose option: ")

        try:
            if choice == "1":
                description = input("Description: ")
                amount = float(input("Amount: "))
                category = input("Category (optional): ")

                new_id = service.add_expense(
                    description,
                    amount,
                    category if category else None
                )

                print(f"Expense added successfully (ID: {new_id})")

            elif choice == "2":
                expenses = service.list_expenses()

                if not expenses:
                    print("No expenses found.")
                else:
                    print("ID  Date       Description   Category   Amount")
                    for e in expenses:
                        print(
                            f"{e['id']}   {e['date']}   "
                            f"{e['description']}   "
                            f"{e['category']}   "
                            f"${e['amount']}"
                        )

            elif choice == "3":
                total = service.summary()
                print(f"Total expenses: ${total}")

            elif choice == "4":
                month = int(input("Enter month (1-12): "))
                total = service.summary(month)
                print(f"Total expenses for month {month}: ${total}")

            elif choice == "5":
                expense_id = int(input("Enter Expense ID to delete: "))
                service.delete_expense(expense_id)
                print("Expense deleted successfully")

            elif choice == "6":
                expense_id = int(input("Enter Expense ID to update: "))
                description = input("New Description (leave blank to skip): ")
                amount_input = input("New Amount (leave blank to skip): ")

                amount = float(amount_input) if amount_input else None

                service.update_expense(
                    expense_id,
                    description if description else None,
                    amount
                )

                print("Expense updated successfully")

            elif choice == "7":
                category_name = input("Enter category: ")
                expenses, total = service.filter_by_category(category_name)

                if not expenses:
                    print("No expenses found.")
                else:
                    print("ID  Date       Description   Amount")
                    for e in expenses:
                        print(
                            f"{e['id']}   {e['date']}   "
                            f"{e['description']}   "
                            f"${e['amount']}"
                        )

                    print(f"\nTotal for category {category_name}: ${total}")

            elif choice == "8":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")

        except Exception as e:
            print("Error:", e)


def main():
    storage = JSONStorage()
    service = ExpenseService(storage)

    parser = argparse.ArgumentParser(prog="expense-tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add = subparsers.add_parser("add")
    add.add_argument("--description", required=True)
    add.add_argument("--amount", type=float, required=True)
    add.add_argument("--category")

    # List
    subparsers.add_parser("list")

    # Delete
    delete = subparsers.add_parser("delete")
    delete.add_argument("--id", type=int, required=True)

    # Update
    update = subparsers.add_parser("update")
    update.add_argument("--id", type=int, required=True)
    update.add_argument("--description")
    update.add_argument("--amount", type=float)

    # Summary
    summary = subparsers.add_parser("summary")
    summary.add_argument("--month", type=int)

    # Category Filter
    category = subparsers.add_parser("category")
    category.add_argument("--name", required=True)

    # Interactive
    subparsers.add_parser("interactive")

    args = parser.parse_args()

    try:
        if args.command == "add":
            new_id = service.add_expense(
                args.description,
                args.amount,
                args.category
            )
            print(f"Expense added successfully (ID: {new_id})")

        elif args.command == "list":
            expenses = service.list_expenses()
            print("ID  Date       Description   Category   Amount")
            for e in expenses:
                print(
                    f"{e['id']}   {e['date']}   "
                    f"{e['description']}   "
                    f"{e['category']}   "
                    f"${e['amount']}"
                )

        elif args.command == "delete":
            service.delete_expense(args.id)
            print("Expense deleted successfully")

        elif args.command == "update":
            service.update_expense(
                args.id,
                args.description,
                args.amount
            )
            print("Expense updated successfully")

        elif args.command == "summary":
            total = service.summary(args.month)
            if args.month:
                print(f"Total expenses for month {args.month}: ${total}")
            else:
                print(f"Total expenses: ${total}")

        elif args.command == "category":
            expenses, total = service.filter_by_category(args.name)

            if not expenses:
                print(f"No expenses found for category: {args.name}")
            else:
                print(f"Expenses for category: {args.name}")
                print("ID  Date       Description   Amount")
                for e in expenses:
                    print(
                        f"{e['id']}   {e['date']}   "
                        f"{e['description']}   "
                        f"${e['amount']}"
                    )

                print(f"\nTotal for category {args.name}: ${total}")

        elif args.command == "interactive":
            interactive_mode(service)

        else:
            parser.print_help()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()