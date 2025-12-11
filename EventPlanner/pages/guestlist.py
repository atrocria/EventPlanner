import customtkinter as ctk
from tkinter import messagebox, simpledialog
import os

# ===========================
# FILE SAVE PATH
# ===========================
SAVE_PATH = "C:/EventPlanner/guests.txt"

# ===========================
# FILE SAVE & LOAD FUNCTIONS
# ===========================
def save_guest_to_file(name, rsvp):
    folder = os.path.dirname(SAVE_PATH)
    os.makedirs(folder, exist_ok=True)
    with open(SAVE_PATH, "a", encoding="utf-8") as f:
        f.write(f"Guest Name: {name} | RSVP Status: {rsvp}\n")

def load_guests_from_file():
    if not os.path.exists(SAVE_PATH):
        return []
    guests_list = []
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "Guest Name:" in line and "| RSVP Status:" in line:
                parts = line.split("|")
                name = parts[0].replace("Guest Name:", "").strip()
                rsvp = parts[1].replace("RSVP Status:", "").strip()
                guests_list.append({"name": name, "rsvp": rsvp})
    return guests_list

# ===========================
# INITIAL APP SETTINGS
# ===========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
guests = load_guests_from_file()

# ===========================
# STATUS BAR UPDATE FUNCTION
# ===========================
def update_status(message):
    status_label.configure(text=message)

# ===========================
# GUEST FUNCTIONS
# ===========================
def add_guest():
    name = name_entry.get().strip()
    rsvp = rsvp_var.get()
    if not name:
        update_status("Error: Guest name cannot be empty.")
        return
    guests.append({"name": name, "rsvp": rsvp})
    save_guest_to_file(name, rsvp)

    # ✅ Notification popup
    messagebox.showinfo("Guest Added", f"Guest '{name}' added with RSVP: {rsvp}")

    update_status(f"Guest '{name}' added with RSVP: {rsvp}")
    clear_form()

def view_guests():
    if not guests:
        update_status("No guests added yet.")
        return
    guest_list_str = "\n".join(f"- {g['name']} (RSVP: {g['rsvp']})" for g in guests)
    messagebox.showinfo("Guest List", f"Total Guests: {len(guests)}\n\n{guest_list_str}")
    update_status("Displayed guest list.")

def remove_guest():
    if not guests:
        update_status("No guests to remove.")
        return
    names = [g["name"] for g in guests]
    choice = simpledialog.askstring("Remove Guest", f"Enter guest name to remove:\n{', '.join(names)}")
    if not choice:
        return
    for g in guests:
        if g["name"].lower() == choice.lower():
            guests.remove(g)
            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                for entry in guests:
                    f.write(f"Guest Name: {entry['name']} | RSVP Status: {entry['rsvp']}\n")
            guest_count_label.configure(text=f"Total Guests: {len(guests)}")

            # ✅ Notification popup
            messagebox.showinfo("Guest Removed", f"Guest '{choice}' has been removed.")

            update_status(f"Guest '{choice}' removed.")
            return
    update_status("Error: Guest not found!")

def clear_form():
    name_entry.delete(0, "end")
    rsvp_var.set("Yes")
    guest_count_label.configure(text=f"Total Guests: {len(guests)}")
    update_status("Form cleared.")
    rsvp_dropdown.focus()  # ensures focus shifts away from entry

# ===========================
# MAIN WINDOW — 1440x788
# ===========================
root = ctk.CTk()
root.title("Event Planner")
root.geometry("1440x788")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ===========================
# CENTERED CONTENT
# ===========================
guest_menu = ctk.CTkFrame(root)
guest_menu.grid(row=0, column=0, sticky="nsew")
container = ctk.CTkFrame(guest_menu, fg_color="transparent")
container.place(relx=0.5, rely=0.44, anchor="center")

# ===========================
# HEADER
# ===========================
header = ctk.CTkFrame(container, fg_color="transparent")
header.pack(pady=(0, 10))
ctk.CTkLabel(header, text="GUEST LIST MANAGER", font=("Segoe UI", 32, "bold")).pack()
guest_count_label = ctk.CTkLabel(header, text=f"Total Guests: {len(guests)}", font=("Segoe UI", 20, "italic"))
guest_count_label.pack(pady=(0, 2))

# ===========================
# FORM CARD
# ===========================
form_card = ctk.CTkFrame(container, fg_color="#2a2a2a", corner_radius=12)
form_card.pack(pady=20, padx=10, fill="x")

ctk.CTkLabel(form_card, text="Guest Name:", font=("Segoe UI", 22)).pack(anchor="w", pady=(10, 5), padx=15)
name_entry = ctk.CTkEntry(form_card, width=520, height=45)  # no placeholder
name_entry.pack(pady=5, anchor="w", padx=15)

ctk.CTkLabel(form_card, text="RSVP Status:", font=("Segoe UI", 22)).pack(anchor="w", pady=(15, 5), padx=15)
rsvp_var = ctk.StringVar(value="Yes")
rsvp_dropdown = ctk.CTkComboBox(
    form_card,
    values=["Yes", "No"],
    variable=rsvp_var,
    width=520,
    height=45,
    state="readonly"   # ✅ user can select Yes/No but cannot type custom text
)
rsvp_dropdown.pack(pady=5, anchor="w", padx=15)

# ===========================
# DIVIDER ABOVE BUTTONS
# ===========================
ctk.CTkFrame(container, height=2, fg_color="#888").pack(fill="x", pady=(25, 0))

# ===========================
# BUTTON CARD
# ===========================
btn_card = ctk.CTkFrame(container, fg_color="#2a2a2a", corner_radius=12)
btn_card.pack(pady=10, padx=10)

button_style = {
    "width": 260,
    "height": 55,
    "fg_color": "#3A6EA5",
    "hover_color": "#ff8800",
    "corner_radius": 12,
    "font": ("Segoe UI", 18)
}

ctk.CTkButton(btn_card, text="Add Guest", command=add_guest, **button_style).grid(row=0, column=0, padx=12, pady=12)
ctk.CTkButton(btn_card, text="View Guest List", command=view_guests, **button_style).grid(row=0, column=1, padx=12, pady=12)
ctk.CTkButton(btn_card, text="Remove Guest", command=remove_guest, **button_style).grid(row=1, column=0, padx=12, pady=12)
ctk.CTkButton(btn_card, text="Clear Form", command=clear_form, **button_style).grid(row=1, column=1, padx=12, pady=12)

# ===========================
# DIVIDER BELOW BUTTONS
# ===========================
ctk.CTkFrame(container, height=2, fg_color="#888").pack(fill="x", pady=(0, 10))

# ===========================
# STATUS BAR (FOOTER)
# ===========================
status_label = ctk.CTkLabel(root, text="Ready.", font=("Segoe UI", 16), text_color="#cccccc")
status_label.place(relx=0.5, rely=0.98, anchor="center")

# ===========================
# START APP
# ===========================
root.mainloop()
