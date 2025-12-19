class GuestListModel:
    def __init__(self, name: str, rsvp: str):
        self.name = name
        self.rsvp = rsvp

    def to_dict(self):
        return {
            "name": self.name,
            "rsvp": self.rsvp
        }

    @staticmethod
    def from_dict(data: dict):
        return GuestListModel(
            name=data.get("name", ""),
            rsvp=data.get("rsvp", "pending")
        )