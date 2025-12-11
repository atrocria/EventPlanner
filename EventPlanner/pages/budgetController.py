# pages/budgetController.py

class BudgetController:
    def __init__(self, service):
        self.service = service

    def add_budget_item(self, name, amount):
        return self.service.add_item(name, amount)

    def remove_budget_item(self, name):
        return self.service.remove_item(name)

    def get_budget_items(self):
        return self.service.get_items()

