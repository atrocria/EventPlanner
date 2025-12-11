from pages.budgetModel import BudgetItem

class BudgetService:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, amount: float):
        item = BudgetItem(name, amount)
        self.items.append(item)
        return item

    def delete_item(self, index: int):
        if 0 <= index < len(self.items):
            del self.items[index]

    def get_items(self):
        return self.items

    def get_total(self):
        return sum(item.amount for item in self.items)
