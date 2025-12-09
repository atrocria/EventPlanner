# This code launches directly into Guest List Manager.

import customtkinter as ctk
from tkinter import messagebox, simpledialog
import os

# ===========================
# FILE SAVE PATH
# Define the file path where guest data will be stored.
SAVE_PATH = "C:/EventPlanner/guests.txt"
# ===========================

# ===========================
# FILE SAVE & LOAD FUNCTIONS
# ===========================
def save_guest_to_file(name, rsvp):
    """
    Save a guest entry to the text file in a readable format.
    Demonstrates file writing and string formatting.
    """
    folder = os.path.dirname(SAVE_PATH)
    os.makedirs(folder, exist_ok=True)  # Ensure folder exists

    with open(SAVE_PATH, "a", encoding="utf-8") as f:
        f.write(f"Guest Name: {name} | RSVP Status: {rsvp}\n")


def load_guests_from_file():
    """
    Load guest entries from the text file when the app starts.
    Uses string processing and collections (list + dictionary).
    """
    if not os.path.exists(SAVE_PATH):
        return []

    guests_list = []
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Guest Name:") and "| RSVP Status:" in line:
                # Split into parts using string operations
                parts = line.split("|")
                name = parts[0].replace("Guest Name:", "").strip()
                rsvp = parts[1].replace("RSVP Status:", "").strip()
                guests_list.append({"name": name, "rsvp": rsvp})
    return guests_list


# ===========================
# INITIAL APP SETTINGS
# ===========================
# Configure global appearance settings for the GUI.
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Load saved guests into memory.
guests = load_guests_from_file()


# ===========================
# GUEST FUNCTIONS
# ===========================
def add_guest():
    """
    Add a new guest to the list and save to file.
    Includes validation, file writing, and updating collections.
    """
    name = name_entry.get().strip()
    rsvp = rsvp_var.get()

    if not name:
        messagebox.showerror("Error", "Guest name cannot be empty.")
        return

    guests.append({"name": name, "rsvp": rsvp})

    # Save to text file
    save_guest_to_file(name, rsvp)

    messagebox.showinfo("Success", f"Guest added with RSVP: {rsvp}")
    clear_form()


def view_guests():
    """
    Display all guests in a message box.
    Demonstrates iteration (loop) and string formatting.
    """
    if not guests:
        messagebox.showinfo("Guest List", "No guests added yet.")
        return

    guest_list_str = "\n".join(f"- {g['name']} (RSVP: {g['rsvp']})" for g in guests)
    messagebox.showinfo("Guest List",
                        f"Total Guests: {len(guests)}\n\n{guest_list_str}")


def remove_guest():
    """
    Remove a guest by name and update the file.
    Demonstrates selection (if-else), string processing, and file rewriting.
    """
    if not guests:
        messagebox.showinfo("Info", "No guests to remove.")
        return

    names = [g["name"] for g in guests]
    choice = simpledialog.askstring("Remove Guest",
                                    f"Enter guest name to remove:\n{', '.join(names)}")

    if not choice:
        return

    for g in guests:
        if g["name"].lower() == choice.lower():
            guests.remove(g)

            # Rewrite file after removal (maintains consistent format)
            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                for entry in guests:
                    f.write(f"Guest Name: {entry['name']} | RSVP Status: {entry['rsvp']}\n")

            guest_count_label.configure(text=f"Total Guests: {len(guests)}")
            messagebox.showinfo("Success", "Guest removed!")
            return

    messagebox.showerror("Error", "Guest not found!")


def clear_form():
    """
    Reset the input fields to default values.
    Demonstrates encapsulation and GUI state management.
    """
    name_entry.delete(0, "end")
    rsvp_var.set("Yes")
    guest_count_label.configure(text=f"Total Guests: {len(guests)}")


# ===========================
# MAIN WINDOW
# ===========================
# Create the main application window and configure layout.
root = ctk.CTk()
root.title("Event Planner")
root.geometry("450x600")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Define only the Guest Manager frame (main menu removed).
guest_menu = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)
guest_menu.grid(row=0, column=0, sticky="nsew")


# ===========================
# GUEST MANAGER UI
# ===========================
# Guest Manager interface with form and buttons.
container = ctk.CTkFrame(guest_menu, fg_color="transparent", corner_radius=0)
container.place(relx=0.5, rely=0.5, anchor="center")

header = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
header.pack(pady=(0, 15))

ctk.CTkLabel(header, text="GUEST LIST MANAGER",
             font=("Arial", 20, "bold")).pack()

guest_count_label = ctk.CTkLabel(header,
                                 text=f"Total Guests: {len(guests)}",
                                 font=("Arial", 14))
guest_count_label.pack(pady=5)


# ===========================
# FORM SECTION
# ===========================
# Input form for guest name and RSVP status.
form = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
form.pack(pady=15)

ctk.CTkLabel(form, text="Guest Name:", font=("Arial", 14)).pack(anchor="w")
name_entry = ctk.CTkEntry(form, width=260, corner_radius=8)
name_entry.pack(pady=5)

ctk.CTkLabel(form, text="RSVP Status:", font=("Arial", 14)).pack(anchor="w", pady=(10, 0))
rsvp_var = ctk.StringVar(value="Yes")
rsvp_dropdown = ctk.CTkComboBox(form, values=["Yes", "No"], variable=rsvp_var,
                                width=260, corner_radius=8)
rsvp_dropdown.pack(pady=5)


# ===========================
# BUTTONS
# ===========================
# Action buttons for guest management operations.
btn_frame = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
btn_frame.pack(pady=20)

ctk.CTkButton(btn_frame,
              text="Add Guest", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=add_guest) \
    .grid(row=0, column=0, padx=5, pady=5)

ctk.CTkButton(btn_frame,
              text="View Guest List", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=view_guests) \
    .grid(row=0, column=1, padx=5, pady=5)

ctk.CTkButton(btn_frame,
              text="Remove Guest", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=remove_guest) \
    .grid(row=1, column=0, padx=5, pady=5)

ctk.CTkButton(btn_frame,
              text="Clear Form", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=clear_form) \
    .grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
