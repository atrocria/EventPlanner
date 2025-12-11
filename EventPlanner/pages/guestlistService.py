import os
from guestlistModel import get_save_path

def save_guest(name, rsvp):
    path = get_save_path()
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"Guest Name: {name} | RSVP Status: {rsvp}\n")

def load_guests():
    path = get_save_path()
    if not os.path.exists(path):
        return []
    guests = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "Guest Name:" in line and "| RSVP Status:" in line:
                parts = line.strip().split("|")
                name = parts[0].replace("Guest Name:", "").strip()
                rsvp = parts[1].replace("RSVP Status:", "").strip()
                guests.append({"name": name, "rsvp": rsvp})
    return guests

def overwrite_guests(guests):
    path = get_save_path()
    with open(path, "w", encoding="utf-8") as f:
        for g in guests:
            f.write(f"Guest Name: {g['name']} | RSVP Status: {g['rsvp']}\n")
