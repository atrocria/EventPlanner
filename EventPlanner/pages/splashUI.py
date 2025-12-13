import customtkinter as ctk
from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkButton

class SplashUI(CTkToplevel):
    def __init__(self, parent, on_close=None):
        super().__init__(parent)
        
        self.on_close = on_close
        
        self.title("Welcome")
        self.resizable(False, False)

        # lock focus
        self.transient(parent)
        self.grab_set()
        
        width = 500
        height = 300
        self.center_on_screen(width, height)
        
        container = CTkFrame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        CTkLabel(
            container, 
            text="Welcome to Event Planner",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(30,10))

        CTkLabel(
            container, 
            text="Plan tasks, manage budgets, \and keep your sanity",
            justify="center"
        ).pack(pady=10)

        CTkButton(
            container,
            text="Let's go!",
            command=self.close
        ).pack(pady=(30, 0))

    def close(self):
        self.grab_release()
        self.destroy()
        if self.on_close:
            self.on_close()
            
    def center_on_screen(self, w, h):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")