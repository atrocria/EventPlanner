# model.py

class BudgetItem:
    def __init__(self, category: str, amount: float, item_type: str):
        self.category = category
        self.amount = amount
        self.type = item_type  # "Income" or "Expense"

    def __repr__(self):
        return f"{self.category} ({self.type}: {self.amount:.2f})"