import os

SAVE_PATH = "C:/EventPlanner/guests.txt"

def save_guest(name, rsvp):
    folder = os.path.dirname(SAVE_PATH)
    os.makedirs(folder, exist_ok=True)
    with open(SAVE_PATH, "a", encoding="utf-8") as f:
        f.write(f"Guest Name: {name} | RSVP Status: {rsvp}\n")

def load_guests():
    if not os.path.exists(SAVE_PATH):
        return []
    guests = []
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if "Guest Name:" in line and "| RSVP Status:" in line:
                parts = line.strip().split("|")
                name = parts[0].replace("Guest Name:", "").strip()
                rsvp = parts[1].replace("RSVP Status:", "").strip()
                guests.append({"name": name, "rsvp": rsvp})
    return guests

def overwrite_guests(guests):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        for g in guests:
            f.write(f"Guest Name: {g['name']} | RSVP Status: {g['rsvp']}\n")
