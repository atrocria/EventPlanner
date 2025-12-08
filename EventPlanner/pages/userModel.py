import uuid
import hashlib

class UserModel:
    def __init__(self, username: str, password_hash: str, user_id: str | None = None):
        self.id = user_id or uuid.uuid4().hex
        self.username = username
        self.password_hash = password_hash
        
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password_hash == self.password_hash(password)
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash
            }
        
    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            username=data["username"],
            password_hash = data["password_hash"],
            user_id = data["id"]
        )