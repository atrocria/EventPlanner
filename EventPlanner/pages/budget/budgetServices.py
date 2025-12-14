import json
import os
from .budgetModel import BudgetItem

class BudgetService:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "budget_data.json")
        self.items = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            self.save_data()
            return

        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.items = [
                    BudgetItem(item["name"], item["amount"])
                    for item in data
                ]
        except json.JSONDecodeError:
            self.items = []
            self.save_data()

    def save_data(self):
        data = [{"name": item.name, "amount": item.amount} for item in self.items]
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add_item(self, name, amount):
        new_item = BudgetItem(name, amount)
        self.items.append(new_item)
        self.save_data()
        return new_item

    def delete_item(self, index):
        if 0 <= index < len(self.items):
            removed = self.items.pop(index)
            self.save_data()
            return removed
        return None

    def get_items(self):
        return self.items

    def get_total(self):
        return sum(item.amount for item in self.items)
