import customtkinter as ctk
from EventPlanner.countdownModel import CountdownModel
from EventPlanner.countdownService import CountdownService
from EventPlanner.countdownUI import CountdownUI

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")        # optional: "light", "dark", or "system"
    ctk.set_default_color_theme("blue")    # optional: color theme

    root = ctk.CTk()
    model = CountdownModel()
    service = CountdownService(model)
    app = CountdownUI(root, service, model)
    root.mainloop()

