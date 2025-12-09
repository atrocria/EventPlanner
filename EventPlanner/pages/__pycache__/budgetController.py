# controller.py
from tkinter import messagebox, simpledialog

class BudgetController:
    def __init__(self, service, ui):
        self.service = service
        self.ui = ui

    def add_item(self):
        category = self.ui.category_entry.get().strip()
        amount_str = self.ui.amount_entry.get().strip()
        item_type = self.ui.type_var.get()

        if not category or not amount_str:
            messagebox.showerror("Error", "Category and amount cannot be empty.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        item = self.service.add_item(category, amount, item_type)
        messagebox.showinfo("Success", f"{item_type} added: {item}")
        self.ui.clear_form()

    def view_budget(self):
        if not self.service.items:
            messagebox.showinfo("Budget Tracker", "No budget items yet.")
            return

        total_income, total_expense, balance = self.service.get_summary()
        items_str = "\n".join(self.service.list_items())
        messagebox.showinfo(
            "Event Budget",
            f"Total Income: {total_income:.2f}\n"
            f"Total Expense: {total_expense:.2f}\n"
            f"Balance: {balance:.2f}\n\nItems:\n{items_str}"
        )

    def remove_item(self):
        if not self.service.items:
            messagebox.showinfo("Info", "No items to remove.")
            return

        categories = [i.category for i in self.service.items]
        choice = simpledialog.askstring("Remove Item", f"Enter category to remove:\n{', '.join(categories)}")

        if not choice:
            return

        if self.service.remove_item(choice):
            messagebox.showinfo("Success", "Item removed!")
            self.ui.update_summary()
        else:
            messagebox.showerror("Error", "Item not found!")