import customtkinter as ctk
from pages.countdownService import CountdownService

#! UI -> controller -> service <- model

class CountdownController(ctk.CTkFrame):
    def __init__(self, root, model: CountdownService, view):
        super().__init__(root)
        self.root = root
        self.model = model
        self.view = view

        # Bind UI buttons to controller actions
        self.view.start_button.configure(command=self.start_countdown)
        self.view.pause_button.configure(command=self.pause_countdown)
        self.view.reset_button.configure(command=self.reset_countdown)

    # --------------------------
    # Controller METHODS
    # --------------------------

    def start_countdown(self):
        self.model.start()
        self.update_ui()

    def pause_countdown(self):
        self.model.pause()

    def reset_countdown(self):
        self.model.reset()
        self.update_ui()

    # Update UI every 1000ms
    def update_ui(self):
        remaining = self.model.get_remaining_time()
        self.view.update_timer_label(remaining)

        if remaining > 0 and self.model.is_running:
            self.root.after(1000, self.update_ui)