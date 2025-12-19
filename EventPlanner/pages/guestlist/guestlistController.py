from .guestlistModel   import GuestListModel
from .guestlistService import GuestListService

class GuestController:
    def __init__(self, service: GuestListService):
        self.service = service

    def add_guest(self, name, rsvp):
        if not name:
            raise ValueError("Guest name cannot be empty.")

        guest = GuestListModel(name, rsvp)
        self.service.save_guest(guest)

        guests = self.service.load_guests()
        return guest, len(guests)

    def get_guests(self):
        return self.service.load_guests()

    def remove_guest(self, name):
        guests = self.service.load_guests()

        for g in guests:
            if g.name.lower() == name.lower():
                guests.remove(g)
                self.service.overwrite_guests(guests)
                return g, len(guests)

        raise LookupError("Guest not found")
    
    def count_all(self):
        return self.service.count_all()