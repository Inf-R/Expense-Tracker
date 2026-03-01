from models import Expense
from datetime import datetime


class ExpenseService:

    def __init__(self, storage):
        self.storage = storage

    def _generate_id(self, expenses):
        if not expenses:
            return 1
        return max(e["id"] for e in expenses) + 1

    def add_expense(self, description, amount, category=None):
        data = self.storage.load()
        new_id = self._generate_id(data["expenses"])

        expense = Expense.create(new_id, description, amount, category)
        data["expenses"].append(expense.__dict__)

        self.storage.save(data)
        return new_id

    def list_expenses(self):
        return self.storage.load()["expenses"]

    def delete_expense(self, expense_id):
        data = self.storage.load()
        original_len = len(data["expenses"])

        data["expenses"] = [
            e for e in data["expenses"] if e["id"] != expense_id
        ]

        if len(data["expenses"]) == original_len:
            raise ValueError("Expense ID not found")

        self.storage.save(data)

    def update_expense(self, expense_id, description=None, amount=None):
        data = self.storage.load()

        for e in data["expenses"]:
            if e["id"] == expense_id:
                if description:
                    e["description"] = description
                if amount is not None:
                    if amount < 0:
                        raise ValueError("Amount cannot be negative")
                    e["amount"] = amount

                self.storage.save(data)
                return

        raise ValueError("Expense ID not found")

    def summary(self, month=None):
        data = self.storage.load()
        total = 0

        for e in data["expenses"]:
            if month:
                expense_month = datetime.strptime(
                    e["date"], "%Y-%m-%d"
                ).month
                if expense_month == month:
                    total += e["amount"]
            else:
                total += e["amount"]

        return total

    def filter_by_category(self, category_name):
        data = self.storage.load()

        filtered = [
            e for e in data["expenses"]
            if e["category"].lower() == category_name.lower()
        ]

        total = sum(e["amount"] for e in filtered)

        return filtered, total