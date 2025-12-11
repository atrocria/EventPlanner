# guestlistServices.py
import os

SAVE_PATH = "C:/EventPlanner/guests.txt"

class GuestListServices:
    def save_guest_to_file(self, name, rsvp):
        folder = os.path.dirname(SAVE_PATH)
        os.makedirs(folder, exist_ok=True)
        with open(SAVE_PATH, "a", encoding="utf-8") as f:
            f.write(f"Guest Name: {name} | RSVP Status: {rsvp}\n")

    def load_guests_from_file(self):
        if not os.path.exists(SAVE_PATH):
            return []
        guests_list = []
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Guest Name:") and "| RSVP Status:" in line:
                    parts = line.split("|")
                    name = parts[0].replace("Guest Name:", "").strip()
                    rsvp = parts[1].replace("RSVP Status:", "").strip()
                    guests_list.append({"name": name, "rsvp": rsvp})
        return guests_list

    def rewrite_file(self, guests):
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            for entry in guests:
                f.write(f"Guest Name: {entry['name']} | RSVP Status: {entry['rsvp']}\n")
