import customtkinter as ctk
from tkinter import messagebox, simpledialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

guests = [{"name": "Mikhail", "rsvp": "Yes"}]

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
    choice = simpledialog.askstring("Remove Guest",
                                    f"Enter guest name to remove:\n{', '.join(names)}")
    
    if not choice:
        return
    
    for g in guests:
        if g["name"].lower() == choice.lower():
            guests.remove(g)
            messagebox.showinfo("Success", "Guest removed!")
            guest_count_label.configure(text=f"Total Guests: {len(guests)}")
            return
        
    messagebox.showerror("Error", "Guest not found!")

def clear_form():
    name_entry.delete(0, "end")
    rsvp_var.set("Yes")
    guest_count_label.configure(text=f"Total Guests: {len(guests)}")


# --------------------------
# MAIN WINDOW
# --------------------------
root = ctk.CTk()
root.title("Event Planner")
root.geometry("450x600")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_menu = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)
guest_menu = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)

for frame in (main_menu, guest_menu):
    frame.grid(row=0, column=0, sticky="nsew")


# --------------------------
# MAIN MENU UI
# --------------------------
ctk.CTkLabel(main_menu, text="EVENT PLANNER", font=("Arial", 26, "bold")).pack(pady=40)

ctk.CTkButton(main_menu,
              text="Guest Manager",
              width=200,
              height=50,
              command=lambda: show_frame(guest_menu)).pack(pady=20)


# --------------------------
# GUEST MANAGER UI
# --------------------------
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


# --------------------------
# FORM SECTION
# --------------------------
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


# --------------------------
# BUTTONS
# --------------------------
btn_frame = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
btn_frame.pack(pady=20)

ctk.CTkButton(btn_frame, 
              text="Add Guest", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=add_guest)\
    .grid(row=0, column=0, padx=5, pady=5)

ctk.CTkButton(btn_frame, 
              text="View Guest List", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=view_guests)\
    .grid(row=0, column=1, padx=5, pady=5)

ctk.CTkButton(btn_frame, 
              text="Remove Guest", width=180,
              fg_color="#3A6EA5",
              hover_color="#ff8800",
              command=remove_guest)\
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
