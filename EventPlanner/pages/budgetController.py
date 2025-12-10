# pages/budgetController.py

from .budgetServices import BudgetService

class BudgetController:
    def __init__(self, service: BudgetService):
        self.service = service

    def add(self, item, amount):
        return self.service.add_item(item, amount)

    def remove(self, item_name):
        return self.service.remove_item(item_name)

    def get_items(self):
        return self.service.get_items()

    def total(self):
        return self.service.get_total()
