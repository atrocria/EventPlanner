import os
import json
from .guestlistModel import GuestListModel

class GuestListService:
    def __init__(self, file_path="guests.json"):
        self.file_path = file_path
        self._ensure_file()

    # -----------------------
    # Internal helpers
    # -----------------------

    def _ensure_file(self):
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load_raw(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_raw(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # -----------------------
    # Public API
    # -----------------------

    def load_guests(self):
        return [
            GuestListModel.from_dict(d)
            for d in self._load_raw()
        ]

    def save_guest(self, guest: GuestListModel):
        data = self._load_raw()
        data.append(guest.to_dict())
        self._save_raw(data)

    def overwrite_guests(self, guests):
        self._save_raw([g.to_dict() for g in guests])

    # -----------------------
    # Dashboard helpers
    # -----------------------

    def count_all(self) -> int:
        return len(self._load_raw())

    def count_confirmed(self) -> int:
        return sum(
            1 for g in self._load_raw()
            if g.get("rsvp", "").lower() == "yes"
        )

    def count_declined(self) -> int:
        return sum(
            1 for g in self._load_raw()
            if g.get("rsvp", "").lower() == "no"
        )

    def count_pending(self) -> int:
        return sum(
            1 for g in self._load_raw()
            if g.get("rsvp", "").lower() not in ("yes", "no")
        )
