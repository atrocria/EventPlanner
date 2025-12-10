# service.py

from model import BudgetItem

class BudgetService:
    def __init__(self):
        self.budget_items = []

    def add_item(self, item_name, amount):
        new_item = BudgetItem(item_name, amount)
        self.budget_items.append(new_item)
        return new_item

    def remove_item(self, item_name):
        for item in self.budget_items:
            if item.item.lower() == item_name.lower():
                self.budget_items.remove(item)
                return True
        return False

    def get_total(self):
        return sum(item.amount for item in self.budget_items)

    def get_items(self):
        return self.budget_items
