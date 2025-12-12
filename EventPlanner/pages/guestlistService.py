# guestlistService.py
import os
from guestlistModel import Guest

SAVE_PATH = os.path.join(os.getcwd(), "guests.txt")

def save_guest_to_file(guest: Guest):
    folder = os.path.dirname(SAVE_PATH)
    os.makedirs(folder, exist_ok=True)
    with open(SAVE_PATH, "a", encoding="utf-8") as f:
        f.write(f"Guest Name: {guest.name} | RSVP Status: {guest.rsvp}\n")

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
                guests_list.append(Guest(name, rsvp))
    return guests_list

def overwrite_guests(guests):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        for g in guests:
            f.write(f"Guest Name: {g.name} | RSVP Status: {g.rsvp}\n")
