class BudgetController:
    def __init__(self, service):
        self.service = service

    def add_budget_item(self, name: str, amount: float):
        return self.service.add_item(name, amount)

    def delete_budget_item(self, index: int):
        self.service.delete_item(index)

    def get_all_items(self):
        return self.service.get_items()

    def get_total_budget(self):
        return self.service.get_total()
