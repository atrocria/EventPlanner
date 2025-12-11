import customtkinter as ctk

#! UI -> controller -> service <- model

class CountdownController(ctk.CTkFrame):
    def __init__(self, root):
        self.root = root