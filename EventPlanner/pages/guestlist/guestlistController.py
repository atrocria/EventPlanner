from .guestlistModel   import GuestListModel
from .guestlistService import GuestListService

class GuestController():
    def __init__(self, service: GuestListService):
        self.service = service
        self.guests = self.service.load_guests()

    def add_guest(self, name, rsvp):
        if not name:
            raise ValueError("Error: Guest name cannot be empty.")

        guest = GuestListModel(name, rsvp)
        self.guests.append(guest)
        self.guests.save_guest(guest)
        
        return guest, len(self.guests)

    def get_guest(self):
        return list(self.guests)

    def remove_guest(self, name):
        for g in self.guests:
            if g.name.lower() == name.lower():
                self.guests.remove(g)
                self.service.overwrite_guests(self.guests)
                return g, len(self.guests)

        raise LookupError("Guest not found")
