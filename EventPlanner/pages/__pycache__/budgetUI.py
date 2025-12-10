# ui.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from controller import BudgetController

class BudgetUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker MVC")
        self.root.geometry("400x420")
        self.root.configure(bg="#d3d3d3")

        self.controller = BudgetController()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="BUDGET TRACKER",
                 font=("Arial", 18, "bold"), bg="#d3d3d3").pack(pady=10)

        self.total_label = tk.Label(self.root, text="Total: RM 0",
                                    font=("Arial", 12), bg="#d3d3d3")
        self.total_label.pack(pady=5)

        tk.Label(self.root, text="Item:", font=("Arial", 11), bg="#d3d3d3").pack()
        self.item_entry = tk.Entry(self.root, font=("Arial", 11), width=25)
        self.item_entry.pack(pady=5)

        tk.Label(self.root, text="Amount (RM):", font=("Arial", 11),
                 bg="#d3d3d3").pack()
        self.amount_entry = tk.Entry(self.root, font=("Arial", 11), width=25)
        self.amount_entry.pack(pady=5)

        tk.Button(self.root, text="Add Expense", width=15, height=2,
                  bg="#4CAF50", fg="white",
                  command=self.add_expense).pack(pady=5)

        tk.Button(self.root, text="View Expenses", width=15, height=2,
                  bg="#2196F3", fg="white",
                  command=self.view_expenses).pack(pady=5)

        tk.Button(self.root, text="Remove Expense", width=15, height=2,
                  bg="#FF9800", fg="white",
                  command=self.remove_expense).pack(pady=5)

    def add_expense(self):
        item = self.item_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not item or not amount:
            messagebox.showerror("Error", "Item and amount cannot be empty.")
            return

        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a valid number.")
            return

        self.controller.add_expense(item, amount)
        messagebox.showinfo("Success", f"Added {item} (RM{amount})")

        self.item_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.update_total()

    def view_expenses(self):
        items = self.controller.view_expenses()
        if not items:
            messagebox.showinfo("Expenses", "No expenses added.")
            return

        text = "\n".join(f"- {i.item}: RM{i.amount}" for i in items)
        total = self.controller.total_expenses()

        messagebox.showinfo("Expense List", f"{text}\n\nTotal: RM {total}")

    def remove_expense(self):
        items = self.controller.view_expenses()
        if not items:
            messagebox.showinfo("Info", "No items to remove.")
            return

        names = ", ".join(i.item for i in items)
        choice = simpledialog.askstring("Remove Expense", f"Enter item to remove:\n{names}")

        if not choice:
            return

        if self.controller.remove_expense(choice):
            messagebox.showinfo("Success", "Item removed.")
        else:
            messagebox.showerror("Error", "Item not found.")

        self.update_total()

    def update_total(self):
        total = self.controller.total_expenses()
        self.total_label.config(text=f"Total: RM {total}")


# RUN UI
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetUI(root)
    root.mainloop()
