# pages/budgetServices.py
from .budgetModel import BudgetItem

class BudgetService:
    def __init__(self):
        self.items = []

    def add_item(self, name, amount):
        item = BudgetItem(name, amount)
        self.items.append(item)
        return item

    def remove_item(self, name):
        self.items = [i for i in self.items if i.name != name]

    def get_items(self):
        return self.items
