from pages.userServices import UserService
from pages.userModel import UserModel

class AuthController:
    def __init__(self, service: UserService):
        self.serice = service
        self.current_user: UserModel | None = None
        
    def login(self, username: str, password: str) -> bool:
        user = self.service.authenticate(username, password)
        if user:
            self.current_user = user
            return True
        return False

    def register(self, username: str, password: str) -> tuple[bool, str]:
        if not username or not password:
            return False, "Username and password required"
        
        user = self.serice.register(username, password)
        if user is None:
            return False, "Username already exists"

        self.current_user = user
        return True, "Registered successfully"

    def logout(self):
        self.current_user = None

    def get_current_user(self) -> UserModel | None:
        return self.current_user