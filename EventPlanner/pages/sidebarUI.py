import customtkinter as ctk
from customtkinter import CTk,CTkFrame, CTkEntry, CTkButton, CTkLabel

class SideBarUI(CTkFrame):
    def __init__(self, parent, title="untitled"):
        super().__init__(parent)
        self.propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.button = CTkButton(self, text="test button", width=20, command=lambda: print("pinging"))
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")