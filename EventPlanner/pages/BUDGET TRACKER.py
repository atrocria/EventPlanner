import customtkinter as ctk
from tkinter import messagebox, simpledialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --------------------------
# DATA
# --------------------------
budget_items = []  # Each entry: {"category": str, "amount": float, "type": "Income"/"Expense"}

def show_frame(frame):
    frame.tkraise()

# --------------------------
# FUNCTIONS
# --------------------------
def add_item():
    category = category_entry.get().strip()
    amount_str = amount_entry.get().strip()
    t_type = type_var.get()

    if not category or not amount_str:
        messagebox.showerror("Error", "Category and amount cannot be empty.")
        return

    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    budget_items.append({"category": category, "amount": amount, "type": t_type})
    messagebox.showinfo("Success", f"{t_type} added: {category} - {amount:.2f}")
    clear_form()

def view_budget():
    if not budget_items:
        messagebox.showinfo("Budget Tracker", "No budget items yet.")
    else:
        total_income = sum(b["amount"] for b in budget_items if b["type"] == "Income")
        total_expense = sum(b["amount"] for b in budget_items if b["type"] == "Expense")
        balance = total_income - total_expense

        items_str = "\n".join(
            f"- {b['category']} ({b['type']}: {b['amount']:.2f})" for b in budget_items
        )
        messagebox.showinfo(
            "Event Budget",
            f"Total Income: {total_income:.2f}\n"
            f"Total Expense: {total_expense:.2f}\n"
            f"Balance: {balance:.2f}\n\nItems:\n{items_str}"
        )

def remove_item():
    if not budget_items:
        messagebox.showinfo("Info", "No items to remove.")
        return

    categories = [b['category'] for b in budget_items]
    choice = simpledialog.askstring("Remove Item",
                                    f"Enter category to remove:\n{', '.join(categories)}")

    if not choice:
        return

    for b in budget_items:
        if b["category"].lower() == choice.lower():
            budget_items.remove(b)
            messagebox.showinfo("Success", "Item removed!")
            update_summary()
            return

    messagebox.showerror("Error", "Item not found!")

def clear_form():
    category_entry.delete(0, "end")
    amount_entry.delete(0, "end")
    type_var.set("Expense")
    update_summary()

def update_summary():
    total_income = sum(b["amount"] for b in budget_items if b["type"] == "Income")
    total_expense = sum(b["amount"] for b in budget_items if b["type"] == "Expense")
    balance = total_income - total_expense
    summary_label.configure(
        text=f"Income: {total_income:.2f} | Expense: {total_expense:.2f} | Balance: {balance:.2f}"
    )

# --------------------------
# MAIN WINDOW
# --------------------------
root = ctk.CTk()
root.title("Event Planner - Budget Tracker")
root.geometry("450x600")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_menu = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)
budget_menu = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)

for frame in (main_menu, budget_menu):
    frame.grid(row=0, column=0, sticky="nsew")

# --------------------------
# MAIN MENU UI
# --------------------------
ctk.CTkLabel(main_menu, text="EVENT PLANNER", font=("Arial", 26, "bold")).pack(pady=40)

ctk.CTkButton(main_menu,
              text="Budget Manager",
              width=200,
              height=50,
              command=lambda: show_frame(budget_menu)).pack(pady=20)

# --------------------------
# BUDGET MANAGER UI
# --------------------------
container = ctk.CTkFrame(budget_menu, fg_color="transparent", corner_radius=0)
container.place(relx=0.5, rely=0.5, anchor="center")

header = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
header.pack(pady=(0, 15))

ctk.CTkLabel(header, text="EVENT BUDGET MANAGER",
             font=("Arial", 20, "bold")).pack()

summary_label = ctk.CTkLabel(header,
                             text="Income: 0.00 | Expense: 0.00 | Balance: 0.00",
                             font=("Arial", 14))
summary_label.pack(pady=5)

# --------------------------
# FORM SECTION
# --------------------------
form = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
form.pack(pady=15)

ctk.CTkLabel(form, text="Category:", font=("Arial", 14)).pack(anchor="w")
category_entry = ctk.CTkEntry(form, width=260, corner_radius=8)
category_entry.pack(pady=5)

ctk.CTkLabel(form, text="Amount:", font=("Arial", 14)).pack(anchor="w", pady=(10, 0))
amount_entry = ctk.CTkEntry(form, width=260, corner_radius=8)
amount_entry.pack(pady=5)

ctk.CTkLabel(form, text="Type:", font=("Arial", 14)).pack(anchor="w", pady=(10, 0))
type_var = ctk.StringVar(value="Expense")
type_dropdown = ctk.CTkComboBox(form, values=["Income", "Expense"], variable=type_var,
                                width=260, corner_radius=8)
type_dropdown.pack(pady=5)

# --------------------------
# BUTTONS
# --------------------------
btn_frame = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
btn_frame.pack(pady=20)

ctk.CTkButton(btn_frame,
              text="Add Item", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=add_item)\
    .grid(row=0, column=0, padx=5, pady=5)

ctk.CTkButton(btn_frame,
              text="View Budget", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=view_budget)\
    .grid(row=0, column=1, padx=5, pady=5)

ctk.CTkButton(btn_frame,
              text="Remove Item", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=remove_item)\
    .grid(row=1, column=0, padx=5, pady=5)

ctk.CTkButton(btn_frame,
              text="Clear Form", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=clear_form)\
    .grid(row=1, column=1, padx=5, pady=5)

# Back Button
ctk.CTkButton(container,
              text="← Back to Main Menu",
              width=200,
              fg_color="#1f6aa5",
              hover_color="#ff8800",
              command=lambda: show_frame(main_menu))\
        .pack(pady=15)

show_frame(main_menu)
root.mainloop()
