#dependencies
import  datetime
import  tkinter         as tk
from    tkinter         import ttk, messagebox, simpledialog
from    customtkinter   import CTk

#import pages
from pages.dashboard    import DashBoard
from pages.tasks        import Tasks
from pages.guestlist    import GuestList
from pages.calculator   import Calculator
from pages.timer        import Timer

guests = []
budget_items = []
budget_limit = 0

def show_frame(frame):
    frame.tkraise()

# -------------------------
# GUEST MENU 
# -------------------------
def add_guest_gui():
    name = name_entry.get().strip()
    rsvp = rsvp_entry.get().lower().strip()

    if not name:
        messagebox.showerror("Error", "Guest name cannot be empty.")
        return

    #! make into a button
    if rsvp not in ["y", "yes", "n", "no"]:
        messagebox.showerror("Invalid Input", "RSVP must be yes/no or y/n.")
        return

    final_rsvp = "yes" if rsvp in ["y", "yes"] else "no"
    guests.append({"name": name, "rsvp": final_rsvp})
    messagebox.showinfo("Success", f"Guest added with RSVP: {final_rsvp}")

    # Clear inputs
    name_entry.delete(0, CTk.END)
    rsvp_entry.delete(0, CTk.END)


def view_guests_gui():
    if not guests:
        messagebox.showinfo("Guest List", "No guests added yet.")
    else:
        guest_list_str = "\n".join(f"- {g['name']} (RSVP: {g['rsvp']})" for g in guests)
        messagebox.showinfo("Guest List", guest_list_str)


def clear_guest_form():
    name_entry.delete(0, CTk.END)
    rsvp_entry.delete(0, CTk.END)

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
# Countdown module
# -------------------------
def show_countdown():
    date_str = simpledialog.askstring("Countdown", "Enter event date (YYYY-MM-DD):")
    if not date_str:
        return

    try:
        event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        days_left = (event_date - today).days
        messagebox.showinfo("Countdown", f"Days left: {days_left}")
    except:
        messagebox.showerror("Error", "Invalid date format!")


# -------------------------
# Main menu setup
# -------------------------
root = CTk.Tk()
root.title("Event Planner")
root.geometry("430x500")
CTk.set_appearance_mode("Dark")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#sidebar = ttk.Frame(self, width=80)
#sidebar.grid(row=0, column=0, sticky="ns")
#sidebar.grid_propagate(False)

main_menu = CTk.Frame(master=root)
guest_menu = CTk.Frame(master=root)
task_menu = Tasks(root, title="hello from app")
budget_menu = CTk.Frame(master=root)

for frame in (main_menu, guest_menu, task_menu, budget_menu):
    frame.grid(row=0, column=0, sticky="nsew")


# -------------------------
# MAIN MENU
# -------------------------
CTk.Label(main_menu, text="EVENT PLANNER", font=("Arial", 18, "bold")).pack(pady=20)

CTk.Button(main_menu, text="Guest Manager", width=25, command=lambda: show_frame(GuestList)).pack(pady=5)
CTk.Button(main_menu, text="Task Checklist", width=25, command=lambda: show_frame(Tasks)).pack(pady=5)
CTk.Button(main_menu, text="Budget Tracker", width=25, command=lambda: show_frame(Calculator)).pack(pady=5)
CTk.Button(main_menu, text="Countdown", width=25, command=Timer).pack(pady=5)
CTk.Button(main_menu, text="Exit", width=25, command=root.quit).pack(pady=20)


# -------------------------
# GUEST MENU 
# -------------------------
CTk.Label(guest_menu, text="Guest Manager", font=("Arial", 16)).pack(pady=10)

CTk.Label(guest_menu, text="Guest Name:").pack()
name_entry = CTk.Entry(guest_menu, width=30)
name_entry.pack(pady=2)

CTk.Label(guest_menu, text="RSVP - répondez s'il vous plaît (are you attending?):").pack()
rsvp_entry = CTk.Entry(guest_menu, width=30)
rsvp_entry.pack(pady=2)

CTk.Button(guest_menu, text="Add Guest", width=20, command=add_guest_gui).pack(pady=5)
CTk.Button(guest_menu, text="Clear Form", width=20, command=clear_guest_form).pack(pady=5)
CTk.Button(guest_menu, text="View Guests", width=20, command=view_guests_gui).pack(pady=5)
CTk.Button(guest_menu, text="Back", width=20, command=lambda: show_frame(main_menu)).pack(pady=10)

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


show_frame(main_menu)
root.mainloop()