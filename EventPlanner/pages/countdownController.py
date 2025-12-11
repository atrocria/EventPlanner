import customtkinter as ctk
from pages.countdownModel import CountdownModel

class CountdownController(ctk.CTkFrame):
    def __init__(self, root, model:CountdownModel):
        super().__init__(root)
        self.root = root
        self.model = model

    def start_countdown(self):
        self.model.start()
        self.update_countdown()  # start updating UI every second
        
    def pause_countdown(self):
        self.model.pause()

    def reset_countdown(self):
        self.model.reset()

    def update_countdown(self):
        remaining = self.model.tick()

        # TODO: update the UI label or canvas etc with `remaining`

        if remaining > 0 and self.model.is_running:
            self.root.after(1000, self.update_countdown)
