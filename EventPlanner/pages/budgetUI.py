import customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox


class BudgetUI(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        CTkLabel(self, text="Budget Tracker", font=("Arial", 24, "bold")).pack(pady=20)

        # Inputs
        self.name_entry = CTkEntry(self, placeholder_text="Item Name", width=300)
        self.name_entry.pack(pady=5)

        self.amount_entry = CTkEntry(self, placeholder_text="Amount (RM)", width=300)
        self.amount_entry.pack(pady=5)

        # Buttons
        CTkButton(self, text="Add Item", command=self.add_item).pack(pady=10)

        # Budget list
        self.list_box = CTkTextbox(self, width=450, height=300)
        self.list_box.pack(pady=10)

        # Total label
        self.total_label = CTkLabel(self, text="Total: RM 0.00", font=("Arial", 18, "bold"))
        self.total_label.pack(pady=10)

    def add_item(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()

        if not name or not amount:
            return

        try:
            amount = float(amount)
        except ValueError:
            return

        self.controller.add_budget_item(name, amount)
        self.update_list()

        self.name_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")

    def update_list(self):
        self.list_box.delete("0.0", "end")

        items = self.controller.get_all_items()
        total = self.controller.get_total_budget()

        for i, item in enumerate(items):
            self.list_box.insert("end", f"{i + 1}. {item.name} - RM {item.amount:.2f}\n")

        self.total_label.configure(text=f"Total: RM {total:.2f}")
