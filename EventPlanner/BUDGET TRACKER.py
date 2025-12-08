import tkinter as tk
from tkinter import messagebox, simpledialog

# ------------------------------
# DATA STORAGE
# ------------------------------
budget_items = []

# ------------------------------
# BUDGET TRACKER FUNCTIONS
# ------------------------------
def add_expense():
    item = budget_item_entry.get().strip()
    amount = budget_amount_entry.get().strip()

    if not item or not amount:
        messagebox.showerror("Error", "Item and amount cannot be empty.")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    budget_items.append({"item": item, "amount": amount})
    messagebox.showinfo("Success", f"Added: {item} (RM{amount})")

    budget_item_entry.delete(0, tk.END)
    budget_amount_entry.delete(0, tk.END)
    update_budget_total()

def view_expenses():
    if not budget_items:
        messagebox.showinfo("Budget", "No expenses added.")
        return

    text = "\n".join(f"- {b['item']}: RM{b['amount']}" for b in budget_items)
    total = sum(b["amount"] for b in budget_items)

    messagebox.showinfo("Budget List", f"{text}\n\nTotal: RM{total}")

def remove_expense():
    if not budget_items:
        messagebox.showinfo("Info", "No expenses to remove.")
        return

    names = [b['item'] for b in budget_items]
    choice = simpledialog.askstring("Remove Expense", f"Enter item to remove:\n{', '.join(names)}")

    if not choice:
        return

    for b in budget_items:
        if b["item"].lower() == choice.lower():
            budget_items.remove(b)
            messagebox.showinfo("Success", "Expense removed!")
            update_budget_total()
            return

    messagebox.showerror("Error", "Item not found!")

def update_budget_total():
    total = sum(b["amount"] for b in budget_items)
    budget_total_label.config(text=f"Total: RM {total}")

# ------------------------------
# GUI SETUP
# ------------------------------
root = tk.Tk()
root.title("Budget Tracker")
root.geometry("400x400")
root.configure(bg="#d3d3d3")

tk.Label(root, text="BUDGET TRACKER",
         font=("Arial", 18, "bold"), bg="#d3d3d3").pack(pady=10)

budget_total_label = tk.Label(root, text="Total: RM 0",
                              font=("Arial", 12), bg="#d3d3d3")
budget_total_label.pack(pady=5)

# Form
tk.Label(root, text="Item:", font=("Arial", 11), bg="#d3d3d3").pack()
budget_item_entry = tk.Entry(root, font=("Arial", 11), width=25)
budget_item_entry.pack(pady=5)

tk.Label(root, text="Amount (RM):", font=("Arial", 11), bg="#d3d3d3").pack()
budget_amount_entry = tk.Entry(root, font=("Arial", 11), width=25)
budget_amount_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Add Expense", font=("Arial", 11, "bold"),
          width=15, height=2, bg="#4CAF50", fg="white",
          command=add_expense).pack(pady=5)

tk.Button(root, text="View Expenses", font=("Arial", 11, "bold"),
          width=15, height=2, bg="#2196F3", fg="white",
          command=view_expenses).pack(pady=5)

tk.Button(root, text="Remove Expense", font=("Arial", 11, "bold"),
          width=15, height=2, bg="#FF9800", fg="white",
          command=remove_expense).pack(pady=5)

root.mainloop()