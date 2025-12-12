class BudgetController:
    def __init__(self, service):
        self.service = service

    def add_item(self, name, amount):
        return self.service.add_item(name, amount)

    def delete_item(self, index):
        return self.service.delete_item(index)

    def get_items(self):
        return self.service.get_items()

    def get_total(self):
        return self.service.get_total()
