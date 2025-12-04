import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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

guests = [{"name": "Mikhail-this", "rsvp": "Yes"}]

def show_frame(frame):
    frame.tkraise()

def add_guest():
    name = name_entry.get().strip()
    rsvp = rsvp_var.get()

    if not name:
        messagebox.showerror("Error", "Guest name cannot be empty.")
        return

    guests.append({"name": name, "rsvp": rsvp})
    messagebox.showinfo("Success", f"Guest added with RSVP: {rsvp}")
    clear_form()

def view_guests():
    if not guests:
        messagebox.showinfo("Guest List", "No guests added yet.")
    else:
        guest_list_str = "\n".join(f"- {g['name']} (RSVP: {g['rsvp']})" for g in guests)
        messagebox.showinfo("Guest List", f"Total Guests: {len(guests)}\n\n{guest_list_str}")

def remove_guest():
    if not guests:
        messagebox.showinfo("Info", "No guests to remove.")
        return
    
    names = [g['name'] for g in guests]
    choice = simpledialog.askstring("Remove Guest", f"Enter guest name to remove:\n{', '.join(names)}")
    
    if not choice: 
        return
    
    for g in guests:
        if g["name"].lower() == choice.lower():
            guests.remove(g)
            messagebox.showinfo("Success", "Guest removed!")
            guest_count_label.config(text=f"Total Guests: {len(guests)}")
            return
        
    messagebox.showerror("Error", "Guest not found!")

def clear_form():
    name_entry.delete(0, tk.END)
    rsvp_var.set("Yes")
    guest_count_label.config(text=f"Total Guests: {len(guests)}")

root = tk.Tk()
root.title("Event Planner")
root.geometry("450x600")
root.configure(bg="#d3d3d3")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

main_menu = tk.Frame(root, bg="#d3d3d3")
guest_menu = tk.Frame(root, bg="gray")

for frame in (main_menu, guest_menu):
    frame.grid(row=0, column=0, sticky="nsew")

tk.Label(main_menu, text="EVENT PLANNER", 
         font=("Arial", 20, "bold"), bg="#d3d3d3", fg="#333333").pack(pady=30)

tk.Button(main_menu, text="Guest Manager", font=("Arial", 12),
          width=20, height=2, command=lambda: show_frame(guest_menu)).pack(pady=10)

center_container = tk.Frame(guest_menu, bg="gray")
center_container.place(relx=0.5, rely=0.5, anchor="center")

header_frame = tk.Frame(center_container, bg="gray")
header_frame.pack(pady=(0, 10))

tk.Label(header_frame, text="GUEST LIST MANAGER", 
         font=("Arial", 18, "bold"), bg="gray", fg="white").pack()

guest_count_label = tk.Label(header_frame, text=f"Total Guests: {len(guests)}", 
                             font=("Arial", 11), bg="gray", fg="white")
guest_count_label.pack(pady=5)

tk.Frame(center_container, height=2, width=350, bg="white").pack(pady=10, fill="x")

form_frame = tk.Frame(center_container, bg="gray")
form_frame.pack(pady=15)

name_frame = tk.Frame(form_frame, bg="gray")
name_frame.pack(pady=5)
tk.Label(name_frame, text="Guest Name:", font=("Arial", 11), bg="gray", fg="white").pack(side="left", padx=(0, 10))
name_entry = tk.Entry(name_frame, font=("Arial", 11), width=25, relief="solid", bd=1, bg="white")
name_entry.pack(side="left")

rsvp_frame = tk.Frame(form_frame, bg="gray")
rsvp_frame.pack(pady=10)
tk.Label(rsvp_frame, text="RSVP Status:", font=("Arial", 11), bg="gray", fg="white").pack(side="left", padx=(0, 10))
rsvp_var = tk.StringVar(value="Yes")
rsvp_dropdown = ttk.Combobox(rsvp_frame, textvariable=rsvp_var, values=["Yes", "No"], 
                             state="readonly", font=("Arial", 11), width=22)
rsvp_dropdown.pack(side="left")

tk.Frame(center_container, height=2, width=350, bg="white").pack(pady=15, fill="x")

button_frame = tk.Frame(center_container, bg="gray")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Guest", font=("Arial", 11, "bold"),
          width=15, height=2, bg="#4CAF50", fg="white",
          relief="groove", bd=3, command=add_guest).grid(row=0, column=0, padx=5, pady=5)

tk.Button(button_frame, text="View Guest List", font=("Arial", 11, "bold"),
          width=15, height=2, bg="#2196F3", fg="white",
          relief="groove", bd=3, command=view_guests).grid(row=0, column=1, padx=5, pady=5)

tk.Button(button_frame, text="Remove Guest", font=("Arial", 11, "bold"),
          width=15, height=2, bg="#FF9800", fg="white",
          relief="groove", bd=3, command=remove_guest).grid(row=1, column=0, padx=5, pady=5)

tk.Button(button_frame, text="Clear Form", font=("Arial", 11, "bold"),
          width=15, height=2, bg="#9E9E9E", fg="white",
          relief="groove", bd=3, command=clear_form).grid(row=1, column=1, padx=5, pady=5)

tk.Frame(center_container, height=2, width=350, bg="white").pack(pady=15, fill="x")

nav_frame = tk.Frame(center_container, bg="gray")
nav_frame.pack(pady=10)
tk.Button(nav_frame, text="← Back to Main Menu", font=("Arial", 10),
          width=20, bg="#666666", fg="white",
          command=lambda: show_frame(main_menu)).pack()

show_frame(main_menu)
root.mainloop()