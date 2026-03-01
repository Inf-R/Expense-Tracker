from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    id: int
    date: str
    description: str
    amount: float
    category: str = "General"

    @staticmethod
    def create(expense_id, description, amount, category=None):
        if amount < 0:
            raise ValueError("Amount cannot be negative")

        return Expense(
            id=expense_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            description=description,
            amount=amount,
            category=category if category else "General"
        )