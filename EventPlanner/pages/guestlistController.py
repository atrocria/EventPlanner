from tkinter import messagebox, simpledialog
import guestlistService as service

def add_guest(name_entry, rsvp_var, guests, update_status, clear_form):
    name = name_entry.get().strip()
    rsvp = rsvp_var.get()
    if not name:
        update_status("Error: Guest name cannot be empty.")
        return
    guests.append({"name": name, "rsvp": rsvp})
    service.save_guest(name, rsvp)
    messagebox.showinfo("Guest Added", f"Guest '{name}' added with RSVP: {rsvp}")
    update_status(f"Guest '{name}' added with RSVP: {rsvp}")
    clear_form()

def view_guests(guests, update_status):
    if not guests:
        update_status("No guests added yet.")
        return
    guest_list_str = "\n".join(f"- {g['name']} (RSVP: {g['rsvp']})" for g in guests)
    messagebox.showinfo("Guest List", f"Total Guests: {len(guests)}\n\n{guest_list_str}")
    update_status("Displayed guest list.")

def remove_guest(guests, guest_count_label, update_status):
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
            service.overwrite_guests(guests)
            guest_count_label.configure(text=f"Total Guests: {len(guests)}")
            messagebox.showinfo("Guest Removed", f"Guest '{choice}' has been removed.")
            update_status(f"Guest '{choice}' removed.")
            return
    update_status("Error: Guest not found!")
