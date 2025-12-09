# services.py
from model import BudgetItem

class BudgetService:
    def __init__(self):
        self.items = []

    def add_item(self, category: str, amount: float, item_type: str):
        item = BudgetItem(category, amount, item_type)
        self.items.append(item)
        return item

    def remove_item(self, category: str):
        for item in self.items:
            if item.category.lower() == category.lower():
                self.items.remove(item)
                return True
        return False

    def get_summary(self):
        total_income = sum(i.amount for i in self.items if i.type == "Income")
        total_expense = sum(i.amount for i in self.items if i.type == "Expense")
        balance = total_income - total_expense
        return total_income, total_expense, balance

    def list_items(self):
        return [repr(i) for i in self.items]