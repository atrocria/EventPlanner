# guestlistService.py
import os
from pages.guestlistModel import GuestListModel

class GuestListService:
    def __init__(self, file_path="guests.txt"):
        # Define where guest data will be saved
        self.file_path = file_path

    def save_guest(self, guest: GuestListModel):
        """Append a new guest to the file"""
        folder = os.path.dirname(self.file_path)
        os.makedirs(folder, exist_ok=True)
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"Guest Name: {guest.name} | RSVP Status: {guest.rsvp}\n")

    def load_guests(self):
        """Load all guests from the file"""
        if not os.path.exists(self.file_path):
            return []
        guests_list = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "Guest Name:" in line and "| RSVP Status:" in line:
                    parts = line.split("|")
                    name = parts[0].replace("Guest Name:", "").strip()
                    rsvp = parts[1].replace("RSVP Status:", "").strip()
                    guests_list.append(GuestListModel(name, rsvp))
        return guests_list

    def overwrite_guests(self, guests):
        """Rewrite the file with the current guest list"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            for g in guests:
                f.write(f"Guest Name: {g.name} | RSVP Status: {g.rsvp}\n")
