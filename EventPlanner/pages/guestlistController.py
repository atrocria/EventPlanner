# guestlistController.py
from tkinter import messagebox, simpledialog
from guestlistModel import Guest
import guestlistService as service

class GuestController:
    def __init__(self, ui):
        self.ui = ui
        self.guests = service.load_guests_from_file()

    def add_guest(self, name, rsvp):
        if not name:
            self.ui.update_status("Error: Guest name cannot be empty.")
            return
        guest = Guest(name, rsvp)
        self.guests.append(guest)
        service.save_guest_to_file(guest)
        messagebox.showinfo("Guest Added", f"Guest '{name}' added with RSVP: {rsvp}")
        self.ui.update_status(f"Guest '{name}' added with RSVP: {rsvp}")
        self.ui.refresh_guest_count(len(self.guests))
        self.ui.clear_form()

    def view_guests(self):
        if not self.guests:
            self.ui.update_status("No guests added yet.")
            return
        guest_list_str = "\n".join(f"- {g.name} (RSVP: {g.rsvp})" for g in self.guests)
        messagebox.showinfo("Guest List", f"Total Guests: {len(self.guests)}\n\n{guest_list_str}")
        self.ui.update_status("Displayed guest list.")

    def remove_guest(self):
        if not self.guests:
            self.ui.update_status("No guests to remove.")
            return
        names = [g.name for g in self.guests]
        choice = simpledialog.askstring("Remove Guest", f"Enter guest name to remove:\n{', '.join(names)}")
        if not choice:
            return
        for g in self.guests:
            if g.name.lower() == choice.lower():
                self.guests.remove(g)
                service.overwrite_guests(self.guests)
                self.ui.refresh_guest_count(len(self.guests))
                messagebox.showinfo("Guest Removed", f"Guest '{choice}' has been removed.")
                self.ui.update_status(f"Guest '{choice}' removed.")
                return
        self.ui.update_status("Error: Guest not found!")

    def clear_form(self):
        self.ui.clear_form()
        self.ui.refresh_guest_count(len(self.guests))
        self.ui.update_status("Form cleared.")
