# controller.py

from service import BudgetService

class BudgetController:
    def __init__(self):
        self.service = BudgetService()

    def add_expense(self, name, amount):
        return self.service.add_item(name, amount)

    def remove_expense(self, name):
        return self.service.remove_item(name)

    def view_expenses(self):
        return self.service.get_items()

    def total_expenses(self):
        return self.service.get_total()
