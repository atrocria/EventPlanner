# guestlistController.py
import pages.guestlistModel as model

class GuestListController:
    def __init__(self, service):
        self.service = service
        model.guests = self.service.load_guests_from_file()

    def add_guest(self, name, rsvp):
        if not name:
            return {"status": "error", "message": "Guest name cannot be empty"}
        model.guests.append({"name": name, "rsvp": rsvp})
        self.service.save_guest_to_file(name, rsvp)
        return {"status": "success", "message": f"Guest added with RSVP: {rsvp}"}

    def view_guests(self):
        if not model.guests:
            return {"status": "empty", "message": "No guests added yet"}
        guest_list_str = "\n".join(f"- {g['name']} (RSVP: {g['rsvp']})" for g in model.guests)
        return {"status": "success", "message": f"Total Guests: {len(model.guests)}\n\n{guest_list_str}"}

    def remove_guest(self, name):
        for g in model.guests:
            if g["name"].lower() == name.lower():
                model.guests.remove(g)
                self.service.rewrite_file(model.guests)
                return {"status": "success", "message": "Guest removed!"}
        return {"status": "error", "message": "Guest not found"}