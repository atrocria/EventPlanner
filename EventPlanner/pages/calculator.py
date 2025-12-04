# -------------------------
# Budget Tracker module
# -------------------------
def add_expense():
    item = simpledialog.askstring("Add Expense", "Item:")
    if not item:
        return

    amount = simpledialog.askfloat("Amount", "Amount (RM):")
    if amount is None:
        return

    budget_items.append({"item": item, "amount": amount})
    messagebox.showinfo("Success", "Expense added!")

def view_budget():
    budget_text.delete(1.0, CTk.END)
    if not budget_items:
        budget_text.insert(CTk.END, "No expenses yet.")
        return

    total = sum(b["amount"] for b in budget_items)

    for b in budget_items:
        budget_text.insert(CTk.END, f"- {b['item']}: RM{b['amount']}\n")

    budget_text.insert(CTk.END, f"\nTotal: RM{total}")

    if budget_limit > 0 and total > budget_limit:
        budget_text.insert(CTk.END, "\n⚠ OVER BUDGET!")

def set_budget_limit():
    global budget_limit
    limit = simpledialog.askfloat("Set Budget Limit", "Enter total budget limit (RM):")

    if limit is not None:
        budget_limit = limit
        messagebox.showinfo("Success", f"Budget limit set to RM{limit}")


def remaining_budget():
    total = sum(b["amount"] for b in budget_items)

    if budget_limit == 0:
        messagebox.showinfo("Info", "No budget limit set.")
        return

    remaining = budget_limit - total
    messagebox.showinfo("Remaining", f"Remaining Budget: RM{remaining}")

def edit_expense():
    if not budget_items:
        messagebox.showinfo("Info", "No expenses yet.")
        return

    names = [b['item'] for b in budget_items]
    old = simpledialog.askstring("Edit Expense", f"Enter item name to edit:\n{names}")

    for b in budget_items:
        if b["item"] == old:
            new_name = simpledialog.askstring("New Name", "New item name:")
            new_amount = simpledialog.askfloat("New Amount", "New amount (RM):")

            if new_name:
                b["item"] = new_name
            if new_amount is not None:
                b["amount"] = new_amount

            messagebox.showinfo("Updated", "Expense updated!")
            return

    messagebox.showerror("Error", "Item not found!")

def delete_expense():
    if not budget_items:
        messagebox.showinfo("Info", "No expenses to delete.")
        return

    names = [b['item'] for b in budget_items]
    choice = simpledialog.askstring("Delete Expense", f"Enter item to delete:\n{names}")

    for b in budget_items:
        if b["item"] == choice:
            budget_items.remove(b)
            messagebox.showinfo("Deleted", "Expense deleted!")
            return

    messagebox.showerror("Error", "Item not found!")
    
    # -------------------------
    # BUDGET MENU
    # -------------------------
    CTk.Label(budget_menu, text="Budget Manager", font=("Arial", 16)).pack(pady=10)

    CTk.Button(budget_menu, text="Add Expense", width=20, command=add_expense).pack(pady=5)
    CTk.Button(budget_menu, text="View Expenses", width=20, command=view_budget).pack(pady=5)
    CTk.Button(budget_menu, text="Set Budget Limit", width=20, command=set_budget_limit).pack(pady=5)
    CTk.Button(budget_menu, text="Remaining Budget", width=20, command=remaining_budget).pack(pady=5)
    CTk.Button(budget_menu, text="Edit Expense", width=20, command=edit_expense).pack(pady=5)
    CTk.Button(budget_menu, text="Delete Expense", width=20, command=delete_expense).pack(pady=5)
    CTk.Button(budget_menu, text="Back", width=20, command=lambda: show_frame(main_menu)).pack(pady=20)

    budget_text = CTk.Text(budget_menu, height=10, width=40)
    budget_text.pack(pady=10)